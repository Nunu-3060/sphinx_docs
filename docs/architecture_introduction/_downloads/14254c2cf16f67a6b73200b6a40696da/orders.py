"""注文を表すモジュール（悪い例）."""

from dataclasses import dataclass

from .customers import Customer  # customers も orders を import している


@dataclass
class Order:
    """注文です. 注文した顧客を持ちます."""

    order_id: str
    amount: int
    customer: Customer

    def label(self) -> str:
        """表示用のラベルを返します."""
        return f"{self.order_id}（{self.customer.name} 様）"
