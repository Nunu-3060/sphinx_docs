"""二分探索木のサンプル。

挿入・探索・中間順の走査を実装し、同じ値の集合でも挿入する順序によって
木の高さが大きく変わることを示す。整列済みの順に挿入すると木は一直線に
なり、探索が連結リストと同じ O(n) になる。

実行方法: python ch04_bst.py
関連する章: 第 4 章「データ構造」
"""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass
class TreeNode:
    """二分探索木のノード。左の子孫は key より小さく、右の子孫は大きい。"""

    key: int
    left: TreeNode | None = None
    right: TreeNode | None = None


class BinarySearchTree:
    """重複しない整数のキーを格納する（平衡化しない）二分探索木。"""

    def __init__(self) -> None:
        """空の木を作る。"""
        self.root: TreeNode | None = None

    def insert(self, key: int) -> None:
        """キーを挿入する。根から比較しながら下り、空いた位置に置く。"""
        if self.root is None:
            self.root = TreeNode(key)
            return
        node = self.root
        while True:
            if key < node.key:
                if node.left is None:
                    node.left = TreeNode(key)
                    return
                node = node.left
            elif key > node.key:
                if node.right is None:
                    node.right = TreeNode(key)
                    return
                node = node.right
            else:
                return  # 既にあるキーは挿入しない

    def search(self, key: int) -> int:
        """キーを探し、比較したノードの数を返す（見つからなければ負の値）。"""
        node = self.root
        visited = 0
        while node is not None:
            visited += 1
            if key == node.key:
                return visited
            node = node.left if key < node.key else node.right
        return -visited

    def inorder(self) -> list[int]:
        """中間順（左の子孫、自分、右の子孫）に走査したキーの列を返す。"""
        result: list[int] = []
        stack: list[TreeNode] = []
        node = self.root
        while stack or node is not None:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            result.append(node.key)
            node = node.right
        return result

    def height(self) -> int:
        """木の高さ（根から最も深い葉までのノード数）を返す。"""
        best = 0
        stack: list[tuple[TreeNode | None, int]] = [(self.root, 1)]
        while stack:
            node, depth = stack.pop()
            if node is not None:
                best = max(best, depth)
                stack.append((node.left, depth + 1))
                stack.append((node.right, depth + 1))
        return best


def build(keys: list[int]) -> BinarySearchTree:
    """キーを与えられた順に挿入した木を作る。"""
    tree = BinarySearchTree()
    for k in keys:
        tree.insert(k)
    return tree


def main() -> None:
    """挿入順による木の形の違いを表示する。"""
    small = build([50, 30, 70, 20, 40, 60, 80])
    print("中間順の走査:", small.inorder())
    print("60 の探索で比較したノード数:", small.search(60))

    n = 1023
    shuffled = list(range(1, n + 1))
    random.seed(1)
    random.shuffle(shuffled)
    cases = [("ランダムな順", shuffled),
             ("整列済みの順", list(range(1, n + 1)))]
    for label, keys in cases:
        tree = build(keys)
        total = sum(tree.search(k) for k in range(1, n + 1))
        print(f"{label}に {n} 個挿入: 高さ {tree.height()}, "
              f"探索で比較するノード数の平均 {total / n:.1f}")


if __name__ == "__main__":
    main()
