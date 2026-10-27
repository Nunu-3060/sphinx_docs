"""量子化: 3 ビットで量子化した信号と、量子化誤差を描く."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import fig_common

BITS = 3


def create_figure() -> Figure:
    t = np.linspace(0.0, 1.0, 2001)
    x = 0.9 * np.sin(2 * np.pi * t) + 0.05 * np.sin(2 * np.pi * 7 * t)
    step = 2.0 / 2**BITS  # -1 から 1 を 2^BITS 段階に分ける
    q = step * (np.floor(x / step) + 0.5)  # 各段の中央の値に丸める
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
    ax = axes[0]
    ax.plot(t, x, color="0.6", label="入力")
    ax.plot(t, q, color="C0", label=f"{BITS} ビットで量子化")
    ax.set_yticks(np.arange(-1.0, 1.01, step))
    ax.set_xlabel("時間 t [s]")
    ax.set_title(f"量子化（刻み Δ = {step}）")
    ax.legend(loc="upper right", fontsize=9)
    ax = axes[1]
    ax.plot(t, q - x, color="C3", linewidth=0.8)
    ax.axhline(step / 2, color="0.4", linestyle=":")
    ax.axhline(-step / 2, color="0.4", linestyle=":")
    ax.set_ylim(-0.2, 0.2)
    ax.set_xlabel("時間 t [s]")
    ax.set_title("量子化誤差（-Δ/2 から Δ/2 の範囲）")
    for ax in axes:
        fig_common.style_axes(ax)
    fig.tight_layout()
    return fig
