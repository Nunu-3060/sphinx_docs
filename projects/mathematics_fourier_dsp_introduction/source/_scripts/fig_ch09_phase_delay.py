"""フィルタによる遅延と波形のひずみ: IIR（lfilter）、FIR（線形位相）、filtfilt を比べる.

雑音を加えたパルス状の信号に、カットオフ周波数 50 Hz の 4 次バタワース LPF（IIR）と、
51 タップの FIR LPF を掛ける。
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from scipy import signal

import fig_common

FS = 1000.0


def create_figure() -> Figure:
    t = np.arange(400) / FS
    clean = np.exp(-(((t - 0.15) / 0.02) ** 2)) - 0.6 * np.exp(-(((t - 0.25) / 0.012) ** 2))
    rng = np.random.default_rng(5)
    x = clean + 0.15 * rng.standard_normal(len(t))
    sos = signal.butter(4, 50.0, fs=FS, output="sos")
    fir = signal.firwin(51, 50.0, fs=FS)
    fig, ax = plt.subplots(figsize=(10, 3.8))
    ax.plot(t, x, color="0.8", linewidth=0.8, label="入力（雑音あり）")
    ax.plot(t, clean, color="k", linewidth=1.5, label="雑音のない信号")
    ax.plot(t, signal.sosfilt(sos, x), color="C0", label="IIR（sosfilt）")
    ax.plot(t, signal.lfilter(fir, [1.0], x), color="C1", label="FIR（lfilter）：25 標本遅れる")
    ax.plot(t, signal.sosfiltfilt(sos, x), color="C3", linestyle="--", label="IIR（sosfiltfilt）")
    ax.set_xlabel("時間 [s]")
    ax.set_ylim(-1.0, 1.5)
    ax.legend(loc="upper right", fontsize=8, ncols=2)
    fig_common.style_axes(ax)
    fig.tight_layout()
    return fig
