"""毎月の積立投資の結果を試算する。

毎月同じ金額を積み立て、一定の利回りで運用できたと仮定したときの、
各年末の元本・残高・運用益を表にして表示する。

実際の運用成果は毎年大きく上下する。この試算は「平均してこの利回りだった場合」の目安であり、
将来の成果を約束するものではない。

使い方の例:
    python accumulation_simulation.py
    python accumulation_simulation.py --monthly 30000 --rate 4 --years 20 --cost 0.2
"""

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class YearResult:
    """ある年の年末時点の状態。"""

    year: int
    principal: float
    balance: float

    @property
    def gain(self) -> float:
        """運用益 (残高から元本を引いた額)。"""
        return self.balance - self.principal


def simulate(monthly: float, annual_rate: float, years: int, annual_cost: float = 0.0) -> list[YearResult]:
    """積立投資を試算し、各年末の結果を返す。

    Args:
        monthly: 毎月の積立額 (円)。
        annual_rate: コストを引く前の年率リターン (例: 年 5 % なら 0.05)。
        years: 積立期間 (年)。
        annual_cost: 信託報酬などの年率コスト (例: 年 0.1 % なら 0.001)。

    Returns:
        1 年目から years 年目までの年末の結果。
    """
    # 年率を月率に直す (月ごとに複利で増えると考える)
    monthly_rate = (1.0 + annual_rate - annual_cost) ** (1.0 / 12.0) - 1.0
    balance = 0.0
    results: list[YearResult] = []
    for year in range(1, years + 1):
        for _ in range(12):
            # 月初に積み立て、その月の運用成果を加える
            balance = (balance + monthly) * (1.0 + monthly_rate)
        results.append(YearResult(year, monthly * 12 * year, balance))
    return results


def print_table(results: list[YearResult], step: int) -> None:
    """結果を表として表示する。step 年ごとと最終年を表示する。"""
    print(f"{'年':>4} {'元本 (円)':>14} {'残高 (円)':>14} {'運用益 (円)':>14}")
    for result in results:
        if result.year % step == 0 or result.year == len(results):
            print(f"{result.year:>4} {result.principal:>14,.0f} {result.balance:>14,.0f} {result.gain:>14,.0f}")


def main() -> None:
    """コマンドライン引数を読み取り、試算結果を表示する。"""
    parser = argparse.ArgumentParser(description="毎月の積立投資の結果を試算する。")
    parser.add_argument("--monthly", type=float, default=30000, help="毎月の積立額 (円)。既定値は 30000")
    parser.add_argument("--rate", type=float, default=5.0, help="コストを引く前の年率リターン (%%)。既定値は 5")
    parser.add_argument("--cost", type=float, default=0.1, help="信託報酬などの年率コスト (%%)。既定値は 0.1")
    parser.add_argument("--years", type=int, default=30, help="積立期間 (年)。既定値は 30")
    parser.add_argument("--step", type=int, default=5, help="何年ごとに表示するか。既定値は 5")
    args = parser.parse_args()

    results = simulate(args.monthly, args.rate / 100.0, args.years, args.cost / 100.0)
    print(f"毎月 {args.monthly:,.0f} 円、年率 {args.rate} % (コスト {args.cost} %)、{args.years} 年間の試算")
    print_table(results, args.step)


if __name__ == "__main__":
    main()
