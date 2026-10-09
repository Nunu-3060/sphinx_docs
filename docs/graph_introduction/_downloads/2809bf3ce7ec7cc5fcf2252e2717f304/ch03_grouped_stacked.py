"""グループ化棒グラフと積み上げ棒グラフ.

架空の 3 製品の地域別売上を、2 つの形式で描く。グループ化棒グラフは
製品どうしの比較に、積み上げ棒グラフは地域ごとの合計の比較に向く。

使い方: python ch03_grouped_stacked.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont

REGIONS = ["北海道", "関東", "近畿", "九州"]
SALES = {  # 製品ごとの地域別売上（百万円）
    "製品 X": np.array([12.0, 45.0, 30.0, 15.0]),
    "製品 Y": np.array([8.0, 38.0, 35.0, 10.0]),
    "製品 Z": np.array([5.0, 20.0, 18.0, 12.0]),
}


def create_figure() -> Figure:
    """グループ化棒グラフと積み上げ棒グラフを並べて描く."""
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(10, 3.8),
                                            sharey=True)
    positions = np.arange(len(REGIONS))
    width = 0.27

    # 左: グループ化棒グラフ。製品ごとに棒の位置を少しずつずらす
    for index, (product, values) in enumerate(SALES.items()):
        offset = (index - 1) * width
        ax_left.bar(positions + offset, values, width, label=product)
    ax_left.set_title("グループ化棒グラフ")
    ax_left.set_ylabel("売上（百万円）")

    # 右: 積み上げ棒グラフ。bottom に、それまでの製品の合計を渡す
    bottom = np.zeros(len(REGIONS))
    for product, values in SALES.items():
        ax_right.bar(positions, values, 0.6, bottom=bottom, label=product)
        bottom += values
    ax_right.set_title("積み上げ棒グラフ")

    for ax in (ax_left, ax_right):
        ax.set_xticks(positions, REGIONS)
        ax.legend()
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
