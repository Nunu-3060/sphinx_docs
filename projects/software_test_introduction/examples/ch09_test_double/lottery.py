"""購入者に抽選でクーポンを配る."""

from random import random

WIN_PROBABILITY = 0.1
"""当選確率."""


def draw_coupon() -> str | None:
    """抽選を行い、当選したらクーポンコードを、外れたら None を返す."""
    if random() < WIN_PROBABILITY:
        return "SAVE10"
    return None
