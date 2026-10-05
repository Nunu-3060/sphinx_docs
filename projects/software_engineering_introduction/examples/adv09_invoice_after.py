"""発展課題 9-A の解答例: リファクタリング後の請求書の作成（第 9 章）.

``adv09_invoice_before.py`` の ``inv`` と同じ文字列を返す。
仕様（会員割引と送料）を名前付きの定数と関数で表した。
"""

from dataclasses import dataclass

MEMBER_DISCOUNT_THRESHOLD = 3000
MEMBER_DISCOUNT_PERCENT = 5
FREE_SHIPPING_THRESHOLD = 5000
SHIPPING_FEE = 500


@dataclass(frozen=True)
class LineItem:
    """請求明細の 1 行."""

    name: str
    unit_price: int
    quantity: int

    @property
    def amount(self) -> int:
        """単価と数量から求めた金額."""
        return self.unit_price * self.quantity

    def to_line(self) -> str:
        """明細を 1 行の文字列にする."""
        return f"{self.name} x{self.quantity} = {self.amount}"


def billed_amount(subtotal: int, is_member: bool) -> int:
    """小計に会員割引または送料を適用した請求額を返す.

    会員は小計がしきい値以上なら割引される（送料は常に無料）。
    非会員は小計がしきい値未満なら送料がかかる。
    """
    if is_member:
        if subtotal >= MEMBER_DISCOUNT_THRESHOLD:
            return subtotal * (100 - MEMBER_DISCOUNT_PERCENT) // 100
        return subtotal
    if subtotal < FREE_SHIPPING_THRESHOLD:
        return subtotal + SHIPPING_FEE
    return subtotal


def make_invoice(items: list[LineItem], is_member: bool) -> str:
    """請求書の文字列を返す."""
    subtotal = sum(item.amount for item in items)
    lines = [item.to_line() for item in items]
    lines.append(f"合計 {billed_amount(subtotal, is_member)}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(make_invoice([LineItem("ノート", 300, 4), LineItem("ペン", 150, 10)],
                       is_member=True))
