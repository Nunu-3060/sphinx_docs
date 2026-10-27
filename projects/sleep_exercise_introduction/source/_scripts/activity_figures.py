"""座りすぎ・運動・習慣化の章で使う図を生成する。

1 週間の身体活動量と睡眠記録の図は、examples のサンプルコードとサンプルデータから作る。
"""

from collections.abc import Callable
from pathlib import Path

import matplotlib.pyplot as plt

import activity_calc
import sleep_log
from figure_style import BLUE, EXAMPLES_DIR, GRAY, GREEN, ORANGE, save_figure, setup_style

# 1 日の過ごし方 (開始時刻 [時], 終了時刻 [時], 座っているなら True)
SitPattern = list[tuple[float, float, bool]]


def _continuous_sitting() -> SitPattern:
    """昼休み以外は座り続ける場合。"""
    return [(9, 12, True), (12, 13, False), (13, 18, True)]


def _with_breaks() -> SitPattern:
    """約 30 分ごとに立ち、1 時間ごとに休止を入れる場合。"""
    pattern: SitPattern = []
    for hour in range(9, 18):
        if hour == 12:
            pattern.append((12, 13, False))
            continue
        pattern += [(hour, hour + 0.42, True), (hour + 0.42, hour + 0.47, False),
                    (hour + 0.47, hour + 0.83, True), (hour + 0.83, hour + 1, False)]
    return pattern


def _longest_sitting(pattern: SitPattern) -> float:
    """最も長く座り続けた時間 (分)。"""
    return max((end - start) * 60 for start, end, sitting in pattern if sitting)


def sitting_breaks() -> Path:
    """座りっぱなしの 1 日と、こまめに立つ 1 日の比較。"""
    setup_style()
    rows = [("座りっぱなし", _continuous_sitting()), ("こまめに立つ", _with_breaks())]
    fig, ax = plt.subplots(figsize=(9, 2.6))
    for y, (_, pattern) in enumerate(rows):
        for start, end, sitting in pattern:
            ax.barh(y, end - start, left=start, height=0.5, color=BLUE if sitting else ORANGE)
        ax.text(18.15, y, f"連続して座る時間は\n最長 {_longest_sitting(pattern):.0f} 分", va="center", fontsize=9)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([name for name, _ in rows])
    ax.invert_yaxis()
    ax.set_xlim(9, 18)
    ax.set_xticks(range(9, 19))
    ax.set_xticklabels([f"{h}:00" for h in range(9, 19)])
    ax.barh(0, 0, color=BLUE, label="座っている")
    ax.barh(0, 0, color=ORANGE, label="立つ・歩く")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=2, fontsize=9, frameon=False)
    return save_figure(fig, "sitting_breaks.png")


def weekly_activity() -> Path:
    """活動記録のサンプルデータから、1 週間の身体活動量を曜日ごとに積み上げる。"""
    setup_style()
    entries = activity_calc.load_entries(EXAMPLES_DIR / "activity_sample.csv")
    groups: list[tuple[str, str, Callable[[activity_calc.Activity], bool]]] = [
        ("生活活動 (歩行・階段など)", BLUE, lambda a: not a.is_exercise),
        ("運動 (速歩・ジョギングなど)", ORANGE, lambda a: a.is_exercise and not a.is_strength),
        ("筋力トレーニング", GREEN, lambda a: a.is_strength),
    ]
    days = list(activity_calc.DAYS)
    bottoms = [0.0] * len(days)
    fig, ax = plt.subplots(figsize=(8, 3.8))
    for label, color, match in groups:
        values = [
            sum(e.mets_hours for e in entries
                if e.day == day and e.activity.mets >= activity_calc.MODERATE_METS and match(e.activity))
            for day in days
        ]
        ax.bar(days, values, bottom=bottoms, color=color, label=label, width=0.6)
        bottoms = [b + v for b, v in zip(bottoms, values)]
    daily_target = activity_calc.TARGET_ACTIVITY / 7
    ax.axhline(daily_target, color=GRAY, linestyle="--", linewidth=1,
               label=f"推奨量 (週 23 メッツ・時) の 1 日あたり (約 {daily_target:.1f})")
    ax.set_ylabel("身体活動量 (メッツ・時)")
    ax.set_ylim(0, 7.5)
    ax.legend(loc="upper left", fontsize=9, frameon=False)
    return save_figure(fig, "weekly_activity.png")


def sleep_log_chart() -> Path:
    """睡眠記録のサンプルデータを、examples の sleep_log.py でグラフにする。"""
    records = sleep_log.load_records(EXAMPLES_DIR / "sleep_log_sample.csv")
    path = Path(__file__).resolve().parent.parent / "figures" / "sleep_log.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    sleep_log.plot_records(records, path)
    return path


def main() -> list[Path]:
    return [sitting_breaks(), weekly_activity(), sleep_log_chart()]


if __name__ == "__main__":
    for path in main():
        print(path)
