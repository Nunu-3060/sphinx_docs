"""DFT は DTFT を等間隔に標本化したものである.

長さ 8 の矩形の信号（すべて 1）の DTFT の大きさ |sin(4 w) / sin(w / 2)| に、
N = 8 の DFT と、ゼロ詰めして N = 32 にした DFT の値を重ねて描く。
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import fig_common

LENGTH = 8


def create_figure() -> Figure:
    x = np.ones(LENGTH)
    w = np.linspace(0, 2 * np.pi, 2001)
    dtft = np.abs(np.sum(x[:, None] * np.exp(-1j * np.outer(np.arange(LENGTH), w)), axis=0))
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
    for ax, n_fft in zip(axes, (8, 32)):
        ax.plot(w, dtft, color="0.6", label="DTFT の大きさ")
        spectrum = np.abs(np.fft.fft(x, n=n_fft))
        fig_common.stem(ax, 2 * np.pi * np.arange(n_fft) / n_fft, spectrum, color="C3", label=f"DFT（N = {n_fft}）")
        ax.set_xticks(np.arange(0, 2.01, 0.5) * np.pi, ["0", r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$"])
        ax.set_xlabel(r"正規化角周波数 $\hat{\omega}$ [rad/標本]")
        ax.legend(loc="upper center", fontsize=9)
        ax.set_ylim(0, 10)
        fig_common.style_axes(ax)
    axes[0].set_title("ゼロ詰めなし（N = 8）")
    axes[1].set_title("ゼロ詰めあり（N = 32）")
    fig.tight_layout()
    return fig
