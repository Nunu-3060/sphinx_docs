"""虹色のカラーマップの問題: 明るさが値の順に並ばない.

同じなだらかなデータを jet（虹色）と viridis で描く。下の段には、
各カラーマップの色を明るさ（輝度）だけに変換した帯を描く。jet は
明るさが上下するため、データにない境界が見え、白黒で印刷すると
値の大小が分からなくなる。

使い方: python ch14_rainbow.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont


def luminance(colors: np.ndarray) -> np.ndarray:
    """RGB の色の配列から、おおよその明るさ（0 から 1）を計算する."""
    # ITU-R BT.601 の重み。人間の目は緑を最も明るく感じる
    return np.asarray(colors[..., :3] @ np.array([0.299, 0.587, 0.114]))


def create_figure() -> Figure:
    """2 つのカラーマップによる表示と、その明るさの帯を描く."""
    x = np.linspace(0, 1, 200)
    xx, yy = np.meshgrid(x, x)
    data = xx * 0.7 + yy * 0.3  # 左下から右上へなだらかに増える値
    gradient = np.linspace(0, 1, 256)

    fig, axes = plt.subplots(2, 2, figsize=(8, 4.6),
                             height_ratios=[4, 1])
    for col, (name, title) in enumerate((("jet", "悪い例: jet（虹色）"),
                                         ("viridis", "改善例: viridis"))):
        cmap = plt.get_cmap(name)
        axes[0, col].imshow(data, cmap=cmap, origin="lower")
        axes[0, col].set_title(title, fontsize=11)
        gray = luminance(cmap(gradient))
        axes[1, col].imshow(gray.reshape(1, -1), cmap="gray", vmin=0,
                            vmax=1, aspect="auto")
        axes[1, col].set_title("色を明るさだけに変換した帯", fontsize=9)
        for ax in axes[:, col]:
            ax.set_xticks([])
            ax.set_yticks([])
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
