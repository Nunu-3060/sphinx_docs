"""State パターンの例（状態遷移を表で表す方法との比較）.

注文の状態（下書き → 確定 → 発送済み、または取り消し）に応じて、
できる操作が変わる例です。

* 悪い例: メソッドごとに状態の分岐を書く
* 良い例 1: 状態ごとのクラスに、その状態でできる操作を書く（State パターン）
* 良い例 2: 状態遷移を表（辞書）で表す. Python ではこちらで十分なことも多い

実行方法::

    python ch08_state.py
"""

from enum import Enum


class InvalidTransitionError(Exception):
    """その状態ではできない操作が要求されたときに送出します."""


# ---------------------------------------------------------------------------
# 悪い例: メソッドごとに状態の分岐がある
# ---------------------------------------------------------------------------


class BadOrder:
    """注文（悪い例）."""

    def __init__(self) -> None:
        self.status = "draft"

    def place(self) -> None:
        if self.status == "draft":
            self.status = "placed"
        else:
            raise InvalidTransitionError(f"cannot place: {self.status}")

    def ship(self) -> None:
        if self.status == "placed":
            self.status = "shipped"
        else:
            raise InvalidTransitionError(f"cannot ship: {self.status}")

    def cancel(self) -> None:
        if self.status in ("draft", "placed"):
            self.status = "cancelled"
        else:
            raise InvalidTransitionError(f"cannot cancel: {self.status}")


# ---------------------------------------------------------------------------
# 良い例 1: State パターン
# ---------------------------------------------------------------------------


class OrderState:
    """注文の状態の基底クラスです. 既定では、どの操作もできません."""

    name = "unknown"

    def place(self) -> "OrderState":
        raise InvalidTransitionError(f"cannot place: {self.name}")

    def ship(self) -> "OrderState":
        raise InvalidTransitionError(f"cannot ship: {self.name}")

    def cancel(self) -> "OrderState":
        raise InvalidTransitionError(f"cannot cancel: {self.name}")


class Draft(OrderState):
    name = "draft"

    def place(self) -> OrderState:
        return Placed()

    def cancel(self) -> OrderState:
        return Cancelled()


class Placed(OrderState):
    name = "placed"

    def ship(self) -> OrderState:
        return Shipped()

    def cancel(self) -> OrderState:
        return Cancelled()


class Shipped(OrderState):
    name = "shipped"


class Cancelled(OrderState):
    name = "cancelled"


class Order:
    """注文（State パターン）. 操作を現在の状態オブジェクトに任せます."""

    def __init__(self) -> None:
        self._state: OrderState = Draft()

    @property
    def status(self) -> str:
        return self._state.name

    def place(self) -> None:
        self._state = self._state.place()

    def ship(self) -> None:
        self._state = self._state.ship()

    def cancel(self) -> None:
        self._state = self._state.cancel()


# ---------------------------------------------------------------------------
# 良い例 2: 状態遷移表
# ---------------------------------------------------------------------------


class Status(Enum):
    DRAFT = "draft"
    PLACED = "placed"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"


# (現在の状態, 操作) -> 次の状態
TRANSITIONS: dict[tuple[Status, str], Status] = {
    (Status.DRAFT, "place"): Status.PLACED,
    (Status.DRAFT, "cancel"): Status.CANCELLED,
    (Status.PLACED, "ship"): Status.SHIPPED,
    (Status.PLACED, "cancel"): Status.CANCELLED,
}


def next_status(current: Status, action: str) -> Status:
    """現在の状態と操作から、次の状態を返します."""
    try:
        return TRANSITIONS[(current, action)]
    except KeyError:
        raise InvalidTransitionError(
            f"cannot {action}: {current.value}") from None


def main() -> None:
    """3 つの実装で、同じ操作を順に実行します."""
    orders: list[BadOrder | Order] = [BadOrder(), Order()]
    for order in orders:
        order.place()
        order.ship()
        print(type(order).__name__, order.status)
        try:
            order.cancel()
        except InvalidTransitionError as error:
            print("  エラー:", error)

    status = Status.DRAFT
    for action in ("place", "ship", "cancel"):
        try:
            status = next_status(status, action)
            print("遷移表", action, "->", status.value)
        except InvalidTransitionError as error:
            print("  エラー:", error)


if __name__ == "__main__":
    main()
