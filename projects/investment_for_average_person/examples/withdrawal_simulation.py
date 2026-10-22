"""資産を運用しながら取り崩す場合の、定額方式と定率方式を比べる。

* 定額方式: 毎年同じ金額を引き出す。受け取る額は安定するが、資産が尽きることがある。
* 定率方式: 毎年、その時点の残高の一定割合を引き出す。資産は尽きにくいが、受け取る額は変動する。

毎年、年初に引き出し、残りを一定の利回りで 1 年間運用したと仮定する。
実際の運用成果は毎年大きく上下するため、この試算は目安である。

使い方の例:
    python withdrawal_simulation.py
    python withdrawal_simulation.py --assets 15000000 --rate 2 --amount 900000 --ratio 4 --years 35
"""

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class YearRecord:
    """ある年の引き出し額と、年末の残高。"""

    year: int
    withdrawal: float
    balance: float


def fixed_amount(assets: float, annual_rate: float, amount: float, years: int) -> list[YearRecord]:
    """定額方式で取り崩したときの各年の記録を返す。残高が足りない年は残高すべてを引き出す。"""
    balance = assets
    records: list[YearRecord] = []
    for year in range(1, years + 1):
        withdrawal = min(amount, balance)
        balance = (balance - withdrawal) * (1.0 + annual_rate)
        records.append(YearRecord(year, withdrawal, balance))
    return records


def fixed_ratio(assets: float, annual_rate: float, ratio: float, years: int) -> list[YearRecord]:
    """定率方式で取り崩したときの各年の記録を返す。"""
    balance = assets
    records: list[YearRecord] = []
    for year in range(1, years + 1):
        withdrawal = balance * ratio
        balance = (balance - withdrawal) * (1.0 + annual_rate)
        records.append(YearRecord(year, withdrawal, balance))
    return records


def main() -> None:
    """コマンドライン引数を読み取り、2 つの方式の結果を並べて表示する。"""
    parser = argparse.ArgumentParser(description="定額方式と定率方式の取り崩しを比べる。")
    parser.add_argument("--assets", type=float, default=20_000_000, help="取り崩し開始時の資産 (円)。既定値は 20000000")
    parser.add_argument("--rate", type=float, default=3.0, help="運用の年率リターン (%%)。既定値は 3")
    parser.add_argument("--amount", type=float, default=1_000_000, help="定額方式で毎年引き出す額 (円)。既定値は 1000000")
    parser.add_argument("--ratio", type=float, default=5.0, help="定率方式で毎年引き出す割合 (%%)。既定値は 5")
    parser.add_argument("--years", type=int, default=30, help="試算する年数。既定値は 30")
    parser.add_argument("--step", type=int, default=5, help="何年ごとに表示するか。既定値は 5")
    args = parser.parse_args()

    rate = args.rate / 100.0
    amount_records = fixed_amount(args.assets, rate, args.amount, args.years)
    ratio_records = fixed_ratio(args.assets, rate, args.ratio / 100.0, args.years)

    print(f"資産 {args.assets:,.0f} 円、年率 {args.rate} % で運用しながら取り崩す試算")
    print(f"定額方式: 毎年 {args.amount:,.0f} 円 / 定率方式: 毎年 残高の {args.ratio} %")
    print(f"{'年':>4} {'定額 引出 (円)':>14} {'定額 残高 (円)':>14} {'定率 引出 (円)':>14} {'定率 残高 (円)':>14}")
    for amount, ratio in zip(amount_records, ratio_records):
        if amount.year % args.step == 0 or amount.year == 1 or amount.year == args.years:
            print(f"{amount.year:>4} {amount.withdrawal:>14,.0f} {amount.balance:>14,.0f} "
                  f"{ratio.withdrawal:>14,.0f} {ratio.balance:>14,.0f}")

    depleted = next((record.year for record in amount_records if record.balance <= 0.0), None)
    if depleted is None:
        print(f"定額方式では、{args.years} 年後も資産が残る。")
    else:
        print(f"定額方式では、{depleted} 年目に資産が尽きる。")


if __name__ == "__main__":
    main()
