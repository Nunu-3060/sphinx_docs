"""4 章で設計した送料計算のテストケースを parametrize で実装する."""

import pytest

from shop.shipping import calc_shipping_fee


@pytest.mark.parametrize(
    ("subtotal", "expected"),
    [
        (0, 500),     # 有効な同値クラスの下限
        (4999, 500),  # 送料無料になる直前
        (5000, 0),    # 送料無料になる境界
    ],
)
def test_boundary_for_regular_member(subtotal: int, expected: int) -> None:
    assert calc_shipping_fee(subtotal, is_premium=False,
                             is_remote=False) == expected


@pytest.mark.parametrize(
    ("subtotal", "expected"),
    [
        (2999, 500),  # 送料無料になる直前
        (3000, 0),    # 送料無料になる境界
    ],
)
def test_boundary_for_premium_member(subtotal: int, expected: int) -> None:
    assert calc_shipping_fee(subtotal, is_premium=True,
                             is_remote=False) == expected


def test_negative_subtotal_raises_value_error() -> None:
    # 無効な同値クラスの上限（境界の直前）
    with pytest.raises(ValueError):
        calc_shipping_fee(-1, is_premium=False, is_remote=False)


# デシジョンテーブルの 8 つの規則。id でテスト名に規則の番号を付ける
@pytest.mark.parametrize(
    ("is_premium", "subtotal", "is_remote", "expected"),
    [
        pytest.param(False, 4000, False, 500, id="rule1"),
        pytest.param(False, 4000, True, 1500, id="rule2"),
        pytest.param(False, 6000, False, 0, id="rule3"),
        pytest.param(False, 6000, True, 1000, id="rule4"),
        pytest.param(True, 2000, False, 500, id="rule5"),
        pytest.param(True, 2000, True, 1500, id="rule6"),
        pytest.param(True, 4000, False, 0, id="rule7"),
        pytest.param(True, 4000, True, 1000, id="rule8"),
    ],
)
def test_decision_table(is_premium: bool, subtotal: int, is_remote: bool,
                        expected: int) -> None:
    assert calc_shipping_fee(subtotal, is_premium, is_remote) == expected
