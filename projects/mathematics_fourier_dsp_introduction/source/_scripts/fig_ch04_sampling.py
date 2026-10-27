"""標本化: 連続時間信号から一定の間隔 Ts で値を取り出す."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import fig_common

FS = 20.0  # 標本化周波数 [Hz]


def waveform(t: NDArray[np.float64]) -> NDArray[np.float64]:
    """例に使う信号."""
    result: NDArray[np.float64] = np.sin(2 * np.pi * 1.5 * t) + 0.4 * np.cos(2 * np.pi * 4 * t)
    return result


def create_figure() -> Figure:
    t = np.linspace(0.0, 1.0, 1001)
    tn = np.arange(int(FS) + 1) / FS
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.plot(t, waveform(t), color="0.6", label="連続時間信号 x(t)")
    fig_common.stem(ax, tn, waveform(tn), color="C0", label=r"標本値 $x[n] = x(nT_s)$")
    ax.annotate("", xy=(6 / FS, -1.55), xytext=(5 / FS, -1.55), arrowprops={"arrowstyle": "<->"})
    ax.text(5.5 / FS, -1.5, r"$T_s$", ha="center", va="bottom")
    ax.set_xlabel("時間 t [s]")
    ax.set_ylim(-1.7, 1.9)
    ax.legend(loc="upper right", ncols=2)
    fig_common.style_axes(ax)
    fig.tight_layout()
    return fig
