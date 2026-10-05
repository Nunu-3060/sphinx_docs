"""学習の記録（CSV ファイル）を集計する。

CSV ファイルには、次の 4 つの列を書く。1 行目は列名とする。

* date: 学習した日（例：2026-09-01）
* theme: 学習のテーマ（例：英会話）
* minutes: 学習した時間（分）
* note: 学んだことや気づいたこと

テーマごとの合計時間と回数、週ごとの合計時間を表示する。

使い方::

    python learning_log.py learning_log_sample.csv
"""

import argparse
import csv
import datetime
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Record:
    """学習の記録 1 件を表す。"""

    date: datetime.date
    theme: str
    minutes: int
    note: str


def read_records(path: Path) -> list[Record]:
    """CSV ファイルから学習の記録を読み込む。"""
    with path.open(encoding='utf-8', newline='') as f:
        return [
            Record(date=datetime.date.fromisoformat(row['date']),
                   theme=row['theme'],
                   minutes=int(row['minutes']),
                   note=row['note'])
            for row in csv.DictReader(f)
        ]


def total_by_theme(records: list[Record]) -> dict[str, tuple[int, int]]:
    """テーマごとに（合計時間（分）、回数）を求める。"""
    minutes: dict[str, int] = defaultdict(int)
    counts: dict[str, int] = defaultdict(int)
    for record in records:
        minutes[record.theme] += record.minutes
        counts[record.theme] += 1
    return {theme: (minutes[theme], counts[theme]) for theme in minutes}


def total_by_week(records: list[Record]) -> dict[datetime.date, int]:
    """週ごとの合計時間（分）を求める。週は月曜日の日付で表す。"""
    totals: dict[datetime.date, int] = defaultdict(int)
    for record in records:
        monday = record.date - datetime.timedelta(days=record.date.weekday())
        totals[monday] += record.minutes
    return dict(sorted(totals.items()))


def main() -> None:
    """学習の記録を集計して表示する。"""
    parser = argparse.ArgumentParser(description='学習の記録を集計します。')
    parser.add_argument('csv_file', type=Path, help='学習の記録の CSV ファイル')
    args = parser.parse_args()
    records = read_records(args.csv_file)

    print('テーマごとの合計')
    for theme, (minutes, count) in total_by_theme(records).items():
        print(f'  {theme}：{minutes} 分（{count} 回）')

    print('週ごとの合計')
    for monday, minutes in total_by_week(records).items():
        print(f'  {monday.isoformat()} の週：{minutes} 分')


if __name__ == '__main__':
    main()
