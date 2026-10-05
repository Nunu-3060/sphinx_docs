"""第 4 章: Union-Find (素集合データ構造)。

要素を互いに素な集合に分け、次の 2 つの操作を高速に行う。

* union(x, y): x を含む集合と y を含む集合を合併する。
* same(x, y): x と y が同じ集合に属するかを判定する。

経路圧縮と、小さい木を大きい木の下につなぐ工夫 (union by size) により、
1 操作あたりの償却計算量はほぼ定数 (逆アッカーマン関数) になる。

実行例::

    python ch04_union_find.py
"""

from __future__ import annotations


class UnionFind:
    """要素 0, 1, ..., n - 1 を扱う Union-Find。"""

    def __init__(self, n: int) -> None:
        # parent[x] は x の親。根では parent[x] == x となる。
        self.parent = list(range(n))
        # size[r] は根 r を持つ木の要素数 (根以外では意味を持たない)。
        self.size = [1] * n

    def find(self, x: int) -> int:
        """x を含む木の根を返す。途中の要素は根に直接つなぎ直す。"""
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:  # 経路圧縮
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, x: int, y: int) -> bool:
        """x と y の集合を合併する。既に同じ集合なら False を返す。"""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.size[rx] < self.size[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx  # 小さい木を大きい木の下につなぐ
        self.size[rx] += self.size[ry]
        return True

    def same(self, x: int, y: int) -> bool:
        """x と y が同じ集合に属するなら True を返す。"""
        return self.find(x) == self.find(y)


def main() -> None:
    uf = UnionFind(6)
    for x, y in [(0, 1), (1, 2), (3, 4)]:
        uf.union(x, y)
        print(f"union({x}, {y})")
    print("same(0, 2) =", uf.same(0, 2))  # True
    print("same(0, 3) =", uf.same(0, 3))  # False
    print("same(3, 4) =", uf.same(3, 4))  # True
    print("same(5, 5) =", uf.same(5, 5))  # True


if __name__ == "__main__":
    main()
