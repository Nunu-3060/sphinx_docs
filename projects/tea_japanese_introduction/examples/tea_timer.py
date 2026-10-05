"""日本茶の浸出時間を計るタイマー.

お茶の種類と何煎目かを指定すると, 湯温の目安を表示してから
浸出時間をカウントダウンし, 時間になったら音とメッセージで知らせます.

使い方:
    python tea_timer.py                  # 対話形式で入力する
    python tea_timer.py sencha           # 上級煎茶の 1 煎目
    python tea_timer.py sencha --brew 2  # 上級煎茶の 2 煎目
    python tea_timer.py --seconds 50     # 好みの秒数で計る

Python 3.10 以上の標準ライブラリだけで動作します.
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class Brew:
    """1 回分の淹れ方."""

    temperature: str  # 湯温の目安
    seconds: int      # 浸出時間 [秒]


# 本文「おいしい淹れ方」の目安の中間の値を使う
# 2 煎目以降は湯温を上げ, 浸出時間を短くする
TIMERS: dict[str, tuple[str, list[Brew]]] = {
    'sencha': ('上級煎茶', [
        Brew('70 ℃', 90), Brew('80 ℃', 10), Brew('90 ℃', 30)]),
    'futsu': ('普通煎茶・深蒸し煎茶', [
        Brew('80〜90 ℃', 45), Brew('90 ℃', 10), Brew('熱湯', 30)]),
    'gyokuro': ('玉露', [
        Brew('50〜60 ℃', 135), Brew('60 ℃', 30), Brew('70 ℃', 60)]),
    'bancha': ('番茶・ほうじ茶・玄米茶', [
        Brew('熱湯', 30), Brew('熱湯', 15)]),
}


def format_time(seconds: int) -> str:
    """秒数を「m 分 ss 秒」の形にする."""
    minutes, rest = divmod(seconds, 60)
    return f'{minutes} 分 {rest:02d} 秒'


def countdown(seconds: int) -> None:
    """残り時間を 1 秒ごとに表示しながら待つ."""
    for remaining in range(seconds, 0, -1):
        print(f'\r残り {format_time(remaining)}', end='', flush=True)
        time.sleep(1)
    print(f'\r残り {format_time(0)}')


def ask_key() -> str:
    """お茶の種類を番号で選んでもらう."""
    keys = list(TIMERS)
    for number, key in enumerate(keys, start=1):
        print(f'  {number}: {TIMERS[key][0]}')
    while True:
        answer = input('お茶の種類を番号で選んでください: ').strip()
        if answer.isdigit() and 1 <= int(answer) <= len(keys):
            return keys[int(answer) - 1]
        print('一覧にある番号を入力してください。')


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """コマンドライン引数を解析する."""
    parser = argparse.ArgumentParser(
        description='日本茶の浸出時間を計ります。')
    parser.add_argument('tea', nargs='?', choices=list(TIMERS),
                        help='お茶の種類')
    parser.add_argument('--brew', type=int, default=1,
                        help='何煎目か（既定値: 1）')
    parser.add_argument('--seconds', type=int,
                        help='好みの浸出時間 [秒]')
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """エントリーポイント."""
    args = parse_args(argv)
    if args.seconds is not None:
        if args.seconds <= 0:
            print('秒数は 1 以上で指定してください。', file=sys.stderr)
            return 1
        seconds: int = args.seconds
        print(f'{format_time(seconds)}を計ります。Ctrl+C で中止できます。')
    else:
        key: str = args.tea if args.tea is not None else ask_key()
        name, brews = TIMERS[key]
        if not 1 <= args.brew <= len(brews):
            print(f'{name}は {len(brews)} 煎目までです。', file=sys.stderr)
            return 1
        brew = brews[args.brew - 1]
        seconds = brew.seconds
        print(f'{name}の {args.brew} 煎目: 湯温は {brew.temperature}が'
              '目安です。')
        print(f'{format_time(seconds)}を計ります。Ctrl+C で中止できます。')
    try:
        countdown(seconds)
    except KeyboardInterrupt:
        print('\n中止しました。')
        return 1
    print('\a時間になりました。最後の一滴まで注ぎ切りましょう。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
