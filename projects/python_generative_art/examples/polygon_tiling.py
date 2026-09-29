"""正方形以外の正多角形によるタイリング: 三角形・六角形グリッド。

:doc:`../tiling` のトルシェ・タイルは正方形の格子を前提としていたが、
平面を隙間なく敷き詰められる正多角形は正方形だけではない。正三角形と
正六角形も同様に敷き詰められる（この3種類だけが正多角形による
正則タイリングを作れることが知られている）。ここでは、それぞれの
格子上の各セルをランダムな色で塗り分け、タイルの形そのものが
模様の印象をどう変えるかを見る。
"""

import math

import numpy as np
from PIL import Image, ImageDraw


def triangular_mesh(
    cols: int, rows: int, size: float
) -> list[list[tuple[float, float]]]:
    """正三角形格子の、各三角形の頂点リストを返す。

    1行につき上向き・下向きの三角形が交互に ``cols * 2`` 枚並び、
    それが ``rows`` 行分続く。辺の長さはすべて ``size`` で揃う。
    """
    height: float = size * (3 ** 0.5) / 2
    half: float = size / 2
    triangles: list[list[tuple[float, float]]] = []

    for row in range(rows):
        y_top: float = row * height
        y_bot: float = y_top + height
        for i in range(cols * 2):
            x_left: float = i * half
            x_mid: float = x_left + half
            x_right: float = x_left + size
            if i % 2 == 0:
                triangles.append(
                    [(x_left, y_bot), (x_right, y_bot), (x_mid, y_top)]
                )
            else:
                triangles.append(
                    [(x_left, y_top), (x_right, y_top), (x_mid, y_bot)]
                )

    return triangles


def render_triangular_mosaic(
    cols: int,
    rows: int,
    size: float,
    rng: np.random.Generator,
    palette: list[tuple[int, int, int]],
    line_color: tuple[int, int, int] = (255, 255, 255),
) -> Image.Image:
    """三角形格子の各セルを、パレットからランダムに選んだ色で塗る。"""
    triangles: list[list[tuple[float, float]]] = triangular_mesh(
        cols, rows, size
    )
    width: int = int(cols * size)
    height: int = int(rows * size * (3 ** 0.5) / 2)
    img: Image.Image = Image.new("RGB", (width, height), line_color)
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)

    choices: np.ndarray = rng.integers(0, len(palette), size=len(triangles))
    for triangle, choice in zip(triangles, choices):
        draw.polygon(triangle, fill=palette[int(choice)])

    return img


def hex_centers(
    cols: int, rows: int, size: float
) -> list[tuple[float, float]]:
    """正六角形格子(頂点が上下にある向き)の各セルの中心座標を返す。"""
    width: float = (3 ** 0.5) * size
    vert_spacing: float = size * 1.5
    centers: list[tuple[float, float]] = []

    for row in range(rows):
        y: float = row * vert_spacing
        x_offset: float = (width / 2) if row % 2 else 0.0
        for col in range(cols):
            x: float = col * width + x_offset
            centers.append((x, y))

    return centers


def hex_vertices(
    cx: float, cy: float, size: float
) -> list[tuple[float, float]]:
    """中心 (cx, cy)、外接円の半径 size の正六角形の頂点リストを返す。"""
    return [
        (
            cx + size * math.cos(math.radians(60 * i - 30)),
            cy + size * math.sin(math.radians(60 * i - 30)),
        )
        for i in range(6)
    ]


def render_hex_mosaic(
    cols: int,
    rows: int,
    size: float,
    rng: np.random.Generator,
    palette: list[tuple[int, int, int]],
    line_color: tuple[int, int, int] = (255, 255, 255),
) -> Image.Image:
    """六角形格子の各セルを、パレットからランダムに選んだ色で塗る。"""
    centers: list[tuple[float, float]] = hex_centers(cols, rows, size)
    width: int = int(cols * (3 ** 0.5) * size + size)
    height: int = int(rows * size * 1.5 + size)
    img: Image.Image = Image.new("RGB", (width, height), line_color)
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)

    choices: np.ndarray = rng.integers(0, len(palette), size=len(centers))
    for (cx, cy), choice in zip(centers, choices):
        draw.polygon(hex_vertices(cx, cy, size), fill=palette[int(choice)])

    return img


def main() -> None:
    rng: np.random.Generator = np.random.default_rng(seed=4)
    palette: list[tuple[int, int, int]] = [
        (230, 100, 90),
        (240, 180, 80),
        (90, 170, 150),
        (80, 120, 190),
    ]

    render_triangular_mosaic(16, 14, 30.0, rng, palette).save(
        "triangular_mosaic.png"
    )
    render_hex_mosaic(12, 12, 22.0, rng, palette).save("hex_mosaic.png")


if __name__ == "__main__":
    main()
