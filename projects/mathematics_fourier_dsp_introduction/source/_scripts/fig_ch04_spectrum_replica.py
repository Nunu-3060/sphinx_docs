"""標本化した信号のスペクトルは、元のスペクトルを fs ごとに繰り返したものになる.

帯域幅 B の信号を、fs > 2B で標本化した場合（上）と、fs < 2B で標本化した場合（下）を描く。
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import fig_common

BAND = 1.0  # 帯域幅 B


def base_spectrum(f: NDArray[np.float64]) -> NDArray[np.float64]:
    """帯域幅 BAND の三角形のスペクトル（左右の区別が付くように傾けてある）."""
    result: NDArray[np.float64] = np.where(np.abs(f) < BAND, (1 - np.abs(f) / BAND) * (1 + 0.3 * f / BAND), 0.0)
    return result


def create_figure() -> Figure:
    f = np.linspace(-5.0, 5.0, 4001)
    fig, axes = plt.subplots(2, 1, figsize=(10, 5.2), sharex=True)
    cases = ((3.0, r"$f_s = 3B$（$f_s > 2B$）：重ならない"),
             (1.5, r"$f_s = 1.5B$（$f_s < 2B$）：重なる（エイリアシング）"))
    for ax, (fs, title) in zip(axes, cases):
        total = np.zeros_like(f)
        for m in range(-4, 5):
            copy = base_spectrum(f - m * fs)
            total += copy
            ax.fill_between(f, copy, color="C0" if m == 0 else "C1", alpha=0.4 if m == 0 else 0.25, linewidth=0)
        ax.plot(f, total, color="k", linewidth=1.2, label="標本化した信号のスペクトル")
        ax.axvspan(-fs / 2, fs / 2, color="0.92", zorder=0)
        ax.axvline(fs / 2, color="C3", linestyle=":")
        ax.text(fs / 2 + 0.05, 1.55, r"$f_s/2$", color="C3")
        ax.set_title(title)
        ax.set_ylim(0, 1.8)
        ax.legend(loc="upper left", fontsize=9)
        fig_common.style_axes(ax)
    axes[-1].set_xlabel("周波数（B を 1 とする）")
    fig.tight_layout()
    return fig
