"""「座標変換と投影」の章で使う変換行列と、その章の図を作るスクリプト。

変換行列を作る関数は、3 次元の描画を行う renderer.py からも使う。
座標系は右手系とし、カメラは -z 方向を向くものとする(OpenGL と同じ)。
点は列ベクトルとして扱い、変換は「行列 @ 点」の順に掛ける。

次の図を作る。

* transform_order.png: 回転と平行移動を掛ける順序による結果の違い
* projection.png: 平行投影と透視投影の比較
"""

import numpy as np
from PIL import Image, ImageDraw

from cg_utils import (FloatArray, from_pil, hstack, normalize, output_dir,
                      save_image)

# ---------------------------------------------------------------------------
# 2 次元の変換(3 × 3 の同次座標の行列)
# ---------------------------------------------------------------------------


def scale_2d(sx: float, sy: float) -> FloatArray:
    """x 方向に sx 倍、y 方向に sy 倍する拡大縮小の行列。"""
    return np.array([
        [sx, 0.0, 0.0],
        [0.0, sy, 0.0],
        [0.0, 0.0, 1.0],
    ])


def rotate_2d(degrees: float) -> FloatArray:
    """原点を中心に反時計回りに回転する行列。"""
    t = np.radians(degrees)
    c, s = np.cos(t), np.sin(t)
    return np.array([
        [c, -s, 0.0],
        [s, c, 0.0],
        [0.0, 0.0, 1.0],
    ])


def translate_2d(tx: float, ty: float) -> FloatArray:
    """x 方向に tx、y 方向に ty だけ平行移動する行列。"""
    return np.array([
        [1.0, 0.0, tx],
        [0.0, 1.0, ty],
        [0.0, 0.0, 1.0],
    ])


def apply_2d(matrix: FloatArray, points: FloatArray) -> FloatArray:
    """(N, 2) の点の配列に 3 × 3 の行列を掛けた結果を返す。"""
    homogeneous = np.hstack([points, np.ones((len(points), 1))])
    return np.asarray((matrix @ homogeneous.T).T[:, :2])


# ---------------------------------------------------------------------------
# 3 次元の変換(4 × 4 の同次座標の行列)
# ---------------------------------------------------------------------------

def translate(tx: float, ty: float, tz: float) -> FloatArray:
    """平行移動の行列。"""
    m = np.eye(4)
    m[:3, 3] = [tx, ty, tz]
    return m


def scale(sx: float, sy: float, sz: float) -> FloatArray:
    """拡大縮小の行列。"""
    return np.diag([sx, sy, sz, 1.0])


def rotate_x(degrees: float) -> FloatArray:
    """x 軸のまわりの回転の行列(x 軸の正の向きから見て反時計回り)。"""
    t = np.radians(degrees)
    c, s = np.cos(t), np.sin(t)
    return np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, c, -s, 0.0],
        [0.0, s, c, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ])


def rotate_y(degrees: float) -> FloatArray:
    """y 軸のまわりの回転の行列(y 軸の正の向きから見て反時計回り)。"""
    t = np.radians(degrees)
    c, s = np.cos(t), np.sin(t)
    return np.array([
        [c, 0.0, s, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [-s, 0.0, c, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ])


def look_at(eye: FloatArray, target: FloatArray,
            up: FloatArray) -> FloatArray:
    """ビュー変換の行列。ワールド座標をカメラ座標に変換する。

    カメラを eye に置き、target の方向に向ける。up はカメラの上の向きの
    目安である。カメラ座標では、カメラは原点にあって -z 方向を向き、
    上が +y、右が +x になる。
    """
    forward = normalize(target - eye)          # カメラの前方
    right = normalize(np.cross(forward, up))   # カメラの右
    true_up = np.cross(right, forward)         # カメラの上
    rotation = np.eye(4)
    rotation[0, :3] = right
    rotation[1, :3] = true_up
    rotation[2, :3] = -forward
    return rotation @ translate(-eye[0], -eye[1], -eye[2])


def perspective(fovy_degrees: float, aspect: float, near: float,
                far: float) -> FloatArray:
    """透視投影の行列。

    fovy_degrees は縦方向の視野角、aspect は画面の幅 / 高さである。
    カメラから near から far までの範囲が、正規化デバイス座標の
    z = -1 から 1 に対応する。
    """
    s = 1.0 / np.tan(np.radians(fovy_degrees) / 2.0)
    return np.array([
        [s / aspect, 0.0, 0.0, 0.0],
        [0.0, s, 0.0, 0.0],
        [0.0, 0.0, (far + near) / (near - far),
         2.0 * far * near / (near - far)],
        [0.0, 0.0, -1.0, 0.0],
    ])


def orthographic(half_width: float, half_height: float, near: float,
                 far: float) -> FloatArray:
    """平行投影の行列。

    カメラ座標の x が -half_width から half_width、y が -half_height から
    half_height、奥行きが near から far の直方体を、正規化デバイス座標の
    -1 から 1 の立方体に対応させる。
    """
    return np.array([
        [1.0 / half_width, 0.0, 0.0, 0.0],
        [0.0, 1.0 / half_height, 0.0, 0.0],
        [0.0, 0.0, -2.0 / (far - near), -(far + near) / (far - near)],
        [0.0, 0.0, 0.0, 1.0],
    ])


def to_clip(matrix: FloatArray, points: FloatArray) -> FloatArray:
    """(N, 3) の点に 4 × 4 の行列を掛け、(N, 4) の同次座標を返す。"""
    homogeneous = np.hstack([points, np.ones((len(points), 1))])
    return np.asarray((matrix @ homogeneous.T).T)


def to_screen(clip: FloatArray, width: int, height: int) -> FloatArray:
    """同次座標を w で割り(透視除算)、画面の画素の座標に変換する。

    戻り値は (N, 3) の配列で、各行は (x, y, z) である。x と y は画素の
    座標(y 軸は下向き)、z は正規化デバイス座標の z(-1 から 1)である。
    """
    ndc = clip[:, :3] / clip[:, 3:4]
    x = (ndc[:, 0] + 1.0) * 0.5 * width
    y = (1.0 - ndc[:, 1]) * 0.5 * height
    return np.stack([x, y, ndc[:, 2]], axis=-1)


# ---------------------------------------------------------------------------
# 図の作成
# ---------------------------------------------------------------------------

# 図をなめらかにするため、2 倍の大きさで描いてから縮小する。
SUPERSAMPLE = 2

# 家の形をした多角形(原点が家の床の中央)。
HOUSE: FloatArray = np.array([
    [-0.5, 0.0], [0.5, 0.0], [0.5, 0.6], [0.0, 1.0], [-0.5, 0.6],
])


def world_to_pixel(points: FloatArray, size: int,
                   extent: float) -> list[tuple[float, float]]:
    """-extent から extent の範囲の 2 次元の座標を、画像の座標に変換する。"""
    px = (points[:, 0] / extent + 1.0) * 0.5 * size
    py = (1.0 - points[:, 1] / extent) * 0.5 * size
    return list(zip(px.tolist(), py.tolist()))


def house_panel(matrix: FloatArray) -> FloatArray:
    """座標軸、元の家(灰色の輪郭)、変換した家(青)を描いた画像を返す。"""
    size, extent = 300 * SUPERSAMPLE, 2.5
    image = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(image)
    axes = np.array([[-extent, 0.0], [extent, 0.0],
                     [0.0, -extent], [0.0, extent]])
    pixels = world_to_pixel(axes, size, extent)
    draw.line(pixels[0:2], fill=(160, 160, 160), width=SUPERSAMPLE)
    draw.line(pixels[2:4], fill=(160, 160, 160), width=SUPERSAMPLE)

    draw.polygon(world_to_pixel(HOUSE, size, extent),
                 outline=(120, 120, 120), width=2 * SUPERSAMPLE)
    moved = apply_2d(matrix, HOUSE)
    draw.polygon(world_to_pixel(moved, size, extent), fill=(60, 110, 190))
    image = image.resize((size // SUPERSAMPLE, size // SUPERSAMPLE),
                         Image.Resampling.LANCZOS)
    return from_pil(image)


def transform_order_figure() -> FloatArray:
    """回転と平行移動を掛ける順序を変えた 2 つの結果を並べる。

    左: 先に 45 度回転し、次に x 方向に 1.5 平行移動する(T @ R)。
    右: 先に x 方向に 1.5 平行移動し、次に 45 度回転する(R @ T)。
    """
    r = rotate_2d(45.0)
    t = translate_2d(1.5, 0.0)
    return hstack([house_panel(t @ r), house_panel(r @ t)])


CUBE_VERTICES: FloatArray = np.array(
    [[x, y, z] for x in (-0.5, 0.5) for y in (-0.5, 0.5) for z in (-0.5, 0.5)]
)

# 立方体の 12 本の辺(頂点の番号の組)。座標が 1 つだけ異なる頂点を結ぶ。
CUBE_EDGES = [(i, j) for i in range(8) for j in range(i + 1, 8)
              if np.count_nonzero(CUBE_VERTICES[i] != CUBE_VERTICES[j]) == 1]


def wireframe_panel(projection: FloatArray) -> FloatArray:
    """奥に向かって並ぶ 3 つの立方体を、指定した投影で線画として描く。"""
    width, height = 320, 240
    size = (width * SUPERSAMPLE, height * SUPERSAMPLE)
    image = Image.new("RGB", size, "white")
    draw = ImageDraw.Draw(image)
    view = look_at(np.array([2.2, 1.6, 3.0]), np.array([0.0, 0.0, -2.0]),
                   np.array([0.0, 1.0, 0.0]))
    colors = [(200, 60, 50), (60, 140, 70), (50, 90, 190)]
    for k, color in enumerate(colors):
        model = translate(0.0, 0.0, -2.0 * k)
        clip = to_clip(projection @ view @ model, CUBE_VERTICES)
        screen = to_screen(clip, *size)
        for i, j in CUBE_EDGES:
            draw.line([tuple(screen[i, :2]), tuple(screen[j, :2])],
                      fill=color, width=2 * SUPERSAMPLE)
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    return from_pil(image)


def projection_figure() -> FloatArray:
    """同じ立方体を平行投影(左)と透視投影(右)で描いて並べる。"""
    aspect = 320 / 240
    ortho = orthographic(2.6 * aspect, 2.6, 0.1, 20.0)
    persp = perspective(50.0, aspect, 0.1, 20.0)
    return hstack([wireframe_panel(ortho), wireframe_panel(persp)])


def main() -> None:
    out = output_dir()
    save_image(transform_order_figure(), out / "transform_order.png")
    save_image(projection_figure(), out / "projection.png")


if __name__ == "__main__":
    main()
