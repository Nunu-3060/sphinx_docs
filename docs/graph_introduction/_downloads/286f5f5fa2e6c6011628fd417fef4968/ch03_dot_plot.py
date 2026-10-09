"""ドットプロット: 2 時点の値を点と線で比較する.

架空の 6 部署の残業時間（月平均）について、2024 年と 2025 年の値を
点で示し、線で結ぶ。棒を使わないため、0 から始まらない軸でも誤解を
招きにくい。

使い方: python ch03_dot_plot.py
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import jpfont

# 部署: (2024 年, 2025 年) の月平均残業時間
OVERTIME = {
    "開発": (32.5, 28.0),
    "品質保証": (25.0, 26.5),
    "インフラ": (30.0, 21.5),
    "営業": (22.0, 23.0),
    "人事": (15.5, 14.0),
    "経理": (18.0, 12.5),
}


def create_figure() -> Figure:
    """2 時点の値を並べたドットプロットを描く."""
    # 2025 年の値の小さい順に並べる（下から上へ）
    items = sorted(OVERTIME.items(), key=lambda item: item[1][1])
    names = [name for name, _ in items]
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    for row, (_, (before, after)) in enumerate(items):
        ax.plot([before, after], [row, row], color="lightgray", zorder=1)
    ax.scatter([v[0] for _, v in items], range(len(items)), color="C7",
               label="2024 年", zorder=2)
    ax.scatter([v[1] for _, v in items], range(len(items)), color="C0",
               label="2025 年", zorder=2)
    ax.set_yticks(range(len(items)), names)
    ax.set_xlabel("月平均残業時間（時間）")
    ax.grid(axis="x", alpha=0.3)
    ax.legend(loc="lower right")
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
