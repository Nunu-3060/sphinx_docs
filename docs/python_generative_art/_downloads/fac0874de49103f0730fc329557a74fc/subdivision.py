"""再帰的分割による画面の構成: 矩形の再帰分割と四分木。

1つの領域を2つ(または4つ)に分け、分けた領域それぞれに同じ処理を
繰り返す、という再帰的な手続きで画面を区切る。分割を続けるか
止めるかの規則を変えるだけで、モンドリアン風の抽象画から、画像の
細かさに応じてマス目の大きさが変わるモザイクまで作り分けられる。
"""

import numpy as np
from matplotlib import colormaps
from PIL import Image, ImageDraw

from mandelbrot import julia_escape

# 矩形は (左, 上, 右, 下) の座標で表す。
Rect = tuple[float, float, float, float]


def split_rect(
    rect: Rect,
    rng: np.random.Generator,
    depth: int = 0,
    max_depth: int = 6,
    min_size: float = 40.0,
) -> list[Rect]:
    """矩形を再帰的に2分割し、それ以上分割しなかった矩形のリストを返す。

    長いほうの辺に垂直な線で、辺の 30〜70% の位置から選んだ場所で
    分割する。深くなるほど分割を止める確率を上げることで、大きな
    矩形と小さな矩形が混ざった構成になる(最初の2段は必ず分割する)。
    分割後の辺が ``min_size``
    より短くなる場合や、``max_depth`` に達した場合も分割を止める。
    """
    left, top, right, bottom = rect
    width: float = right - left
    height: float = bottom - top
    longer: float = max(width, height)

    stop_probability: float = 0.0 if depth < 2 else 0.6 * depth / max_depth
    too_small: bool = longer < 2 * min_size
    if depth >= max_depth or too_small or rng.random() < stop_probability:
        return [rect]

    ratio: float = float(rng.uniform(0.3, 0.7))
    first: Rect
    second: Rect
    if width >= height:
        x: float = left + width * ratio
        first, second = (left, top, x, bottom), (x, top, right, bottom)
    else:
        y: float = top + height * ratio
        first, second = (left, top, right, y), (left, y, right, bottom)

    return split_rect(
        first, rng, depth + 1, max_depth, min_size
    ) + split_rect(second, rng, depth + 1, max_depth, min_size)


def render_mondrian(
    rects: list[Rect],
    size: int,
    rng: np.random.Generator,
    line_width: int = 8,
) -> Image.Image:
    """分割した矩形を、白を主体に赤・青・黄・黒で塗り、太い黒線で区切る。"""
    palette: list[tuple[int, int, int]] = [
        (245, 243, 236),  # 白
        (206, 38, 42),  # 赤
        (28, 72, 155),  # 青
        (245, 200, 40),  # 黄
        (25, 25, 25),  # 黒
    ]
    weights: np.ndarray = np.array([0.62, 0.12, 0.1, 0.1, 0.06])

    image: Image.Image = Image.new("RGB", (size, size), palette[0])
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)
    for rect in rects:
        color: tuple[int, int, int] = palette[
            int(rng.choice(len(palette), p=weights))
        ]
        draw.rectangle(
            rect, fill=color, outline=(20, 20, 20), width=line_width
        )
    return image


def quadtree(
    values: np.ndarray,
    left: int,
    top: int,
    size: int,
    threshold: float,
    min_size: int = 4,
) -> list[tuple[int, int, int]]:
    """正方形の領域を、中の値のばらつきが大きい間だけ4分割し続ける。

    ``values`` は2次元配列で、領域 (``left``, ``top``) から一辺
    ``size`` の範囲の標準偏差が ``threshold`` を超え、かつ一辺が
    ``min_size`` の2倍以上なら、4つの小さな正方形に分けて再帰する。
    戻り値は、分割しなかった正方形の (左, 上, 一辺) のリスト。
    """
    block: np.ndarray = values[top:top + size, left:left + size]
    if size < 2 * min_size or float(block.std()) <= threshold:
        return [(left, top, size)]

    half: int = size // 2
    squares: list[tuple[int, int, int]] = []
    for dy in (0, half):
        for dx in (0, half):
            squares += quadtree(
                values, left + dx, top + dy, half, threshold, min_size
            )
    return squares


def render_quadtree(
    rgb: np.ndarray, squares: list[tuple[int, int, int]]
) -> Image.Image:
    """各正方形を、元画像のその範囲の平均色で塗り、細い線で縁取る。"""
    height: int
    width: int
    height, width = rgb.shape[:2]
    image: Image.Image = Image.new("RGB", (width, height))
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)
    for left, top, size in squares:
        block: np.ndarray = rgb[top:top + size, left:left + size]
        mean: np.ndarray = block.reshape(-1, 3).mean(axis=0)
        color: tuple[int, int, int] = (
            int(mean[0]), int(mean[1]), int(mean[2])
        )
        draw.rectangle(
            (left, top, left + size - 1, top + size - 1),
            fill=color,
            outline=(20, 20, 30),
        )
    return image


def main() -> None:
    # 1. モンドリアン風の再帰的な矩形分割。
    size: int = 480
    rng: np.random.Generator = np.random.default_rng(seed=5)
    rects: list[Rect] = split_rect((0.0, 0.0, float(size), float(size)), rng)
    render_mondrian(rects, size, rng).save("subdivision_mondrian.png")

    # 2. ジュリア集合の画像を、明るさのばらつきに応じて四分木で分割する。
    side: int = 512
    max_iter: int = 200
    iterations: np.ndarray = julia_escape(
        complex(-0.7, 0.27015), side, side, max_iter=max_iter
    )
    normalized: np.ndarray = np.sqrt(iterations / max_iter)
    rgb: np.ndarray = (
        colormaps["twilight_shifted"](normalized)[..., :3] * 255
    )
    rgb[iterations >= max_iter] = 0.0
    squares: list[tuple[int, int, int]] = quadtree(
        normalized, 0, 0, side, threshold=0.04, min_size=8
    )
    render_quadtree(rgb, squares).save("subdivision_quadtree.png")


if __name__ == "__main__":
    main()
