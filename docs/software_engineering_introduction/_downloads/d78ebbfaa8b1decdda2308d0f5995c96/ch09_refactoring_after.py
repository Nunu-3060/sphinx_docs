"""リファクタリング後のコード（第 9 章）.

``ch09_refactoring_before.py`` と同じ結果を出力するが、次の改善を行った。

* 意図が分かる名前に変更した（名前の変更）
* マジックナンバーを名前付き定数に置き換えた
* 計算と表示を別の関数に分けた（関数の抽出）
* 明細をデータクラスで表した
"""

from dataclasses import dataclass

TAX_RATE = 0.10
DISCOUNT_THRESHOLD = 10_000
DISCOUNT_RATE = 0.10


@dataclass(frozen=True)
class LineItem:
    """注文明細の 1 行."""

    name: str
    unit_price: int
    quantity: int

    @property
    def amount(self) -> int:
        """単価と数量から求めた金額."""
        return self.unit_price * self.quantity


def subtotal(items: list[LineItem]) -> int:
    """明細の金額の合計を返す."""
    return sum(item.amount for item in items)


def apply_discount(amount: float) -> float:
    """しきい値以上の金額に割引を適用する."""
    if amount >= DISCOUNT_THRESHOLD:
        return amount * (1 - DISCOUNT_RATE)
    return amount


def total_with_tax(items: list[LineItem]) -> int:
    """割引と消費税を適用した支払額（円未満切り捨て）を返す."""
    return int(apply_discount(subtotal(items)) * (1 + TAX_RATE))


def print_total(items: list[LineItem]) -> None:
    """支払額を表示する."""
    print(f"合計: {total_with_tax(items)} 円")


if __name__ == "__main__":
    print_total([LineItem("ノート", 300, 10), LineItem("ペン", 150, 50)])
