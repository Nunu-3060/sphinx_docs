"""SM-2 アルゴリズムで次回の復習日を計算する。

SM-2 は 1980 年代に P. A. Wozniak が SuperMemo のために考案したアルゴリズムで、
多くの間隔反復ソフトの基礎になっている。復習のたびに、思い出せた度合いを
0 から 5 の 6 段階で自己評価し、その値から次回の復習間隔を決める。

    5: 完璧に思い出せた
    4: 少し迷ったが思い出せた
    3: かなり苦労して思い出せた
    2: 思い出せなかったが、答えを見ると簡単に感じた
    1: 思い出せなかったが、答えを見て思い出した
    0: まったく思い出せなかった

使い方:
    py sm2_scheduler.py 5 4 3 5 2 4    # 復習ごとの自己評価を順に与える
    py sm2_scheduler.py --start 2026-11-01 5 5 5
"""

from __future__ import annotations

import argparse
import datetime
from dataclasses import dataclass

MIN_EASINESS = 1.3


@dataclass(frozen=True)
class CardState:
    """カードの学習状態。"""

    repetition: int = 0  # 連続して正解した回数
    interval: int = 0  # 次回までの間隔（日）
    easiness: float = 2.5  # 易しさ係数（E-Factor）


def update_easiness(easiness: float, quality: int) -> float:
    """自己評価 quality に応じて易しさ係数を更新する。"""
    new_value = easiness + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    return max(MIN_EASINESS, new_value)


def review(state: CardState, quality: int) -> CardState:
    """自己評価 quality で復習した後の状態を返す。"""
    if not 0 <= quality <= 5:
        raise ValueError(f"自己評価は 0 から 5 の整数で指定する: {quality}")

    easiness = update_easiness(state.easiness, quality)
    if quality < 3:
        # 思い出せなかった場合は、最初から覚え直す。
        return CardState(repetition=0, interval=1, easiness=easiness)

    repetition = state.repetition + 1
    if repetition == 1:
        interval = 1
    elif repetition == 2:
        interval = 6
    else:
        interval = round(state.interval * easiness)
    return CardState(repetition=repetition, interval=interval, easiness=easiness)


def main() -> None:
    parser = argparse.ArgumentParser(description="SM-2 アルゴリズムで次回の復習日を計算する。")
    parser.add_argument("qualities", type=int, nargs="+", help="復習ごとの自己評価（0 から 5）")
    parser.add_argument(
        "--start", type=datetime.date.fromisoformat, default=datetime.date.today(), help="初回学習日（YYYY-MM-DD）"
    )
    args = parser.parse_args()

    qualities: list[int] = args.qualities
    day: datetime.date = args.start
    state = CardState()

    print("回 学習日       評価 易しさ 間隔 次回")
    for count, quality in enumerate(qualities, start=1):
        state = review(state, quality)
        next_day = day + datetime.timedelta(days=state.interval)
        print(f"{count:>2} {day} {quality:>4} {state.easiness:>6.2f} {state.interval:>4} {next_day}")
        day = next_day


if __name__ == "__main__":
    main()
