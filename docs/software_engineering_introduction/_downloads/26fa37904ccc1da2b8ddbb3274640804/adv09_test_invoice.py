"""発展課題 9-A の解答例: 仕様化テスト（第 9 章）.

まず ``test_characterization`` で、リファクタリング前の ``inv`` の
現在の出力をそのまま記録した。次に ``test_same_behavior`` で、
リファクタリング後の ``make_invoice`` が同じ出力を返すことを確認する。

実行方法: ``python -m unittest adv09_test_invoice``
"""

import unittest

from adv09_invoice_after import LineItem, make_invoice
from adv09_invoice_before import inv

# (明細, 会員か) の組み合わせ。割引・送料の境界をまたぐように選んだ
CASES: list[tuple[list[tuple[str, int, int]], bool]] = [
    ([], True),
    ([], False),
    ([("ノート", 300, 4), ("ペン", 150, 10)], True),  # 小計 2700
    ([("ノート", 300, 10)], True),  # 小計 3000
    ([("ノート", 300, 10)], False),  # 小計 3000
    ([("かばん", 4999, 1)], False),  # 小計 4999
    ([("かばん", 5000, 1)], False),  # 小計 5000
    ([("ペン", 99, 31)], True),  # 小計 3069、割引後の端数を切り捨て
]


class TestInvoice(unittest.TestCase):
    """請求書の作成のテスト."""

    def test_characterization(self) -> None:
        """リファクタリング前の現在の出力を記録する（仕様化テスト）."""
        self.assertEqual(
            inv([("ノート", 300, 4), ("ペン", 150, 10)], True),
            "ノート x4 = 1200\nペン x10 = 1500\n合計 2700",
        )
        self.assertEqual(inv([("ノート", 300, 10)], True),
                         "ノート x10 = 3000\n合計 2850")
        self.assertEqual(inv([("かばん", 4999, 1)], False),
                         "かばん x1 = 4999\n合計 5499")
        self.assertEqual(inv([], False), "合計 500")

    def test_same_behavior(self) -> None:
        """リファクタリング後も、すべての入力で同じ出力になる."""
        for rows, is_member in CASES:
            items = [LineItem(*row) for row in rows]
            with self.subTest(rows=rows, is_member=is_member):
                self.assertEqual(make_invoice(items, is_member),
                                 inv(rows, is_member))


if __name__ == "__main__":
    unittest.main()
