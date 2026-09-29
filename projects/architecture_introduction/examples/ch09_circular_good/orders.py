"""注文を表すモジュール. customers だけに依存します."""

from dataclasses import dataclass

from .customers import Customer


@dataclass(frozen=True)
class Order:
    """注文です."""

    order_id: str
    amount: int
    customer: Customer

    def label(self) -> str:
        """表示用のラベルを返します."""
        return f"{self.order_id}（{self.customer.name} 様）"
