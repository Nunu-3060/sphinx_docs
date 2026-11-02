"""CSV 形式の学習ログを集計し、週ごとの学習時間をグラフにする。

CSV の形式（1 行目は見出し）:
    date,topic,minutes,method
    2026-10-05,Rust,40,読書

    date: 学習した日（YYYY-MM-DD）
    topic: 学習した項目
    minutes: 学習時間（分）
    method: 学習の方法（読書、検索練習、実装、執筆 など自由に決めてよい）

使い方:
    py study_log.py                    # study_log_sample.csv を集計する
    py study_log.py my_log.csv

項目別・方法別の合計時間を表示し、週ごとの学習時間を output/study_log.png に保存する。
"""

from __future__ import annotations

import argparse
import csv
import datetime
import pathlib
import unicodedata
from collections import defaultdict
from dataclasses import dataclass

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402

BASE_DIR = pathlib.Path(__file__).resolve().parent
DEFAULT_FILE = BASE_DIR / "study_log_sample.csv"
OUTPUT_DIR = BASE_DIR / "output"


@dataclass(frozen=True)
class Record:
    """学習ログの 1 行。"""

    date: datetime.date
    topic: str
    minutes: int
    method: str


def load_records(path: pathlib.Path) -> list[Record]:
    """CSV ファイルから学習ログを読み込む。"""
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [
            Record(
                date=datetime.date.fromisoformat(row["date"]),
                topic=row["topic"],
                minutes=int(row["minutes"]),
                method=row["method"],
            )
            for row in reader
        ]


def total_by(records: list[Record], key: str) -> dict[str, int]:
    """key（"topic" または "method"）ごとの合計時間を、多い順に返す。"""
    totals: dict[str, int] = defaultdict(int)
    for record in records:
        totals[getattr(record, key)] += record.minutes
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))


def week_start(day: datetime.date) -> datetime.date:
    """day を含む週の月曜日を返す。"""
    return day - datetime.timedelta(days=day.weekday())


def weekly_minutes(records: list[Record]) -> dict[datetime.date, int]:
    """週（月曜日の日付）ごとの合計時間を、日付順に返す。"""
    totals: dict[datetime.date, int] = defaultdict(int)
    for record in records:
        totals[week_start(record.date)] += record.minutes
    return dict(sorted(totals.items()))


def pad(text: str, width: int) -> str:
    """全角文字を半角 2 文字分と数えて、表示幅が width になるまで右側を空白で埋める。"""
    display_width = sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in text)
    return text + " " * max(0, width - display_width)


def print_totals(title: str, totals: dict[str, int]) -> None:
    """合計時間と割合を表示する。"""
    whole = sum(totals.values())
    print(f"## {title}")
    for name, minutes in totals.items():
        print(f"  {pad(name, 10)} {minutes:>5} 分 ({minutes / whole:>5.1%})")
    print()


def save_weekly_chart(weekly: dict[datetime.date, int], path: pathlib.Path) -> None:
    """週ごとの学習時間を棒グラフにして保存する。"""
    labels = [day.strftime("%m-%d") for day in weekly]
    hours = [minutes / 60 for minutes in weekly.values()]
    fig, ax = plt.subplots(figsize=(7.0, 3.5))
    ax.bar(labels, hours)
    ax.set_xlabel("week (starting Monday)")
    ax.set_ylabel("hours")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=100)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="学習ログを集計し、週ごとの学習時間をグラフにする。")
    parser.add_argument("file", type=pathlib.Path, nargs="?", default=DEFAULT_FILE, help="学習ログの CSV ファイル")
    args = parser.parse_args()

    records = load_records(args.file)
    if not records:
        print("記録がない。")
        return

    total = sum(r.minutes for r in records)
    days = len({r.date for r in records})
    print(f"期間: {min(r.date for r in records)} から {max(r.date for r in records)}")
    print(f"合計: {total} 分（{total / 60:.1f} 時間）、学習した日数: {days} 日\n")
    print_totals("項目別", total_by(records, "topic"))
    print_totals("方法別", total_by(records, "method"))

    weekly = weekly_minutes(records)
    print("## 週別")
    for day, minutes in weekly.items():
        print(f"  {day} の週: {minutes:>4} 分")

    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / "study_log.png"
    save_weekly_chart(weekly, path)
    print(f"\nグラフを保存した: {path}")


if __name__ == "__main__":
    main()
