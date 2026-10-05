"""日本茶の淹れ方の目安を表示するスクリプト.

お茶の種類と人数を指定すると, 茶葉の量, お湯の量, 湯温, 浸出時間の
目安を表示します.

使い方:
    python brewing_guide.py              # 対話形式で入力する
    python brewing_guide.py sencha 3     # 上級煎茶を 3 人分

Python 3.10 以上の標準ライブラリだけで動作します.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class TeaRecipe:
    """1 人分の淹れ方の目安."""

    name: str          # お茶の名前
    leaf_g: float      # 1 人分の茶葉の量 [g]
    water_ml: int      # 1 人分のお湯の量 [ml]
    temperature: str   # 湯温の目安
    steep_time: str    # 浸出時間の目安
    spoon: str         # 量るときに使う道具
    spoon_g: float     # その道具 1 杯分の重さの目安 [g]


# 本文「おいしい淹れ方」「抹茶を点てる」の表と同じ値を使う
RECIPES: dict[str, TeaRecipe] = {
    'sencha': TeaRecipe('上級煎茶', 2.0, 60, '70 ℃', '1〜2 分',
                        '茶さじ', 2.0),
    'futsu': TeaRecipe('普通煎茶・深蒸し煎茶', 2.0, 90, '80〜90 ℃',
                       '30 秒〜1 分', '茶さじ', 2.0),
    'gyokuro': TeaRecipe('玉露', 3.0, 20, '50〜60 ℃', '2〜2.5 分',
                         '茶さじ', 2.0),
    'bancha': TeaRecipe('番茶・ほうじ茶・玄米茶', 3.0, 130, '熱湯',
                        '30 秒', '大さじ', 3.0),
    'matcha': TeaRecipe('抹茶（薄茶）', 2.0, 70, '80 ℃ 前後',
                        '茶筅で 15〜20 秒点てる', '茶杓', 1.0),
}

MAX_PEOPLE = 10


def calculate(recipe: TeaRecipe, people: int) -> tuple[float, int]:
    """人数分の茶葉の量 [g] とお湯の量 [ml] を返す.

    茶葉の量 W = n × w, お湯の量 V = n × v で求める.
    """
    if not 1 <= people <= MAX_PEOPLE:
        raise ValueError(f'人数は 1〜{MAX_PEOPLE} で指定してください。')
    return recipe.leaf_g * people, recipe.water_ml * people


def format_guide(key: str, people: int) -> str:
    """表示用の文字列を作る."""
    recipe = RECIPES[key]
    leaf_g, water_ml = calculate(recipe, people)
    lines = [
        f'{recipe.name} {people} 人分の目安',
        f'  茶葉の量  : {leaf_g:.1f} g'
        f'（{recipe.spoon}約 {leaf_g / recipe.spoon_g:.1f} 杯）',
        f'  お湯の量  : {water_ml} ml',
        f'  湯温      : {recipe.temperature}',
        f'  浸出時間  : {recipe.steep_time}',
    ]
    return '\n'.join(lines)


def ask_key() -> str:
    """お茶の種類を番号で選んでもらう."""
    keys = list(RECIPES)
    for number, key in enumerate(keys, start=1):
        print(f'  {number}: {RECIPES[key].name}')
    while True:
        answer = input('お茶の種類を番号で選んでください: ').strip()
        if answer.isdigit() and 1 <= int(answer) <= len(keys):
            return keys[int(answer) - 1]
        print('一覧にある番号を入力してください。')


def ask_people() -> int:
    """人数を入力してもらう."""
    while True:
        answer = input(f'人数を入力してください（1〜{MAX_PEOPLE}）: ').strip()
        if answer.isdigit() and 1 <= int(answer) <= MAX_PEOPLE:
            return int(answer)
        print(f'1〜{MAX_PEOPLE} の数字を入力してください。')


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """コマンドライン引数を解析する."""
    parser = argparse.ArgumentParser(
        description='日本茶の淹れ方の目安を表示します。')
    parser.add_argument('tea', nargs='?', choices=list(RECIPES),
                        help='お茶の種類')
    parser.add_argument('people', nargs='?', type=int, help='人数')
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """エントリーポイント."""
    args = parse_args(argv)
    key: str = args.tea if args.tea is not None else ask_key()
    people: int = args.people if args.people is not None else ask_people()
    try:
        print(format_guide(key, people))
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
