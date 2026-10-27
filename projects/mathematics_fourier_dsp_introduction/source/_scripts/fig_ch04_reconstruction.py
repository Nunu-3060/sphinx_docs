"""理想的な再構成: 標本値ごとに sinc 関数を置き、足し合わせると元の信号に戻る."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import fig_common

FS = 8.0  # 標本化周波数 [Hz]


def waveform(t: NDArray[np.float64]) -> NDArray[np.float64]:
    """fs / 2 = 4 Hz より低い周波数（1 Hz と 2.5 Hz）だけを含む信号."""
    result: NDArray[np.float64] = 0.7 * np.sin(2 * np.pi * 1.0 * t) + 0.4 * np.cos(2 * np.pi * 2.5 * t + 0.3)
    return result


def create_figure() -> Figure:
    t = np.linspace(-0.5, 1.5, 2001)
    n = np.arange(-400, 413)  # 図の範囲の外の標本も足す
    samples = waveform(n / FS)
    fig, ax = plt.subplots(figsize=(10, 3.6))
    total = np.zeros_like(t)
    for nk, value in zip(n, samples):
        term = value * np.sinc(FS * t - nk)
        total += term
        if 0 <= nk <= 8:
            ax.plot(t, term, color="C0", linewidth=0.6, alpha=0.6)
    ax.plot(t, waveform(t), color="0.6", linewidth=4, label="元の信号")
    ax.plot(t, total, color="C3", linewidth=1.2, linestyle="--", label="sinc 関数の和")
    visible = (n >= -4) & (n <= 12)
    ax.plot(n[visible] / FS, samples[visible], "o", color="k", label="標本値")
    ax.set_xlim(-0.5, 1.5)
    ax.set_xlabel("時間 t [s]")
    ax.legend(loc="upper right", ncols=3, fontsize=9)
    ax.set_ylim(-1.3, 1.6)
    fig_common.style_axes(ax)
    fig.tight_layout()
    return fig
