"""2 つのベクトルが張る空間を描く.

線形結合 c1 u + c2 v の係数 c1、c2 をいろいろに変えて、その点を打つ。
左: u と v が線形独立なら、点は平面全体に広がる。
右: u と v が線形従属（平行）なら、点は 1 本の直線の上にしか乗らない。

使い方: python ch07_span.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import la_plot


def create_figure() -> Figure:
    """線形独立な場合と線形従属な場合の、線形結合の点を描く."""
    cases = [
        ("線形独立（平面全体を張る）", np.array([2.0, 1.0]), np.array([1.0, 2.0])),
        ("線形従属（直線しか張らない）", np.array([2.0, 1.0]), np.array([-1.0, -0.5])),
    ]
    coefficients = np.linspace(-2.0, 2.0, 9)
    c1, c2 = np.meshgrid(coefficients, coefficients)
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.4))
    for ax, (title, u, v) in zip(axes, cases):
        la_plot.setup_plane(ax, (-5, 5), (-5, 5))
        points = np.outer(c1.ravel(), u) + np.outer(c2.ravel(), v)
        ax.scatter(points[:, 0], points[:, 1], s=8, color="C2", alpha=0.6)
        la_plot.draw_vector(ax, u, color="C0", label=r"$\mathbf{u}$")
        la_plot.draw_vector(ax, v, color="C1", label=r"$\mathbf{v}$", offset=(-0.6, 0.1))
        ax.set_title(title)
    fig.tight_layout()
    return fig


def main() -> None:
    la_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
