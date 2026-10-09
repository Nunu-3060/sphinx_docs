"""100% 積み上げ棒グラフ: 合計の異なるグループの構成比を比べる.

架空の社内満足度調査の回答（5 段階）を、部署ごとの割合で描く。
部署の人数が違っても、割合にすれば比較できる。

使い方: python ch06_stacked_percent.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont

LEVELS = ["不満", "やや不満", "どちらでもない", "やや満足", "満足"]
# 部署ごとの回答数（LEVELS の順）
ANSWERS = {
    "開発": [5, 12, 20, 35, 28],
    "営業": [2, 6, 10, 15, 7],
    "管理": [1, 3, 8, 6, 2],
}


def create_figure() -> Figure:
    """部署ごとの回答の割合を横向きの 100% 積み上げ棒グラフで描く."""
    names = list(ANSWERS)
    counts = np.array(list(ANSWERS.values()), dtype=float)
    percents = counts / counts.sum(axis=1, keepdims=True) * 100
    colors = plt.get_cmap("RdBu")(np.linspace(0.15, 0.85, len(LEVELS)))

    fig, ax = plt.subplots(figsize=(8, 3))
    left = np.zeros(len(names))
    for index, level in enumerate(LEVELS):
        ax.barh(names, percents[:, index], left=left, color=colors[index],
                label=level)
        left += percents[:, index]
    for row, total in enumerate(counts.sum(axis=1)):
        ax.text(101, row, f"{total:.0f} 人", va="center")
    ax.invert_yaxis()  # 1 つ目の部署を上に置く
    ax.set_xlim(0, 100)
    ax.set_xlabel("割合（%）")
    ax.legend(ncols=len(LEVELS), loc="lower center",
              bbox_to_anchor=(0.5, 1.0), frameon=False)
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
