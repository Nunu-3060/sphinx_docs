"""演習問題 7-4 の解答例: スタックへの peek メソッドの追加（第 7 章）.

``ex07_test_stack_peek.py`` のテストを先に書き、失敗することを確認してから
実装した。元の ``ch07_stack.Stack`` を継承し、``peek`` だけを追加している。
"""

from typing import TypeVar

from ch07_stack import Stack

T = TypeVar("T")


class PeekableStack(Stack[T]):
    """最後に積んだ要素を、取り出さずに参照できるスタック."""

    def peek(self) -> T:
        """最後に積んだ要素を返す（取り出さない）。空なら IndexError を送出する."""
        if self.is_empty():
            raise IndexError("空のスタックは参照できない")
        return self._items[-1]


if __name__ == "__main__":
    stack: PeekableStack[str] = PeekableStack()
    stack.push("a")
    stack.push("b")
    print(stack.peek(), len(stack))
