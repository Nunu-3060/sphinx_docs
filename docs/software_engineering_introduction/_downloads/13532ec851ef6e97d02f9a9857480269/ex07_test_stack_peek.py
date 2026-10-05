"""演習問題 7-4 の解答例: peek メソッドのテスト（第 7 章）.

実行方法: ``python -m unittest ex07_test_stack_peek``
"""

import unittest

from ex07_stack_peek import PeekableStack


class TestPeek(unittest.TestCase):
    """``PeekableStack.peek`` のテスト."""

    def setUp(self) -> None:
        self.stack: PeekableStack[str] = PeekableStack()

    def test_peek_returns_last_pushed_item(self) -> None:
        """最後に積んだ要素を返す."""
        self.stack.push("a")
        self.stack.push("b")
        self.assertEqual(self.stack.peek(), "b")

    def test_peek_does_not_remove_item(self) -> None:
        """peek しても要素の数は変わらない."""
        self.stack.push("a")
        self.stack.peek()
        self.assertEqual(len(self.stack), 1)

    def test_peek_on_empty_stack_raises(self) -> None:
        """空のスタックでは IndexError が送出される."""
        with self.assertRaises(IndexError):
            self.stack.peek()


if __name__ == "__main__":
    unittest.main()
