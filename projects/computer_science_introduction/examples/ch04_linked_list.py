"""単方向連結リストのサンプル。

先頭への挿入と、位置が分かっているノードの直後への挿入は要素数によらず
一定時間でできる一方、値の探索には先頭から順にたどる必要があることを、
たどったノードの数を数えて確かめる。

実行方法: python ch04_linked_list.py
関連する章: 第 4 章「データ構造」
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Node:
    """連結リストの 1 つの要素（ノード）。値と次のノードへの参照を持つ。"""

    value: int
    next: Node | None = None


class LinkedList:
    """先頭ノードへの参照だけを持つ単方向連結リスト。"""

    def __init__(self) -> None:
        """空のリストを作る。"""
        self.head: Node | None = None
        self.size = 0

    def push_front(self, value: int) -> None:
        """先頭に値を挿入する。要素数によらず O(1) である。"""
        self.head = Node(value, self.head)
        self.size += 1

    def insert_after(self, node: Node, value: int) -> None:
        """指定したノードの直後に値を挿入する。参照の付け替えだけで済む。"""
        node.next = Node(value, node.next)
        self.size += 1

    def find(self, value: int) -> tuple[Node | None, int]:
        """値を探し、見つかったノードと、たどったノードの数を返す。"""
        steps = 0
        node = self.head
        while node is not None:
            steps += 1
            if node.value == value:
                return node, steps
            node = node.next
        return None, steps

    def remove(self, value: int) -> bool:
        """最初に見つかった値を削除する。削除できたら True を返す。"""
        prev: Node | None = None
        node = self.head
        while node is not None:
            if node.value == value:
                # 1 つ前のノードの参照を、削除するノードの次へ付け替える
                if prev is None:
                    self.head = node.next
                else:
                    prev.next = node.next
                self.size -= 1
                return True
            prev, node = node, node.next
        return False

    def __iter__(self) -> Iterator[int]:
        """先頭から順に値を返すイテレータを作る。"""
        node = self.head
        while node is not None:
            yield node.value
            node = node.next


def main() -> None:
    """連結リストの基本操作を実行して結果を表示する。"""
    lst = LinkedList()
    for v in [50, 40, 30, 20, 10]:
        lst.push_front(v)  # 先頭に挿入するので逆順に入れる
    print("初期状態:", list(lst))

    node, steps = lst.find(30)
    print(f"30 の探索: {steps} 個のノードをたどった")
    if node is not None:
        lst.insert_after(node, 35)
    print("30 の直後に 35 を挿入:", list(lst))

    _, steps = lst.find(99)
    print(f"99 の探索: {steps} 個のノードをたどって見つからず")

    lst.remove(10)
    print("先頭の 10 を削除:", list(lst))
    lst.remove(50)
    print("末尾の 50 を削除:", list(lst), "要素数", lst.size)


if __name__ == "__main__":
    main()
