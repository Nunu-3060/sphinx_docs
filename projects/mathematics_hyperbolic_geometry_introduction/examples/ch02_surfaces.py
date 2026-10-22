"""曲率が正、0、負の曲面（球面、平面、擬球）を並べて描く.

使い方: python ch02_surfaces.py
"""

from typing import cast

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

import hg_plot


def create_figure() -> Figure:
    """球面（K = 1）、平面（K = 0）、擬球（K = -1）を 3 次元で描く."""
    fig = plt.figure(figsize=(10.5, 3.8))
    v = np.linspace(0.0, 2.0 * np.pi, 60)

    # 球面: 半径 1 の球. ガウス曲率は 1
    ax = cast(Axes3D, fig.add_subplot(131, projection="3d"))
    u = np.linspace(0.0, np.pi, 40)
    uu, vv = np.meshgrid(u, v)
    ax.plot_surface(np.sin(uu) * np.cos(vv), np.sin(uu) * np.sin(vv), np.cos(uu), color="C1", alpha=0.6,
                    linewidth=0.2, edgecolor="0.4")
    ax.set_title("球面（$K = 1$）")

    # 平面: ガウス曲率は 0
    ax = cast(Axes3D, fig.add_subplot(132, projection="3d"))
    x = np.linspace(-1.0, 1.0, 12)
    xx, yy = np.meshgrid(x, x)
    ax.plot_surface(xx, yy, np.zeros_like(xx), color="C2", alpha=0.6, linewidth=0.2, edgecolor="0.4")
    ax.set_zlim(-1.0, 1.0)
    ax.set_title("平面（$K = 0$）")

    # 擬球: 牽引曲線を z 軸のまわりに回転した曲面. ガウス曲率は -1
    ax = cast(Axes3D, fig.add_subplot(133, projection="3d"))
    u = np.linspace(0.0, 3.0, 40)
    uu, vv = np.meshgrid(u, v)
    r = 1.0 / np.cosh(uu)
    z = uu - np.tanh(uu)
    for sign in (1.0, -1.0):
        ax.plot_surface(r * np.cos(vv), r * np.sin(vv), sign * z, color="C0", alpha=0.6, linewidth=0.2,
                        edgecolor="0.4")
    ax.set_title("擬球（$K = -1$）")

    for ax3 in fig.axes:
        cast(Axes3D, ax3).set_box_aspect((1.0, 1.0, 1.0))
        ax3.set_axis_off()
    fig.tight_layout()
    return fig


def main() -> None:
    hg_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
