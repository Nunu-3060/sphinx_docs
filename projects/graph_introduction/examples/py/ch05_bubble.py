"""バブルチャート: 3 つの量を 1 つの図に描く.

架空の 8 つの開発プロジェクトについて、横軸に開発規模、縦軸に不具合密度、
円の面積に開発メンバーの人数を割り当てる。

使い方: python ch05_bubble.py
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import jpfont

# プロジェクト名: (開発規模（千行）, 不具合密度（件/千行）, 人数)
PROJECTS = {
    "P1": (20, 1.8, 4),
    "P2": (45, 1.2, 6),
    "P3": (80, 2.5, 15),
    "P4": (120, 1.0, 10),
    "P5": (150, 2.9, 25),
    "P6": (60, 0.8, 5),
    "P7": (200, 1.5, 20),
    "P8": (95, 2.0, 12),
}
AREA_PER_MEMBER = 40  # 1 人あたりの円の面積（ポイントの 2 乗）


def create_figure() -> Figure:
    """プロジェクトのバブルチャートを描く."""
    fig, ax = plt.subplots(figsize=(6.5, 4))
    for name, (size, density, members) in PROJECTS.items():
        # scatter の s は面積を指定する。人数に比例させる
        ax.scatter(size, density, s=members * AREA_PER_MEMBER, color="C0",
                   alpha=0.5, edgecolor="C0")
        ax.annotate(name, (size, density), ha="center", va="center")
    # 円の大きさの凡例を作る
    for members in (5, 10, 20):
        ax.scatter([], [], s=members * AREA_PER_MEMBER, color="C0",
                   alpha=0.5, label=f"{members} 人")
    ax.legend(title="人数", labelspacing=1.5, borderpad=1,
              loc="upper left", bbox_to_anchor=(1.02, 1))
    ax.set_xlabel("開発規模（千行）")
    ax.set_ylabel("不具合密度（件/千行）")
    ax.set_xlim(0, 230)
    ax.set_ylim(0, 3.5)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
