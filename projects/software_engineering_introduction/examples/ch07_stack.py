"""テスト駆動開発で作成したスタック（第 7 章）.

``ch07_test_stack.py`` のテストを 1 つずつ追加し、
テストが通る最小限のコードを書く、という手順を繰り返して作成した。
"""

from typing import Generic, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    """後入れ先出し（LIFO）のスタック."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def is_empty(self) -> bool:
        """スタックが空なら True を返す."""
        return not self._items

    def push(self, item: T) -> None:
        """要素を積む."""
        self._items.append(item)

    def pop(self) -> T:
        """最後に積んだ要素を取り出す。空なら IndexError を送出する."""
        if self.is_empty():
            raise IndexError("空のスタックからは取り出せない")
        return self._items.pop()

    def __len__(self) -> int:
        return len(self._items)


if __name__ == "__main__":
    stack: Stack[int] = Stack()
    for number in (1, 2, 3):
        stack.push(number)
    while not stack.is_empty():
        print(stack.pop())
