"""点の重なり（オーバープロット）への対策.

5 万点のデータを、そのままの散布図、半透明の散布図、六角形のビンで
数えた hexbin の 3 通りで描く。

使い方: python ch05_overplot.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont


def make_data() -> tuple[np.ndarray, np.ndarray]:
    """2 つの塊が重なった 5 万点のデータを作る."""
    rng = np.random.default_rng(6)
    main_x = rng.normal(0, 1, 40000)
    main_y = 0.6 * main_x + rng.normal(0, 0.8, 40000)
    sub_x = rng.normal(1.5, 0.3, 10000)
    sub_y = rng.normal(-1.0, 0.3, 10000)
    return np.concatenate([main_x, sub_x]), np.concatenate([main_y, sub_y])


def create_figure() -> Figure:
    """同じデータを 3 通りの方法で描く."""
    x, y = make_data()
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.4), sharex=True,
                             sharey=True)
    axes[0].scatter(x, y, s=4, color="C0")
    axes[0].set_title("そのまま")
    axes[1].scatter(x, y, s=4, color="C0", alpha=0.03)
    axes[1].set_title("半透明（alpha = 0.03）")
    hexbin = axes[2].hexbin(x, y, gridsize=40, cmap="viridis", mincnt=1)
    axes[2].set_title("hexbin")
    fig.colorbar(hexbin, ax=axes[2], label="点の数")
    for ax in axes:
        ax.set_xlim(-4, 4)
        ax.set_ylim(-4, 4)
        ax.set_xlabel("x")
    axes[0].set_ylabel("y")
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
