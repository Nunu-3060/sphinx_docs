"""外積 a×b の向きと大きさを 3 次元の図で示す.

使い方: python ch02_cross_product.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import vc_plot


def create_figure() -> Figure:
    """a、b、a×b と、a と b が作る平行四辺形を描く."""
    a = np.array([2.0, 0.0, 0.0])
    b = np.array([1.0, 1.5, 0.0])
    axb = np.cross(a, b)  # (0, 0, 3)

    fig = plt.figure(figsize=(6.0, 5.0))
    ax = vc_plot.add_axes3d(fig)

    # a と b が作る平行四辺形（面積は |a×b|）
    corners = np.array([np.zeros(3), a, a + b, b, np.zeros(3)])
    ax.plot(corners[:, 0], corners[:, 1], corners[:, 2], color="0.5", linewidth=1)
    ax.plot_trisurf([0.0, a[0], a[0] + b[0], b[0]], [0.0, a[1], a[1] + b[1], b[1]],
                    [0.0, 0.0, 0.0, 0.0], color="C0", alpha=0.15)

    vc_plot.draw_vector3d(ax, a, color="C0", label=r"$\mathbf{a}$")
    vc_plot.draw_vector3d(ax, b, color="C1", label=r"$\mathbf{b}$")
    vc_plot.draw_vector3d(ax, axb, color="C3", label=r"$\mathbf{a}\times\mathbf{b}$")

    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.set_zlim(0, 3)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=22, azim=-60)
    ax.set_title(r"外積 $\mathbf{a}\times\mathbf{b}$ は $\mathbf{a}$ と $\mathbf{b}$ の両方に垂直")
    return fig


def main() -> None:
    vc_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
