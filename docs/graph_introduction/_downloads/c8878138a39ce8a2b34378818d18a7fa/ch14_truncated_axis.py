"""縦軸を 0 から始めない棒グラフ: 差が誇張される.

2 つの製品の満足度（100 点満点）を、縦軸を 70 から始めた棒グラフと、
0 から始めた棒グラフで描く。

使い方: python ch14_truncated_axis.py
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import jpfont

SCORES = {"製品 A": 78, "製品 B": 82}


def create_figure() -> Figure:
    """縦軸の始点が違う 2 つの棒グラフを並べて描く."""
    fig, (ax_bad, ax_good) = plt.subplots(1, 2, figsize=(8, 3.4))
    for ax, bottom, title in ((ax_bad, 70, "悪い例: 縦軸が 70 から始まる"),
                              (ax_good, 0, "改善例: 縦軸が 0 から始まる")):
        bars = ax.bar(list(SCORES), list(SCORES.values()), width=0.5,
                      color=["C7", "C0"])
        ax.bar_label(bars)
        ax.set_ylim(bottom, 100)
        ax.set_title(title, fontsize=11)
        ax.set_ylabel("満足度（点）")
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
