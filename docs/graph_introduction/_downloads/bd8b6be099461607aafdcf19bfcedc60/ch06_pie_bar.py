"""円グラフと棒グラフ: 構成比の読み取りやすさを比べる.

値の近い 5 つの項目の構成比を、円グラフと棒グラフで描く。
円グラフでは項目の大小の順が分かりにくい。

使い方: python ch06_pie_bar.py
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import jpfont

SHARES = {"A": 23, "B": 21, "C": 20, "D": 19, "E": 17}


def create_figure() -> Figure:
    """同じ構成比を円グラフと棒グラフで描く."""
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(9, 3.6))
    ax_left.pie(list(SHARES.values()), labels=list(SHARES), startangle=90,
                counterclock=False, wedgeprops={"edgecolor": "white"})
    ax_left.set_title("円グラフ")

    bars = ax_right.bar(list(SHARES), list(SHARES.values()), color="C0")
    ax_right.bar_label(bars, fmt="%d%%")
    ax_right.set_ylim(0, 30)
    ax_right.set_ylabel("構成比（%）")
    ax_right.set_title("棒グラフ")
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
