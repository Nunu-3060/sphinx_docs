"""2 つの山がある地形の等高線と、勾配ベクトルを重ねて描く.

使い方: python ch05_gradient_contour.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import vc_plot


def height(x: NDArray[np.float64], y: NDArray[np.float64]) -> NDArray[np.float64]:
    """地形の高さ f(x, y). 点 (1, 0) と点 (-1, 0.5) に山がある."""
    hill1 = np.exp(-((x - 1.0)**2 + y**2))
    hill2 = 0.7 * np.exp(-((x + 1.0)**2 + (y - 0.5)**2) / 0.6)
    return hill1 + hill2


def gradient(x: NDArray[np.float64],
             y: NDArray[np.float64]) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """f の勾配 (df/dx, df/dy) を、手計算で求めた偏導関数から計算する."""
    hill1 = np.exp(-((x - 1.0)**2 + y**2))
    hill2 = 0.7 * np.exp(-((x + 1.0)**2 + (y - 0.5)**2) / 0.6)
    fx = -2.0 * (x - 1.0) * hill1 - 2.0 * (x + 1.0) / 0.6 * hill2
    fy = -2.0 * y * hill1 - 2.0 * (y - 0.5) / 0.6 * hill2
    return fx, fy


def create_figure() -> Figure:
    """等高線（細い線）と勾配ベクトル（矢印）を描く."""
    xx, yy = vc_plot.mesh((-2.5, 2.5), (-1.8, 2.2), 200)
    fig, ax = plt.subplots(figsize=(6.5, 5.2))
    filled = ax.contourf(xx, yy, height(xx, yy), levels=12, cmap="Greens", alpha=0.6)
    ax.contour(xx, yy, height(xx, yy), levels=12, colors="0.3", linewidths=0.6)

    # 矢印は粗い格子の上に描く
    qx, qy = vc_plot.mesh((-2.4, 2.4), (-1.7, 2.1), 17)
    fx, fy = gradient(qx, qy)
    ax.quiver(qx, qy, fx, fy, color="C3", angles="xy", scale_units="xy", scale=2.5, width=0.004)

    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-1.8, 2.2)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title(r"等高線と勾配ベクトル $\nabla f$")
    fig.colorbar(filled, ax=ax, label="高さ $f(x, y)$", shrink=0.8)
    fig.tight_layout()
    return fig


def main() -> None:
    vc_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
