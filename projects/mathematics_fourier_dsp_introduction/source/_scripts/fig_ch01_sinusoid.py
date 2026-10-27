"""正弦波の振幅、周波数、位相を変えたときの波形を描く."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import fig_common


def create_figure() -> Figure:
    t = np.linspace(0.0, 1.0, 1001)
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.2), sharey=True)
    base = np.cos(2 * np.pi * 2 * t)
    cases = [
        ("振幅を変える", 0.5 * np.cos(2 * np.pi * 2 * t), "A = 0.5"),
        ("周波数を変える", np.cos(2 * np.pi * 4 * t), "f = 4 Hz"),
        ("位相を変える", np.cos(2 * np.pi * 2 * t - np.pi / 2), r"$\phi = -\pi/2$"),
    ]
    for ax, (title, other, label) in zip(axes, cases):
        ax.plot(t, base, color="C0", label=r"A = 1, f = 2 Hz, $\phi = 0$")
        ax.plot(t, other, color="C1", linestyle="--", label=label)
        ax.set_title(title)
        ax.set_xlabel("時間 t [s]")
        ax.set_ylim(-1.3, 1.9)
        ax.legend(loc="upper right", fontsize=8)
        fig_common.style_axes(ax)
    fig.tight_layout()
    return fig
