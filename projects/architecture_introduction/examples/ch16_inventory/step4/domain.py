"""ドメイン: 商品と在庫の規則と、リポジトリのインターフェースです.

ほかのモジュールに依存しません。
"""

from dataclasses import dataclass
from typing import Protocol

REORDER_POINT = 5  # 在庫がこの数を下回ったら発注する


class InventoryError(Exception):
    """在庫の規則に反する操作をしたときに送出します."""


@dataclass
class Item:
    """在庫を管理する商品です."""

    sku: str
    name: str
    quantity: int = 0

    def __post_init__(self) -> None:
        if not self.sku or not self.name:
            raise InventoryError("商品コードと商品名は必須です")
        if self.quantity < 0:
            raise InventoryError("在庫の数は 0 以上です")

    @property
    def needs_reorder(self) -> bool:
        """発注が必要かどうかを返します."""
        return self.quantity < REORDER_POINT

    def receive(self, quantity: int) -> None:
        """入庫します."""
        _check_positive(quantity)
        self.quantity += quantity

    def ship(self, quantity: int) -> None:
        """出庫します."""
        _check_positive(quantity)
        if self.quantity < quantity:
            raise InventoryError(
                f"{self.sku} の在庫が足りません"
                f"（在庫 {self.quantity} 個、出庫 {quantity} 個）")
        self.quantity -= quantity


def _check_positive(quantity: int) -> None:
    if quantity <= 0:
        raise InventoryError("数量は 1 以上です")


class ItemRepository(Protocol):
    """商品のリポジトリのインターフェースです."""

    def get(self, sku: str) -> Item | None:
        """商品コードに一致する商品を返します. なければ None を返します."""
        ...

    def save(self, item: Item) -> None:
        """商品を保存します（同じ商品コードがあれば上書きします）."""
        ...

    def list_all(self) -> list[Item]:
        """すべての商品を商品コードの順に返します."""
        ...
