"""3D の棒グラフ: 奥行きと遠近で値が読み取りにくくなる.

同じ 4 つの値を、3D の棒グラフと 2D の棒グラフで描く。3D では、
手前の棒が奥の棒を隠し、棒の高さを目盛りと比べにくい。

使い方: python ch14_3d_bar.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont

QUARTERS = ["1Q", "2Q", "3Q", "4Q"]
VALUES = np.array([42.0, 45.0, 38.0, 47.0])


def create_figure() -> Figure:
    """同じ値の 3D の棒グラフと 2D の棒グラフを描く."""
    fig = plt.figure(figsize=(9, 3.6))

    ax_bad = fig.add_subplot(1, 2, 1, projection="3d")
    positions = np.arange(len(VALUES))
    ax_bad.bar3d(positions, np.zeros(len(VALUES)), np.zeros(len(VALUES)),
                 0.6, 0.6, VALUES, color="C0", shade=True)
    ax_bad.set_xlim(-0.2, 4)
    ax_bad.set_ylim(0, 3)
    ax_bad.view_init(elev=25, azim=-60)
    ax_bad.set_xticks(positions + 0.3, QUARTERS)
    ax_bad.set_yticks([])
    ax_bad.set_title("悪い例: 3D の棒グラフ", fontsize=11)

    ax_good = fig.add_subplot(1, 2, 2)
    bars = ax_good.bar(QUARTERS, VALUES, color="C0", width=0.6)
    ax_good.bar_label(bars)
    ax_good.set_ylim(0, 55)
    ax_good.set_title("改善例: 2D の棒グラフ", fontsize=11)
    ax_good.set_ylabel("売上（百万円）")
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
