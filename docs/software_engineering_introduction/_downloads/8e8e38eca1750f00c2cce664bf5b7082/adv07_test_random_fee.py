"""発展課題 7-A の解答例: ランダムな入力によるテスト（第 7 章）.

仕様の表から期待値を求める単純な関数（テストオラクル）を用意し、
ランダムに選んだ多数の年齢について ``admission_fee`` の結果と比較する。
乱数の種を固定しているため、失敗した場合も同じ入力で再現できる。

実行方法: ``python -m unittest adv07_test_random_fee``
"""

import random
import unittest

from ch07_boundary import admission_fee

# (最小年齢, 最大年齢, 料金) の表。仕様をそのまま書き写したもの
FEE_TABLE = [
    (0, 5, 0),
    (6, 12, 500),
    (13, 64, 1000),
    (65, 150, 700),
]


def expected_fee(age: int) -> int:
    """仕様の表から期待される料金を求める（テストオラクル）."""
    for low, high, fee in FEE_TABLE:
        if low <= age <= high:
            return fee
    raise ValueError(f"表の範囲外の年齢: {age}")


class TestAdmissionFeeRandom(unittest.TestCase):
    """ランダムな入力による ``admission_fee`` のテスト."""

    def test_random_ages(self) -> None:
        """0 歳から 150 歳までのランダムな 1000 件で期待値と一致する."""
        rng = random.Random(20261005)
        for _ in range(1000):
            age = rng.randint(0, 150)
            with self.subTest(age=age):
                self.assertEqual(admission_fee(age), expected_fee(age))

    def test_random_negative_ages(self) -> None:
        """負の年齢では常に ValueError が送出される."""
        rng = random.Random(20261005)
        for _ in range(100):
            age = rng.randint(-1000, -1)
            with self.subTest(age=age):
                with self.assertRaises(ValueError):
                    admission_fee(age)


if __name__ == "__main__":
    unittest.main()
