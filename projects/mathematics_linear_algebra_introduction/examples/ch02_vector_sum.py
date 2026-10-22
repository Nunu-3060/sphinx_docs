"""ベクトルの和と線形結合を矢印で描く.

左: u と v の和（平行四辺形の対角線）
右: 線形結合 2u - v（u を 2 倍した矢印の先に -v をつなぐ）

使い方: python ch02_vector_sum.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import la_plot


def create_figure() -> Figure:
    """ベクトルの和と線形結合の図を描く."""
    u = np.array([3.0, 1.0])
    v = np.array([1.0, 2.0])
    fig, (ax_sum, ax_comb) = plt.subplots(1, 2, figsize=(9, 4.2))

    # 左: 和 u + v。v を u の終点まで平行移動しても、u を v の終点まで
    # 平行移動しても、同じ点に着く
    la_plot.setup_plane(ax_sum, (-0.5, 5), (-0.5, 3.8))
    la_plot.draw_vector(ax_sum, u, color="C0", label=r"$\mathbf{u}$")
    la_plot.draw_vector(ax_sum, v, color="C1", label=r"$\mathbf{v}$", offset=(-0.4, 0.1))
    la_plot.draw_vector(ax_sum, v, origin=u, color="C1", linestyle="--")
    la_plot.draw_vector(ax_sum, u, origin=v, color="C0", linestyle="--")
    la_plot.draw_vector(ax_sum, u + v, color="C2", label=r"$\mathbf{u}+\mathbf{v}$")
    ax_sum.set_title("ベクトルの和")

    # 右: 線形結合 2u - v
    la_plot.setup_plane(ax_comb, (-0.5, 7), (-2.5, 3))
    la_plot.draw_vector(ax_comb, u, color="C0", label=r"$\mathbf{u}$", offset=(-0.2, 0.2))
    la_plot.draw_vector(ax_comb, v, color="C1", label=r"$\mathbf{v}$", offset=(-0.3, 0.2))
    la_plot.draw_vector(ax_comb, 2 * u, color="C0", linestyle="--", label=r"$2\mathbf{u}$")
    la_plot.draw_vector(ax_comb, -v, origin=2 * u, color="C1", linestyle="--",
                        label=r"$-\mathbf{v}$", offset=(0.15, 0.6))
    la_plot.draw_vector(ax_comb, 2 * u - v, color="C2", label=r"$2\mathbf{u}-\mathbf{v}$",
                        offset=(-0.6, -0.6))
    ax_comb.set_title("線形結合")

    fig.tight_layout()
    return fig


def main() -> None:
    la_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
