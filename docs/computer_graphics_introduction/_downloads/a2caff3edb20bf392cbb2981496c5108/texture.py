"""「テクスチャマッピング」の章のサンプリングの関数と、その章の図を作る。

テクスチャは (高さ, 幅, 3) の配列で表す。テクスチャ座標 (u, v) は、
テクスチャの左下を (0, 0)、右上を (1, 1) とする。範囲外の座標の扱い
(ラップモード)は、繰り返す(repeat)か、端のテクセルを延長する(clamp)
かを選べる。

次の図を作る。

* textured.png: テクスチャを貼った立方体と球
* texture_filter.png: 拡大したテクスチャの最近傍補間とバイリニア補間
* mipmap.png: 遠くの床の模様と、ミップマップの効果
"""

import numpy as np

from cg_utils import (FloatArray, IntArray, hstack, linear_to_srgb,
                      normalize, output_dir, save_image, srgb_to_linear)
from renderer import (FrameBuffer, Mesh, draw_mesh, make_cube, make_plane,
                      make_sphere, transform_normals)
from shading import lambert
from transform import look_at, perspective, rotate_x, rotate_y

# ---------------------------------------------------------------------------
# サンプリング
# ---------------------------------------------------------------------------


def texel_coords(texture: FloatArray,
                 uv: FloatArray) -> tuple[FloatArray, FloatArray]:
    """テクスチャ座標を、テクセル(テクスチャの画素)単位の座標に変換する。

    テクセル (i, j) の中心が (i, j) になるように 0.5 をずらす。画像の行は
    上から数えるので、v の向きを反転する。
    """
    height, width = texture.shape[:2]
    x = uv[..., 0] * width - 0.5
    y = (1.0 - uv[..., 1]) * height - 0.5
    return x, y


def fetch(texture: FloatArray, x: IntArray, y: IntArray,
          wrap: str = "repeat") -> FloatArray:
    """整数のテクセル座標の色を返す。

    wrap が "repeat" なら範囲外の座標は繰り返し、"clamp" なら最も近い端の
    テクセルの色を使う。
    """
    height, width = texture.shape[:2]
    if wrap == "clamp":
        return np.asarray(texture[np.clip(y, 0, height - 1),
                                  np.clip(x, 0, width - 1)])
    return np.asarray(texture[y % height, x % width])


def sample_nearest(texture: FloatArray, uv: FloatArray,
                   wrap: str = "repeat") -> FloatArray:
    """最も近いテクセルの色を返す(最近傍補間)。"""
    x, y = texel_coords(texture, uv)
    return fetch(texture, np.rint(x).astype(np.int64),
                 np.rint(y).astype(np.int64), wrap)


def sample_bilinear(texture: FloatArray, uv: FloatArray,
                    wrap: str = "repeat") -> FloatArray:
    """周りの 4 つのテクセルの色を、距離に応じて混ぜる(バイリニア補間)。"""
    x, y = texel_coords(texture, uv)
    x0 = np.floor(x).astype(np.int64)
    y0 = np.floor(y).astype(np.int64)
    fx = (x - x0)[..., None]
    fy = (y - y0)[..., None]
    top = (fetch(texture, x0, y0, wrap) * (1 - fx)
           + fetch(texture, x0 + 1, y0, wrap) * fx)
    bottom = (fetch(texture, x0, y0 + 1, wrap) * (1 - fx)
              + fetch(texture, x0 + 1, y0 + 1, wrap) * fx)
    return np.asarray(top * (1 - fy) + bottom * fy)


def build_mipmaps(texture: FloatArray) -> list[FloatArray]:
    """縦横を半分ずつに縮めたテクスチャの列(ミップマップ)を作る。

    幅と高さは 2 のべき乗とする。縮小は 2 × 2 のテクセルの平均で行い、
    1 × 1 になるまで繰り返す。
    """
    levels = [texture]
    while levels[-1].shape[0] > 1 and levels[-1].shape[1] > 1:
        t = levels[-1]
        smaller = (t[0::2, 0::2] + t[1::2, 0::2]
                   + t[0::2, 1::2] + t[1::2, 1::2]) / 4.0
        levels.append(smaller)
    return levels


def mip_level(uv: FloatArray, texture_size: int) -> FloatArray:
    """画素ごとに、使うべきミップマップの段(詳細度、LOD)を求める。

    隣の画素とのテクスチャ座標の差から、1 画素が何テクセル分に当たるかを
    求め、その 2 を底とする対数を段とする。GPU も、隣り合う 2 × 2 の画素の
    差から同じように段を決めている。
    """
    du_dy, du_dx = np.gradient(uv[..., 0] * texture_size)
    dv_dy, dv_dx = np.gradient(uv[..., 1] * texture_size)
    footprint = np.maximum(np.hypot(du_dx, dv_dx), np.hypot(du_dy, dv_dy))
    return np.asarray(np.log2(np.maximum(footprint, 1e-8)))


def sample_trilinear(mipmaps: list[FloatArray], uv: FloatArray,
                     level: FloatArray) -> FloatArray:
    """隣り合う 2 つの段をバイリニア補間で読み、段の間でも補間する。"""
    level = np.clip(level, 0.0, len(mipmaps) - 1)
    lower = np.floor(level).astype(np.int64)
    upper = np.minimum(lower + 1, len(mipmaps) - 1)
    t = (level - lower)[..., None]
    result = np.zeros(uv.shape[:-1] + (3,))
    for k, texture in enumerate(mipmaps):
        use_lower = lower == k
        use_upper = upper == k
        if not (use_lower.any() or use_upper.any()):
            continue
        color = sample_bilinear(texture, uv)
        result += np.where(use_lower[..., None], color * (1 - t), 0.0)
        result += np.where(use_upper[..., None], color * t, 0.0)
    return result


# ---------------------------------------------------------------------------
# テクスチャの作成
# ---------------------------------------------------------------------------

def tile_texture(size: int = 64, tiles: int = 4) -> FloatArray:
    """色の異なるタイルを並べ、境目に溝を付けたテクスチャ(sRGB の値)。"""
    palette = np.array([[0.85, 0.45, 0.3], [0.95, 0.8, 0.45],
                        [0.4, 0.65, 0.45], [0.35, 0.55, 0.8]])
    cell = size // tiles
    ys, xs = np.mgrid[0:size, 0:size]
    index = (xs // cell + 2 * (ys // cell)) % len(palette)
    texture = palette[index]
    groove = (xs % cell == 0) | (ys % cell == 0)
    texture[groove] = 0.25
    return np.asarray(texture)


def small_texture() -> FloatArray:
    """拡大の図に使う 4 × 4 テクセルのテクスチャ(sRGB の値)。"""
    return np.array([
        [[0.9, 0.2, 0.2], [0.95, 0.85, 0.3], [0.2, 0.6, 0.3],
         [0.2, 0.3, 0.8]],
        [[0.95, 0.85, 0.3], [1.0, 1.0, 1.0], [0.1, 0.1, 0.1],
         [0.2, 0.6, 0.3]],
        [[0.2, 0.6, 0.3], [0.1, 0.1, 0.1], [1.0, 1.0, 1.0],
         [0.95, 0.85, 0.3]],
        [[0.2, 0.3, 0.8], [0.2, 0.6, 0.3], [0.95, 0.85, 0.3],
         [0.9, 0.2, 0.2]],
    ])


def checker_texture(size: int = 256, cells: int = 8) -> FloatArray:
    """白と黒の市松模様のテクスチャ(線形な値)。"""
    ys, xs = np.mgrid[0:size, 0:size] // (size // cells)
    value = np.where((xs + ys) % 2 == 0, 0.85, 0.02)
    return np.repeat(value[..., None], 3, axis=-1)


# ---------------------------------------------------------------------------
# 図の作成
# ---------------------------------------------------------------------------

def render_textured(mesh: Mesh, model: FloatArray,
                    texture: FloatArray) -> FloatArray:
    """テクスチャの色に拡散反射と環境光の照明を掛けて描く。"""
    eye = np.array([0.0, 0.0, 3.6])
    light_dir = normalize(np.array([-0.5, 0.6, 0.8]))
    view = look_at(eye, np.zeros(3), np.array([0.0, 1.0, 0.0]))
    proj = perspective(40.0, 1.0, 0.5, 10.0)
    fb = FrameBuffer(240, 240, {"normal": 3, "uv": 2})
    draw_mesh(fb, proj @ view @ model, mesh, {
        "normal": transform_normals(model, mesh.normals),
        "uv": mesh.uvs,
    })
    albedo = srgb_to_linear(sample_bilinear(texture, fb.attributes["uv"]))
    normal = normalize(fb.attributes["normal"])
    color = albedo * (0.15 + 0.85 * lambert(normal, light_dir))
    return np.where(fb.covered[..., None], linear_to_srgb(color), 1.0)


def textured_figure() -> FloatArray:
    """テクスチャを貼った立方体(左)と球(右)を並べる。"""
    cube_model = rotate_x(25.0) @ rotate_y(-35.0)
    sphere_model = rotate_x(20.0) @ rotate_y(30.0)
    return hstack([
        render_textured(make_cube(), cube_model, tile_texture(256, 4)),
        render_textured(make_sphere(), sphere_model, tile_texture(256, 8)),
    ])


def filter_figure() -> FloatArray:
    """4 × 4 のテクスチャを 256 × 256 画素に拡大して比べる。

    左は最近傍補間、右はバイリニア補間である。端の様子が分かりやすい
    ように、ラップモードは clamp にしている。
    """
    texture = small_texture()
    size = 256
    ys, xs = np.mgrid[0:size, 0:size]
    uv = np.stack([(xs + 0.5) / size, 1.0 - (ys + 0.5) / size], axis=-1)
    return hstack([sample_nearest(texture, uv, "clamp"),
                   sample_bilinear(texture, uv, "clamp")])


def mipmap_figure() -> FloatArray:
    """遠くまで続く市松模様の床を描いて比べる。

    左: ミップマップを使わずにバイリニア補間だけで読んだもの。
    中: ミップマップを使い、トライリニア補間で読んだもの。
    右: 中の図で使った段を色で表したもの(青が 0 段、赤ほど縮小した段)。
    """
    width, height = 320, 200
    texture = checker_texture()
    mipmaps = build_mipmaps(texture)
    # draw_mesh() はカメラの後ろに頂点がある三角形を捨てるので、床は
    # カメラの少し前から奥に向かって広げる。
    floor = make_plane(400.0, 100.0)
    floor.positions[:, 2] -= 200.5
    view = look_at(np.array([0.0, 1.0, 0.0]), np.array([0.0, 0.6, -4.0]),
                   np.array([0.0, 1.0, 0.0]))
    proj = perspective(60.0, width / height, 0.1, 500.0)
    fb = FrameBuffer(width, height, {"uv": 2})
    draw_mesh(fb, proj @ view, floor,
              {"uv": floor.uvs})
    uv = fb.attributes["uv"]
    covered = fb.covered[..., None]
    sky = np.array([0.8, 0.88, 0.95])

    plain = sample_bilinear(texture, uv)
    level = mip_level(uv, texture.shape[0])
    filtered = sample_trilinear(mipmaps, uv, level)

    t = np.clip(level / (len(mipmaps) - 1), 0.0, 1.0)[..., None]
    level_colors = (1 - t) * np.array([0.1, 0.3, 0.9]) \
        + t * np.array([0.9, 0.15, 0.1])

    panels = [np.where(covered, linear_to_srgb(plain), sky),
              np.where(covered, linear_to_srgb(filtered), sky),
              np.where(covered, level_colors, sky)]
    return hstack(panels)


def main() -> None:
    out = output_dir()
    save_image(textured_figure(), out / "textured.png")
    save_image(filter_figure(), out / "texture_filter.png")
    save_image(mipmap_figure(), out / "mipmap.png")


if __name__ == "__main__":
    main()
