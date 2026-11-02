"""第 4 章「パターンとマテリアル」: 2 次元の距離関数（SDF）で図形を描く図を作る。

* sdf_shapes.png: 円と箱の距離関数を、等高線付きの色で表した図
* sdf_ops.png: 和・積・差・滑らかな和による図形の組み合わせ
* sdf_smooth.png: 滑らかな和の k を変えた図形
"""

from __future__ import annotations

import numpy as np

from color import hex_to_rgb
from common import FloatArray, grid, output_dir, setup_matplotlib
from texture import mix, show_panels, smoothstep

SIZE = 256


def sd_circle(x: FloatArray, y: FloatArray, cx: float, cy: float, radius: float) -> FloatArray:
    """中心 (cx, cy)、半径 radius の円までの符号付き距離（内側で負）。"""
    return np.hypot(x - cx, y - cy) - radius


def sd_box(x: FloatArray, y: FloatArray, cx: float, cy: float, half_w: float, half_h: float) -> FloatArray:
    """中心 (cx, cy)、半分の幅 half_w、半分の高さ half_h の長方形までの符号付き距離。"""
    dx = np.abs(x - cx) - half_w  # 各軸について、辺からどれだけ外にあるか
    dy = np.abs(y - cy) - half_h
    outside = np.hypot(np.maximum(dx, 0.0), np.maximum(dy, 0.0))  # 外側: 最も近い辺または角までの距離
    inside = np.minimum(np.maximum(dx, dy), 0.0)  # 内側: 最も近い辺までの距離（負）
    return outside + inside


def op_union(a: FloatArray, b: FloatArray) -> FloatArray:
    """和（どちらかの内側）。"""
    return np.minimum(a, b)


def op_intersection(a: FloatArray, b: FloatArray) -> FloatArray:
    """積（両方の内側）。"""
    return np.maximum(a, b)


def op_subtraction(a: FloatArray, b: FloatArray) -> FloatArray:
    """差（a の内側で、b の外側）。"""
    return np.maximum(a, -b)


def op_smooth_union(a: FloatArray, b: FloatArray, k: float) -> FloatArray:
    """滑らかな和（多項式による smooth min）。k は角を丸める幅で、0 なら普通の和になる。"""
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
    return b + (a - b) * h - k * h * (1.0 - h)


def visualize(distance: FloatArray, pixel: float) -> FloatArray:
    """距離を色で表す。外側は橙、内側は青、0.1 ごとに等高線、境界（距離 0）を白い線で描く。"""
    outside = np.array(hex_to_rgb("#e8a35d"))
    inside = np.array(hex_to_rgb("#5d8fc9"))
    base = mix(inside, outside, (distance > 0).astype(np.float64))
    base = base * (1.0 - np.exp(-6.0 * np.abs(distance)))[..., None] * 0.6 + base * 0.4  # 境界の近くを暗く
    bands = 0.85 + 0.15 * np.cos(2.0 * np.pi * distance / 0.1)  # 等高線
    color = base * bands[..., None]
    edge = smoothstep(1.5 * pixel, 0.5 * pixel, np.abs(distance))
    return mix(color, np.ones(3), edge)


def fill(distance: FloatArray, pixel: float) -> FloatArray:
    """距離 0 を境に、内側を塗りつぶした画像（境界を 1 画素分ぼかす）。

    滑らかな和などでは値が正確な距離からずれる（傾きが 1 より小さくなる）ので、
    傾きの大きさで割って、ぼかす幅を画素単位にそろえる。
    """
    d_row, d_col = np.gradient(distance, pixel)
    slope = np.maximum(np.hypot(d_row, d_col), 1e-3)
    return smoothstep(pixel, -pixel, distance / slope)


def draw_shapes(file_name: str) -> None:
    x, y = grid(SIZE, SIZE, scale=2.0)
    pixel = 2.0 / SIZE
    circle = sd_circle(x, y, 1.0, 1.0, 0.6)
    box = sd_box(x, y, 1.0, 1.0, 0.6, 0.35)
    images = [fill(circle, pixel), visualize(circle, pixel), fill(box, pixel), visualize(box, pixel)]
    titles = ["円（塗りつぶし）", "円の距離", "長方形（塗りつぶし）", "長方形の距離"]
    show_panels(images, titles, output_dir(__file__) / file_name)


def draw_ops(file_name: str) -> None:
    x, y = grid(SIZE, SIZE, scale=2.0)
    pixel = 2.0 / SIZE
    circle = sd_circle(x, y, 1.25, 0.8, 0.45)
    box = sd_box(x, y, 0.8, 1.15, 0.45, 0.35)
    shapes = [
        ("和 min(a, b)", op_union(circle, box)),
        ("積 max(a, b)", op_intersection(circle, box)),
        ("差 max(a, −b)", op_subtraction(box, circle)),
        ("滑らかな和（k = 0.25）", op_smooth_union(circle, box, 0.25)),
    ]
    show_panels([visualize(d, pixel) for _, d in shapes], [title for title, _ in shapes],
                output_dir(__file__) / file_name)


def draw_smooth(file_name: str) -> None:
    """smooth min の k を変えて、2 つの円がつながる様子を比べる。"""
    x, y = grid(SIZE, SIZE // 2, scale=2.0)
    pixel = 2.0 / SIZE
    a = sd_circle(x, y, 0.7, 0.5, 0.3)
    b = sd_circle(x, y, 1.3, 0.5, 0.3)
    ks = (0.0, 0.1, 0.25, 0.5)
    images = [fill(op_union(a, b) if k == 0.0 else op_smooth_union(a, b, k), pixel) for k in ks]
    show_panels(images, [f"k = {k:g}" for k in ks], output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_shapes("sdf_shapes.png")
    draw_ops("sdf_ops.png")
    draw_smooth("sdf_smooth.png")


if __name__ == "__main__":
    main()
