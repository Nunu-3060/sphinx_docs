"""リファクタリングの前後で出力が変わらないことを確かめるテストです.

リファクタリングを始める前に、現在の振る舞いを記録するテスト（仕様化
テスト）を用意します。境界の値（10000 円の前後）や、税率の異なる明細を
含めて、さまざまな入力を試します。
"""

import unittest
from typing import Any

from . import after, before

CUSTOMERS: list[dict[str, str]] = [
    {"name": "佐藤", "rank": "regular"},
    {"name": "鈴木", "rank": "gold"},
]

ITEM_SETS: list[list[dict[str, Any]]] = [
    [],
    [{"name": "りんご", "type": "food", "price": 120, "qty": 3}],
    [{"name": "りんご", "type": "food", "price": 120, "qty": 3},
     {"name": "ノート", "type": "goods", "price": 250, "qty": 2}],
    # ゴールド会員の割引後に 10000 円をわずかに超える / 超えない
    [{"name": "椅子", "type": "goods", "price": 9570, "qty": 1}],
    [{"name": "椅子", "type": "goods", "price": 9569, "qty": 1}],
    [{"name": "米", "type": "food", "price": 4999, "qty": 3},
     {"name": "机", "type": "goods", "price": 33333, "qty": 1}],
]


class InvoiceCharacterizationTest(unittest.TestCase):
    """before と after の出力を比較します."""

    def test_same_output(self) -> None:
        for customer in CUSTOMERS:
            for items in ITEM_SETS:
                for ja in (True, False):
                    with self.subTest(customer=customer["name"],
                                      items=len(items), ja=ja):
                        self.assertEqual(
                            before.make_invoice(customer, items, ja),
                            after.make_invoice(customer, items, ja))

    def test_known_output(self) -> None:
        items = ITEM_SETS[2]
        self.assertEqual(
            after.format_invoice_ja(
                after.Customer("佐藤", "regular"),
                [after.LineItem(i["name"], i["type"], i["price"], i["qty"])
                 for i in items]),
            "佐藤 様\nりんご x3 388\nノート x2 550\n合計: 938 円")


if __name__ == "__main__":
    unittest.main()
