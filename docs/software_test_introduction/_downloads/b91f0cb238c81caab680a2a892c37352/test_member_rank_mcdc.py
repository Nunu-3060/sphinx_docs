"""5 章で設計した MC/DC を満たすテストケースで member_rank をテストする.

条件 A: total_purchase >= 100_000、条件 B: years >= 3
条件 C: total_purchase >= 50_000、条件 D: years >= 5
"""

import pytest

from shop.member import member_rank


@pytest.mark.parametrize(
    ("total_purchase", "years", "expected"),
    [
        pytest.param(120_000, 3, "gold", id="1: A=T B=T"),
        pytest.param(80_000, 3, "silver", id="2: A=F B=T C=T D=F"),
        pytest.param(120_000, 2, "silver", id="3: A=T B=F C=T D=F"),
        pytest.param(10_000, 6, "silver", id="4: A=F B=T C=F D=T"),
        pytest.param(10_000, 1, "bronze", id="5: A=F B=F C=F D=F"),
    ],
)
def test_member_rank_mcdc(total_purchase: int, years: int,
                          expected: str) -> None:
    assert member_rank(total_purchase, years) == expected
