"""「2 次元の図形のラスタライズ」の章の図を作るスクリプト。

考え方が分かりやすいように、画素を 1 つずつ調べる素朴な書き方をしている。
小さな画像にしか使わないので、速さは重視していない。

次の図を作る。

* line.png: ブレゼンハムのアルゴリズムで描いた線分
* triangle.png: エッジ関数で塗りつぶした三角形
* barycentric.png: 重心座標で頂点の色を補間した三角形
* aliasing.png: 画素ごとに 1 点で判定した図形と、16 点で判定した図形
"""

import numpy as np
from PIL import Image, ImageDraw

from cg_utils import (FloatArray, enlarge, from_pil, hstack, output_dir,
                      save_image, to_pil)

Point = tuple[float, float]

# 拡大図で、画素の境界の線と塗りつぶした画素に使う色。
GRID_COLOR = (190, 190, 190)
FILL_COLOR = np.array([0.15, 0.35, 0.7])
OUTLINE_COLOR = (220, 40, 40)


# ---------------------------------------------------------------------------
# 線分
# ---------------------------------------------------------------------------

def draw_line(x0: int, y0: int, x1: int, y1: int) -> list[tuple[int, int]]:
    """ブレゼンハムのアルゴリズムで、線分上の画素の座標を求める。

    整数の加算と比較だけで、全ての向きの線分を扱える形にしている。
    """
    pixels = []
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy  # 理想的な線分からのずれ(を整数倍したもの)
    x, y = x0, y0
    while True:
        pixels.append((x, y))
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 >= dy:  # x 方向に進む
            err += dy
            x += sx
        if e2 <= dx:  # y 方向に進む
            err += dx
            y += sy
    return pixels


# ---------------------------------------------------------------------------
# 三角形
# ---------------------------------------------------------------------------

def edge_function(a: Point, b: Point, p: Point) -> float:
    """辺 a→b に対して、点 p がどちら側にあるかを表す値を返す。

    ベクトル (b - a) と (p - a) の外積の z 成分であり、値の絶対値は
    3 点 a、b、p が作る三角形の面積の 2 倍に等しい。
    """
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


def barycentric(v0: Point, v1: Point, v2: Point,
                p: Point) -> tuple[float, float, float] | None:
    """点 p の重心座標 (w0, w1, w2) を返す。p が三角形の外にあれば None。"""
    area = edge_function(v0, v1, v2)
    if area == 0.0:
        return None  # 面積が 0 の三角形は描かない
    w0 = edge_function(v1, v2, p) / area
    w1 = edge_function(v2, v0, p) / area
    w2 = edge_function(v0, v1, p) / area
    if w0 < 0.0 or w1 < 0.0 or w2 < 0.0:
        return None
    return w0, w1, w2


def rasterize_triangle(
        v0: Point, v1: Point, v2: Point, width: int, height: int
) -> list[tuple[int, int, tuple[float, float, float]]]:
    """三角形の内側にある画素と、その中心の重心座標を求める。

    三角形を囲む長方形(バウンディングボックス)の画素だけを調べる。
    """
    xs = [v0[0], v1[0], v2[0]]
    ys = [v0[1], v1[1], v2[1]]
    x_min = max(int(np.floor(min(xs))), 0)
    x_max = min(int(np.ceil(max(xs))), width - 1)
    y_min = max(int(np.floor(min(ys))), 0)
    y_max = min(int(np.ceil(max(ys))), height - 1)

    result = []
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            center = (x + 0.5, y + 0.5)
            weights = barycentric(v0, v1, v2, center)
            if weights is not None:
                result.append((x, y, weights))
    return result


# ---------------------------------------------------------------------------
# 図の作成
# ---------------------------------------------------------------------------

def grid_image(mask: FloatArray, scale: int) -> Image.Image:
    """塗りつぶす画素を表す配列を拡大し、画素の境界の線を引いた画像を返す。"""
    height, width = mask.shape
    image = np.where(mask[..., None] > 0.0, FILL_COLOR, 1.0)
    pil = to_pil(enlarge(image, scale))
    draw = ImageDraw.Draw(pil)
    for i in range(width + 1):
        draw.line([(i * scale, 0), (i * scale, height * scale)],
                  fill=GRID_COLOR)
    for j in range(height + 1):
        draw.line([(0, j * scale), (width * scale, j * scale)],
                  fill=GRID_COLOR)
    return pil


def line_figure() -> FloatArray:
    """ブレゼンハムのアルゴリズムで描いた線分と、元の線分を重ねて示す。"""
    width, height, scale = 24, 14, 20
    mask = np.zeros((height, width))
    segments = [(1, 12, 22, 2), (2, 2, 9, 12)]
    for x0, y0, x1, y1 in segments:
        for x, y in draw_line(x0, y0, x1, y1):
            mask[y, x] = 1.0
    pil = grid_image(mask, scale)
    draw = ImageDraw.Draw(pil)
    for x0, y0, x1, y1 in segments:
        # 画素 (x, y) の中心は拡大図の ((x + 0.5) * scale, ...) にある。
        start = ((x0 + 0.5) * scale, (y0 + 0.5) * scale)
        end = ((x1 + 0.5) * scale, (y1 + 0.5) * scale)
        draw.line([start, end], fill=OUTLINE_COLOR, width=2)
    return from_pil(pil)


def triangle_figure() -> FloatArray:
    """エッジ関数で塗りつぶした三角形と、元の三角形の輪郭を重ねて示す。"""
    width, height, scale = 24, 14, 20
    v0, v1, v2 = (2.3, 12.4), (21.6, 9.2), (8.7, 1.4)
    mask = np.zeros((height, width))
    for x, y, _ in rasterize_triangle(v0, v1, v2, width, height):
        mask[y, x] = 1.0
    pil = grid_image(mask, scale)
    draw = ImageDraw.Draw(pil)
    corners = [(x * scale, y * scale) for x, y in (v0, v1, v2)]
    draw.polygon(corners, outline=OUTLINE_COLOR, width=2)
    # 画素の中心に小さな点を打ち、判定に使う位置を示す。
    for j in range(height):
        for i in range(width):
            cx, cy = (i + 0.5) * scale, (j + 0.5) * scale
            draw.ellipse([cx - 1.5, cy - 1.5, cx + 1.5, cy + 1.5],
                         fill=(90, 90, 90))
    return from_pil(pil)


def barycentric_figure() -> FloatArray:
    """頂点に赤、緑、青を与え、重心座標で内部の色を補間した三角形を描く。"""
    width, height = 320, 256
    v0, v1, v2 = (30.0, 236.0), (290.0, 236.0), (160.0, 20.0)
    colors = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    image = np.ones((height, width, 3))
    for x, y, weights in rasterize_triangle(v0, v1, v2, width, height):
        image[y, x] = np.array(weights) @ colors
    return image


def coverage(v0: Point, v1: Point, v2: Point, width: int, height: int,
             n: int) -> FloatArray:
    """各画素を n × n 個の点で調べ、三角形に覆われる割合を求める。

    n = 1 のときは画素の中心だけを調べることになる。
    """
    result = np.zeros((height, width))
    offsets = (np.arange(n) + 0.5) / n
    for y in range(height):
        for x in range(width):
            inside = 0
            for oy in offsets:
                for ox in offsets:
                    if barycentric(v0, v1, v2, (x + ox, y + oy)) is not None:
                        inside += 1
            result[y, x] = inside / (n * n)
    return result


def aliasing_figure() -> FloatArray:
    """細長い三角形を、1 点の判定と 4 × 4 点の判定で描いて比べる。"""
    width, height, scale = 48, 32, 6
    v0, v1, v2 = (2.0, 29.0), (46.0, 4.0), (45.0, 9.0)
    panels = []
    for n in (1, 4):
        c = coverage(v0, v1, v2, width, height, n)[..., None]
        image = c * FILL_COLOR + (1.0 - c) * 1.0
        panels.append(enlarge(image, scale))
    return hstack(panels)


def main() -> None:
    out = output_dir()
    save_image(line_figure(), out / "line.png")
    save_image(triangle_figure(), out / "triangle.png")
    save_image(barycentric_figure(), out / "barycentric.png")
    save_image(aliasing_figure(), out / "aliasing.png")


if __name__ == "__main__":
    main()
