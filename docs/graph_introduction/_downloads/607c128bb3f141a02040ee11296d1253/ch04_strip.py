"""ストリッププロット: 個々のデータ点をすべて描く.

データ数の少ない 3 グループの測定値を、箱ひげ図の上に点として重ねる。
点が重ならないよう、横方向に小さな乱数（ジッター）を加える。

使い方: python ch04_strip.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont

GROUPS = ["条件 1", "条件 2", "条件 3"]


def create_figure() -> Figure:
    """箱ひげ図にジッター付きの点を重ねて描く."""
    rng = np.random.default_rng(3)
    data = [rng.normal(50, 5, 12), rng.normal(55, 8, 9),
            rng.normal(47, 4, 15)]
    fig, ax = plt.subplots(figsize=(5.5, 3.6))
    ax.boxplot(data, tick_labels=GROUPS, showfliers=False,
               medianprops={"color": "black"})
    for position, values in enumerate(data, start=1):
        jitter = rng.uniform(-0.12, 0.12, len(values))
        ax.scatter(position + jitter, values, color="C0", alpha=0.7,
                   zorder=3)
    ax.set_ylabel("測定値")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
