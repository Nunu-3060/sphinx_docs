"""平行座標プロット: 多数の項目を持つデータを折れ線で描く.

項目ごとに縦軸を立てて横に並べ、1 台の機器の測定値を 1 本の折れ線で
結ぶ。項目ごとに単位と範囲が違うため、最小値が 0、最大値が 1 になるよう
正規化してから描く。

使い方: python ch08_parallel.py
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

import jpfont
from multivariate_data import FEATURES, GROUPS, UNITS, make_dataset


def create_figure() -> Figure:
    """機種ごとに色分けした平行座標プロットを描く."""
    data, labels = make_dataset()
    low = data.min(axis=0)
    high = data.max(axis=0)
    normalized = (data - low) / (high - low)

    fig, ax = plt.subplots(figsize=(8, 4))
    positions = range(len(FEATURES))
    for values, group in zip(normalized, labels):
        ax.plot(positions, values, color=f"C{group}", alpha=0.3,
                linewidth=1)
    for position in positions:
        ax.axvline(position, color="black", linewidth=1)
    # 各軸の上端と下端に、元の単位での最大値と最小値を書く
    for position, (lo, hi, unit) in enumerate(zip(low, high, UNITS)):
        ax.text(position, 1.03, f"{hi:.0f} {unit}", ha="center")
        ax.text(position, -0.03, f"{lo:.0f} {unit}", ha="center", va="top")
    ax.set_xticks(list(positions), FEATURES)
    ax.tick_params(axis="x", pad=14)
    ax.set_yticks([])
    ax.set_ylim(-0.1, 1.1)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    handles = [Line2D([], [], color=f"C{group}", label=name)
               for group, name in enumerate(GROUPS)]
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(1.0, 1.0))
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
