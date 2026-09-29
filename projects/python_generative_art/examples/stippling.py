"""重み付きボロノイ図による点描(Weighted Voronoi Stippling)。

画像の暗さを密度として、重み付きのロイド緩和で点を配置する
(Secord, 2002)。暗い場所ほど重心が引き寄せられるため点が密に集まり、
明るい場所では点がまばらになる。点どうしの間隔は近い場所どうしで
そろうため、一様乱数で点を打つ場合のような粒のむらが出にくい。
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from lloyd import lloyd_relaxation


def darkness(image: Image.Image, size: int, gamma: float = 2.0) -> np.ndarray:
    """画像を size x size のグレースケールに縮小し、暗さ(0.0-1.0)を返す。

    元の画像の明るさの幅が狭くても濃淡が点の密度に表れるように、
    明るさの下位 2% から上位 2% までを 0.0-1.0 に引き伸ばす。
    ``gamma`` を 1 より大きくすると、明るい部分の密度がさらに下がり、
    濃淡の差がはっきりした点描になる。
    """
    gray: Image.Image = image.convert("L").resize((size, size))
    values: np.ndarray = np.asarray(gray, dtype=float)
    low: float
    high: float
    low, high = np.percentile(values, [2.0, 98.0])
    stretched: np.ndarray = np.clip((values - low) / (high - low), 0.0, 1.0)
    return (1.0 - stretched) ** gamma + 1e-3  # 真っ白な場所にも僅かな重み


def initial_points(
    density: np.ndarray, count: int, rng: np.random.Generator
) -> np.ndarray:
    """密度に比例した確率で画素を選び、ロイド緩和の初期配置にする。"""
    height: int
    width: int
    height, width = density.shape
    probability: np.ndarray = density.ravel() / density.sum()
    indices: np.ndarray = rng.choice(
        height * width, size=count, replace=False, p=probability
    )
    ys: np.ndarray
    xs: np.ndarray
    ys, xs = np.divmod(indices, width)
    # 画素の中心(整数座標)から ±0.5 の範囲で、画素内のどこに置くかを決める。
    jitter: np.ndarray = rng.random((count, 2)) - 0.5
    return np.stack([xs, ys], axis=1) + jitter


def render_stipples(
    points: np.ndarray, size: int, scale: int, radius: float
) -> Image.Image:
    """点の配列を、``scale`` 倍に拡大したキャンバスに黒い円として描く。

    点の座標は画素の中心を整数とする座標系なので、0.5 を足してから
    拡大し、拡大後の画素の中心に合わせる。
    """
    image: Image.Image = Image.new("L", (size * scale, size * scale), 255)
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)
    for x, y in (points + 0.5) * scale:
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=0)
    return image


def main() -> None:
    gallery: Path = Path("source/_static/gallery")
    source: Image.Image = Image.open(gallery / "perlin_noise.png")

    size: int = 160  # 計算に使う密度画像の解像度
    scale: int = 2  # 出力は 320 x 320
    count: int = 2500
    rng: np.random.Generator = np.random.default_rng(seed=0)

    density: np.ndarray = darkness(source, size)
    start: np.ndarray = initial_points(density, count, rng)
    render_stipples(start, size, scale, radius=1.3).save(
        "stipple_initial.png"
    )

    relaxed: np.ndarray = lloyd_relaxation(
        start, size, size, iterations=40, density=density
    )
    render_stipples(relaxed, size, scale, radius=1.3).save("stipple.png")


if __name__ == "__main__":
    main()
