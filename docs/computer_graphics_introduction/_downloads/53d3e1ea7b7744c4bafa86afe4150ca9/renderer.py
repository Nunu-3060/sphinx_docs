"""三角形のメッシュを Z バッファー法で描く、小さなソフトウェアレンダラー。

「3 次元のラスタライズ」の章で使う。ライティングとテクスチャの章でも、
このモジュールで描いた結果に色を付ける。

描画は次の 2 段階で行う。

1. draw_mesh(): 三角形をラスタライズし、各画素に最も手前の面の深度と
   属性(位置、法線、テクスチャ座標など)を書き込む。
2. 書き込まれた属性を使い、画素ごとの色を NumPy の配列演算でまとめて
   計算する(shading.py、texture.py)。

1 の段階は、raster2d.py で画素を 1 つずつ調べていた処理を、三角形を
囲む長方形の画素についてまとめて計算するように書き換えたものである。

次の図を作る。

* depth.png: 描画した色と、Z バッファーに書き込まれた深度
* perspective_correct.png: 透視補正の有無による、床の模様の違い
"""

from dataclasses import dataclass

import numpy as np

from cg_utils import (BoolArray, FloatArray, IntArray, hstack, output_dir,
                      save_image)
from transform import look_at, perspective, rotate_x, rotate_y, scale, \
    to_clip, translate


# ---------------------------------------------------------------------------
# メッシュ
# ---------------------------------------------------------------------------

@dataclass
class Mesh:
    """三角形のメッシュ。

    positions、normals、uvs は頂点ごとの属性で、行の数は頂点の数に等しい。
    faces は三角形ごとに 3 つの頂点の番号を並べたもので、外側から見て
    反時計回りの順に並べる。
    """

    positions: FloatArray  # (頂点の数, 3)
    normals: FloatArray    # (頂点の数, 3)
    uvs: FloatArray        # (頂点の数, 2)
    faces: IntArray        # (三角形の数, 3)


def make_cube() -> Mesh:
    """1 辺の長さが 1 の立方体を作る。

    面ごとに法線が異なるので、各面に専用の 4 つの頂点を持たせる
    (頂点は全部で 24 個)。
    """
    positions: list[FloatArray] = []
    normals: list[FloatArray] = []
    uvs: list[tuple[int, int]] = []
    faces: list[tuple[int, int, int]] = []
    # 各面の法線と、面の上で u、v が増える向き。
    sides = [
        ((1, 0, 0), (0, 0, -1), (0, 1, 0)),
        ((-1, 0, 0), (0, 0, 1), (0, 1, 0)),
        ((0, 1, 0), (1, 0, 0), (0, 0, -1)),
        ((0, -1, 0), (1, 0, 0), (0, 0, 1)),
        ((0, 0, 1), (1, 0, 0), (0, 1, 0)),
        ((0, 0, -1), (-1, 0, 0), (0, 1, 0)),
    ]
    for normal, u_dir, v_dir in sides:
        n, u, v = np.array(normal), np.array(u_dir), np.array(v_dir)
        base = len(positions)
        for su, sv in ((0, 0), (1, 0), (1, 1), (0, 1)):
            positions.append(0.5 * n + (su - 0.5) * u + (sv - 0.5) * v)
            normals.append(n)
            uvs.append((su, sv))
        faces += [(base, base + 1, base + 2), (base, base + 2, base + 3)]
    return Mesh(np.array(positions, dtype=np.float64),
                np.array(normals, dtype=np.float64),
                np.array(uvs, dtype=np.float64),
                np.array(faces, dtype=np.int64))


def make_sphere(n_lon: int = 48, n_lat: int = 24) -> Mesh:
    """半径 1 の球を、経線 n_lon 本、緯線 n_lat 本で区切って作る(UV 球)。"""
    lon = np.linspace(0.0, 2.0 * np.pi, n_lon + 1)
    lat = np.linspace(0.0, np.pi, n_lat + 1)
    lon_grid, lat_grid = np.meshgrid(lon, lat)
    x = np.sin(lat_grid) * np.cos(lon_grid)
    y = np.cos(lat_grid)
    z = -np.sin(lat_grid) * np.sin(lon_grid)
    positions = np.stack([x, y, z], axis=-1).reshape(-1, 3)
    u = lon_grid / (2.0 * np.pi)
    v = 1.0 - lat_grid / np.pi
    uvs = np.stack([u, v], axis=-1).reshape(-1, 2)

    faces = []
    row = n_lon + 1
    for j in range(n_lat):
        for i in range(n_lon):
            a = j * row + i          # 左上
            b = a + row              # 左下
            # 極に接する四角形は三角形に縮退するので、1 つだけ作る。
            if j > 0:
                faces.append((a, b + 1, a + 1))
            if j < n_lat - 1:
                faces.append((a, b, b + 1))
    # 球の中心は原点なので、位置ベクトルがそのまま法線になる。
    return Mesh(positions, positions.copy(), uvs,
                np.array(faces, dtype=np.int64))


def make_plane(size: float, repeat: float) -> Mesh:
    """y = 0 の平面上に、1 辺の長さが size の正方形を作る。上が表である。

    テクスチャ座標は 0 から repeat まで変わる。
    """
    h = size / 2.0
    positions = np.array([[-h, 0, h], [h, 0, h], [h, 0, -h], [-h, 0, -h]],
                         dtype=np.float64)
    normals = np.tile([0.0, 1.0, 0.0], (4, 1))
    uvs = np.array([[0, 0], [1, 0], [1, 1], [0, 1]],
                   dtype=np.float64) * repeat
    faces = np.array([[0, 1, 2], [0, 2, 3]], dtype=np.int64)
    return Mesh(positions, normals, uvs, faces)


def flatten(mesh: Mesh) -> Mesh:
    """頂点を三角形ごとに複製し、法線を面の法線に置き換えたメッシュを返す。

    フラットシェーディングで使う。
    """
    positions = mesh.positions[mesh.faces].reshape(-1, 3)
    p0, p1, p2 = (mesh.positions[mesh.faces[:, k]] for k in range(3))
    face_normals = np.cross(p1 - p0, p2 - p0)
    face_normals /= np.linalg.norm(face_normals, axis=-1, keepdims=True)
    normals = np.repeat(face_normals, 3, axis=0)
    uvs = mesh.uvs[mesh.faces].reshape(-1, 2)
    faces = np.arange(len(positions), dtype=np.int64).reshape(-1, 3)
    return Mesh(positions, normals, uvs, faces)


# ---------------------------------------------------------------------------
# フレームバッファーとラスタライズ
# ---------------------------------------------------------------------------

class FrameBuffer:
    """描画結果を書き込む画像の集まり。

    depth は各画素の深度(正規化デバイス座標の z、小さいほど手前)で、
    何も描かれていない画素は無限大である。attributes には、画素ごとに
    補間した頂点の属性を名前ごとに格納する。
    """

    def __init__(self, width: int, height: int,
                 channels: dict[str, int]) -> None:
        self.width = width
        self.height = height
        self.depth: FloatArray = np.full((height, width), np.inf)
        self.attributes: dict[str, FloatArray] = {
            name: np.zeros((height, width, n)) for name, n in channels.items()
        }

    @property
    def covered(self) -> BoolArray:
        """何かが描かれた画素で True となる配列。"""
        return np.asarray(np.isfinite(self.depth))


def edge_function(ax: float, ay: float, bx: float, by: float,
                  px: FloatArray, py: FloatArray) -> FloatArray:
    """raster2d.py の edge_function() を、多数の点 (px, py) に対して計算する。"""
    return (bx - ax) * (py - ay) - (by - ay) * (px - ax)


def draw_mesh(fb: FrameBuffer, mvp: FloatArray, mesh: Mesh,
              attributes: dict[str, FloatArray], cull_back: bool = True,
              perspective_correct: bool = True) -> None:
    """メッシュを描き、深度と属性をフレームバッファーに書き込む。

    mvp はモデル、ビュー、投影の変換を掛け合わせた行列である。
    attributes には頂点ごとの属性を、fb の attributes と同じ名前で渡す。
    """
    clip = to_clip(mvp, mesh.positions)
    w = clip[:, 3]
    # 透視除算とビューポート変換(y 軸は下向き)。
    sx = (clip[:, 0] / w + 1.0) * 0.5 * fb.width
    sy = (1.0 - clip[:, 1] / w) * 0.5 * fb.height
    sz = clip[:, 2] / w

    for i0, i1, i2 in mesh.faces:
        # 簡略化のため、カメラの近くの面(ニアクリップ面)より手前に頂点が
        # ある三角形は、切り取らずに丸ごと捨てる。
        if min(w[i0], w[i1], w[i2]) <= 0.0 or \
                min(sz[i0], sz[i1], sz[i2]) < -1.0:
            continue
        area = edge_function(sx[i0], sy[i0], sx[i1], sy[i1],
                             np.array(sx[i2]), np.array(sy[i2]))
        if area == 0.0:
            continue
        # 画面の y 軸は下向きなので、表を向いた(反時計回りの)三角形は
        # 画面上では時計回りになり、area が負になる。
        if cull_back and area > 0.0:
            continue

        # 三角形を囲む長方形の画素の中心の座標を作る。
        x_min = max(int(np.floor(min(sx[i0], sx[i1], sx[i2]))), 0)
        x_max = min(int(np.ceil(max(sx[i0], sx[i1], sx[i2]))), fb.width)
        y_min = max(int(np.floor(min(sy[i0], sy[i1], sy[i2]))), 0)
        y_max = min(int(np.ceil(max(sy[i0], sy[i1], sy[i2]))), fb.height)
        if x_min >= x_max or y_min >= y_max:
            continue
        px, py = np.meshgrid(np.arange(x_min, x_max) + 0.5,
                             np.arange(y_min, y_max) + 0.5)

        # 重心座標を求め、三角形の内側の画素を選ぶ。
        b0 = edge_function(sx[i1], sy[i1], sx[i2], sy[i2], px, py) / area
        b1 = edge_function(sx[i2], sy[i2], sx[i0], sy[i0], px, py) / area
        b2 = 1.0 - b0 - b1
        inside = (b0 >= 0.0) & (b1 >= 0.0) & (b2 >= 0.0)

        # 深度テスト: すでに書かれている深度より手前の画素だけを残す。
        z = b0 * sz[i0] + b1 * sz[i1] + b2 * sz[i2]
        region = (slice(y_min, y_max), slice(x_min, x_max))
        passed = inside & (z < fb.depth[region])
        if not passed.any():
            continue
        fb.depth[region][passed] = z[passed]

        # 属性の補間に使う重み。透視補正では各頂点の 1 / w を掛けて
        # 補間し、最後に重みの合計で割る。
        if perspective_correct:
            q0, q1, q2 = b0 / w[i0], b1 / w[i1], b2 / w[i2]
            total = q0 + q1 + q2
            q0, q1, q2 = q0 / total, q1 / total, q2 / total
        else:
            q0, q1, q2 = b0, b1, b2
        for name, values in attributes.items():
            value = (q0[..., None] * values[i0] + q1[..., None] * values[i1]
                     + q2[..., None] * values[i2])
            fb.attributes[name][region][passed] = value[passed]


def transform_normals(model: FloatArray, normals: FloatArray) -> FloatArray:
    """モデル変換に合わせて法線を変換する。

    法線には、モデル変換の左上 3 × 3 の逆行列の転置を掛ける。
    """
    normal_matrix = np.linalg.inv(model[:3, :3]).T
    result = (normal_matrix @ normals.T).T
    return np.asarray(result / np.linalg.norm(result, axis=-1, keepdims=True))


def transform_positions(model: FloatArray,
                        positions: FloatArray) -> FloatArray:
    """モデル変換を掛けた (N, 3) のワールド座標を返す。"""
    return np.asarray(to_clip(model, positions)[:, :3])


# ---------------------------------------------------------------------------
# 図の作成
# ---------------------------------------------------------------------------

def demo_scene(fb: FrameBuffer) -> None:
    """交差する立方体と球を描く。属性は物体ごとの色(color)だけを使う。"""
    view = look_at(np.array([0.0, 1.6, 4.2]), np.array([0.0, 0.0, 0.0]),
                   np.array([0.0, 1.0, 0.0]))
    proj = perspective(45.0, fb.width / fb.height, 0.5, 10.0)
    objects = [
        (make_cube(), translate(-0.35, 0.0, 0.0) @ rotate_y(30.0)
         @ rotate_x(20.0) @ scale(1.3, 1.3, 1.3), (0.85, 0.35, 0.25)),
        (make_sphere(), translate(0.45, 0.0, 0.1) @ scale(0.8, 0.8, 0.8),
         (0.25, 0.5, 0.85)),
    ]
    for mesh, model, color in objects:
        colors = np.tile(color, (len(mesh.positions), 1))
        draw_mesh(fb, proj @ view @ model, mesh, {"color": colors})


def depth_figure() -> FloatArray:
    """描画した色(左)と、Z バッファーの深度を濃淡で表した画像(右)を並べる。"""
    fb = FrameBuffer(320, 240, {"color": 3})
    demo_scene(fb)
    covered = fb.covered[..., None]
    color = np.where(covered, fb.attributes["color"], 1.0)

    # 描かれた範囲の深度を 0 から 1 に引き伸ばし、手前ほど明るく表す。
    depth = fb.depth[fb.covered]
    near, far = depth.min(), depth.max()
    t = np.where(fb.covered, (fb.depth - near) / (far - near), 1.0)
    gray = np.where(fb.covered, 0.9 - 0.75 * t, 0.0)
    depth_image = np.repeat(gray[..., None], 3, axis=-1)
    return hstack([color, depth_image])


def checker(uv: FloatArray) -> FloatArray:
    """テクスチャ座標 (u, v) の整数部分にもとづく白と黒の市松模様の色。"""
    cell = np.floor(uv[..., 0]) + np.floor(uv[..., 1])
    value = np.where(cell % 2 == 0, 0.9, 0.15)
    return np.repeat(value[..., None], 3, axis=-1)


def perspective_correct_figure() -> FloatArray:
    """2 つの三角形でできた床を、透視補正なし(左)とあり(右)で描く。"""
    panels = []
    view = look_at(np.array([0.0, 1.2, 2.5]), np.array([0.0, 0.0, -1.0]),
                   np.array([0.0, 1.0, 0.0]))
    proj = perspective(60.0, 320 / 240, 0.1, 20.0)
    plane = make_plane(4.0, 8.0)
    for correct in (False, True):
        fb = FrameBuffer(320, 240, {"uv": 2})
        draw_mesh(fb, proj @ view, plane, {"uv": plane.uvs},
                  perspective_correct=correct)
        image = np.where(fb.covered[..., None], checker(fb.attributes["uv"]),
                         1.0)
        panels.append(image)
    return hstack(panels)


def main() -> None:
    out = output_dir()
    save_image(depth_figure(), out / "depth.png")
    save_image(perspective_correct_figure(), out / "perspective_correct.png")


if __name__ == "__main__":
    main()
