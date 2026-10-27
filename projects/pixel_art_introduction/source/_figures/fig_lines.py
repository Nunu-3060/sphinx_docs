"""第 4 章の図。"""

from pathlib import Path

from common import hstack, points_image, save, with_grid
from bresenham_line import bresenham

Point = tuple[int, int]
Run = tuple[str, int]


def stroke(runs: list[Run]) -> list[Point]:
    """連続するピクセルの並び（ラン）から線の座標を作る。

    ("h", n) は横に n ピクセル、("v", n) は縦に n ピクセル並べる。
    ランとランの間は斜め（角で接する）につなぐ。座標は左下原点、上向きが正。
    """
    points: list[Point] = []
    x = y = 0
    for axis, length in runs:
        for _ in range(length):
            points.append((x, y))
            if axis == "h":
                x += 1
            else:
                y += 1
        if axis == "h":
            y += 1
        else:
            x += 1
    return points


def add_doubles(points: list[Point]) -> list[Point]:
    """斜めにつながる箇所に余分なピクセルを足し、L 字型の角（ダブルドット）を作る。"""
    result = list(points)
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if x1 != x0 and y1 != y0:
            result.append((x1, y0))
    return result


def lines_clean(out_dir: Path) -> None:
    """きれいに見える代表的な傾きの直線（1:1、2:1、3:1、4:1）。"""
    images = [with_grid(points_image(stroke([("h", n)] * (12 // n))), 12) for n in (1, 2, 3, 4)]
    save(hstack(images), out_dir, "lines_clean.png")


def lines_compare(out_dir: Path) -> None:
    """同じ傾きで、ランの長さがそろった直線とばらばらな直線。"""
    even = stroke([("h", 2)] * 6)
    uneven = stroke([("h", n) for n in (3, 1, 2, 3, 1, 2)])
    save(hstack([with_grid(points_image(even), 12), with_grid(points_image(uneven), 12)]), out_dir,
         "lines_compare.png")


def curves(out_dir: Path) -> None:
    """ランの長さが単調に変化する曲線と、ばらばらに変化する曲線。"""
    smooth = stroke([("v", 4), ("v", 2), ("v", 1), ("h", 1), ("h", 2), ("h", 4)])
    bumpy = stroke([("v", 3), ("v", 1), ("v", 3), ("h", 2), ("h", 1), ("h", 4)])
    save(hstack([with_grid(points_image(smooth), 12), with_grid(points_image(bumpy), 12)]), out_dir, "curves.png")


def doubles(out_dir: Path) -> None:
    """L 字型の角があるダブルドットの線と、それを取り除いた線。"""
    clean = stroke([("v", 4), ("v", 2), ("v", 1), ("h", 1), ("h", 2), ("h", 4)])
    save(hstack([with_grid(points_image(add_doubles(clean)), 12), with_grid(points_image(clean), 12)]), out_dir,
         "doubles.png")


def bresenham_figure(out_dir: Path) -> None:
    """ブレゼンハムのアルゴリズムで中心から放射状に引いた直線。"""
    points: list[Point] = []
    for target in [(0, 0), (8, 0), (16, 0), (24, 0), (32, 0), (32, 8), (32, 16), (32, 24),
                   (32, 32), (24, 32), (16, 32), (8, 32), (0, 32), (0, 24), (0, 16), (0, 8)]:
        points += bresenham(16, 16, *target)
    save(with_grid(points_image(points, margin=0), 8), out_dir, "bresenham.png")


def generate(out_dir: Path) -> None:
    lines_clean(out_dir)
    lines_compare(out_dir)
    curves(out_dir)
    doubles(out_dir)
    bresenham_figure(out_dir)
