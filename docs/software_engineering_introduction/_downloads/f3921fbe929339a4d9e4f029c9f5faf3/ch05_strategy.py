"""Strategy パターンの例（第 5 章）.

送料の計算方法（戦略）をクラスとして切り出し、実行時に差し替えられるようにする。
新しい計算方法を追加するときは、既存のコードを変更せずに
新しいクラスを追加するだけでよい（開放閉鎖の原則）。
"""

from typing import Protocol


class ShippingStrategy(Protocol):
    """送料の計算方法の抽象."""

    def fee(self, weight_kg: float) -> int:
        """重さ ``weight_kg`` の荷物の送料（円）を返す."""
        ...


class FlatRate:
    """重さに関係なく一律の送料."""

    def __init__(self, amount: int) -> None:
        self.amount = amount

    def fee(self, weight_kg: float) -> int:
        return self.amount


class WeightBased:
    """基本料金に 1 kg ごとの料金を加算する."""

    def __init__(self, base: int, per_kg: int) -> None:
        self.base = base
        self.per_kg = per_kg

    def fee(self, weight_kg: float) -> int:
        return self.base + round(self.per_kg * weight_kg)


class Checkout:
    """会計処理。送料の計算は戦略オブジェクトに任せる."""

    def __init__(self, strategy: ShippingStrategy) -> None:
        self.strategy = strategy

    def total(self, price: int, weight_kg: float) -> int:
        """商品価格と送料の合計を返す."""
        return price + self.strategy.fee(weight_kg)


if __name__ == "__main__":
    for strategy in (FlatRate(500), WeightBased(300, 100)):
        checkout = Checkout(strategy)
        name = type(strategy).__name__
        print(f"{name}: {checkout.total(price=3000, weight_kg=2.5)} 円")
