"""座りすぎを防ぐための休憩タイマー。

作業時間と休憩時間を交互に繰り返し、決まった時刻に端末へメッセージを表示する。
作業時間の途中でも、一定の間隔で「立ち上がる」合図を出す。

使い方::

    python break_timer.py                       # 作業 50 分、休憩 10 分、25 分ごとに立つ合図
    python break_timer.py --work 45 --rest 15   # 作業 45 分、休憩 15 分
    python break_timer.py --stand 0             # 立つ合図を出さない
    python break_timer.py --work 0.2 --rest 0.1 --stand 0.1 --cycles 1   # 動作確認用

Ctrl+C で終了する。
"""

import argparse
import time
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Event:
    """タイマーが知らせる出来事。"""

    at_minutes: float  # 開始からの経過時間 (分)
    message: str


def build_schedule(work: float, rest: float, stand: float, cycles: int) -> list[Event]:
    """作業と休憩を cycles 回繰り返すときの、知らせる出来事の一覧を作る。"""
    if work <= 0 or rest <= 0 or stand < 0 or cycles <= 0:
        raise ValueError("work と rest は正の値、stand は 0 以上、cycles は 1 以上にする")

    events: list[Event] = []
    start = 0.0
    for cycle in range(1, cycles + 1):
        events.append(Event(start, f"作業開始 ({cycle} 回目、{work:g} 分)"))
        # 作業の途中で、stand 分ごとに立ち上がる合図を出す
        if stand > 0:
            elapsed = stand
            while elapsed < work:
                events.append(Event(start + elapsed, "立ち上がって、肩を回したり少し歩いたりしよう (1〜2 分)"))
                elapsed += stand
        events.append(Event(start + work, f"休憩 ({rest:g} 分): 画面から離れ、遠くを見て、体を動かそう"))
        start += work + rest
    events.append(Event(start, "終了"))
    return events


def notify(message: str) -> None:
    """時刻を付けてメッセージを表示し、ベルを鳴らす。"""
    print(f"\a[{datetime.now():%H:%M}] {message}", flush=True)


def run(events: list[Event]) -> None:
    """出来事の一覧に従って、時刻になったらメッセージを表示する。"""
    start = time.monotonic()
    for event in events:
        wait = start + event.at_minutes * 60 - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        notify(event.message)


def main() -> None:
    parser = argparse.ArgumentParser(description="作業と休憩を交互に知らせるタイマー。")
    parser.add_argument("--work", type=float, default=50, help="1 回の作業時間 (分)。既定値は 50")
    parser.add_argument("--rest", type=float, default=10, help="休憩時間 (分)。既定値は 10")
    parser.add_argument("--stand", type=float, default=25, help="作業中に立つ合図の間隔 (分)。0 で無効。既定値は 25")
    parser.add_argument("--cycles", type=int, default=8, help="作業と休憩を繰り返す回数。既定値は 8")
    args = parser.parse_args()

    events = build_schedule(args.work, args.rest, args.stand, args.cycles)
    try:
        run(events)
    except KeyboardInterrupt:
        print("\nタイマーを終了した。")


if __name__ == "__main__":
    main()
