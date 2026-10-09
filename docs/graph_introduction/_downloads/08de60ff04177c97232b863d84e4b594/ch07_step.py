"""ステップグラフ: 値が段階的に変わるデータを描く.

架空の在庫数の変化を、折れ線グラフとステップグラフで比べる。
在庫数は入荷や出荷の時点でだけ変わるため、ステップグラフが実態に合う。

使い方: python ch07_step.py
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import jpfont

# 在庫数が変わった日（月初からの日数）と、変わった後の在庫数
DAYS = [0, 3, 5, 9, 10, 14, 18, 21, 25, 30]
STOCK = [100, 80, 65, 40, 120, 95, 70, 30, 110, 110]


def create_figure() -> Figure:
    """同じデータを折れ線グラフとステップグラフで描く."""
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(10, 3.4),
                                            sharey=True)
    ax_left.plot(DAYS, STOCK, marker="o")
    ax_left.set_title("折れ線グラフ")
    ax_left.set_ylabel("在庫数（個）")
    # where="post": 各点の値を次の点まで保つ
    ax_right.step(DAYS, STOCK, where="post", marker="o")
    ax_right.set_title("ステップグラフ")
    for ax in (ax_left, ax_right):
        ax.set_xlabel("月初からの日数")
        ax.set_ylim(0, 140)
        ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
