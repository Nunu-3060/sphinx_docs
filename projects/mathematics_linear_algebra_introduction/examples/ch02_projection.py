"""内積と正射影: u を v の方向の成分と、v に直交する成分に分ける.

使い方: python ch02_projection.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import la_plot


def create_figure() -> Figure:
    """u の v 方向への正射影 p と、残りの成分 u - p を描く."""
    u = np.array([2.0, 3.0])
    v = np.array([4.0, 1.0])
    p = (u @ v) / (v @ v) * v  # 正射影
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    la_plot.setup_plane(ax, (-0.5, 4.8), (-0.5, 3.6))

    # v を含む直線
    t = np.array([-0.2, 1.15])
    ax.plot(t * v[0], t * v[1], color="0.6", linestyle=":")
    la_plot.draw_vector(ax, v, color="C1", label=r"$\mathbf{v}$", offset=(0.1, -0.3))
    la_plot.draw_vector(ax, u, color="C0", label=r"$\mathbf{u}$", offset=(-0.2, 0.15))
    la_plot.draw_vector(ax, p, color="C2", label=r"$\mathbf{p}$", offset=(-0.1, -0.45))
    la_plot.draw_vector(ax, u - p, origin=p, color="C3", linestyle="--",
                        label=r"$\mathbf{u}-\mathbf{p}$", offset=(0.1, -0.4))

    # 直角の記号
    d1 = v / np.linalg.norm(v) * 0.25
    d2 = (u - p) / np.linalg.norm(u - p) * 0.25
    corner = np.array([p + d1, p + d1 + d2, p + d2])
    ax.plot(corner[:, 0], corner[:, 1], color="0.3", linewidth=0.8)

    ax.set_title(r"$\mathbf{u}$ の $\mathbf{v}$ 方向への正射影")
    fig.tight_layout()
    return fig


def main() -> None:
    la_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
