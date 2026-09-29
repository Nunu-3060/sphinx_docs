"""請求書を作る処理（リファクタリング後）.

before.py と同じ出力を返します。次の手順で書き換えました。

1. マジックナンバーを名前付きの定数にする
2. 重複した小計の計算を 1 か所にまとめる
3. 辞書をデータクラス（Customer, LineItem）に置き換える
4. 明細の計算、会員の特典、整形を別々の関数に抽出する
5. フラグ引数をやめ、言語ごとの関数に分ける

端数の扱い（int による切り捨て）や計算の順序も、元のコードのままに
しています。これらを変えると、出力が変わる可能性があるからです。
振る舞いを変える修正は、リファクタリングとは別の変更として行います。
"""

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

REDUCED_TAX_RATE = 0.08  # 食品に適用する軽減税率
STANDARD_TAX_RATE = 0.1
REDUCED_TAX_TYPES = frozenset({"food"})

GOLD_DISCOUNT_FACTOR = 0.95  # ゴールド会員は 5% 引き
GOLD_BONUS_THRESHOLD = 10000  # この金額を超えると、さらに値引きする
GOLD_BONUS = 500


@dataclass(frozen=True)
class Customer:
    """請求先の顧客です."""

    name: str
    rank: str

    @property
    def is_gold(self) -> bool:
        return self.rank == "gold"


@dataclass(frozen=True)
class LineItem:
    """請求書の明細です."""

    name: str
    item_type: str
    price: int
    quantity: int

    @property
    def subtotal(self) -> int:
        """税抜きの小計を返します."""
        return self.price * self.quantity

    @property
    def tax(self) -> float:
        """消費税額を返します."""
        rate = (REDUCED_TAX_RATE if self.item_type in REDUCED_TAX_TYPES
                else STANDARD_TAX_RATE)
        return self.subtotal * rate

    @property
    def total(self) -> float:
        """税込みの金額を返します."""
        return self.subtotal + self.tax


def apply_member_benefits(amount: float, customer: Customer) -> float:
    """会員の特典を適用した金額を返します."""
    if not customer.is_gold:
        return amount
    amount = amount * GOLD_DISCOUNT_FACTOR
    if amount > GOLD_BONUS_THRESHOLD:
        amount = amount - GOLD_BONUS
    return amount


def invoice_total(customer: Customer, items: Iterable[LineItem]) -> int:
    """請求額を返します."""
    amount = 0.0
    for item in items:
        amount += item.total
    return int(apply_member_benefits(amount, customer))


def _format_lines(items: Iterable[LineItem]) -> str:
    return "".join(f"{item.name} x{item.quantity} {int(item.total)}\n"
                   for item in items)


def format_invoice_ja(customer: Customer, items: list[LineItem]) -> str:
    """日本語の請求書を返します."""
    total = invoice_total(customer, items)
    return f"{customer.name} 様\n{_format_lines(items)}合計: {total} 円"


def format_invoice_en(customer: Customer, items: list[LineItem]) -> str:
    """英語の請求書を返します."""
    total = invoice_total(customer, items)
    return f"Dear {customer.name}\n{_format_lines(items)}Total: {total} JPY"


def make_invoice(customer: dict[str, str], items: list[dict[str, Any]],
                 ja: bool) -> str:
    """元の関数と同じ呼び出し方を残すための関数です.

    呼び出し側をすべて format_invoice_ja と format_invoice_en に移行したら
    削除します。
    """
    converted_customer = Customer(customer["name"], customer["rank"])
    converted_items = [LineItem(i["name"], i["type"], i["price"], i["qty"])
                       for i in items]
    if ja:
        return format_invoice_ja(converted_customer, converted_items)
    return format_invoice_en(converted_customer, converted_items)
