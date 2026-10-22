"""山の形をしたスカラー場と、そのラプラシアンを並べて描く.

使い方: python ch08_laplacian_bump.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm
from matplotlib.figure import Figure

import vc_plot


def create_figure() -> Figure:
    """f = exp(-(x^2 + y^2)) と、そのラプラシアン 4 (r^2 - 1) exp(-r^2) を色で描く."""
    xx, yy = vc_plot.mesh((-2.5, 2.5), (-2.5, 2.5), 201)
    r2 = xx**2 + yy**2
    f = np.exp(-r2)
    lap = 4.0 * (r2 - 1.0) * np.exp(-r2)

    fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.4))
    image = axes[0].contourf(xx, yy, f, levels=20, cmap="viridis")
    axes[0].contour(xx, yy, f, levels=10, colors="w", linewidths=0.5)
    fig.colorbar(image, ax=axes[0], shrink=0.85)
    axes[0].set_title(r"$f = e^{-(x^2 + y^2)}$")

    norm = TwoSlopeNorm(vmin=-4.0, vcenter=0.0, vmax=1.0)  # 0 を白にする
    image = axes[1].contourf(xx, yy, lap, levels=20, cmap="RdBu_r", norm=norm)
    axes[1].contour(xx, yy, r2, levels=[1.0], colors="k", linewidths=1.0, linestyles="--")
    fig.colorbar(image, ax=axes[1], shrink=0.85)
    axes[1].set_title(r"$\nabla^2 f = 4(r^2 - 1)e^{-r^2}$（破線は $r = 1$）")

    for ax in axes:
        ax.set_aspect("equal")
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
    fig.tight_layout()
    return fig


def main() -> None:
    vc_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
