"""引越し日から逆算して、やることリスト(スケジュール)を作成するスクリプト.

使い方:
    python moving_schedule.py 2026-11-15
    python moving_schedule.py 2026-11-15 --csv schedule.csv

1 つ目の引数に引越し日を「年-月-日」の形式で指定します。
--csv を付けると、表計算ソフトで開ける CSV ファイルも保存します。
"""

from __future__ import annotations

import argparse
import csv
import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    """やること 1 件分の情報."""

    offset_days: int  # 引越し日との差(マイナスは引越し前、プラスは引越し後)
    category: str  # 分類
    title: str  # やること


# 標準的なやることの一覧です。必要に応じて追加・削除してください。
TASKS: list[Task] = [
    Task(-60, "住まい", "新居を探し始める"),
    Task(-45, "住まい", "今の住まいの解約を管理会社・大家に連絡する"),
    Task(-45, "業者", "引越し業者から見積もりを取る(3 社程度)"),
    Task(-40, "業者", "引越し業者を決めて予約する"),
    Task(-30, "学校・職場", "学校・勤務先に引越しを伝える"),
    Task(-30, "片付け", "粗大ごみの収集を申し込む"),
    Task(-21, "片付け", "荷造りを始める(使わない物から)"),
    Task(-14, "役所", "転出届を出す(他の市区町村へ引越す場合)"),
    Task(-14, "役所", "国民健康保険・児童手当などの手続きをする"),
    Task(-10, "郵便・通信", "郵便の転送を申し込む"),
    Task(-10, "郵便・通信", "インターネット回線の移転を申し込む"),
    Task(-7, "ライフライン", "電気・ガス・水道の停止と開始を申し込む"),
    Task(-1, "当日準備", "冷蔵庫の電源を切り、洗濯機の水を抜く"),
    Task(0, "当日", "荷物の搬出・旧居の掃除と明け渡し"),
    Task(0, "当日", "新居でガスの開栓に立ち会う"),
    Task(1, "新居", "荷物に破損や紛失がないか確認する"),
    Task(3, "新居", "近所へあいさつする"),
    Task(7, "役所", "転入届(または転居届)を出す"),
    Task(7, "役所", "マイナンバーカードの住所を変更する"),
    Task(14, "警察", "運転免許証の住所を変更する"),
    Task(14, "各種変更", "銀行・クレジットカード・保険などの住所を変更する"),
]


def parse_date(text: str) -> datetime.date:
    """「年-月-日」形式の文字列を日付に変換する."""
    try:
        return datetime.date.fromisoformat(text)
    except ValueError as error:
        message = f"日付は 2026-11-15 のような形式で指定してください: {text}"
        raise argparse.ArgumentTypeError(message) from error


def describe_offset(offset_days: int) -> str:
    """引越し日との差を「○日前」「当日」「○日後」の文字列にする."""
    if offset_days < 0:
        return f"{-offset_days} 日前"
    if offset_days == 0:
        return "当日"
    return f"{offset_days} 日後"


def build_schedule(
    moving_day: datetime.date, tasks: list[Task]
) -> list[tuple[datetime.date, Task]]:
    """各やることに実際の日付を割り当て、日付順に並べる."""
    schedule = [
        (moving_day + datetime.timedelta(days=task.offset_days), task)
        for task in tasks
    ]
    return sorted(schedule, key=lambda item: item[0])


def print_schedule(schedule: list[tuple[datetime.date, Task]]) -> None:
    """スケジュールを画面に表示する."""
    weekdays = "月火水木金土日"
    for day, task in schedule:
        weekday = weekdays[day.weekday()]
        timing = describe_offset(task.offset_days)
        print(f"[ ] {day:%Y-%m-%d}({weekday}) {timing:>7} "
              f"[{task.category}] {task.title}")


def save_csv(path: str, schedule: list[tuple[datetime.date, Task]]) -> None:
    """スケジュールを CSV ファイルに保存する(Excel で開けるよう BOM 付き)."""
    with open(path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["完了", "日付", "時期", "分類", "やること"])
        for day, task in schedule:
            writer.writerow(
                ["", day.isoformat(), describe_offset(task.offset_days),
                 task.category, task.title]
            )


def main() -> None:
    """コマンドライン引数を読み取り、スケジュールを出力する."""
    parser = argparse.ArgumentParser(
        description="引越し日から逆算したやることリストを作成します。"
    )
    parser.add_argument("moving_day", type=parse_date,
                        help="引越し日(例: 2026-11-15)")
    parser.add_argument("--csv", metavar="FILE",
                        help="CSV ファイルの保存先(省略可)")
    args = parser.parse_args()

    schedule = build_schedule(args.moving_day, TASKS)
    print(f"引越し日: {args.moving_day:%Y-%m-%d}")
    print_schedule(schedule)
    if args.csv:
        save_csv(args.csv, schedule)
        print(f"CSV ファイルを保存しました: {args.csv}")


if __name__ == "__main__":
    main()
