"""複数の学習項目から、交互学習の計画表を作成する。

項目ごとの問題数を与えると、同じ項目ができるだけ連続しないように並べ、
1 日あたりの問題数で区切った計画表を出力する。比較のため、項目ごとにまとめて
解くブロック学習の順序も表示する。

使い方:
    py interleave_plan.py Python=6 SQL=4 正規表現=4
    py interleave_plan.py Python=6 SQL=4 正規表現=4 --per-day 5
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass
class Topic:
    """学習項目と、残りの問題数。"""

    name: str
    remaining: int


def parse_topic(text: str) -> Topic:
    """「項目名=問題数」の形式の文字列を Topic に変換する。"""
    name, sep, count = text.partition("=")
    if not sep or not name or not count.isdigit() or int(count) <= 0:
        raise argparse.ArgumentTypeError(f"「項目名=問題数」の形式で指定する: {text}")
    return Topic(name, int(count))


def blocked_order(topics: list[Topic]) -> list[str]:
    """項目ごとにまとめて解く順序（ブロック学習）を返す。"""
    return [topic.name for topic in topics for _ in range(topic.remaining)]


def interleaved_order(topics: list[Topic]) -> list[str]:
    """同じ項目ができるだけ連続しない順序（交互学習）を返す。

    毎回、直前と異なる項目のうち残りの問題数が最も多いものを選ぶ。
    残りの問題数が多い項目を先に減らすことで、終盤に同じ項目が続くのを防ぐ。
    """
    pool = [Topic(t.name, t.remaining) for t in topics]
    order: list[str] = []
    previous = ""
    while any(t.remaining > 0 for t in pool):
        candidates = [t for t in pool if t.remaining > 0 and t.name != previous]
        if not candidates:
            # 残りが 1 項目だけになった場合は連続を避けられない。
            candidates = [t for t in pool if t.remaining > 0]
        chosen = max(candidates, key=lambda t: t.remaining)
        chosen.remaining -= 1
        order.append(chosen.name)
        previous = chosen.name
    return order


def split_by_day(order: list[str], per_day: int) -> list[list[str]]:
    """順序を 1 日あたり per_day 問ずつに区切る。"""
    return [order[i:i + per_day] for i in range(0, len(order), per_day)]


def count_repeats(order: list[str]) -> int:
    """同じ項目が直前と連続した回数を返す。"""
    return sum(1 for a, b in zip(order, order[1:]) if a == b)


def print_plan(title: str, order: list[str], per_day: int) -> None:
    """計画表を表示する。"""
    print(f"## {title}（同じ項目の連続: {count_repeats(order)} 回）")
    for day, items in enumerate(split_by_day(order, per_day), start=1):
        print(f"  {day} 日目: {' → '.join(items)}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="交互学習の計画表を作成する。")
    parser.add_argument("topics", type=parse_topic, nargs="+", help="「項目名=問題数」の形式で学習項目を指定する")
    parser.add_argument("--per-day", type=int, default=4, help="1 日に解く問題数")
    args = parser.parse_args()

    topics: list[Topic] = args.topics
    per_day: int = args.per_day

    print_plan("ブロック学習", blocked_order(topics), per_day)
    print_plan("交互学習", interleaved_order(topics), per_day)


if __name__ == "__main__":
    main()
