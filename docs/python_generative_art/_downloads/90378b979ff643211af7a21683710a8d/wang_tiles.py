"""ワン・タイル (Wang tiles) による、辺の制約を満たすタイリング。

これまでのタイリングは、タイルの向きをランダムに選ぶか
（トルシェ・タイル）、あるいは市松模様のような決め打ちの規則で
選ぶか（編み込みパターン）のどちらかだった。ワン・タイルは、隣り
合うタイルの辺どうしが必ず一致するように配置する、制約充足に基づく
タイリングである。

正しいワン・タイルの理論では、あらかじめ用意したタイル集合から
制約を満たすタイルを探索して配置するが、ここでは逆に、格子の
縦線・横線それぞれに先にラベル（色）を割り振ってしまうことで、
探索なしで辺の一致を保証する簡単な方法を使う。各タイルは、上下左右
の境界線のラベルによって4つの三角形に塗り分けられ、隣接するタイル
との境界では必ず同じラベル（同じ色）の三角形どうしが接する。
"""

import numpy as np
from PIL import Image, ImageDraw


def wang_edge_labels(
    rows: int, cols: int, num_labels: int, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    """タイル格子の内部にある縦線・横線それぞれにラベルを割り当てる。

    ``vertical_line_labels`` (形状 ``(rows, cols - 1)``) は、列 ``c``
    と ``c + 1`` の間にある縦線のラベルを行ごとに持つ。
    ``horizontal_line_labels`` (形状 ``(rows - 1, cols)``) は、行
    ``r`` と ``r + 1`` の間にある横線のラベルを列ごとに持つ。
    """
    vertical_line_labels: np.ndarray = rng.integers(
        0, num_labels, size=(rows, max(cols - 1, 0))
    )
    horizontal_line_labels: np.ndarray = rng.integers(
        0, num_labels, size=(max(rows - 1, 0), cols)
    )
    return vertical_line_labels, horizontal_line_labels


def render_wang_tiling(
    rows: int,
    cols: int,
    tile_size: int,
    num_labels: int,
    rng: np.random.Generator,
    palette: list[tuple[int, int, int]],
    border_label: int = 0,
) -> Image.Image:
    """辺のラベル配列から、辺の一致が保証されたタイル格子を描く。

    各タイルは、上(N)・右(E)・下(S)・左(W)の4つの三角形に分けて
    塗り分ける。あるタイルの東の三角形の色は、右隣のタイルの西の
    三角形の色と、共有する縦線のラベルを通じて必ず一致する。
    """
    vertical_line_labels: np.ndarray
    horizontal_line_labels: np.ndarray
    vertical_line_labels, horizontal_line_labels = wang_edge_labels(
        rows, cols, num_labels, rng
    )

    img: Image.Image = Image.new(
        "RGB", (cols * tile_size, rows * tile_size), "white"
    )
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)

    for row in range(rows):
        for col in range(cols):
            west: int = (
                int(vertical_line_labels[row, col - 1])
                if col > 0
                else border_label
            )
            east: int = (
                int(vertical_line_labels[row, col])
                if col < cols - 1
                else border_label
            )
            north: int = (
                int(horizontal_line_labels[row - 1, col])
                if row > 0
                else border_label
            )
            south: int = (
                int(horizontal_line_labels[row, col])
                if row < rows - 1
                else border_label
            )

            x0: float = col * tile_size
            y0: float = row * tile_size
            x1: float = x0 + tile_size
            y1: float = y0 + tile_size
            cx: float = (x0 + x1) / 2.0
            cy: float = (y0 + y1) / 2.0

            draw.polygon(
                [(x0, y0), (x1, y0), (cx, cy)],
                fill=palette[north],
            )
            draw.polygon(
                [(x1, y0), (x1, y1), (cx, cy)],
                fill=palette[east],
            )
            draw.polygon(
                [(x0, y1), (x1, y1), (cx, cy)],
                fill=palette[south],
            )
            draw.polygon(
                [(x0, y0), (x0, y1), (cx, cy)],
                fill=palette[west],
            )

    return img


def main() -> None:
    rng: np.random.Generator = np.random.default_rng(seed=6)
    palette: list[tuple[int, int, int]] = [
        (230, 100, 90),
        (240, 180, 80),
        (90, 170, 150),
        (80, 120, 190),
    ]

    render_wang_tiling(18, 18, 28, len(palette), rng, palette).save(
        "wang_tiles.png"
    )


if __name__ == "__main__":
    main()
