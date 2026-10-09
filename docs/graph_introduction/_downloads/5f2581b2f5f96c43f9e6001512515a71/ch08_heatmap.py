"""ヒートマップ: 相関行列を色で表す.

4 つの項目の相関係数を計算し、発散カラーマップのヒートマップで描く。
各マスには相関係数の値も書く。

使い方: python ch08_heatmap.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont
from multivariate_data import FEATURES, make_dataset


def create_figure() -> Figure:
    """相関行列のヒートマップを描く."""
    data, _ = make_dataset()
    corr = np.corrcoef(data, rowvar=False)  # 列どうしの相関係数
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    # 相関係数は -1 から 1 の値なので、0 を中心とする発散カラーマップを使う
    image = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    for row in range(len(FEATURES)):
        for col in range(len(FEATURES)):
            value = corr[row, col]
            color = "white" if abs(value) > 0.6 else "black"
            ax.text(col, row, f"{value:.2f}", ha="center", va="center",
                    color=color)
    ax.set_xticks(range(len(FEATURES)), FEATURES)
    ax.set_yticks(range(len(FEATURES)), FEATURES)
    fig.colorbar(image, ax=ax, label="相関係数")
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
