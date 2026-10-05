"""演習問題 5-1 の解答例: 段階的な送料の戦略の追加（第 5 章）.

重さ 2 kg までは 400 円、2 kg を超えた分は 1 kg ごとに 200 円を加算する
（1 kg 未満の端数は切り上げる）。``Checkout`` を変更せずに追加できる。
"""

import math

from ch05_strategy import Checkout


class TieredRate:
    """一定の重さまでは定額、超えた分は 1 kg ごとに加算する送料."""

    def __init__(self, base: int, base_kg: float, per_kg: int) -> None:
        self.base = base
        self.base_kg = base_kg
        self.per_kg = per_kg

    def fee(self, weight_kg: float) -> int:
        excess_kg = max(0.0, weight_kg - self.base_kg)
        return self.base + self.per_kg * math.ceil(excess_kg)


if __name__ == "__main__":
    checkout = Checkout(TieredRate(base=400, base_kg=2.0, per_kg=200))
    for weight in (1.5, 2.0, 2.1, 4.5):
        print(f"{weight} kg: {checkout.total(price=3000, weight_kg=weight)} 円")
