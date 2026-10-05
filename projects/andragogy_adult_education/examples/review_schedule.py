"""学習した日から、復習する日の予定を作る。

分散学習（間隔を空けて復習すること）の考え方に従い、学習した日の
1 日後、3 日後、7 日後、14 日後、30 日後を復習日として表示する。
間隔は --intervals で変更できる。

使い方::

    python review_schedule.py 2026-10-01
    python review_schedule.py 2026-10-01 --intervals 2 5 10
"""

import argparse
import datetime

DEFAULT_INTERVALS: list[int] = [1, 3, 7, 14, 30]
WEEKDAYS: list[str] = ['月', '火', '水', '木', '金', '土', '日']


def make_schedule(start: datetime.date,
                  intervals: list[int]) -> list[datetime.date]:
    """学習した日と間隔（日数）から、復習日のリストを返す。

    Args:
        start: 学習した日。
        intervals: 学習した日から数えた日数のリスト。

    Returns:
        復習日のリスト。日付の早い順に並べる。
    """
    return sorted(start + datetime.timedelta(days=days)
                  for days in intervals)


def format_date(day: datetime.date) -> str:
    """日付を「2026-10-02（金）」の形の文字列にする。"""
    return f'{day.isoformat()}（{WEEKDAYS[day.weekday()]}）'


def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析する。"""
    parser = argparse.ArgumentParser(description='復習する日の予定を作ります。')
    parser.add_argument('start', type=datetime.date.fromisoformat,
                        help='学習した日（例：2026-10-01）')
    parser.add_argument('--intervals', type=int, nargs='+',
                        default=DEFAULT_INTERVALS,
                        help='学習した日から数えた日数（既定：1 3 7 14 30）')
    return parser.parse_args()


def main() -> None:
    """復習日の予定を表示する。"""
    args = parse_args()
    start: datetime.date = args.start
    intervals: list[int] = args.intervals
    print(f'学習した日：{format_date(start)}')
    for number, day in enumerate(make_schedule(start, intervals), start=1):
        days = (day - start).days
        print(f'{number} 回目の復習：{format_date(day)}（{days} 日後）')


if __name__ == '__main__':
    main()
