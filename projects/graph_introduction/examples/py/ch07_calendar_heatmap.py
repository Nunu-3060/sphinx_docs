"""カレンダーヒートマップ: 曜日と週の周期を見る.

架空のリポジトリの 1 日あたりのコミット数（半年分）を、縦に曜日、
横に週を取ったマスの色で描く。

使い方: python ch07_calendar_heatmap.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont

WEEKDAYS = ["月", "火", "水", "木", "金", "土", "日"]
START = np.datetime64("2025-12-29")  # 月曜日
WEEKS = 26
HOLIDAY_WEEK = 12  # 休暇でコミットの少ない週


def make_commits() -> np.ndarray:
    """曜日（行）と週（列）ごとのコミット数を作る."""
    rng = np.random.default_rng(9)
    means = np.array([6, 6, 6, 6, 6, 1, 1], dtype=float)  # 週末は少ない
    commits = rng.poisson(means[:, np.newaxis], (7, WEEKS)).astype(float)
    commits[:, HOLIDAY_WEEK] = rng.poisson(1.0, 7)
    return commits


def month_ticks() -> tuple[list[int], list[str]]:
    """月が変わる週の位置と、その月の名前を返す."""
    ticks: list[int] = []
    labels: list[str] = []
    for week in range(WEEKS):
        # 週の最終日（日曜日）の月を、その週の月とする
        date = START + np.timedelta64(7 * week + 6, "D")
        label = f"{int(str(date)[5:7])} 月"
        if not labels or labels[-1] != label:
            ticks.append(week)
            labels.append(label)
    return ticks, labels


def create_figure() -> Figure:
    """コミット数のカレンダーヒートマップを描く."""
    fig, ax = plt.subplots(figsize=(9, 2.8))
    image = ax.imshow(make_commits(), cmap="Greens", aspect="equal")
    ax.set_yticks(range(7), WEEKDAYS)
    ticks, labels = month_ticks()
    ax.set_xticks(ticks, labels)
    fig.colorbar(image, ax=ax, label="コミット数", shrink=0.8)
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
