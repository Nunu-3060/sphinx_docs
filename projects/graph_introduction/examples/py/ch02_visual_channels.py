"""同じ 5 つの値を、異なる視覚変数で表す.

位置、長さ、角度、面積、色の濃さで同じ値を表し、どれが読み取りやすいかを
比べる。

使い方: python ch02_visual_channels.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont

LABELS = ["A", "B", "C", "D", "E"]
VALUES = np.array([22.0, 19.0, 25.0, 16.0, 18.0])


def create_figure() -> Figure:
    """5 種類の視覚変数で同じ値を表した図を描く."""
    fig, axes = plt.subplots(1, 5, figsize=(11, 2.8))
    positions = np.arange(len(VALUES))

    # 位置: 共通の軸の上の点の位置
    ax = axes[0]
    ax.scatter(positions, VALUES, color="C0")
    ax.set_ylim(0, 30)
    ax.set_title("位置")

    # 長さ: 棒の長さ
    ax = axes[1]
    ax.bar(positions, VALUES, color="C0")
    ax.set_ylim(0, 30)
    ax.set_title("長さ")

    # 角度: 円グラフの扇形の角度
    ax = axes[2]
    ax.pie(VALUES, labels=LABELS, startangle=90, counterclock=False,
           wedgeprops={"edgecolor": "white"})
    ax.set_title("角度")

    # 面積: 円の面積
    ax = axes[3]
    ax.scatter(positions, np.zeros_like(VALUES), s=VALUES * 25, color="C0")
    ax.set_xlim(-0.7, 4.7)
    ax.set_ylim(-1, 1)
    ax.set_yticks([])
    ax.set_title("面積")

    # 色の濃さ: 同じ大きさのマスの濃さ
    ax = axes[4]
    ax.imshow(VALUES.reshape(1, -1), cmap="Blues", vmin=0, vmax=30,
              aspect="auto")
    ax.set_yticks([])
    ax.set_title("色の濃さ")

    for ax in (axes[0], axes[1], axes[3], axes[4]):
        ax.set_xticks(positions, LABELS)
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
