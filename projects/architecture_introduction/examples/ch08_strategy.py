"""Strategy パターンの例.

割引の計算方法（戦略）を、利用する側から切り替えられるようにします。
クラスで実装する方法と、Python の関数で実装する方法を示します。

実行方法::

    python ch08_strategy.py
"""

from collections.abc import Callable
from typing import Protocol

# ---------------------------------------------------------------------------
# クラスによる実装
# ---------------------------------------------------------------------------


class DiscountStrategy(Protocol):
    """割引の計算方法のインターフェースです."""

    def apply(self, price: int) -> int:
        """割引後の価格を返します."""
        ...


class NoDiscount:
    """割引しません."""

    def apply(self, price: int) -> int:
        return price


class RateDiscount:
    """一定の割合で割り引きます."""

    def __init__(self, rate: float) -> None:
        self._rate = rate

    def apply(self, price: int) -> int:
        return int(price * (1 - self._rate))


class FixedDiscount:
    """一定の金額を割り引きます（0 円未満にはしません）."""

    def __init__(self, amount: int) -> None:
        self._amount = amount

    def apply(self, price: int) -> int:
        return max(price - self._amount, 0)


class Checkout:
    """会計です. 割引の計算方法を外から受け取ります."""

    def __init__(self, strategy: DiscountStrategy) -> None:
        self._strategy = strategy

    def total(self, prices: list[int]) -> int:
        """割引後の合計金額を返します."""
        return self._strategy.apply(sum(prices))


# ---------------------------------------------------------------------------
# 関数による実装: 戦略が 1 つのメソッドだけなら、関数で十分です
# ---------------------------------------------------------------------------

Discount = Callable[[int], int]


def no_discount(price: int) -> int:
    """割引しません."""
    return price


def rate_discount(rate: float) -> Discount:
    """一定の割合で割り引く関数を返します."""
    def apply(price: int) -> int:
        return int(price * (1 - rate))
    return apply


def checkout_total(prices: list[int], discount: Discount) -> int:
    """割引後の合計金額を返します."""
    return discount(sum(prices))


def main() -> None:
    """同じ会計を、異なる割引の計算方法で実行します."""
    prices = [1200, 800, 3000]
    strategies: dict[str, DiscountStrategy] = {
        "割引なし": NoDiscount(),
        "10% 割引": RateDiscount(0.1),
        "500 円引き": FixedDiscount(500),
    }
    for name, strategy in strategies.items():
        print(f"クラス版 {name}: {Checkout(strategy).total(prices)}")

    print("関数版 割引なし:", checkout_total(prices, no_discount))
    print("関数版 10% 割引:", checkout_total(prices, rate_discount(0.1)))


if __name__ == "__main__":
    main()
