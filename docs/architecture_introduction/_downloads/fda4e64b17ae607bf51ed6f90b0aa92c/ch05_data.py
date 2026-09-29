"""データの設計の例.

辞書で持ち回っていた注文のデータを、次の型に置き換えます。

* Money: 金額を表す不変の値オブジェクト
* OrderStatus: 注文の状態を表す列挙型
* Order: 注文を表すデータクラス

実行方法::

    python ch05_data.py
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

# ---------------------------------------------------------------------------
# 悪い例: 辞書で持ち回る
# ---------------------------------------------------------------------------


def bad_order_total(order: dict[str, Any]) -> int:
    """注文の合計金額を返します（悪い例）.

    キーの名前や値の型は、辞書を作った箇所を読まないと分かりません。
    キーの綴りを誤っても、実行するまで気付けません。
    """
    total = 0
    for line in order["lines"]:
        total += line["price"] * line["qty"]
    return total


# ---------------------------------------------------------------------------
# 良い例: 型を定義する
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Money:
    """金額を表す値オブジェクトです.

    負の金額を作れないようにし、通貨の異なる金額どうしの計算を禁止します。
    """

    amount: int
    currency: str = "JPY"

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError(f"amount must not be negative: {self.amount}")

    def __add__(self, other: "Money") -> "Money":
        self._check_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, times: int) -> "Money":
        return Money(self.amount * times, self.currency)

    def _check_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError(
                f"currency mismatch: {self.currency} and {other.currency}"
            )

    def __str__(self) -> str:
        return f"{self.amount:,} {self.currency}"


class OrderStatus(Enum):
    """注文の状態です."""

    DRAFT = "draft"
    PLACED = "placed"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class OrderLine:
    """注文の明細です."""

    product: str
    unit_price: Money
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError(f"quantity must be positive: {self.quantity}")

    @property
    def subtotal(self) -> Money:
        """小計を返します."""
        return self.unit_price * self.quantity


@dataclass
class Order:
    """注文です."""

    order_id: str
    lines: list[OrderLine] = field(default_factory=list)
    status: OrderStatus = OrderStatus.DRAFT

    @property
    def total(self) -> Money:
        """合計金額を返します."""
        result = Money(0)
        for line in self.lines:
            result = result + line.subtotal
        return result


def main() -> None:
    """悪い例と良い例で合計金額を求めます."""
    raw_order: dict[str, Any] = {
        "id": "A-001",
        "lines": [{"price": 120, "qty": 3}, {"price": 300, "qty": 1}],
        "status": "draft",
    }
    print("悪い例:", bad_order_total(raw_order))

    order = Order(
        "A-001",
        [
            OrderLine("apple", Money(120), 3),
            OrderLine("coffee", Money(300), 1),
        ],
    )
    print("良い例:", order.total, order.status)

    try:
        OrderLine("apple", Money(120), 0)
    except ValueError as error:
        print("不正な明細は作れません:", error)


if __name__ == "__main__":
    main()
