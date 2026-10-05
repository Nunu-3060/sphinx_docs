"""スタックのテスト（第 7 章、テスト駆動開発の例）.

テストメソッドは TDD で追加した順に並べている。
実行方法: ``python -m unittest ch07_test_stack``
"""

import unittest

from ch07_stack import Stack


class TestStack(unittest.TestCase):
    """``Stack`` のテスト."""

    def setUp(self) -> None:
        self.stack: Stack[str] = Stack()

    def test_new_stack_is_empty(self) -> None:
        """作成直後のスタックは空である."""
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(len(self.stack), 0)

    def test_push_makes_stack_not_empty(self) -> None:
        """要素を積むと空ではなくなる."""
        self.stack.push("a")
        self.assertFalse(self.stack.is_empty())
        self.assertEqual(len(self.stack), 1)

    def test_pop_returns_last_pushed_item(self) -> None:
        """最後に積んだ要素から順に取り出される."""
        self.stack.push("a")
        self.stack.push("b")
        self.assertEqual(self.stack.pop(), "b")
        self.assertEqual(self.stack.pop(), "a")

    def test_pop_from_empty_stack_raises(self) -> None:
        """空のスタックから取り出すと IndexError が送出される."""
        with self.assertRaises(IndexError):
            self.stack.pop()


if __name__ == "__main__":
    unittest.main()
