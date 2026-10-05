"""第 4 章のサンプル: ch04_before.py の問題を修正したコードです。"""

from typing import TypedDict


class Item(TypedDict):
    """注文明細 1 行分のデータです。"""

    price: int
    qty: int


def calc_total(items: list[Item], tax_rate: float | None = 0.1) -> float:
    """明細の合計金額を計算します。

    Args:
        items: 注文明細のリストです。
        tax_rate: 税率です。None の場合は税を加算しません。

    Returns:
        税込みの合計金額です。
    """
    subtotal = sum(item["price"] * item["qty"] for item in items)
    if tax_rate is None:
        return subtotal
    return subtotal * (1 + tax_rate)


def format_total(total: float) -> str:
    """合計金額を「1,234 円」の形式の文字列にします。"""
    return f"{total:,.0f} 円"
