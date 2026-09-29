"""CheckoutService の単体テストです.

3 種類のテストダブルを使います。

* スタブ: 決まった値を返す（時刻を固定した時計）
* スパイ: 呼び出された内容を記録する（SpyReceiptSender）
* モック: 呼び出され方を検証する（unittest.mock.Mock）
"""

import unittest
from datetime import datetime
from unittest.mock import Mock

from .checkout import CheckoutService, ReceiptSender


def fixed_clock(hour: int, minute: int = 0) -> datetime:
    """指定した時刻の datetime を返します（スタブの時計の中身）."""
    return datetime(2026, 4, 1, hour, minute)


class SpyReceiptSender:
    """送信した内容を記録するだけの ReceiptSender です（スパイ）."""

    def __init__(self) -> None:
        self.sent: list[tuple[str, str]] = []

    def send(self, email: str, body: str) -> None:
        self.sent.append((email, body))


class CheckoutServiceTest(unittest.TestCase):
    """CheckoutService のテストです."""

    def make_service(self, hour: int, minute: int = 0,
                     sender: ReceiptSender | None = None) -> CheckoutService:
        """時刻を固定した CheckoutService を作ります."""
        return CheckoutService(sender or SpyReceiptSender(),
                               clock=lambda: fixed_clock(hour, minute))

    def test_no_discount_before_happy_hour(self) -> None:
        service = self.make_service(16, 59)
        self.assertEqual(service.checkout("a@example.com", 1000), 1000)

    def test_discount_at_start_of_happy_hour(self) -> None:
        service = self.make_service(17, 0)
        self.assertEqual(service.checkout("a@example.com", 1000), 900)

    def test_no_discount_at_end_of_happy_hour(self) -> None:
        service = self.make_service(19, 0)
        self.assertEqual(service.checkout("a@example.com", 1000), 1000)

    def test_negative_amount_is_rejected(self) -> None:
        service = self.make_service(12)
        with self.assertRaises(ValueError):
            service.checkout("a@example.com", -1)

    def test_receipt_is_recorded_by_spy(self) -> None:
        sender = SpyReceiptSender()
        service = self.make_service(18, sender=sender)
        service.checkout("a@example.com", 2000)
        self.assertEqual(
            sender.sent,
            [("a@example.com", "お支払い金額は 1,800 円です。")])

    def test_receipt_is_sent_once_with_mock(self) -> None:
        sender = Mock(spec=ReceiptSender)
        service = self.make_service(12, sender=sender)
        service.checkout("a@example.com", 2000)
        sender.send.assert_called_once_with(
            "a@example.com", "お支払い金額は 2,000 円です。")


if __name__ == "__main__":
    unittest.main()
