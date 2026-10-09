"""スモールマルチプル: 同じ形式の小さなグラフを並べる.

架空の 6 店舗の月別売上を、店舗ごとの小さな折れ線グラフにして並べる。
すべてのグラフで軸の範囲をそろえるため、店舗どうしを比較できる。

使い方: python ch08_small_multiples.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont

STORES = ["札幌店", "仙台店", "東京店", "名古屋店", "大阪店", "福岡店"]
MONTHS = np.arange(1, 13)


def make_sales() -> np.ndarray:
    """店舗（行）ごとの月別売上（列）を作る."""
    rng = np.random.default_rng(11)
    bases = np.array([30, 25, 60, 40, 50, 35], dtype=float)
    seasonal = 1 + 0.25 * np.sin((MONTHS - 4) / 12 * 2 * np.pi)
    sales = bases[:, np.newaxis] * seasonal
    sales[2] *= 1 + 0.04 * (MONTHS - 1)   # 東京店は増加傾向
    sales[5, 7:] *= 0.6                   # 福岡店は 8 月以降に改装で減少
    return sales + rng.normal(0, 2, sales.shape)


def create_figure() -> Figure:
    """店舗ごとの折れ線グラフを 2 行 3 列に並べる."""
    sales = make_sales()
    fig, axes = plt.subplots(2, 3, figsize=(9, 4.5), sharex=True,
                             sharey=True)
    for ax, store, values in zip(axes.flat, STORES, sales):
        # 背景に全店舗の線を薄く描き、対象の店舗の線を強調する
        for other in sales:
            ax.plot(MONTHS, other, color="lightgray", linewidth=1)
        ax.plot(MONTHS, values, color="C0", linewidth=2)
        ax.set_title(store)
        ax.set_xticks([1, 4, 7, 10])
        ax.grid(alpha=0.3)
    for ax in axes[1]:
        ax.set_xlabel("月")
    for ax in axes[:, 0]:
        ax.set_ylabel("売上（百万円）")
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
