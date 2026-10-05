"""ハンドドリップの蒸らしと注湯のタイミングを案内するタイマー。

粉の量を指定すると、蒸らしから注湯の終わりまでの手順を時間に合わせて
表示します。各手順では、スケール（はかり）の表示が何 g になるまで
お湯を注げばよいかを案内します。

使い方:
    python drip_timer.py         対話形式で粉の量を入力する
    python drip_timer.py 20      粉 20 g で淹れる
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass

# お湯の量 ÷ 粉の量の比率
RATIO = 15

# 蒸らしで注ぐお湯の量（粉の量に対する倍率）
BLOOM_RATE = 2


@dataclass(frozen=True)
class Step:
    """抽出の手順の 1 つ。"""

    start: int  # 開始時刻（抽出を始めてからの秒数）
    message: str  # 画面に表示する案内


def make_steps(coffee_g: float) -> list[Step]:
    """粉の量から、抽出の手順を作る。

    注ぐお湯の合計は粉の量の 15 倍です。蒸らしのあと 3 回に分けて、
    合計の 40 %、70 %、100 % になるまで注ぎます。
    """
    total = round(coffee_g * RATIO)
    bloom = round(coffee_g * BLOOM_RATE)
    first = round(total * 0.4)
    second = round(total * 0.7)
    return [
        Step(0, f"蒸らし：スケールが {bloom} g になるまで、"
                "粉全体を湿らせるように注ぎます。"),
        Step(30, f"1 回目：スケールが {first} g になるまで、"
                 "中心から円を描くように注ぎます。"),
        Step(70, f"2 回目：スケールが {second} g になるまで注ぎます。"),
        Step(110, f"3 回目：スケールが {total} g になるまで注ぎます。"),
        Step(180, "お湯が落ちきっていなくても、ドリッパーを外します。"),
    ]


def format_time(seconds: int) -> str:
    """秒数を「分:秒」の形式の文字列にする。"""
    minutes, rest = divmod(seconds, 60)
    return f"{minutes}:{rest:02d}"


def wait_until(start_time: float, target: int, label: str) -> None:
    """抽出開始から target 秒になるまで、残り時間を表示しながら待つ。"""
    while True:
        remaining = target - int(time.monotonic() - start_time)
        if remaining <= 0:
            break
        print(f"\r  {label}まであと {remaining:3d} 秒 ", end="", flush=True)
        time.sleep(0.2)
    print("\r" + " " * 40 + "\r", end="")


def ask_coffee_g() -> float:
    """粉の量を対話形式で入力してもらう。"""
    while True:
        text = input("粉の量を g で入力してください（例：20）: ")
        try:
            coffee_g = float(text)
        except ValueError:
            coffee_g = 0.0
        if 5 <= coffee_g <= 60:
            return coffee_g
        print("5 から 60 までの数を入力してください。")


def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析する。"""
    parser = argparse.ArgumentParser(
        description="ハンドドリップの手順を時間に合わせて案内します。"
    )
    parser.add_argument(
        "coffee_g", nargs="?", type=float, help="粉の量（g、5〜60）"
    )
    return parser.parse_args()


def main() -> int:
    """スクリプトの入口。"""
    args = parse_args()

    coffee_g: float | None = args.coffee_g
    if coffee_g is None:
        coffee_g = ask_coffee_g()
    elif not 5 <= coffee_g <= 60:
        print("粉の量には 5 から 60 までの数を指定してください。")
        return 1

    steps = make_steps(coffee_g)
    print(f"粉 {coffee_g:g} g、お湯 {round(coffee_g * RATIO)} g で淹れます。")
    input("スケールを 0 g にしてから、Enter キーを押すと始まります。")
    print("Ctrl+C で中止できます。")

    start_time = time.monotonic()
    try:
        for step in steps:
            wait_until(start_time, step.start, format_time(step.start))
            # "\a" はベル文字で、対応している環境では音が鳴ります
            print(f"\a[{format_time(step.start)}] {step.message}")
    except KeyboardInterrupt:
        print("\nタイマーを中止しました。")
        return 1

    print("できあがりです。サーバーを軽く回して混ぜてから注ぎましょう。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
