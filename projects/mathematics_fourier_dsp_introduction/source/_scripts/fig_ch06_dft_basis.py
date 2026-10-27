"""N = 8 の DFT の基底 exp(j 2 pi k n / N) の実部と虚部を描く."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import fig_common

N_POINTS = 8


def create_figure() -> Figure:
    n = np.arange(N_POINTS)
    t = np.linspace(0, N_POINTS - 1, 401)
    ks = (0, 1, 2, 4, 7)
    fig, axes = plt.subplots(len(ks), 2, figsize=(10, 7), sharex=True, sharey=True)
    for row, k in enumerate(ks):
        for col, (part, name) in enumerate(((np.cos, "実部"), (np.sin, "虚部"))):
            ax = axes[row, col]
            ax.plot(t, part(2 * np.pi * k * t / N_POINTS), color="0.8", linewidth=0.8, zorder=0)
            fig_common.stem(ax, n, part(2 * np.pi * k * n / N_POINTS), color=f"C{col}")
            ax.set_ylim(-1.4, 1.4)
            fig_common.style_axes(ax)
            if row == 0:
                ax.set_title(name)
        axes[row, 0].set_ylabel(f"k = {k}")
    for ax in axes[-1]:
        ax.set_xlabel("n")
    fig.tight_layout()
    return fig
