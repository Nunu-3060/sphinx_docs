"""運用コスト (信託報酬など) の違いが最終的な残高に与える影響を比べる。

同じ金額を同じ期間積み立て、コストを引く前の利回りも同じだと仮定し、
年率コストだけを変えたときの最終残高を比べる。

使い方の例:
    python cost_comparison.py
    python cost_comparison.py --monthly 50000 --years 20 --costs 0.1 0.5 1.0 2.0
"""

import argparse

from accumulation_simulation import simulate


def compare(monthly: float, annual_rate: float, years: int, costs: list[float]) -> list[tuple[float, float]]:
    """コストごとの最終残高を計算する。

    Args:
        monthly: 毎月の積立額 (円)。
        annual_rate: コストを引く前の年率リターン (例: 年 5 % なら 0.05)。
        years: 積立期間 (年)。
        costs: 比べる年率コストのリスト (例: 年 0.1 % なら 0.001)。

    Returns:
        (年率コスト, 最終残高) の組のリスト。
    """
    return [(cost, simulate(monthly, annual_rate, years, cost)[-1].balance) for cost in costs]


def main() -> None:
    """コマンドライン引数を読み取り、比較結果を表示する。"""
    parser = argparse.ArgumentParser(description="運用コストの違いによる最終残高の差を比べる。")
    parser.add_argument("--monthly", type=float, default=30000, help="毎月の積立額 (円)。既定値は 30000")
    parser.add_argument("--rate", type=float, default=5.0, help="コストを引く前の年率リターン (%%)。既定値は 5")
    parser.add_argument("--years", type=int, default=30, help="積立期間 (年)。既定値は 30")
    parser.add_argument("--costs", type=float, nargs="+", default=[0.1, 0.8, 1.5],
                        help="比べる年率コスト (%%)。複数指定できる。既定値は 0.1 0.8 1.5")
    args = parser.parse_args()

    costs = [cost / 100.0 for cost in args.costs]
    results = compare(args.monthly, args.rate / 100.0, args.years, costs)
    lowest = results[0][1] if results else 0.0
    print(f"毎月 {args.monthly:,.0f} 円、コスト控除前の年率 {args.rate} %、{args.years} 年間の比較")
    print(f"{'年率コスト':>10} {'最終残高 (円)':>16} {'最初の行との差 (円)':>20}")
    for cost, balance in results:
        print(f"{cost * 100:>9.2f}% {balance:>16,.0f} {balance - lowest:>20,.0f}")


if __name__ == "__main__":
    main()
