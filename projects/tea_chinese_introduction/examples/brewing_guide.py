"""中国茶の淹れ方の目安を表示するスクリプト。

茶類と器の容量を指定すると、茶葉の量、湯温、煎ごとの浸出時間の
目安を表示します。

使い方:
    python brewing_guide.py              対話形式で入力する
    python brewing_guide.py oolong 120   青茶（烏龍茶）を 120 ml の器で淹れる

Python 3.10 以上の標準ライブラリだけで動作します。
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class TeaKind:
    """茶類ごとの淹れ方の目安（蓋碗や茶壺で淹れる場合）。"""

    key: str  # コマンドラインで指定する名前
    name: str  # 画面に表示する名前
    leaf_g: float  # 容量 100 ml あたりの茶葉の量 [g]
    temperature: str  # 湯温の目安
    first_seconds: int  # 1 煎目の浸出時間 [秒]
    step_seconds: int  # 1 煎ごとに延ばす時間 [秒]
    infusions: int  # 楽しめる煎数の目安


# 本文「おいしい淹れ方」の表と同じ値を使う
TEA_KINDS: tuple[TeaKind, ...] = (
    TeaKind("green", "緑茶", 2.0, "80 ℃ 前後", 60, 15, 3),
    TeaKind("white", "白茶", 4.0, "85〜90 ℃", 45, 15, 5),
    TeaKind("yellow", "黄茶", 2.0, "80 ℃ 前後", 60, 15, 3),
    TeaKind("oolong", "青茶（烏龍茶）", 6.0, "95〜100 ℃", 30, 10, 6),
    TeaKind("black", "紅茶", 3.0, "90〜95 ℃", 40, 15, 4),
    TeaKind("dark", "黒茶（プーアル茶）", 5.0, "100 ℃", 20, 10, 8),
    TeaKind("jasmine", "花茶（ジャスミン茶）", 3.0, "85〜90 ℃", 60, 15, 3),
)

MIN_CAPACITY = 30  # 器の容量の下限 [ml]
MAX_CAPACITY = 500  # 器の容量の上限 [ml]


def find_tea_kind(key: str) -> TeaKind:
    """名前（green、oolong など）から茶類を探す。"""
    for kind in TEA_KINDS:
        if kind.key == key:
            return kind
    raise ValueError(f"不明な茶類です: {key}")


def leaf_amount(kind: TeaKind, capacity: int) -> float:
    """器の容量 c [ml] に合った茶葉の量 W [g] を返す。

    W = c × w / 100 で求める（w は 100 ml あたりの茶葉の量）。
    """
    if not MIN_CAPACITY <= capacity <= MAX_CAPACITY:
        raise ValueError(
            f"器の容量は {MIN_CAPACITY}〜{MAX_CAPACITY} ml で"
            "指定してください。"
        )
    return capacity * kind.leaf_g / 100


def infusion_seconds(kind: TeaKind, number: int) -> int:
    """number 煎目の浸出時間 t [秒] を返す。

    t = t1 + (number - 1) × Δt で求める。
    """
    if number < 1:
        raise ValueError("煎数には 1 以上の数を指定してください。")
    return kind.first_seconds + (number - 1) * kind.step_seconds


def format_time(seconds: int) -> str:
    """秒数を「○ 分 ○○ 秒」の形式の文字列にする。"""
    minutes, rest = divmod(seconds, 60)
    return f"{minutes} 分 {rest:02d} 秒"


def format_guide(kind: TeaKind, capacity: int) -> str:
    """淹れ方の目安を、画面に表示する文字列にする。"""
    lines = [
        f"{kind.name}を {capacity} ml の器で淹れる目安",
        f"  茶葉の量  : {leaf_amount(kind, capacity):.1f} g",
        f"  湯温      : {kind.temperature}",
        "  浸出時間  :",
    ]
    for number in range(1, kind.infusions + 1):
        seconds = infusion_seconds(kind, number)
        lines.append(f"    {number} 煎目  {format_time(seconds)}")
    return "\n".join(lines)


def ask_tea_kind() -> TeaKind:
    """茶類を対話形式で選んでもらう。"""
    for number, kind in enumerate(TEA_KINDS, start=1):
        print(f"  {number}: {kind.name}")
    while True:
        text = input("茶類を番号で選んでください: ")
        if text.isdecimal() and 1 <= int(text) <= len(TEA_KINDS):
            return TEA_KINDS[int(text) - 1]
        print("表示されている番号を入力してください。")


def ask_capacity() -> int:
    """器の容量を対話形式で入力してもらう。"""
    while True:
        text = input("器の容量 [ml] を入力してください: ")
        if text.isdecimal() and MIN_CAPACITY <= int(text) <= MAX_CAPACITY:
            return int(text)
        print(f"{MIN_CAPACITY}〜{MAX_CAPACITY} の整数を入力してください。")


def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析する。"""
    parser = argparse.ArgumentParser(
        description="中国茶の淹れ方の目安を表示します。"
    )
    parser.add_argument(
        "kind",
        nargs="?",
        choices=[kind.key for kind in TEA_KINDS],
        help="茶類",
    )
    parser.add_argument(
        "capacity", nargs="?", type=int, help="器の容量 [ml]"
    )
    return parser.parse_args()


def main() -> int:
    """スクリプトの入口。"""
    args = parse_args()
    kind = ask_tea_kind() if args.kind is None else find_tea_kind(args.kind)
    capacity: int = (
        ask_capacity() if args.capacity is None else args.capacity
    )
    try:
        print(format_guide(kind, capacity))
    except ValueError as error:
        print(error)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
