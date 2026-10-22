"""半径 r の円の円周と面積を、球面、平面、双曲平面で比べる.

使い方: python ch07_growth.py
"""

import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import hg_plot


def create_figure() -> Figure:
    """左に円周、右に面積のグラフを描く（縦軸は対数目盛り）."""
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.0))
    r = np.linspace(0.01, 6.0, 300)
    r_sphere = r[r <= math.pi]
    curves = [
        ("球面 $K = 1$", r_sphere, 2.0 * np.pi * np.sin(r_sphere), 2.0 * np.pi * (1.0 - np.cos(r_sphere)), "C1"),
        ("平面 $K = 0$", r, 2.0 * np.pi * r, np.pi * r**2, "C2"),
        ("双曲平面 $K = -1$", r, 2.0 * np.pi * np.sinh(r), 2.0 * np.pi * (np.cosh(r) - 1.0), "C0"),
    ]
    for label, x, length, area, color in curves:
        axes[0].plot(x, length, color=color, linewidth=2.0, label=label)
        axes[1].plot(x, area, color=color, linewidth=2.0, label=label)
    for ax, title in zip(axes, ("円周", "面積")):
        ax.set_yscale("log")
        ax.set_ylim(1e-1, 2e3)
        ax.set_xlabel("半径 $r$")
        ax.set_title(title)
        ax.grid(True, color="0.9", which="both")
        ax.legend(loc="lower right")
    fig.tight_layout()
    return fig


def main() -> None:
    hg_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
