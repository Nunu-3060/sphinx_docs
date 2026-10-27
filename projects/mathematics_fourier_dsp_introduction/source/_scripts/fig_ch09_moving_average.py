"""移動平均フィルタの振幅特性を、平均する点数 M を変えて描く."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from scipy import signal

import fig_common


def create_figure() -> Figure:
    fig, ax = plt.subplots(figsize=(10, 3.6))
    for i, m in enumerate((3, 5, 11)):
        freqs, response = signal.freqz(np.full(m, 1.0 / m), worN=2048, fs=1.0)
        ax.plot(freqs, np.abs(response), color=f"C{i}", label=f"M = {m}")
    ax.set_xlim(0, 0.5)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel(r"正規化周波数 $f / f_s$")
    ax.set_ylabel("利得（倍）")
    ax.legend(loc="upper right")
    fig_common.style_axes(ax)
    fig.tight_layout()
    return fig
