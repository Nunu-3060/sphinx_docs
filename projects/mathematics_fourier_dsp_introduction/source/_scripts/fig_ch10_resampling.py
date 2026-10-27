"""ダウンサンプリング: 間引くだけの場合と、ローパスフィルタを掛けてから間引く場合の比較.

標本化周波数 200 Hz の信号（5 Hz と 30 Hz の正弦波の和）を 1/4 に間引いて 50 Hz にする。
新しいナイキスト周波数は 25 Hz なので、30 Hz の成分は 20 Hz に折り返す。
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray
from scipy import signal

import fig_common

FS = 200.0
FACTOR = 4


def amplitude(x: NDArray[np.float64], fs: float) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """ハン窓を掛けた片側の振幅スペクトルの (周波数, 振幅) を返す."""
    w = np.hanning(len(x))
    return np.fft.rfftfreq(len(x), d=1 / fs), 2 * np.abs(np.fft.rfft(x * w)) / np.sum(w)


def create_figure() -> Figure:
    t = np.arange(800) / FS
    x = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 30 * t)
    naive = x[::FACTOR]
    filtered = signal.resample_poly(x, 1, FACTOR)
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.4), sharey=True)
    cases = [(x, FS, "元の信号（fs = 200 Hz）"), (naive, FS / FACTOR, "間引くだけ（fs = 50 Hz）"),
             (filtered, FS / FACTOR, "LPF の後に間引く（fs = 50 Hz）")]
    for ax, (data, fs, title) in zip(axes, cases):
        freqs, amp = amplitude(np.asarray(data, dtype=np.float64), fs)
        ax.plot(freqs, amp, linewidth=1.0)
        ax.axvline(FS / FACTOR / 2, color="C3", linestyle=":", linewidth=1.0)
        ax.set_xlim(0, 40)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("周波数 [Hz]")
        fig_common.style_axes(ax)
    axes[0].set_ylabel("振幅")
    fig.tight_layout()
    return fig
