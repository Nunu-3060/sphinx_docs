"""CSV の問題集から出題する、検索練習用の小テスト。

問題を表示したら、答えを見る前に自分で答えを思い出す（声に出す、紙に書くなど）。
Enter キーで答えを表示し、思い出せたかどうかを自己評価する。
思い出せなかった問題は、全問を解き終えた後にもう一度出題する。

CSV の形式（1 行目は見出し）:
    question,answer
    Python でリストの末尾に要素を追加するメソッドは?,append

使い方:
    py quiz.py                          # quiz_sample.csv から出題する
    py quiz.py my_questions.csv --seed 1
"""

from __future__ import annotations

import argparse
import csv
import pathlib
import random
from dataclasses import dataclass

DEFAULT_FILE = pathlib.Path(__file__).resolve().parent / "quiz_sample.csv"


@dataclass(frozen=True)
class Question:
    """1 問分の問題と答え。"""

    question: str
    answer: str


def load_questions(path: pathlib.Path) -> list[Question]:
    """CSV ファイルから問題を読み込む。"""
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [Question(row["question"], row["answer"]) for row in reader]


def ask(item: Question, number: int, total: int) -> bool:
    """1 問出題し、思い出せたら True を返す。"""
    print(f"\n[{number}/{total}] {item.question}")
    input("  答えを思い出したら Enter キーを押す...")
    print(f"  答え: {item.answer}")
    while True:
        reply = input("  思い出せたか? [y/n]: ").strip().lower()
        if reply in ("y", "n"):
            return reply == "y"


def run_round(items: list[Question]) -> list[Question]:
    """items を順に出題し、思い出せなかった問題のリストを返す。"""
    missed: list[Question] = []
    for number, item in enumerate(items, start=1):
        if not ask(item, number, len(items)):
            missed.append(item)
    return missed


def main() -> None:
    parser = argparse.ArgumentParser(description="CSV の問題集から出題する検索練習用の小テスト。")
    parser.add_argument("file", type=pathlib.Path, nargs="?", default=DEFAULT_FILE, help="問題集の CSV ファイル")
    parser.add_argument("--seed", type=int, default=None, help="出題順を決める乱数の種")
    args = parser.parse_args()

    questions = load_questions(args.file)
    if not questions:
        print("問題がない。")
        return
    random.Random(args.seed).shuffle(questions)

    try:
        missed = run_round(questions)
        first_score = len(questions) - len(missed)
        round_number = 1
        while missed:
            round_number += 1
            print(f"\n--- 思い出せなかった {len(missed)} 問をもう一度出題する（{round_number} 周目）---")
            missed = run_round(missed)
    except (EOFError, KeyboardInterrupt):
        print("\n中断した。")
        return

    print(f"\n1 周目の結果: {first_score}/{len(questions)} 問を思い出せた。")
    print("思い出せなかった問題は、日を空けてもう一度解くと定着しやすい。")


if __name__ == "__main__":
    main()
