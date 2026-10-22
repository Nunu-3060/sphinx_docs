"""辺の長さがすべて等しい木を、ユークリッド平面と双曲平面（円板モデル）に描いて比べる.

根から 3 本の枝を出し、その先は各頂点から 2 本ずつ枝分かれさせる。
枝分かれの角度と辺の長さは、どちらの平面でも同じにする。

使い方: python ch07_tree.py
"""

import cmath
import math

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import hg
import hg_plot

DEPTH = 6  # 根からの深さ
EDGE = 1.0  # 辺の長さ
SPREAD = 0.7  # 親から来た向きに対して、子へ向かう枝が左右に開く角度（ラジアン）

Edge = tuple[complex, complex]


def euclidean_tree() -> list[Edge]:
    """ユークリッド平面に木を描いたときの辺（両端の座標の組）のリストを返す."""
    edges: list[Edge] = []

    def grow(p: complex, heading: float, depth: int) -> None:
        if depth == DEPTH:
            return
        for delta in (-SPREAD, SPREAD):
            child = p + EDGE * cmath.exp(1j * (heading + delta))
            edges.append((p, child))
            grow(child, heading + delta, depth + 1)

    for k in range(3):
        heading = math.pi / 2.0 + 2.0 * math.pi * k / 3.0
        child = EDGE * cmath.exp(1j * heading)
        edges.append((0j, child))
        grow(child, heading, 1)
    return edges


def hyperbolic_tree(root: complex = 0j) -> list[Edge]:
    """円板モデルに木を描いたときの辺のリストを返す. root は根の位置.

    頂点 p での向きは、p を原点に移した座標で考える（disk_translate は原点での向きを変えない）。
    """
    edges: list[Edge] = []

    def grow(parent: complex, p: complex, depth: int) -> None:
        if depth == DEPTH:
            return
        heading = cmath.phase(-hg.disk_translate(-p, parent))  # 親から来た向き
        for delta in (-SPREAD, SPREAD):
            child = hg.disk_translate(p, hg.disk_point(EDGE, heading + delta))
            edges.append((p, child))
            grow(p, child, depth + 1)

    for k in range(3):
        child = hg.disk_translate(root, hg.disk_point(EDGE, math.pi / 2.0 + 2.0 * math.pi * k / 3.0))
        edges.append((root, child))
        grow(root, child, 1)
    return edges


def create_figure() -> Figure:
    """左にユークリッド平面の木、右に双曲平面の木を描く."""
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 5.0))
    ax = axes[0]
    for p, q in euclidean_tree():
        ax.plot([p.real, q.real], [p.imag, q.imag], color="C0", linewidth=0.8)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("ユークリッド平面")

    ax = axes[1]
    hg_plot.setup_disk(ax, "双曲平面（ポアンカレ円板モデル）")
    for p, q in hyperbolic_tree():
        hg_plot.plot_complex(ax, hg.disk_geodesic(p, q, 20), color="C0", linewidth=0.8)
    fig.tight_layout()
    return fig


def main() -> None:
    hg_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
