"""円板モデルで、正 p 角形を各頂点に q 枚ずつ集めた双曲タイリング {p, q} を描く.

原点を中心とする正 p 角形から始め、辺に関する鏡映を繰り返して隣の多角形を作る。

使い方: python ch08_tiling.py
"""

import math

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

import hg
import hg_plot

Polygon = tuple[complex, list[complex]]  # (中心, 頂点のリスト)


def first_polygon(p: int, q: int) -> Polygon:
    """原点を中心とし、内角が 2 pi / q の正 p 角形.

    中心から頂点までの距離 R は cosh R = cot(pi / p) cot(pi / q) で決まる。
    """
    radius = math.acosh(1.0 / (math.tan(math.pi / p) * math.tan(math.pi / q)))
    return 0j, [hg.disk_point(radius, 2.0 * math.pi * k / p) for k in range(p)]


def tiling(p: int, q: int, layers: int) -> list[list[Polygon]]:
    """{p, q} の多角形を、最初の多角形から辺を何回またぐと届くか（層）ごとに分けて返す."""
    def key(z: complex) -> tuple[int, int]:  # 同じ多角形を 2 回数えないよう、中心の座標で見分ける
        return round(z.real * 1e7), round(z.imag * 1e7)

    start = first_polygon(p, q)
    seen = {key(start[0])}
    result = [[start]]
    for _ in range(layers):
        next_layer: list[Polygon] = []
        for center, vertices in result[-1]:
            for k in range(p):
                a, b = vertices[k], vertices[(k + 1) % p]
                new_center = hg.disk_reflect(center, a, b)
                if key(new_center) in seen:
                    continue
                seen.add(key(new_center))
                next_layer.append((new_center, [hg.disk_reflect(v, a, b) for v in vertices]))
        result.append(next_layer)
    return result


LAYER_COLORS = ["#f28e2b", "#4e79a7", "#7aa1c9", "#a5c3e0", "#cadbed", "#e6eef7", "#f4f7fb"]


def draw_tiling(ax: Axes, p: int, q: int, layers: int) -> None:
    """{p, q} を描く. 最初の多角形から遠い層ほど薄い色で塗る."""
    hg_plot.setup_disk(ax, f"$\\{{{p}, {q}\\}}$")
    for depth, layer in enumerate(tiling(p, q, layers)):
        color = LAYER_COLORS[min(depth, len(LAYER_COLORS) - 1)]
        for _, vertices in layer:
            outline = [hg.disk_geodesic(vertices[k], vertices[(k + 1) % p], 12) for k in range(p)]
            points = [z for side in outline for z in side]
            ax.fill([z.real for z in points], [z.imag for z in points], facecolor=color,
                    edgecolor="0.2", linewidth=0.3)


def create_figure() -> Figure:
    """{7, 3} と {5, 4} と {4, 5} を並べる."""
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.4))
    draw_tiling(axes[0], 7, 3, 5)
    draw_tiling(axes[1], 5, 4, 4)
    draw_tiling(axes[2], 4, 5, 5)
    fig.tight_layout()
    return fig


def report() -> None:
    """層ごとの多角形の数を表示する. 正方形による平面のタイリング {4, 4} では k 層目に 4k 枚ある."""
    for p, q in ((7, 3), (5, 4), (4, 5)):
        counts = [len(layer) for layer in tiling(p, q, 6)]
        ratios = [f"{b / a:.3f}" for a, b in zip(counts[1:], counts[2:])]
        print(f"{{{p}, {q}}} 層ごとの枚数 {counts}")
        print(f"        前の層との比 {ratios}")
    print(f"{{4, 4}} 層ごとの枚数 {[1] + [4 * k for k in range(1, 7)]}")


def main() -> None:
    hg_plot.setup_font()
    report()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
