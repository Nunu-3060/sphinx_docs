"""白色雑音に埋もれた正弦波のパワースペクトル密度: ピリオドグラムとウェルチ法."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from scipy import signal

import fig_common

FS = 1000.0


def create_figure() -> Figure:
    rng = np.random.default_rng(4)
    t = np.arange(8192) / FS
    x = 0.3 * np.sin(2 * np.pi * 123 * t) + rng.standard_normal(len(t))
    f1, p1 = signal.periodogram(x, fs=FS, window="hann")
    f2, p2 = signal.welch(x, fs=FS, window="hann", nperseg=512)
    fig, ax = plt.subplots(figsize=(10, 3.8))
    ax.plot(f1, 10 * np.log10(p1), color="0.7", linewidth=0.6, label="ピリオドグラム（8192 点）")
    ax.plot(f2, 10 * np.log10(p2), color="C0", linewidth=1.5, label="ウェルチ法（512 点ずつ、重なり 50 %）")
    ax.axhline(10 * np.log10(2 / FS), color="C3", linestyle=":", label="雑音の理論値（片側）")
    ax.set_xlabel("周波数 [Hz]")
    ax.set_ylabel("パワースペクトル密度 [dB/Hz]")
    ax.set_xlim(0, FS / 2)
    ax.set_ylim(-60, 0)
    ax.legend(loc="lower right", fontsize=9)
    fig_common.style_axes(ax)
    fig.tight_layout()
    return fig
