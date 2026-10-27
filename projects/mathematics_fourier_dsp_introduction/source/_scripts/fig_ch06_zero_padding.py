"""周波数分解能: ゼロ詰めでは近い 2 つの周波数を分離できず、観測時間を長くすると分離できる.

標本化周波数 100 Hz で、20 Hz と 21 Hz の正弦波の和を観測する。
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import fig_common

FS = 100.0


def create_figure() -> Figure:
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.4), sharey=True)
    cases = [(64, 64, "64 点（0.64 s）"), (64, 1024, "64 点を 1024 点にゼロ詰め"), (256, 256, "256 点（2.56 s）")]
    for ax, (n_obs, n_fft, title) in zip(axes, cases):
        n = np.arange(n_obs)
        x = np.sin(2 * np.pi * 20 * n / FS) + np.sin(2 * np.pi * 21 * n / FS)
        spectrum = np.abs(np.fft.rfft(x, n=n_fft)) * 2 / n_obs
        freqs = np.fft.rfftfreq(n_fft, d=1 / FS)
        ax.plot(freqs, spectrum, ".-" if n_fft == n_obs else "-", linewidth=0.8, markersize=4)
        for f in (20, 21):
            ax.axvline(f, color="C3", linestyle=":", linewidth=0.8)
        ax.set_xlim(12, 29)
        ax.set_title(title)
        ax.set_xlabel("周波数 [Hz]")
        fig_common.style_axes(ax)
    axes[0].set_ylabel("振幅")
    fig.tight_layout()
    return fig
