"""binary_search 関数の単体テスト。"""

import unittest

from binary_search import binary_search


class BinarySearchTest(unittest.TestCase):
    """binary_search 関数の振る舞いを確かめる。"""

    def test_found_in_middle(self) -> None:
        """中ほどにある要素の位置を返す。"""
        self.assertEqual(binary_search([1, 3, 5, 7, 9], 5), 2)

    def test_found_at_both_ends(self) -> None:
        """先頭と末尾の要素の位置を返す。"""
        self.assertEqual(binary_search([1, 3, 5, 7, 9], 1), 0)
        self.assertEqual(binary_search([1, 3, 5, 7, 9], 9), 4)

    def test_not_found(self) -> None:
        """存在しない要素には -1 を返す。"""
        self.assertEqual(binary_search([1, 3, 5, 7, 9], 4), -1)

    def test_empty(self) -> None:
        """空のリストには -1 を返す。"""
        self.assertEqual(binary_search([], 1), -1)


if __name__ == "__main__":
    unittest.main()
