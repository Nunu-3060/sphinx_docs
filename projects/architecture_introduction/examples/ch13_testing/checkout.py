"""会計の処理です.

17 時から 19 時の間は 10% 割引し、会計が済んだら領収書をメールで送ります。
"""

from collections.abc import Callable
from datetime import datetime, time
from typing import Protocol

HAPPY_HOUR_START = time(17, 0)
HAPPY_HOUR_END = time(19, 0)
HAPPY_HOUR_DISCOUNT_RATE = 0.1

# ---------------------------------------------------------------------------
# テストしにくい実装
# ---------------------------------------------------------------------------


def hard_to_test_checkout(email: str, amount: int) -> int:
    """会計を行い、支払額を返します（テストしにくい例）.

    現在時刻を直接取得し、メールの送信も直接行う（ここでは表示で代用）
    ため、テストの結果が実行する時刻によって変わり、送信内容も確認できません。
    """
    now = datetime.now().time()
    if HAPPY_HOUR_START <= now < HAPPY_HOUR_END:
        amount = int(amount * (1 - HAPPY_HOUR_DISCOUNT_RATE))
    print(f"[mail] to={email}: お支払い金額は {amount:,} 円です。")
    return amount


# ---------------------------------------------------------------------------
# テストしやすい実装
# ---------------------------------------------------------------------------


class ReceiptSender(Protocol):
    """領収書の送信先のインターフェースです."""

    def send(self, email: str, body: str) -> None:
        ...


class CheckoutService:
    """会計のサービスです. 時計と領収書の送信先を外から受け取ります."""

    def __init__(self, sender: ReceiptSender,
                 clock: Callable[[], datetime] = datetime.now) -> None:
        self._sender = sender
        self._clock = clock

    def is_happy_hour(self) -> bool:
        """現在が割引の時間帯かどうかを返します."""
        return HAPPY_HOUR_START <= self._clock().time() < HAPPY_HOUR_END

    def checkout(self, email: str, amount: int) -> int:
        """会計を行い、支払額を返します."""
        if amount < 0:
            raise ValueError(f"amount must not be negative: {amount}")
        if self.is_happy_hour():
            amount = int(amount * (1 - HAPPY_HOUR_DISCOUNT_RATE))
        self._sender.send(email, f"お支払い金額は {amount:,} 円です。")
        return amount
