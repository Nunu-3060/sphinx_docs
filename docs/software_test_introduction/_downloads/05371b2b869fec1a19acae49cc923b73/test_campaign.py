"""改善後の campaign モジュールをテストする."""

import io
import random
from datetime import date

import pytest

from campaign import (CODE_CHARS, Campaign, discount_rate,
                      format_announcement, make_coupon_code)


@pytest.mark.parametrize(
    ("today", "expected"),
    [
        (date(2026, 12, 19), 0.0),  # セール開始の前日
        (date(2026, 12, 20), 0.2),  # セール初日
        (date(2026, 12, 31), 0.2),  # セール最終日
        (date(2027, 1, 1), 0.0),    # セール終了の翌日
    ],
)
def test_discount_rate(today: date, expected: float) -> None:
    assert discount_rate(today) == expected


def test_coupon_code_is_reproducible_with_seed() -> None:
    # 同じシードの乱数生成器からは同じコードが得られる
    first = make_coupon_code(random.Random(42))
    second = make_coupon_code(random.Random(42))
    assert first == second


def test_coupon_code_uses_allowed_chars() -> None:
    code = make_coupon_code(random.Random(0), length=100)
    assert len(code) == 100
    assert set(code) <= set(CODE_CHARS)


def test_format_announcement() -> None:
    assert format_announcement(0.2, "ABCDEF") == (
        "本日の割引率: 20%\nクーポンコード: ABCDEF\n")


def test_announce_writes_to_given_stream() -> None:
    campaign = Campaign(clock=lambda: date(2026, 12, 24),
                        rng=random.Random(42))
    out = io.StringIO()

    campaign.announce(out)

    expected_code = make_coupon_code(random.Random(42))
    assert out.getvalue() == format_announcement(0.2, expected_code)
