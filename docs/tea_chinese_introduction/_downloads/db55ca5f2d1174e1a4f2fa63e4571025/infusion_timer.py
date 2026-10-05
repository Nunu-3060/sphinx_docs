"""中国茶の煎ごとの浸出時間を計るタイマー。

茶類を選ぶと、1 煎目から順に浸出時間をカウントダウンします。
煎を重ねるごとに浸出時間が延びる、中国茶の淹れ方に合わせています。

使い方:
    python infusion_timer.py               対話形式で茶類を選ぶ
    python infusion_timer.py oolong        青茶（烏龍茶）
    python infusion_timer.py oolong -s 3   青茶（烏龍茶）の 3 煎目から計る

Python 3.10 以上の標準ライブラリだけで動作します。
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class TeaKind:
    """茶類ごとの浸出時間の目安（蓋碗や茶壺で淹れる場合）。"""

    key: str  # コマンドラインで指定する名前
    name: str  # 画面に表示する名前
    first_seconds: int  # 1 煎目の浸出時間 [秒]
    step_seconds: int  # 1 煎ごとに延ばす時間 [秒]
    infusions: int  # 楽しめる煎数の目安


# 本文「おいしい淹れ方」の表と同じ値を使う
TEA_KINDS: tuple[TeaKind, ...] = (
    TeaKind("green", "緑茶", 60, 15, 3),
    TeaKind("white", "白茶", 45, 15, 5),
    TeaKind("yellow", "黄茶", 60, 15, 3),
    TeaKind("oolong", "青茶（烏龍茶）", 30, 10, 6),
    TeaKind("black", "紅茶", 40, 15, 4),
    TeaKind("dark", "黒茶（プーアル茶）", 20, 10, 8),
    TeaKind("jasmine", "花茶（ジャスミン茶）", 60, 15, 3),
)


def find_tea_kind(key: str) -> TeaKind:
    """名前（green、oolong など）から茶類を探す。"""
    for kind in TEA_KINDS:
        if kind.key == key:
            return kind
    raise ValueError(f"不明な茶類です: {key}")


def ask_tea_kind() -> TeaKind:
    """茶類を対話形式で選んでもらう。"""
    for number, kind in enumerate(TEA_KINDS, start=1):
        print(f"  {number}: {kind.name}")
    while True:
        text = input("茶類を番号で選んでください: ")
        if text.isdecimal() and 1 <= int(text) <= len(TEA_KINDS):
            return TEA_KINDS[int(text) - 1]
        print("表示されている番号を入力してください。")


def infusion_seconds(kind: TeaKind, number: int) -> int:
    """number 煎目の浸出時間 t [秒] を返す。

    t = t1 + (number - 1) × Δt で求める。
    """
    return kind.first_seconds + (number - 1) * kind.step_seconds


def format_time(seconds: int) -> str:
    """秒数を「○ 分 ○○ 秒」の形式の文字列にする。"""
    minutes, rest = divmod(seconds, 60)
    return f"{minutes} 分 {rest:02d} 秒"


def count_down(seconds: int) -> None:
    """指定した秒数をカウントダウンし、残り時間を表示する。"""
    for remaining in range(seconds, 0, -1):
        print(f"\r  残り {format_time(remaining)} ", end="", flush=True)
        time.sleep(1)
    print(f"\r  残り {format_time(0)} ")


def wait_for_start(number: int) -> bool:
    """お湯を注ぐ準備ができるまで待つ。続ける場合は True を返す。"""
    text = input(
        f"{number} 煎目: お湯を注いだら Enter を押してください"
        "（q で終了）: "
    )
    return text.strip().lower() != "q"


def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析する。"""
    parser = argparse.ArgumentParser(
        description="中国茶の煎ごとの浸出時間を計るタイマーです。"
    )
    parser.add_argument(
        "kind",
        nargs="?",
        choices=[kind.key for kind in TEA_KINDS],
        help="茶類",
    )
    parser.add_argument(
        "-s", "--start", type=int, default=1, help="何煎目から計るか"
    )
    return parser.parse_args()


def main() -> int:
    """スクリプトの入口。"""
    args = parse_args()
    kind = ask_tea_kind() if args.kind is None else find_tea_kind(args.kind)
    start: int = args.start
    if not 1 <= start <= kind.infusions:
        print(f"煎数には 1〜{kind.infusions} を指定してください。")
        return 1

    print(f"{kind.name}: {kind.infusions} 煎目まで計ります。"
          "Ctrl+C で中止できます。")
    try:
        for number in range(start, kind.infusions + 1):
            if not wait_for_start(number):
                print("タイマーを終了しました。")
                return 0
            count_down(infusion_seconds(kind, number))
            # "\a" はベル文字で、対応している環境では音が鳴ります
            print(f"\a  {number} 煎目の時間です。茶海に注ぎ切りましょう。")
    except (KeyboardInterrupt, EOFError):
        print("\nタイマーを中止しました。")
        return 1

    print("目安の煎数に達しました。味が薄くなるまで楽しめます。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
