"""ショッピングカート."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    """商品.

    Attributes:
        name: 商品名。
        price: 単価（円）。
    """

    name: str
    price: int


class Cart:
    """商品と数量を保持するショッピングカート."""

    def __init__(self) -> None:
        self._quantities: dict[Item, int] = {}

    def add(self, item: Item, quantity: int = 1) -> None:
        """商品を追加する（同じ商品は数量を加算する）.

        Raises:
            ValueError: 数量が 1 未満の場合。
        """
        if quantity < 1:
            raise ValueError(f"数量は 1 以上にしてください: {quantity}")
        self._quantities[item] = self._quantities.get(item, 0) + quantity

    def remove(self, item: Item) -> None:
        """商品をカートから取り除く.

        Raises:
            KeyError: 商品がカートにない場合。
        """
        del self._quantities[item]

    def quantity_of(self, item: Item) -> int:
        """商品の数量を返す（カートにない商品は 0 を返す）."""
        return self._quantities.get(item, 0)

    def subtotal(self) -> int:
        """注文金額（単価 × 数量の合計）を返す."""
        return sum(item.price * quantity
                   for item, quantity in self._quantities.items())

    def is_empty(self) -> bool:
        """カートが空なら True を返す."""
        return not self._quantities
