"""注文の状態を管理する."""

from enum import Enum


class OrderStatus(Enum):
    """注文の状態."""

    RECEIVED = "受付済み"
    PAID = "支払い済み"
    SHIPPED = "発送済み"
    DELIVERED = "配達完了"
    CANCELLED = "キャンセル"


class InvalidTransitionError(Exception):
    """許されない状態遷移を要求されたときに送出する例外."""


# 操作ごとに、操作できる状態と操作後の状態を定める
_TRANSITIONS: dict[str, dict[OrderStatus, OrderStatus]] = {
    "pay": {OrderStatus.RECEIVED: OrderStatus.PAID},
    "ship": {OrderStatus.PAID: OrderStatus.SHIPPED},
    "deliver": {OrderStatus.SHIPPED: OrderStatus.DELIVERED},
    "cancel": {
        OrderStatus.RECEIVED: OrderStatus.CANCELLED,
        OrderStatus.PAID: OrderStatus.CANCELLED,
    },
}


class Order:
    """注文（作成直後の状態は「受付済み」である）."""

    def __init__(self) -> None:
        self.status = OrderStatus.RECEIVED

    def pay(self) -> None:
        """支払いを記録する."""
        self._apply("pay")

    def ship(self) -> None:
        """発送を記録する."""
        self._apply("ship")

    def deliver(self) -> None:
        """配達完了を記録する."""
        self._apply("deliver")

    def cancel(self) -> None:
        """注文を取り消す（発送後は取り消せない）."""
        self._apply("cancel")

    def _apply(self, action: str) -> None:
        """操作を適用して状態を進める.

        Raises:
            InvalidTransitionError: 現在の状態ではその操作ができない場合。
        """
        next_status = _TRANSITIONS[action].get(self.status)
        if next_status is None:
            raise InvalidTransitionError(
                f"{self.status.value}の注文には {action} を実行できません")
        self.status = next_status
