"""矩形波とのこぎり波の波形と、複素フーリエ係数の大きさ（線スペクトル）を描く."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import fig_common


def create_figure() -> Figure:
    t = np.linspace(-1.0, 2.0, 3001)
    k = np.arange(-15, 16)
    square = np.where(np.mod(t, 1.0) < 0.5, 1.0, -1.0)
    sawtooth = 2 * np.mod(t, 1.0) - 1
    safe_k = np.where(k == 0, 1, np.abs(k))  # 0 で割らないようにする
    square_c = np.where(k % 2 == 1, 2 / (np.pi * safe_k), 0.0)
    sawtooth_c = np.where(k != 0, 1 / (np.pi * safe_k), 0.0)
    fig, axes = plt.subplots(2, 2, figsize=(10, 5.5))
    for col, (x, c, name) in enumerate([(square, square_c, "矩形波"), (sawtooth, sawtooth_c, "のこぎり波")]):
        ax = axes[0, col]
        ax.plot(t, x)
        ax.set_title(f"{name}（周期 T = 1 s）")
        ax.set_xlabel("時間 t [s]")
        ax.set_ylim(-1.4, 1.4)
        fig_common.style_axes(ax)
        ax = axes[1, col]
        fig_common.stem(ax, k, c, color="C1")
        ax.set_xlabel("k（周波数 k / T [Hz]）")
        ax.set_ylabel(r"$|c_k|$")
        ax.set_ylim(0, 0.75)
        fig_common.style_axes(ax)
    fig.tight_layout()
    return fig
