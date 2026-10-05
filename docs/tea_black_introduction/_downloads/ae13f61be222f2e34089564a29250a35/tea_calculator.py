"""紅茶の茶葉の量とお湯の量を計算するスクリプト。

杯数と茶葉の種類を指定すると、ポットに入れる茶葉の量と、
注ぐお湯の量の目安を表示します。

使い方:
    python tea_calculator.py          対話形式で入力する
    python tea_calculator.py 3 bop    3 杯分、BOP などの細かい茶葉
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass

# 1 杯あたりのお湯の量（ml）
WATER_PER_CUP_ML: int = 150

# 一度に計算できる杯数の上限
MAX_CUPS: int = 20


@dataclass(frozen=True)
class LeafType:
    """茶葉の種類ごとの目安。"""

    key: str  # コマンドラインで指定する名前
    name: str  # 画面に表示する名前
    grams_per_cup: float  # 1 杯あたりの茶葉の量（g）
    steep_time: str  # 蒸らし時間の目安


LEAF_TYPES: tuple[LeafType, ...] = (
    LeafType("op", "OP などの大きな茶葉", 3.0, "3〜4 分"),
    LeafType("bop", "BOP などの細かい茶葉", 3.0, "2.5〜3 分"),
    LeafType("ctc", "BOPF や CTC などの特に細かい茶葉", 2.5, "1.5〜2 分"),
)


def find_leaf_type(key: str) -> LeafType:
    """名前（op、bop、ctc）から茶葉の種類を探す。"""
    for leaf in LEAF_TYPES:
        if leaf.key == key:
            return leaf
    raise ValueError(f"不明な茶葉の種類です: {key}")


def ask_cups() -> int:
    """杯数を対話形式で入力してもらう。"""
    while True:
        text = input(f"何杯分淹れますか（1〜{MAX_CUPS}）: ")
        if text.isdecimal() and 1 <= int(text) <= MAX_CUPS:
            return int(text)
        print(f"1 から {MAX_CUPS} までの数字を入力してください。")


def ask_leaf_type() -> LeafType:
    """茶葉の種類を対話形式で選んでもらう。"""
    for number, leaf in enumerate(LEAF_TYPES, start=1):
        print(f"  {number}: {leaf.name}")
    while True:
        text = input("茶葉の種類を番号で選んでください: ")
        if text.isdecimal() and 1 <= int(text) <= len(LEAF_TYPES):
            return LEAF_TYPES[int(text) - 1]
        print("表示されている番号を入力してください。")


def calculate(cups: int, leaf: LeafType) -> tuple[float, int]:
    """茶葉の量（g）とお湯の量（ml）を計算する。"""
    leaf_grams = cups * leaf.grams_per_cup
    water_ml = cups * WATER_PER_CUP_ML
    return leaf_grams, water_ml


def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析する。"""
    parser = argparse.ArgumentParser(
        description="紅茶の茶葉の量とお湯の量を計算します。"
    )
    parser.add_argument(
        "cups", nargs="?", type=int, help=f"杯数（1〜{MAX_CUPS}）"
    )
    parser.add_argument(
        "leaf",
        nargs="?",
        choices=[leaf.key for leaf in LEAF_TYPES],
        help="茶葉の種類（op、bop、ctc）",
    )
    return parser.parse_args()


def main() -> int:
    """スクリプトの入口。"""
    args = parse_args()

    cups: int | None = args.cups
    if cups is None:
        cups = ask_cups()
    elif not 1 <= cups <= MAX_CUPS:
        print(f"杯数は 1 から {MAX_CUPS} までで指定してください。")
        return 1

    leaf = ask_leaf_type() if args.leaf is None else find_leaf_type(args.leaf)

    leaf_grams, water_ml = calculate(cups, leaf)
    print()
    print(f"{cups} 杯分（{leaf.name}）の目安")
    print(f"  茶葉の量    : {leaf_grams:.1f} g（ティースプーン約 {cups} 杯）")
    print(f"  お湯の量    : {water_ml} ml")
    print(f"  蒸らし時間  : {leaf.steep_time}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
