"""テストしやすい書き方の例（改善後）."""

import random
from collections.abc import Callable
from datetime import date
from typing import TextIO

YEAR_END_SALE_RATE = 0.2
"""年末セール（12 月 20 日から 31 日まで）の割引率."""

CODE_CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZ"
"""クーポンコードに使う文字（見間違えやすい I と O を除く）."""


def discount_rate(today: date) -> float:
    """指定した日の割引率を返す（純粋関数）."""
    if today.month == 12 and today.day >= 20:
        return YEAR_END_SALE_RATE
    return 0.0


def make_coupon_code(rng: random.Random, length: int = 6) -> str:
    """乱数生成器を受け取り、クーポンコードを作る."""
    return "".join(rng.choice(CODE_CHARS) for _ in range(length))


def format_announcement(rate: float, code: str) -> str:
    """告知文を組み立てる（純粋関数）."""
    return f"本日の割引率: {rate:.0%}\nクーポンコード: {code}\n"


class Campaign:
    """時刻・乱数・出力先を外から差し替えられる、告知を行うクラス."""

    def __init__(self, clock: Callable[[], date] = date.today,
                 rng: random.Random | None = None) -> None:
        self._clock = clock
        self._rng = rng if rng is not None else random.Random()

    def announce(self, out: TextIO) -> None:
        """告知文を out に書き出す."""
        rate = discount_rate(self._clock())
        code = make_coupon_code(self._rng)
        out.write(format_announcement(rate, code))
