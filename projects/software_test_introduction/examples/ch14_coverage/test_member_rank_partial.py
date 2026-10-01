"""member_rank の不十分なテスト（カバレッジを計測して不足を見つける）."""

from shop.member import member_rank


def test_gold() -> None:
    assert member_rank(150_000, 5) == "gold"


def test_bronze() -> None:
    assert member_rank(1_000, 1) == "bronze"
