"""スカラー場 f(x, y) = x exp(-(x^2 + y^2)) を、等高線図と曲面で描く.

使い方: python ch04_scalar_field.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import vc_plot


def field(x: NDArray[np.float64], y: NDArray[np.float64]) -> NDArray[np.float64]:
    """スカラー場 f(x, y) = x exp(-(x^2 + y^2)) の値を返す."""
    return x * np.exp(-(x**2 + y**2))


def create_figure() -> Figure:
    """左に等高線図、右にグラフの曲面 z = f(x, y) を描く."""
    fig = plt.figure(figsize=(10.0, 4.4))

    ax1 = fig.add_subplot(121)
    xx, yy = vc_plot.mesh((-2.0, 2.0), (-2.0, 2.0), 200)
    levels = np.linspace(-0.45, 0.45, 19)  # f の値は -0.43 から 0.43 の範囲にある
    filled = ax1.contourf(xx, yy, field(xx, yy), levels=levels, cmap="coolwarm")
    lines = ax1.contour(xx, yy, field(xx, yy), levels=levels, colors="k", linewidths=0.5)
    ax1.clabel(lines, levels[[1, 5, 13, 17]], fontsize=8)  # -0.4, -0.2, 0.2, 0.4（0 の線は枠と重なるので省く）
    fig.colorbar(filled, ax=ax1, shrink=0.85)
    ax1.set_aspect("equal")
    ax1.set_xlabel("$x$")
    ax1.set_ylabel("$y$")
    ax1.set_title("等高線図")

    ax2 = vc_plot.add_axes3d(fig, 122)
    xs, ys = vc_plot.mesh((-2.0, 2.0), (-2.0, 2.0), 30)
    ax2.plot_surface(xs, ys, field(xs, ys), cmap="coolwarm", vmin=-0.45, vmax=0.45,
                     edgecolor="0.3", linewidth=0.2)
    ax2.view_init(elev=30, azim=-60)
    ax2.set_title(r"曲面 $z = f(x, y)$")
    fig.tight_layout()
    return fig


def main() -> None:
    vc_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
