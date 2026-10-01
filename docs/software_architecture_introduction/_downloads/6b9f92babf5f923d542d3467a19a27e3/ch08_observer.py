"""Observer パターンの例.

注文の確定という出来事（イベント）を、関心のある複数の処理に通知します。
通知する側（EventBus）は、通知を受ける側の具体的な処理を知りません。
処理の追加や削除は、登録する関数を変えるだけで済みます。

実行方法::

    python ch08_observer.py
"""

from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class OrderPlaced:
    """注文が確定したというイベントです."""

    order_id: str
    email: str
    amount: int


Handler = Callable[[OrderPlaced], None]


class EventBus:
    """イベントの購読と通知を受け持ちます."""

    def __init__(self) -> None:
        self._handlers: defaultdict[type, list[Handler]] = defaultdict(list)

    def subscribe(self, event_type: type, handler: Handler) -> None:
        """event_type のイベントが発生したときに呼ぶ関数を登録します."""
        self._handlers[event_type].append(handler)

    def publish(self, event: OrderPlaced) -> None:
        """登録された関数を、登録した順に呼び出します."""
        for handler in self._handlers[type(event)]:
            handler(event)


def send_confirmation(event: OrderPlaced) -> None:
    """確認メールを送ります（ここでは表示するだけ）."""
    print(f"[mail] {event.email} に注文 {event.order_id} の確認を送信")


def add_points(event: OrderPlaced) -> None:
    """ポイントを付与します."""
    print(f"[point] {event.amount // 100} ポイントを付与")


def main() -> None:
    """注文の確定を、登録した 2 つの処理に通知します."""
    bus = EventBus()
    bus.subscribe(OrderPlaced, send_confirmation)
    bus.subscribe(OrderPlaced, add_points)
    bus.publish(OrderPlaced("A-001", "sato@example.com", 4500))


if __name__ == "__main__":
    main()
