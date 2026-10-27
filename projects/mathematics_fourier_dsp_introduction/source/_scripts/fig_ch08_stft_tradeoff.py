"""STFT の時間分解能と周波数分解能のトレードオフ.

1000 Hz と 1100 Hz の正弦波の和に、0.3 s と 0.6 s の 2 か所でクリック（短いパルス）を
加えた信号を、短い区間（32 点）と長い区間（512 点）の STFT で比べる。
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from scipy import signal

FS = 8000.0


def create_figure() -> Figure:
    t = np.arange(int(FS)) / FS
    x = 0.3 * np.sin(2 * np.pi * 1000 * t) + 0.3 * np.sin(2 * np.pi * 1100 * t)
    for click in (0.3, 0.6):
        x[int(click * FS)] += 5.0
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
    for ax, segment in zip(axes, (32, 512)):
        freqs, times, power = signal.spectrogram(x, fs=FS, window="hann", nperseg=segment,
                                                 noverlap=segment * 7 // 8)
        level = 10 * np.log10(np.maximum(power, 1e-12) / power.max())
        ax.pcolormesh(times, freqs, level, shading="auto", vmin=-60, vmax=0, cmap="viridis", rasterized=True)
        ax.set_ylim(0, 2500)
        ax.set_xlim(0, 1)
        ax.set_xlabel("時間 [s]")
        ax.set_title(f"区間 {segment} 点（{segment / FS * 1000:.0f} ms、分解能 {FS / segment:.1f} Hz）")
    axes[0].set_ylabel("周波数 [Hz]")
    fig.tight_layout()
    return fig
