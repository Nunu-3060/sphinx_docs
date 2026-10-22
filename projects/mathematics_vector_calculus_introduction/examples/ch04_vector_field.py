"""ベクトル場 F(x, y) = (x - y, x + y) を、矢印図と流線で描く.

使い方: python ch04_vector_field.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import vc_plot


def field(x: NDArray[np.float64], y: NDArray[np.float64]) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """ベクトル場 F(x, y) = (x - y, x + y) の x 成分と y 成分を返す."""
    return x - y, x + y


def create_figure() -> Figure:
    """左に quiver による矢印図、右に streamplot による流線を描く."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 4.8))

    # 矢印図：格子点ごとに F の矢印を描く。色は矢印の長さ |F| を表す
    xx, yy = vc_plot.mesh((-2.0, 2.0), (-2.0, 2.0), 13)
    fx, fy = field(xx, yy)
    vc_plot.setup_plane(ax1, (-2.4, 2.4), (-2.4, 2.4))
    ax1.quiver(xx, yy, fx, fy, np.hypot(fx, fy), cmap="viridis", angles="xy")
    ax1.set_title("矢印図（quiver）")

    # 流線：各点で F に接する曲線を描く
    xs, ys = vc_plot.mesh((-2.0, 2.0), (-2.0, 2.0), 100)
    sx, sy = field(xs, ys)
    vc_plot.setup_plane(ax2, (-2.0, 2.0), (-2.0, 2.0))
    ax2.streamplot(xs, ys, sx, sy, color=np.hypot(sx, sy), cmap="viridis", density=1.2, linewidth=1)
    ax2.set_title("流線（streamplot）")
    fig.tight_layout()
    return fig


def main() -> None:
    vc_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
