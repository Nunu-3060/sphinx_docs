"""ガントチャート: 作業の期間と重なりを描く.

架空のシステム開発プロジェクトの作業を、横棒の位置と長さで描く。

使い方: python ch07_gantt.py
"""

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Patch

import jpfont

TASKS = [  # (作業名, 開始日, 終了日（この日を含まない）, 担当)
    ("要件定義", "2026-04-01", "2026-04-22", "企画"),
    ("基本設計", "2026-04-15", "2026-05-13", "開発"),
    ("詳細設計", "2026-05-07", "2026-06-03", "開発"),
    ("実装", "2026-05-27", "2026-07-15", "開発"),
    ("テスト計画", "2026-05-20", "2026-06-10", "品質保証"),
    ("結合テスト", "2026-07-08", "2026-08-05", "品質保証"),
    ("リリース準備", "2026-07-29", "2026-08-12", "企画"),
]
COLORS = {"企画": "C0", "開発": "C1", "品質保証": "C2"}


def create_figure() -> Figure:
    """作業のガントチャートを描く."""
    fig, ax = plt.subplots(figsize=(8, 3.6))
    for row, (_, start, end, owner) in enumerate(TASKS):
        begin = np.datetime64(start)
        days = int((np.datetime64(end) - begin).astype(int))
        # 横軸は matplotlib の日付の数値（1 日が 1）なので、日数を幅に使える
        ax.barh(row, days, left=mdates.date2num(begin), height=0.6,
                color=COLORS[owner])
    ax.set_yticks(range(len(TASKS)), [task[0] for task in TASKS])
    ax.invert_yaxis()  # 最初の作業を上に置く
    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(
        lambda value, _: f"{mdates.num2date(value).month} 月")
    ax.grid(axis="x", alpha=0.3)
    handles = [Patch(color=color, label=owner)
               for owner, color in COLORS.items()]
    ax.legend(handles=handles, loc="lower left")
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
