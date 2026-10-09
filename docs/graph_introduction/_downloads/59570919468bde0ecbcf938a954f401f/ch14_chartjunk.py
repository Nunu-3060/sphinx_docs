"""装飾の多いグラフと、装飾を減らしたグラフ.

同じ月別の問い合わせ件数を、背景色、濃い格子、影付きの棒、凡例などで
飾ったグラフと、データを読むのに必要な要素だけを残したグラフで描く。

使い方: python ch14_chartjunk.py
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import jpfont

MONTHS = ["4 月", "5 月", "6 月", "7 月", "8 月", "9 月"]
INQUIRIES = [120, 135, 128, 160, 152, 171]


def create_figure() -> Figure:
    """装飾の多いグラフと少ないグラフを並べて描く."""
    fig, (ax_bad, ax_good) = plt.subplots(1, 2, figsize=(10, 3.6))

    # 悪い例: データと関係のない装飾が多い
    ax_bad.set_facecolor("#fde8c8")
    ax_bad.grid(color="black", linewidth=1)
    ax_bad.set_axisbelow(True)
    colors = ["C0", "C1", "C2", "C3", "C4", "C5"]
    ax_bad.bar(MONTHS, INQUIRIES, color="gray", width=0.6,
               align="edge")  # 影の代わりにずらした灰色の棒
    ax_bad.bar(MONTHS, INQUIRIES, color=colors, width=0.6, edgecolor="black",
               linewidth=2, hatch="//", label="問い合わせ件数")
    ax_bad.legend(loc="upper left")
    ax_bad.set_title("悪い例: 装飾が多い", fontsize=11)

    # 改善例: 色は 1 色、補助線は薄く、伝えたい点だけを強調する
    bars = ax_good.bar(MONTHS, INQUIRIES, color="C7", width=0.6)
    bars[-1].set_color("C0")  # 最新の月だけ色を変える
    ax_good.bar_label(bars)
    for side in ("top", "right"):
        ax_good.spines[side].set_visible(False)
    ax_good.set_ylabel("問い合わせ件数（件）")
    ax_good.set_title("改善例: 装飾を減らし、最新の月を強調する",
                      fontsize=11)

    for ax in (ax_bad, ax_good):
        ax.set_ylim(0, 200)
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
