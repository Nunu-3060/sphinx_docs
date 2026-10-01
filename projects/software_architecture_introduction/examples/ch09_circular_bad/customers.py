"""顧客を表すモジュール（悪い例）."""

from dataclasses import dataclass, field

from .orders import Order  # orders も customers を import している


@dataclass
class Customer:
    """顧客です. 自分の注文の一覧を持ちます."""

    name: str
    orders: list[Order] = field(default_factory=list)

    def total_spent(self) -> int:
        """これまでの注文の合計金額を返します."""
        return sum(order.amount for order in self.orders)
