"""極座標・対数極座標への変換による、放射状・渦巻き状パターンの生成。

これまでの作例はすべて、画素を直交座標 (x, y) のまま扱ってきた。
出力画像の各画素を、中心からの角度 theta と距離 r という **極座標**
に読み替えてから、既存の模様生成関数にかけると、横方向に繰り返す
模様が中心の周りをぐるりと取り囲む放射状の模様に、縦方向に繰り返す
模様が渦巻き状の模様に変わる。距離 r の代わりに log(r) を使う
**対数極座標** にすると、中心に近づくほど模様が細かく詰まっていく、
渦巻き銀河のような模様になる。
"""

import numpy as np
from PIL import Image

from truchet import render_random_tiling


def polar_remap(
    source: Image.Image,
    width: int,
    height: int,
    center: tuple[float, float],
    max_radius: float,
    log_polar: bool = False,
) -> Image.Image:
    """ソース画像を極座標(または対数極座標)で読み直した画像を返す。

    出力画像の各画素 (x, y) について、``center`` からの角度 theta と
    距離 r を求め、theta をソース画像の横方向、r（``log_polar=True``
    なら log(r)）を縦方向の座標としてソース画像から読み出す。ソース
    画像が横方向に継ぎ目なく繰り返せる模様であれば、出力は中心から
    放射状に広がる模様になる。
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
    theta: np.ndarray = np.arctan2(dy, dx)
    r: np.ndarray = np.hypot(dx, dy)

    u: np.ndarray = (theta + np.pi) / (2.0 * np.pi) * src_width
    if log_polar:
        r_safe: np.ndarray = np.clip(r, 1e-3, None)
        v: np.ndarray = (
            np.log(r_safe) / np.log(max_radius) * src_height
        )
    else:
        v = r / max_radius * src_height

    u = np.mod(u, src_width).astype(np.int64)
    v = np.clip(v, 0, src_height - 1).astype(np.int64)

    return Image.fromarray(src_pixels[v, u])


def main() -> None:
    rng: np.random.Generator = np.random.default_rng(seed=5)

    # 横に長い帯状のトルシェ・タイル模様を土台にする。横方向が角度に
    # 対応するため、両端がつながるよう十分な列数を用意しておく。
    strip: Image.Image = render_random_tiling(72, 6, 20, rng)

    width: int = 480
    height: int = 480
    center: tuple[float, float] = (width / 2.0, height / 2.0)

    polar_remap(strip, width, height, center, max_radius=240.0).save(
        "polar_remap.png"
    )
    polar_remap(
        strip, width, height, center, max_radius=240.0, log_polar=True
    ).save("polar_remap_log.png")


if __name__ == "__main__":
    main()
