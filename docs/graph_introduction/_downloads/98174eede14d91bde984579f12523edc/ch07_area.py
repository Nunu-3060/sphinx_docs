"""積み上げ面グラフ: 合計と内訳の時間変化を見る.

架空のクラウド利用料金の月別推移を、サービスの種類ごとに積み上げる。

使い方: python ch07_area.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont

MONTHS = np.arange(1, 13)
COSTS = {  # サービスの種類: 月別の料金（万円）
    "仮想マシン": [50, 52, 55, 54, 58, 60, 62, 61, 63, 65, 64, 66],
    "ストレージ": [10, 11, 13, 14, 16, 18, 20, 22, 25, 27, 30, 33],
    "データベース": [20, 20, 21, 22, 22, 23, 23, 24, 24, 25, 25, 26],
    "ネットワーク": [5, 5, 6, 6, 7, 7, 8, 9, 9, 10, 11, 12],
}


def create_figure() -> Figure:
    """料金の内訳を積み上げ面グラフで描く."""
    fig, ax = plt.subplots(figsize=(7.5, 4))
    ax.stackplot(MONTHS, list(COSTS.values()), labels=list(COSTS),
                 alpha=0.85)
    ax.set_xticks(MONTHS)
    ax.set_xlim(1, 12)
    ax.set_xlabel("月")
    ax.set_ylabel("利用料金（万円）")
    ax.legend(loc="upper left", reverse=True)  # 凡例を積み上げの順に並べる
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
