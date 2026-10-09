"""流量の行列: 多数のノードの間のやり取りを行列で描く.

架空の 6 部署の間で 1 か月に送られたメールの件数を、行が送信元、
列が送信先のヒートマップで描く。ノードの多い密なグラフでは、
ノードリンク図よりも行列の方が読みやすいことが多い。

使い方: python ch13_flow_matrix.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont

DEPARTMENTS = ["営業", "開発", "品質保証", "人事", "経理", "広報"]
# 行: 送信元、列: 送信先。対角成分は部署内のメール
MAILS = np.array([
    [420, 85, 10, 5, 60, 70],
    [90, 610, 240, 8, 4, 12],
    [15, 260, 180, 3, 2, 5],
    [30, 25, 20, 95, 45, 15],
    [70, 6, 3, 40, 130, 10],
    [80, 20, 6, 12, 8, 110],
])


def create_figure() -> Figure:
    """メールの件数の行列をヒートマップで描く."""
    fig, ax = plt.subplots(figsize=(6, 5))
    image = ax.imshow(MAILS, cmap="Blues")
    for row in range(len(DEPARTMENTS)):
        for col in range(len(DEPARTMENTS)):
            value = MAILS[row, col]
            color = "white" if value > MAILS.max() / 2 else "black"
            ax.text(col, row, str(value), ha="center", va="center",
                    color=color, fontsize=9)
    ax.set_xticks(range(len(DEPARTMENTS)), DEPARTMENTS)
    ax.set_yticks(range(len(DEPARTMENTS)), DEPARTMENTS)
    ax.xaxis.tick_top()  # 送信先の名前を上に置く
    ax.xaxis.set_label_position("top")
    ax.set_xlabel("送信先")
    ax.set_ylabel("送信元")
    fig.colorbar(image, ax=ax, label="メールの件数", shrink=0.8)
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
