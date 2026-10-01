"""4 章で設計した注文の状態遷移テストを実装する."""

import pytest

from shop.order import InvalidTransitionError, Order, OrderStatus

ACTIONS = ["pay", "ship", "deliver", "cancel"]

# 状態遷移表の有効な遷移: (遷移前の状態, 操作) -> 遷移後の状態
VALID_TRANSITIONS = {
    (OrderStatus.RECEIVED, "pay"): OrderStatus.PAID,
    (OrderStatus.PAID, "ship"): OrderStatus.SHIPPED,
    (OrderStatus.SHIPPED, "deliver"): OrderStatus.DELIVERED,
    (OrderStatus.RECEIVED, "cancel"): OrderStatus.CANCELLED,
    (OrderStatus.PAID, "cancel"): OrderStatus.CANCELLED,
}

# 状態遷移表で「－」（遷移なし）とした、残りのすべての組み合わせ
INVALID_TRANSITIONS = [
    (status, action)
    for status in OrderStatus
    for action in ACTIONS
    if (status, action) not in VALID_TRANSITIONS
]

# 各状態に到達するための操作の列
PATHS: dict[OrderStatus, list[str]] = {
    OrderStatus.RECEIVED: [],
    OrderStatus.PAID: ["pay"],
    OrderStatus.SHIPPED: ["pay", "ship"],
    OrderStatus.DELIVERED: ["pay", "ship", "deliver"],
    OrderStatus.CANCELLED: ["cancel"],
}


def make_order(status: OrderStatus) -> Order:
    """指定した状態の注文を、正しい順序で操作して作る."""
    order = Order()
    for action in PATHS[status]:
        getattr(order, action)()
    assert order.status is status
    return order


def test_new_order_is_received() -> None:
    assert Order().status is OrderStatus.RECEIVED


@pytest.mark.parametrize(
    ("status", "action", "expected"),
    [(s, a, e) for (s, a), e in VALID_TRANSITIONS.items()],
)
def test_valid_transition(status: OrderStatus, action: str,
                          expected: OrderStatus) -> None:
    order = make_order(status)
    getattr(order, action)()
    assert order.status is expected


@pytest.mark.parametrize(("status", "action"), INVALID_TRANSITIONS)
def test_invalid_transition(status: OrderStatus, action: str) -> None:
    order = make_order(status)
    with pytest.raises(InvalidTransitionError):
        getattr(order, action)()
    assert order.status is status  # 状態は変わらない
