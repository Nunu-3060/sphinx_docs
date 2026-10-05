"""演習問題 7-3 の解答例: デシジョンテーブルに基づくテスト（第 7 章）.

デシジョンテーブルの 4 つの規則をそれぞれテストケースとする。
金額は境界値（5000 円と 4999 円）を用いる。
実行方法: ``python -m unittest ex07_test_shipping``
"""

import unittest

from ex07_shipping import is_free_shipping


class TestIsFreeShipping(unittest.TestCase):
    """``is_free_shipping`` のテスト."""

    def test_decision_table(self) -> None:
        """デシジョンテーブルの各規則を確認する."""
        rules = [
            # (会員か, 購入金額, 期待される結果)
            (True, 5000, True),  # 規則 1
            (True, 4999, False),  # 規則 2
            (False, 5000, False),  # 規則 3
            (False, 4999, False),  # 規則 4
        ]
        for is_member, amount, expected in rules:
            with self.subTest(is_member=is_member, amount=amount):
                self.assertEqual(is_free_shipping(is_member, amount),
                                 expected)


if __name__ == "__main__":
    unittest.main()
