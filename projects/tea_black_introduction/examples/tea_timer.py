"""紅茶の蒸らし時間を計るタイマー。

茶葉の種類を選ぶと、その茶葉に合った蒸らし時間をカウントダウンし、
時間になったら音とメッセージで知らせます。

使い方:
    python tea_timer.py                 対話形式で茶葉の種類を選ぶ
    python tea_timer.py op              OP などの大きな茶葉
    python tea_timer.py --seconds 200   好きな秒数を指定する
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class LeafType:
    """茶葉の種類ごとの蒸らし時間。"""

    key: str  # コマンドラインで指定する名前
    name: str  # 画面に表示する名前
    seconds: int  # タイマーで計る秒数（目安の範囲の中間）
    steep_time: str  # 蒸らし時間の目安


LEAF_TYPES: tuple[LeafType, ...] = (
    LeafType("op", "OP などの大きな茶葉", 210, "3〜4 分"),
    LeafType("bop", "BOP などの細かい茶葉", 165, "2.5〜3 分"),
    LeafType("ctc", "BOPF や CTC などの特に細かい茶葉", 105, "1.5〜2 分"),
    LeafType("bag", "ティーバッグ", 105, "1.5〜2 分"),
)


def find_leaf_type(key: str) -> LeafType:
    """名前（op、bop、ctc、bag）から茶葉の種類を探す。"""
    for leaf in LEAF_TYPES:
        if leaf.key == key:
            return leaf
    raise ValueError(f"不明な茶葉の種類です: {key}")


def ask_leaf_type() -> LeafType:
    """茶葉の種類を対話形式で選んでもらう。"""
    for number, leaf in enumerate(LEAF_TYPES, start=1):
        print(f"  {number}: {leaf.name}（{leaf.steep_time}）")
    while True:
        text = input("茶葉の種類を番号で選んでください: ")
        if text.isdecimal() and 1 <= int(text) <= len(LEAF_TYPES):
            return LEAF_TYPES[int(text) - 1]
        print("表示されている番号を入力してください。")


def format_time(seconds: int) -> str:
    """秒数を「○ 分 ○○ 秒」の形式の文字列にする。"""
    minutes, rest = divmod(seconds, 60)
    return f"{minutes} 分 {rest:02d} 秒"


def count_down(seconds: int) -> None:
    """指定した秒数をカウントダウンし、残り時間を表示する。"""
    for remaining in range(seconds, 0, -1):
        print(f"\r残り {format_time(remaining)} ", end="", flush=True)
        time.sleep(1)
    print(f"\r残り {format_time(0)} ")


def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析する。"""
    parser = argparse.ArgumentParser(
        description="紅茶の蒸らし時間を計るタイマーです。"
    )
    parser.add_argument(
        "leaf",
        nargs="?",
        choices=[leaf.key for leaf in LEAF_TYPES],
        help="茶葉の種類（op、bop、ctc、bag）",
    )
    parser.add_argument(
        "--seconds", type=int, help="茶葉の種類の代わりに秒数を指定する"
    )
    return parser.parse_args()


def main() -> int:
    """スクリプトの入口。"""
    args = parse_args()

    seconds: int | None = args.seconds
    if seconds is not None:
        if seconds <= 0:
            print("秒数には 1 以上の数を指定してください。")
            return 1
    else:
        if args.leaf is None:
            leaf = ask_leaf_type()
        else:
            leaf = find_leaf_type(args.leaf)
        seconds = leaf.seconds
        print(f"{leaf.name}: 目安は {leaf.steep_time}です。")

    print(f"{format_time(seconds)}を計ります。Ctrl+C で中止できます。")
    try:
        count_down(seconds)
    except KeyboardInterrupt:
        print("\nタイマーを中止しました。")
        return 1

    # "\a" はベル文字で、対応している環境では音が鳴ります
    print("\a蒸らし終わりました。茶こしでこしながら注ぎましょう。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
