"""注文のドメインモデルです."""

from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from typing import Protocol

MAX_LINES = 10


class DomainError(Exception):
    """ドメインの規則に反する操作をしたときに送出します."""


# ---------------------------------------------------------------------------
# 値オブジェクト
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Money:
    """金額（円）を表す値オブジェクトです."""

    amount: int

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise DomainError(f"金額は 0 以上です: {self.amount}")

    def __add__(self, other: "Money") -> "Money":
        return Money(self.amount + other.amount)

    def __mul__(self, times: int) -> "Money":
        return Money(self.amount * times)

    def __str__(self) -> str:
        return f"{self.amount:,} 円"


@dataclass(frozen=True)
class OrderLine:
    """注文の明細を表す値オブジェクトです."""

    product_id: str
    unit_price: Money
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise DomainError(f"数量は 1 以上です: {self.quantity}")

    @property
    def subtotal(self) -> Money:
        """小計を返します."""
        return self.unit_price * self.quantity


class OrderStatus(Enum):
    """注文の状態です."""

    DRAFT = "draft"
    PLACED = "placed"
    CANCELLED = "cancelled"


# ---------------------------------------------------------------------------
# エンティティ（集約ルート）
# ---------------------------------------------------------------------------


class Order:
    """注文です. 明細を含む集約のルートです.

    明細の追加や状態の変更は、必ずこのクラスのメソッドを通して行います。
    これにより、次の規則（不変条件）を常に守ります。

    * 明細を変更できるのは、下書きの状態のときだけ
    * 明細は最大 MAX_LINES 行（同じ商品は 1 行にまとめる）
    * 明細のない注文は確定できない
    """

    def __init__(self, order_id: str, customer_id: str) -> None:
        self._order_id = order_id
        self._customer_id = customer_id
        self._lines: list[OrderLine] = []
        self._status = OrderStatus.DRAFT

    @classmethod
    def restore(cls, order_id: str, customer_id: str, status: OrderStatus,
                lines: Iterable[OrderLine]) -> "Order":
        """保存されていたデータから注文を復元します（リポジトリ用）."""
        order = cls(order_id, customer_id)
        order._lines = list(lines)
        order._status = status
        return order

    @property
    def order_id(self) -> str:
        return self._order_id

    @property
    def customer_id(self) -> str:
        return self._customer_id

    @property
    def status(self) -> OrderStatus:
        return self._status

    @property
    def lines(self) -> tuple[OrderLine, ...]:
        """明細を返します. タプルなので、外から書き換えられません."""
        return tuple(self._lines)

    @property
    def total(self) -> Money:
        """合計金額を返します."""
        result = Money(0)
        for line in self._lines:
            result = result + line.subtotal
        return result

    def add_line(self, product_id: str, unit_price: Money,
                 quantity: int) -> None:
        """明細を追加します. 同じ商品があれば数量を加算します."""
        self._ensure_draft()
        for index, line in enumerate(self._lines):
            if line.product_id == product_id:
                self._lines[index] = OrderLine(
                    product_id, unit_price, line.quantity + quantity)
                return
        if len(self._lines) >= MAX_LINES:
            raise DomainError(f"明細は {MAX_LINES} 行までです")
        self._lines.append(OrderLine(product_id, unit_price, quantity))

    def place(self) -> None:
        """注文を確定します."""
        self._ensure_draft()
        if not self._lines:
            raise DomainError("明細のない注文は確定できません")
        self._status = OrderStatus.PLACED

    def cancel(self) -> None:
        """注文を取り消します."""
        if self._status is OrderStatus.CANCELLED:
            raise DomainError("注文は取り消し済みです")
        self._status = OrderStatus.CANCELLED

    def _ensure_draft(self) -> None:
        if self._status is not OrderStatus.DRAFT:
            raise DomainError(
                f"状態が {self._status.value} の注文は変更できません")

    # エンティティは、属性の値ではなく ID で同一かどうかを判断する
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Order) and other.order_id == self.order_id

    def __hash__(self) -> int:
        return hash(self._order_id)


# ---------------------------------------------------------------------------
# ドメインサービス
# ---------------------------------------------------------------------------

FREE_SHIPPING_THRESHOLD = Money(5000)
SHIPPING_FEES = {"local": Money(500), "remote": Money(1200)}


def shipping_fee(order: Order, region: str) -> Money:
    """注文と配送先の地域から送料を求めます.

    送料の規則は注文そのものの性質ではなく配送の方針なので、Order の
    メソッドにはせず、ドメインサービスとして独立させます。
    """
    if region not in SHIPPING_FEES:
        raise DomainError(f"配送できない地域です: {region}")
    if order.total.amount >= FREE_SHIPPING_THRESHOLD.amount:
        return Money(0)
    return SHIPPING_FEES[region]


# ---------------------------------------------------------------------------
# リポジトリのインターフェース（実装は repository モジュールにあります）
# ---------------------------------------------------------------------------


class OrderRepository(Protocol):
    """注文のリポジトリのインターフェースです."""

    def next_id(self) -> str:
        """新しい注文の ID を返します."""
        ...

    def save(self, order: Order) -> None:
        """注文を保存します（同じ ID があれば上書きします）."""
        ...

    def get(self, order_id: str) -> Order | None:
        """ID に一致する注文を返します. なければ None を返します."""
        ...
