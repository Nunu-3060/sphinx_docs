"""グラフの構成要素: タイトル、軸ラベル、目盛り、凡例、注釈.

架空の Web サービスの月別アクセス数を折れ線グラフで描き、主な構成要素を
付ける。

使い方: python ch02_anatomy.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont

MONTHS = np.arange(1, 13)
SERVICE_A = np.array([120, 125, 140, 150, 148, 160,
                      175, 190, 185, 200, 210, 230])
SERVICE_B = np.array([90, 95, 92, 100, 115, 140,
                      150, 145, 150, 148, 155, 160])


def create_figure() -> Figure:
    """構成要素をそろえた折れ線グラフを描く."""
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(MONTHS, SERVICE_A, marker="o", label="サービス A")
    ax.plot(MONTHS, SERVICE_B, marker="s", label="サービス B")

    ax.set_title("月別アクセス数（2025 年）")      # タイトル
    ax.set_xlabel("月")                            # 横軸のラベル
    ax.set_ylabel("アクセス数（千件）")            # 縦軸のラベル（単位付き）
    ax.set_xticks(MONTHS)                          # 目盛り
    ax.set_ylim(0, 250)
    ax.grid(alpha=0.3)                             # 補助線
    ax.legend(loc="lower right")                   # 凡例
    ax.annotate("キャンペーン開始",                # 注釈
                xy=(6, 140), xytext=(3.5, 200),
                arrowprops={"arrowstyle": "->"})
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
