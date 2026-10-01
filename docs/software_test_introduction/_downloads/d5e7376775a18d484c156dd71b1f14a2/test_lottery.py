"""unittest.mock.patch で乱数を差し替えて、抽選をテストする."""

from unittest.mock import patch

import pytest

import lottery


def test_win() -> None:
    # lottery.py は from random import random としているため、
    # random モジュールではなく lottery モジュールの名前 random を差し替える
    with patch("lottery.random", return_value=0.05):
        assert lottery.draw_coupon() == "SAVE10"


def test_lose() -> None:
    with patch("lottery.random", return_value=0.5):
        assert lottery.draw_coupon() is None


def test_boundary_is_lose(monkeypatch: pytest.MonkeyPatch) -> None:
    # monkeypatch.setattr でも同じように差し替えられる
    monkeypatch.setattr(lottery, "random", lambda: 0.1)
    assert lottery.draw_coupon() is None
