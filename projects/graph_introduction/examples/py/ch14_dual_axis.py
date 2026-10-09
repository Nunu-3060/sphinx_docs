"""二重軸のグラフ: 軸の範囲の選び方で見かけの関係が変わる.

関係のない 2 つの量（架空の社内の会議室の予約数と、Web API の平均応答
時間）を、左右に 2 つの縦軸を持つグラフで描く。右軸の範囲を調整すると、
2 本の線が同じように増えているように見える。改善例では、1 月を 100 と
した指数に換算し、1 つの縦軸で比べる。

使い方: python ch14_dual_axis.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont

MONTHS = np.arange(1, 13)
BOOKINGS = np.array([310, 325, 340, 330, 355, 370, 365, 380, 390, 385, 400,
                     410])
RESPONSE = np.array([120, 121.5, 123, 122, 124.5, 126, 125.5, 127, 128,
                     127.5, 129, 130])


def create_figure() -> Figure:
    """二重軸のグラフと、指数にそろえたグラフを並べて描く."""
    fig, (ax_bad, ax_good) = plt.subplots(1, 2, figsize=(10, 3.6))

    ax_bad.plot(MONTHS, BOOKINGS, color="C0", marker="o")
    ax_bad.set_ylabel("会議室の予約数（件）", color="C0")
    ax_right = ax_bad.twinx()  # 横軸を共有する右側の縦軸
    ax_right.plot(MONTHS, RESPONSE, color="C1", marker="s")
    ax_right.set_ylim(119.5, 130.5)  # 2 本の線が重なるように範囲を選んでいる
    ax_right.set_ylabel("平均応答時間（ミリ秒）", color="C1")
    ax_bad.set_title("悪い例: 二重軸", fontsize=11)

    # 1 月を 100 とした指数にすると、同じ軸で増え方を比べられる
    ax_good.plot(MONTHS, BOOKINGS / BOOKINGS[0] * 100, color="C0",
                 marker="o", label="会議室の予約数")
    ax_good.plot(MONTHS, RESPONSE / RESPONSE[0] * 100, color="C1",
                 marker="s", label="平均応答時間")
    ax_good.set_ylabel("1 月を 100 とした指数")
    ax_good.set_ylim(90, 140)
    ax_good.legend(loc="lower right")
    ax_good.set_title("改善例: 同じ軸の指数で比べる", fontsize=11)

    for ax in (ax_bad, ax_good):
        ax.set_xlabel("月")
        ax.set_xticks(MONTHS)
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
