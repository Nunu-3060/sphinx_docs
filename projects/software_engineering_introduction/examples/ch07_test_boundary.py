"""境界値分析に基づくテスト（第 7 章）.

各同値クラスの境界の両側の値をテストする。
実行方法: ``python -m unittest ch07_test_boundary``
"""

import unittest

from ch07_boundary import admission_fee


class TestAdmissionFee(unittest.TestCase):
    """``admission_fee`` のテスト."""

    def test_boundaries(self) -> None:
        """境界値とその隣の値で料金が正しいことを確認する."""
        cases = [
            (0, 0),
            (5, 0),
            (6, 500),
            (12, 500),
            (13, 1000),
            (64, 1000),
            (65, 700),
        ]
        for age, expected in cases:
            with self.subTest(age=age):
                self.assertEqual(admission_fee(age), expected)

    def test_negative_age(self) -> None:
        """負の年齢では ValueError が送出されることを確認する."""
        with self.assertRaises(ValueError):
            admission_fee(-1)


if __name__ == "__main__":
    unittest.main()
