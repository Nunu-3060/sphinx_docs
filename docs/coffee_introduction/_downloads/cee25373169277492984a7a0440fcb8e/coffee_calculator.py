"""コーヒーの粉の量とお湯の量を計算するスクリプト。

杯数、好みの濃さ、焙煎度、淹れ方を指定すると、粉の量、注ぐお湯の量、
お湯の温度、挽き方の目安を表示します。

使い方:
    python coffee_calculator.py              対話形式で入力する
    python coffee_calculator.py 2            2 杯分（普通の濃さ、中煎り）
    python coffee_calculator.py 3 --strength strong --roast dark
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass

# 1 杯分のできあがり量（ml）
CUP_ML = 140

# 粉 1 g が吸い込んで残すお湯の量（ml）
ABSORPTION_ML_PER_G = 2.0


@dataclass(frozen=True)
class Option:
    """選択肢の 1 つ。"""

    key: str  # コマンドラインで指定する名前
    name: str  # 画面に表示する名前
    detail: str  # 補足情報（お湯の温度や挽き方の目安）


# 濃さ：detail は使わない
STRENGTHS: tuple[Option, ...] = (
    Option("light", "薄め", ""),
    Option("normal", "普通", ""),
    Option("strong", "濃いめ", ""),
)

# 濃さごとの比率（お湯の量 ÷ 粉の量）
RATIOS: dict[str, int] = {"light": 17, "normal": 15, "strong": 13}

# 焙煎度：detail はお湯の温度の目安
ROASTS: tuple[Option, ...] = (
    Option("light", "浅煎り", "90〜95 ℃"),
    Option("medium", "中煎り", "88〜92 ℃"),
    Option("dark", "深煎り", "82〜88 ℃"),
)

# 淹れ方：detail は挽き方の目安
METHODS: tuple[Option, ...] = (
    Option("drip", "ハンドドリップ", "中細挽き"),
    Option("press", "フレンチプレス", "粗挽き"),
)


@dataclass(frozen=True)
class Recipe:
    """計算結果。"""

    coffee_g: float  # 粉の量（g）
    water_ml: int  # 注ぐお湯の量（ml）
    yield_ml: int  # できあがり量（ml）


def find_option(options: tuple[Option, ...], key: str) -> Option:
    """名前から選択肢を探す。"""
    for option in options:
        if option.key == key:
            return option
    raise ValueError(f"不明な選択肢です: {key}")


def calculate(cups: int, ratio: float) -> Recipe:
    """杯数と比率から、粉の量と注ぐお湯の量を計算する。

    できあがり量 = お湯の量 - 2 × 粉の量、お湯の量 = 比率 × 粉の量
    から、粉の量 = できあがり量 ÷ (比率 - 2) となります。
    """
    yield_ml = CUP_ML * cups
    coffee_g = yield_ml / (ratio - ABSORPTION_ML_PER_G)
    water_ml = round(coffee_g * ratio)
    return Recipe(round(coffee_g, 1), water_ml, yield_ml)


def ask_cups() -> int:
    """杯数を対話形式で入力してもらう。"""
    while True:
        text = input("何杯分淹れますか（1〜10）: ")
        if text.isdecimal() and 1 <= int(text) <= 10:
            return int(text)
        print("1 から 10 までの数を入力してください。")


def ask_option(
    title: str, options: tuple[Option, ...], default: int
) -> Option:
    """選択肢を番号で選んでもらう。何も入力しなければ default 番を選ぶ。"""
    for number, option in enumerate(options, start=1):
        print(f"  {number}: {option.name}")
    while True:
        text = input(f"{title}を番号で選んでください（省略時は {default}）: ")
        if text == "":
            return options[default - 1]
        if text.isdecimal() and 1 <= int(text) <= len(options):
            return options[int(text) - 1]
        print("表示されている番号を入力してください。")


def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析する。"""
    parser = argparse.ArgumentParser(
        description="コーヒーの粉の量とお湯の量を計算します。"
    )
    parser.add_argument("cups", nargs="?", type=int, help="杯数（1〜10）")
    parser.add_argument(
        "--strength",
        choices=[option.key for option in STRENGTHS],
        default="normal",
        help="濃さ（light、normal、strong）",
    )
    parser.add_argument(
        "--roast",
        choices=[option.key for option in ROASTS],
        default="medium",
        help="焙煎度（light、medium、dark）",
    )
    parser.add_argument(
        "--method",
        choices=[option.key for option in METHODS],
        default="drip",
        help="淹れ方（drip、press）",
    )
    return parser.parse_args()


def main() -> int:
    """スクリプトの入口。"""
    args = parse_args()

    if args.cups is None:
        cups = ask_cups()
        strength = ask_option("濃さ", STRENGTHS, 2)
        roast = ask_option("焙煎度", ROASTS, 2)
        method = ask_option("淹れ方", METHODS, 1)
    else:
        if not 1 <= args.cups <= 10:
            print("杯数には 1 から 10 までの数を指定してください。")
            return 1
        cups = args.cups
        strength = find_option(STRENGTHS, args.strength)
        roast = find_option(ROASTS, args.roast)
        method = find_option(METHODS, args.method)

    recipe = calculate(cups, RATIOS[strength.key])

    print(f"{cups} 杯分（{strength.name}、{roast.name}、{method.name}）の目安")
    print(f"  粉の量        : {recipe.coffee_g} g")
    print(f"  注ぐお湯の量  : {recipe.water_ml} ml")
    print(f"  できあがり量  : 約 {recipe.yield_ml} ml")
    print(f"  お湯の温度    : {roast.detail}")
    print(f"  挽き方        : {method.detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
