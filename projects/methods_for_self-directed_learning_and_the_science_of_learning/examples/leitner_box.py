"""ライトナー方式によるカード管理をシミュレーションする。

ライトナー方式では、カードを複数の箱に分けて管理する。

* 新しいカードは箱 1 に入れる。
* 箱 k のカードは 2 ** (k - 1) 日ごとに復習する（箱 1 は毎日、箱 2 は 2 日ごと、…）。
* 正解したカードは一つ上の箱へ移す（最上位の箱ではそのまま）。
* 不正解だったカードは箱 1 に戻す。

正解する確率は、箱が上がるほど高くなるように仮定した簡易モデルで決める。
実際の記憶を予測するものではなく、カードが箱の間を移動する様子を見るためのものである。

使い方:
    py leitner_box.py                    # 30 枚のカードを 30 日間シミュレーションする
    py leitner_box.py --cards 50 --days 60 --seed 1
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass

NUM_BOXES = 5
# 各箱のカードに正解する確率（仮定）。箱が上がるほど定着していると考える。
CORRECT_PROBABILITY = {1: 0.6, 2: 0.75, 3: 0.85, 4: 0.9, 5: 0.95}


@dataclass
class Card:
    """1 枚のカード。"""

    card_id: int
    box: int = 1


def review_interval(box: int) -> int:
    """箱 box のカードを復習する間隔（日）を返す。"""
    return int(2 ** (box - 1))


def is_due(box: int, day: int) -> bool:
    """day 日目が箱 box の復習日かどうかを返す。"""
    return day % review_interval(box) == 0


def run_day(cards: list[Card], day: int, rng: random.Random) -> tuple[int, int]:
    """day 日目の復習を行い、(復習した枚数, 正解した枚数) を返す。"""
    reviewed = 0
    correct = 0
    for card in cards:
        if not is_due(card.box, day):
            continue
        reviewed += 1
        if rng.random() < CORRECT_PROBABILITY[card.box]:
            correct += 1
            card.box = min(card.box + 1, NUM_BOXES)
        else:
            card.box = 1
    return reviewed, correct


def box_counts(cards: list[Card]) -> list[int]:
    """箱ごとのカード枚数を返す。"""
    counts = [0] * NUM_BOXES
    for card in cards:
        counts[card.box - 1] += 1
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description="ライトナー方式をシミュレーションする。")
    parser.add_argument("--cards", type=int, default=30, help="カードの枚数")
    parser.add_argument("--days", type=int, default=30, help="シミュレーションする日数")
    parser.add_argument("--seed", type=int, default=0, help="乱数の種（同じ値なら同じ結果になる）")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    cards = [Card(card_id=i) for i in range(args.cards)]

    # 全角文字は半角 2 文字分の幅で表示されるため、見出しは空白で位置を合わせる。
    header = " ".join(f"箱{b}" for b in range(1, NUM_BOXES + 1))
    print(f" 日 復習 正解  {header}")
    total_reviews = 0
    for day in range(args.days):
        reviewed, correct = run_day(cards, day, rng)
        total_reviews += reviewed
        counts = " ".join(f"{c:>3}" for c in box_counts(cards))
        print(f"{day:>3} {reviewed:>4} {correct:>4}  {counts}")

    print(f"復習した延べ枚数: {total_reviews}（毎日すべてのカードを復習すると {args.cards * args.days}）")


if __name__ == "__main__":
    main()
