"""代表的な窓関数の形（左）と、そのスペクトル（右）を描く."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from scipy import signal

import fig_common

N_POINTS = 64
WINDOWS = {"矩形窓": "boxcar", "ハン窓": "hann", "ハミング窓": "hamming", "ブラックマン窓": "blackman"}


def create_figure() -> Figure:
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), width_ratios=(2, 3))
    n_fft = 64 * N_POINTS
    bins = np.fft.fftshift(np.fft.fftfreq(n_fft, d=1 / N_POINTS))  # DFT のビンを単位とする周波数
    for i, (name, window) in enumerate(WINDOWS.items()):
        w = signal.get_window(window, N_POINTS)
        axes[0].plot(np.arange(N_POINTS), w, color=f"C{i}", label=name)
        spectrum = np.fft.fftshift(np.abs(np.fft.fft(w, n=n_fft)))
        axes[1].plot(bins, fig_common.to_db(spectrum / spectrum.max()), color=f"C{i}", linewidth=1.0, label=name)
    axes[0].set_xlabel("n")
    axes[0].set_title(f"窓関数（N = {N_POINTS}）")
    axes[0].set_ylim(0, 1.15)
    axes[1].set_xlim(0, 12)
    axes[1].set_ylim(-110, 5)
    axes[1].set_xlabel("周波数（DFT のビンの間隔 fs / N を単位とする）")
    axes[1].set_ylabel("利得 [dB]")
    axes[1].set_title("窓関数のスペクトル")
    axes[1].legend(loc="upper right", fontsize=9)
    for ax in axes:
        fig_common.style_axes(ax)
    fig.tight_layout()
    return fig
