"""ch07_fee.py のテストです。

同値分割と境界値分析で導いたテストケースを、パラメーター化して記述しています。
"""

import pytest

from ch07_fee import admission_fee


@pytest.mark.parametrize(
    ("age", "expected"),
    [
        (0, 0),  # 幼児の下限
        (5, 0),  # 幼児の上限
        (6, 500),  # 子どもの下限
        (12, 500),  # 子どもの上限
        (13, 1000),  # 大人の下限
        (64, 1000),  # 大人の上限
        (65, 700),  # シニアの下限
        (120, 700),  # シニアの上限
    ],
)
def test_valid_age_boundaries(age: int, expected: int) -> None:
    assert admission_fee(age) == expected


@pytest.mark.parametrize("age", [-1, 121])
def test_invalid_age_raises_value_error(age: int) -> None:
    with pytest.raises(ValueError):
        admission_fee(age)
