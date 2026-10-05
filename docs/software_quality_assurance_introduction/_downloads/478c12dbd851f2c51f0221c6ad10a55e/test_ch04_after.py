"""ch04_after.py のテストです。"""

from ch04_after import Item, calc_total, format_total


def test_calc_total_adds_tax() -> None:
    items: list[Item] = [{"price": 100, "qty": 2}, {"price": 300, "qty": 1}]
    assert calc_total(items, tax_rate=0.1) == 550


def test_calc_total_without_tax() -> None:
    items: list[Item] = [{"price": 100, "qty": 2}]
    assert calc_total(items, tax_rate=None) == 200


def test_format_total() -> None:
    assert format_total(1234.0) == "1,234 円"
