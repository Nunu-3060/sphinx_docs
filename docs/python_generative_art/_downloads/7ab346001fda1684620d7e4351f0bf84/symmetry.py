"""座標の鏡映・回転による対称模様(万華鏡表現)。

:doc:`../tiling` の ``polar_remap`` は、画素を極座標に読み替えて
ソース画像から色を拾うことで、横方向に繰り返す模様を放射状に変換した。
ここでは同じ「極座標に読み替えてソース画像から色を拾う」骨格に、
角度方向の折り返しを加える。角度を ``2*pi/segments`` の剰余に
落とすと、ソース画像の同じ範囲が周囲に ``segments`` 回繰り返される
回転対称模様になり、さらに剰余をノコギリ波ではなく三角波として
折り返す（``segments`` の中点で反転する）と、隣り合う扇形どうしが
線対称に鏡映しあう、万華鏡そのものの見た目になる。
"""

import numpy as np
from PIL import Image

from truchet import render_random_tiling


def kaleidoscope_remap(
    source: Image.Image,
    width: int,
    height: int,
    center: tuple[float, float],
    segments: int,
    max_radius: float,
    mirror: bool = True,
) -> Image.Image:
    """ソース画像を万華鏡状に読み替えた画像を返す。

    出力画像の各画素について、``center`` からの角度 theta と距離 r を
    求める。theta を扇形1枚分の角度 ``wedge = 2*pi/segments`` で割った
    余り ``a`` (``[0, wedge)``) が、ソース画像から読み出す横方向の
    位置に対応する。``mirror=True`` のときは ``a`` をさらに
    ``wedge/2`` を頂点とした三角波に折り返す
    (``a -> wedge/2 - |a - wedge/2|``) ことで、隣り合う扇形が
    ちょうど鏡に映したように反転してつながる。``mirror=False`` なら
    折り返さず、同じ模様が回転方向にそのまま繰り返されるだけになる。
    """
    src_pixels: np.ndarray = np.array(source)
    src_height: int
    src_width: int
    src_height, src_width = src_pixels.shape[:2]

    xs: np.ndarray
    ys: np.ndarray
    xs, ys = np.meshgrid(
        np.arange(width, dtype=float), np.arange(height, dtype=float)
    )
    dx: np.ndarray = xs - center[0]
    dy: np.ndarray = ys - center[1]
    theta: np.ndarray = np.arctan2(dy, dx) + np.pi
    r: np.ndarray = np.hypot(dx, dy)

    wedge: float = 2.0 * np.pi / segments
    a: np.ndarray = np.mod(theta, wedge)
    if mirror:
        a = wedge / 2.0 - np.abs(a - wedge / 2.0)
        u: np.ndarray = a / (wedge / 2.0) * src_width
    else:
        u = a / wedge * src_width

    v: np.ndarray = np.clip(r, 0, max_radius) / max_radius * src_height

    u = np.clip(u, 0, src_width - 1).astype(np.int64)
    v = np.clip(v, 0, src_height - 1).astype(np.int64)

    return Image.fromarray(src_pixels[v, u])


def main() -> None:
    rng: np.random.Generator = np.random.default_rng(seed=7)
    # 万華鏡の「筒の中身」に相当する、種になる模様。
    tile: Image.Image = render_random_tiling(20, 20, 20, rng)

    width: int = 480
    height: int = 480
    center: tuple[float, float] = (width / 2.0, height / 2.0)
    max_radius: float = 260.0

    kaleidoscope_remap(
        tile, width, height, center, segments=8, max_radius=max_radius,
        mirror=True,
    ).save("kaleidoscope_mirror.png")

    kaleidoscope_remap(
        tile, width, height, center, segments=8, max_radius=max_radius,
        mirror=False,
    ).save("kaleidoscope_rotation.png")


if __name__ == "__main__":
    main()
