"""極座標の基底ベクトル e_r と e_θ が、点の位置によって向きを変える様子を描く.

使い方: python ch09_polar_basis.py
"""

import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import vc_plot


def polar_basis(theta: float) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """角度 theta の点での単位ベクトル e_r と e_θ を返す."""
    e_r = np.array([np.cos(theta), np.sin(theta)])
    e_theta = np.array([-np.sin(theta), np.cos(theta)])
    return e_r, e_theta


def create_figure() -> Figure:
    """座標曲線（r 一定の円と θ 一定の半直線）と、いくつかの点での基底ベクトルを描く."""
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    vc_plot.setup_plane(ax, (-3.2, 3.2), (-3.2, 3.2))

    # 座標曲線：r が一定の円と、θ が一定の半直線
    s = np.linspace(0.0, 2.0 * np.pi, 200)
    for radius in (1.0, 2.0, 3.0):
        ax.plot(radius * np.cos(s), radius * np.sin(s), color="0.75", linewidth=0.8)
    for angle in np.linspace(0.0, 2.0 * np.pi, 12, endpoint=False):
        ax.plot([0.0, 3.2 * np.cos(angle)], [0.0, 3.2 * np.sin(angle)], color="0.75", linewidth=0.8)

    # いくつかの点で e_r（青）と e_θ（橙）を描く
    points = [(1.0, math.pi / 6), (2.0, 2 * math.pi / 3), (2.0, 7 * math.pi / 6), (2.4, 5 * math.pi / 3)]
    for i, (r, theta) in enumerate(points):
        e_r, e_theta = polar_basis(theta)
        p = r * e_r
        ax.plot(p[0], p[1], "ko", markersize=4)
        label_r = r"$\mathbf{e}_r$" if i == 0 else None
        label_t = r"$\mathbf{e}_\theta$" if i == 0 else None
        vc_plot.draw_vector(ax, 0.8 * e_r, origin=p, color="C0", label=label_r, offset=(0.05, -0.25))
        vc_plot.draw_vector(ax, 0.8 * e_theta, origin=p, color="C1", label=label_t, offset=(-0.35, 0.05))

    ax.set_title("極座標の基底ベクトル（青：$\\mathbf{e}_r$、橙：$\\mathbf{e}_\\theta$）")
    fig.tight_layout()
    return fig


def main() -> None:
    vc_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
