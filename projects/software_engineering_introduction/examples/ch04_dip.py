"""依存性逆転の原則の例（第 4 章）.

上位モジュール ``OrderService`` は具体的な通知手段（メールなど）に依存せず、
抽象 ``Notifier`` に依存する。通知手段を差し替えても ``OrderService`` は
変更しなくてよく、テストでは偽物の通知手段を渡せる。
"""

from typing import Protocol


class Notifier(Protocol):
    """通知手段の抽象."""

    def send(self, message: str) -> None:
        """メッセージを送信する."""
        ...


class EmailNotifier:
    """メールで通知する（ここでは画面表示で代用する）."""

    def send(self, message: str) -> None:
        print(f"[メール] {message}")


class RecordingNotifier:
    """送信内容を記録するだけの通知手段（テスト用）."""

    def __init__(self) -> None:
        self.messages: list[str] = []

    def send(self, message: str) -> None:
        self.messages.append(message)


class OrderService:
    """注文を受け付け、通知する."""

    def __init__(self, notifier: Notifier) -> None:
        self.notifier = notifier

    def place_order(self, item: str, quantity: int) -> None:
        """注文を受け付ける."""
        if quantity <= 0:
            raise ValueError("数量は 1 以上を指定すること")
        self.notifier.send(f"{item} を {quantity} 個受け付けた")


if __name__ == "__main__":
    OrderService(EmailNotifier()).place_order("ノート", 3)

    recorder = RecordingNotifier()
    OrderService(recorder).place_order("ペン", 2)
    print(recorder.messages)
