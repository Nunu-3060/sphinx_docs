"""連続時間と離散時間、連続値と量子化された値の 4 種類の信号を描く."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import fig_common

STEP = 0.25  # 量子化の刻み


def waveform(t: NDArray[np.float64]) -> NDArray[np.float64]:
    """例に使う信号."""
    result: NDArray[np.float64] = 0.8 * np.sin(2 * np.pi * t) + 0.3 * np.sin(2 * np.pi * 3 * t + 0.5)
    return result


def quantize(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """STEP の整数倍に丸める."""
    result: NDArray[np.float64] = STEP * np.round(x / STEP)
    return result


def create_figure() -> Figure:
    t = np.linspace(0.0, 1.0, 1001)
    tn = np.arange(17) / 16
    fig, axes = plt.subplots(2, 2, figsize=(10, 5.5), sharex=True, sharey=True)
    axes[0, 0].plot(t, waveform(t))
    axes[0, 0].set_title("連続時間・連続値（アナログ信号）")
    axes[1, 0].plot(t, quantize(waveform(t)))
    axes[1, 0].set_title("連続時間・量子化された値")
    axes[0, 1].plot(t, waveform(t), color="0.75", linewidth=0.8, zorder=0)
    fig_common.stem(axes[0, 1], tn, waveform(tn))
    axes[0, 1].set_title("離散時間・連続値")
    fig_common.stem(axes[1, 1], tn, quantize(waveform(tn)), color="C3")
    axes[1, 1].set_title("離散時間・量子化された値（デジタル信号）")
    for ax in axes.flat:
        ax.set_yticks(np.arange(-1.0, 1.01, 0.5))
        ax.set_yticks(np.arange(-1.0, 1.01, STEP), minor=True)
        ax.grid(True, which="minor", color="0.94")
        fig_common.style_axes(ax)
    axes[1, 0].set_xlabel("時間 t [s]")
    axes[1, 1].set_xlabel("時間 t [s]")
    fig.tight_layout()
    return fig
