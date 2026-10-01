"""浮動小数点数を pytest.approx で比較する."""

import pytest


def test_float_sum_is_not_exact() -> None:
    # 0.1 や 0.2 は 2 進数で正確に表せないため、== では一致しない
    assert 0.1 + 0.2 != 0.3


def test_float_sum_with_approx() -> None:
    assert 0.1 + 0.2 == pytest.approx(0.3)


def test_approx_with_tolerance() -> None:
    measured = [9.98, 20.01]
    assert measured == pytest.approx([10.0, 20.0], abs=0.05)
