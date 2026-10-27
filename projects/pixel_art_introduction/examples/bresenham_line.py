"""ブレゼンハムのアルゴリズムで直線を描く。

キャンバスの中心から放射状に直線を引き、拡大した画像を保存する。

使い方::

    python bresenham_line.py
"""

from pathlib import Path

from PIL import Image

Point = tuple[int, int]


def bresenham(x0: int, y0: int, x1: int, y1: int) -> list[Point]:
    """(x0, y0) から (x1, y1) までの直線上のピクセル座標を返す。

    整数の加減算だけで、隣り合うピクセルが辺または角で接する 1 ピクセル幅の線を求める。
    """
    points: list[Point] = []
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    step_x = 1 if x0 < x1 else -1
    step_y = 1 if y0 < y1 else -1
    error = dx + dy  # 理想の直線からのずれ（を整数化したもの）

    x, y = x0, y0
    while True:
        points.append((x, y))
        if x == x1 and y == y1:
            break
        doubled = 2 * error
        if doubled >= dy:  # x 方向に進む
            error += dy
            x += step_x
        if doubled <= dx:  # y 方向に進む
            error += dx
            y += step_y
    return points


def main() -> None:
    size = 33
    center = size // 2
    image = Image.new("RGB", (size, size), (240, 240, 232))

    # 中心から外周の各点に向けて直線を引く
    targets: list[Point] = [(0, 0), (8, 0), (16, 0), (24, 0), (32, 0), (32, 8), (32, 16), (32, 24),
                            (32, 32), (24, 32), (16, 32), (8, 32), (0, 32), (0, 24), (0, 16), (0, 8)]
    for target in targets:
        for point in bresenham(center, center, *target):
            image.putpixel(point, (34, 32, 52))

    output = Path("output/lines.png")
    output.parent.mkdir(parents=True, exist_ok=True)
    image.resize((size * 8, size * 8), Image.Resampling.NEAREST).save(output)
    print(f"保存した: {output}")


if __name__ == "__main__":
    main()
