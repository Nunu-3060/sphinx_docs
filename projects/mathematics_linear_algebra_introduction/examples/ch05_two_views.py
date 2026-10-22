"""連立一次方程式の 2 つの見方を描く.

    2x -  y = 1
     x +  y = 5

左: 行の見方。各式は直線を表し、解は 2 本の直線の交点 (2, 3) である。
右: 列の見方。解は、右辺 b = (1, 5) を列ベクトル a1 = (2, 1) と
a2 = (-1, 1) の線形結合で表すときの係数である（b = 2 a1 + 3 a2）。

使い方: python ch05_two_views.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import la_plot


def create_figure() -> Figure:
    """行の見方と列の見方の図を描く."""
    a1 = np.array([2.0, 1.0])
    a2 = np.array([-1.0, 1.0])
    b = np.array([1.0, 5.0])
    fig, (ax_row, ax_col) = plt.subplots(1, 2, figsize=(10, 4.6))

    # 行の見方: 2 本の直線の交点
    la_plot.setup_plane(ax_row, (-1, 5), (-1, 6))
    x = np.linspace(-1, 5, 2)
    ax_row.plot(x, 2 * x - 1, color="C0", label=r"$2x - y = 1$")
    ax_row.plot(x, 5 - x, color="C1", label=r"$x + y = 5$")
    ax_row.plot(2, 3, "o", color="C3")
    ax_row.annotate("解 (2, 3)", xy=(2, 3), xytext=(2.6, 3.6), color="C3")
    ax_row.legend(loc="lower right")
    ax_row.set_title("行の見方（直線の交点）")

    # 列の見方: 列ベクトルの線形結合
    la_plot.setup_plane(ax_col, (-3.5, 4.5), (-1, 6))
    la_plot.draw_vector(ax_col, a1, color="C0", label=r"$\mathbf{a}_1$", offset=(0.1, -0.4))
    la_plot.draw_vector(ax_col, a2, color="C1", label=r"$\mathbf{a}_2$", offset=(-0.5, 0.0))
    la_plot.draw_vector(ax_col, 2 * a1, color="C0", linestyle="--", label=r"$2\mathbf{a}_1$",
                        offset=(0.1, -0.3))
    la_plot.draw_vector(ax_col, 3 * a2, origin=2 * a1, color="C1", linestyle="--",
                        label=r"$3\mathbf{a}_2$", offset=(0.3, -1.2))
    la_plot.draw_vector(ax_col, b, color="C3", label=r"$\mathbf{b}$", offset=(0.1, 0.1))
    ax_col.set_title("列の見方（列ベクトルの線形結合）")

    fig.tight_layout()
    return fig


def main() -> None:
    la_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
