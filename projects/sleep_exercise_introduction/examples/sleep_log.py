"""睡眠記録 CSV を集計し、睡眠時間と就寝・起床時刻のばらつきを調べる。

CSV には 1 晩ごとに次の 3 列を記録する。

* date: 寝床に入った日の日付 (YYYY-MM-DD)。午前 0 時を過ぎてから寝た場合も前日の日付にする。
* bedtime: 寝た時刻 (HH:MM)
* wake_time: 起きた時刻 (HH:MM)

使い方::

    python sleep_log.py sleep_log_sample.csv
    python sleep_log.py sleep_log_sample.csv --plot sleep_log.png
"""

import argparse
import csv
import statistics
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

# 時刻は「寝た日の 0 時」からの経過分で表す。正午より前の就寝時刻は翌日とみなす。
MINUTES_PER_DAY = 24 * 60
NOON = 12 * 60


@dataclass(frozen=True)
class SleepRecord:
    """1 晩分の睡眠記録。"""

    night: date
    bedtime: int  # 寝た日の 0 時からの経過分
    wake_time: int  # 寝た日の 0 時からの経過分

    @property
    def duration(self) -> int:
        """睡眠時間 (分)。"""
        return self.wake_time - self.bedtime

    @property
    def midpoint(self) -> float:
        """睡眠の中央時刻 (寝た日の 0 時からの経過分)。"""
        return (self.bedtime + self.wake_time) / 2

    @property
    def is_free_day(self) -> bool:
        """翌朝が休日 (土曜・日曜) なら True。"""
        return (self.night + timedelta(days=1)).weekday() >= 5


@dataclass(frozen=True)
class SleepSummary:
    """睡眠記録の集計結果。時間はすべて分単位。"""

    nights: int
    mean_duration: float
    mean_duration_work: float
    mean_duration_free: float
    bedtime_stdev: float
    wake_time_stdev: float
    social_jetlag: float


def parse_clock(text: str) -> int:
    """"HH:MM" 形式の時刻を、その日の 0 時からの経過分に変換する。"""
    hour, minute = text.strip().split(":")
    return int(hour) * 60 + int(minute)


def make_record(night: date, bedtime_text: str, wake_text: str) -> SleepRecord:
    """日付と時刻の文字列から SleepRecord を作る。"""
    bedtime = parse_clock(bedtime_text)
    if bedtime < NOON:
        bedtime += MINUTES_PER_DAY  # 午前 0 時を過ぎてから寝た
    wake_time = parse_clock(wake_text) + MINUTES_PER_DAY
    if wake_time <= bedtime:
        raise ValueError(f"{night}: 起床時刻が就寝時刻より前になっている")
    return SleepRecord(night, bedtime, wake_time)


def load_records(path: Path) -> list[SleepRecord]:
    """CSV ファイルから睡眠記録を読み込む。"""
    with path.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return [
            make_record(date.fromisoformat(row["date"]), row["bedtime"], row["wake_time"])
            for row in reader
        ]


def summarize(records: list[SleepRecord]) -> SleepSummary:
    """睡眠記録を集計する。平日と休日の記録がそれぞれ 1 晩以上必要である。"""
    work = [r for r in records if not r.is_free_day]
    free = [r for r in records if r.is_free_day]
    if len(records) < 2 or not work or not free:
        raise ValueError("平日と休日の記録がそれぞれ 1 晩以上、合計 2 晩以上必要である")

    # 社会的時差ぼけ: 休日と平日の睡眠中央時刻の差
    social_jetlag = statistics.mean(r.midpoint for r in free) - statistics.mean(r.midpoint for r in work)
    return SleepSummary(
        nights=len(records),
        mean_duration=statistics.mean(r.duration for r in records),
        mean_duration_work=statistics.mean(r.duration for r in work),
        mean_duration_free=statistics.mean(r.duration for r in free),
        bedtime_stdev=statistics.stdev(r.bedtime for r in records),
        wake_time_stdev=statistics.stdev(r.wake_time for r in records),
        social_jetlag=abs(social_jetlag),
    )


def format_minutes(minutes: float) -> str:
    """分を「H 時間 M 分」の形式にする。"""
    total = round(minutes)
    return f"{total // 60} 時間 {total % 60:02d} 分"


def format_report(summary: SleepSummary) -> str:
    """集計結果を、人が読みやすい文章にする。"""
    lines = [
        f"記録した夜の数        : {summary.nights} 晩",
        f"平均睡眠時間          : {format_minutes(summary.mean_duration)}",
        f"  平日 (翌日が平日)   : {format_minutes(summary.mean_duration_work)}",
        f"  休日 (翌日が休日)   : {format_minutes(summary.mean_duration_free)}",
        f"就寝時刻のばらつき    : ±{summary.bedtime_stdev:.0f} 分 (標準偏差)",
        f"起床時刻のばらつき    : ±{summary.wake_time_stdev:.0f} 分 (標準偏差)",
        f"社会的時差ぼけ        : {format_minutes(summary.social_jetlag)}",
    ]
    if summary.mean_duration < 6 * 60:
        lines.append("* 平均睡眠時間が 6 時間を下回っている。睡眠時間を確保する工夫をしよう。")
    if summary.social_jetlag >= 60:
        lines.append("* 平日と休日の睡眠の時間帯が 1 時間以上ずれている。休日も起床時刻をそろえよう。")
    return "\n".join(lines)


def plot_records(records: list[SleepRecord], output: Path) -> None:
    """睡眠の時間帯を横棒グラフにして PNG で保存する。"""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch

    plt.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "MS Gothic", "sans-serif"]
    work_color, free_color = "#4878a8", "#e07b39"
    fig, ax = plt.subplots(figsize=(8, 0.35 * len(records) + 1.2))
    for i, record in enumerate(records):
        color = free_color if record.is_free_day else work_color
        ax.barh(i, record.duration / 60, left=record.bedtime / 60, color=color, height=0.6)

    weekdays = "月火水木金土日"
    ax.set_yticks(range(len(records)))
    ax.set_yticklabels([f"{r.night:%m/%d}({weekdays[r.night.weekday()]})" for r in records])
    ax.invert_yaxis()
    ax.set_xlim(20, 36)
    ax.set_xticks(range(20, 37, 2))
    ax.set_xticklabels([f"{h % 24}:00" for h in range(20, 37, 2)])
    ax.set_xlabel("時刻")
    ax.grid(axis="x", alpha=0.3)
    ax.legend(
        handles=[Patch(color=work_color, label="翌日が平日"), Patch(color=free_color, label="翌日が休日")],
        loc="upper right",
        fontsize=9,
    )
    fig.savefig(output, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="睡眠記録 CSV を集計する。")
    parser.add_argument("csv_file", type=Path, help="睡眠記録の CSV ファイル")
    parser.add_argument("--plot", type=Path, help="睡眠の時間帯のグラフを保存する PNG ファイル")
    args = parser.parse_args()

    records = load_records(args.csv_file)
    print(format_report(summarize(records)))
    if args.plot is not None:
        plot_records(records, args.plot)
        print(f"グラフを保存した: {args.plot}")


if __name__ == "__main__":
    main()
