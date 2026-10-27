"""オーバーラップ加算法: ブロックごとの畳み込みの結果を、ずらして足し合わせる."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import fig_common

BLOCK = 12


def create_figure() -> Figure:
    rng = np.random.default_rng(6)
    x = np.sin(2 * np.pi * np.arange(36) / 18) + 0.3 * rng.standard_normal(36)
    h = 0.5 ** np.arange(8)
    fig, axes = plt.subplots(3, 1, figsize=(10, 6.2), sharex=True)
    ax = axes[0]
    for b, start in enumerate(range(0, len(x), BLOCK)):
        n = np.arange(start, start + BLOCK)
        fig_common.stem(ax, n, x[start:start + BLOCK], color=f"C{b}")
    ax.set_title(f"入力を {BLOCK} 点ずつのブロックに分ける")
    ax = axes[1]
    for b, start in enumerate(range(0, len(x), BLOCK)):
        piece = np.convolve(x[start:start + BLOCK], h)
        n = np.arange(start, start + len(piece))
        ax.plot(n, piece, "o-", color=f"C{b}", markersize=3, linewidth=1.0, label=f"ブロック {b + 1} の出力")
        ax.axvspan(start + BLOCK - 0.5, start + len(piece) - 0.5, color=f"C{b}", alpha=0.08)
    ax.set_title(f"各ブロックとインパルス応答（長さ {len(h)}）の畳み込み：後ろの {len(h) - 1} 点が次のブロックと重なる")
    ax.legend(loc="upper right", fontsize=8, ncols=3)
    ax = axes[2]
    fig_common.stem(ax, np.arange(len(x) + len(h) - 1), np.convolve(x, h), color="k")
    ax.set_title("重なる部分を足し合わせた結果（全体を一度に畳み込んだ結果と一致する）")
    ax.set_xlabel("n")
    for ax in axes:
        ax.set_ylim(-3.5, 3.5)
        fig_common.style_axes(ax)
    fig.tight_layout()
    return fig
