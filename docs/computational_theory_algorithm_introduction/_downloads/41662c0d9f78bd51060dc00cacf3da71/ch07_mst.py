"""第 7 章: 最小全域木 (クラスカル法とプリム法)。

無向グラフを辺のリスト (重み, 頂点, 頂点) で与え、
2 つの方法で求めた最小全域木の重みの合計が一致することを確かめる。

実行例::

    python ch07_mst.py
"""

from __future__ import annotations

import heapq

Edge = tuple[int, str, str]


def kruskal(vertices: list[str], edges: list[Edge]) -> list[Edge]:
    """重みの小さい辺から、閉路を作らないものを採用する。O(E log E)。"""
    parent = {v: v for v in vertices}

    def find(x: str) -> str:  # 簡易版 Union-Find (経路半減)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    tree: list[Edge] = []
    for w, u, v in sorted(edges):
        ru, rv = find(u), find(v)
        if ru != rv:  # 別々の木をつなぐ辺なら閉路はできない
            parent[ru] = rv
            tree.append((w, u, v))
    return tree


def prim(vertices: list[str], edges: list[Edge]) -> list[Edge]:
    """1 頂点から木を育て、木と外を結ぶ最小の辺を加える。O(E log V)。"""
    adjacent: dict[str, list[tuple[int, str]]] = {v: [] for v in vertices}
    for w, u, v in edges:
        adjacent[u].append((w, v))
        adjacent[v].append((w, u))
    start = vertices[0]
    in_tree = {start}
    heap = [(w, start, v) for w, v in adjacent[start]]
    heapq.heapify(heap)
    tree: list[Edge] = []
    while heap and len(in_tree) < len(vertices):
        w, u, v = heapq.heappop(heap)
        if v in in_tree:
            continue
        in_tree.add(v)
        tree.append((w, u, v))
        for w2, x in adjacent[v]:
            if x not in in_tree:
                heapq.heappush(heap, (w2, v, x))
    return tree


def main() -> None:
    vertices = ["A", "B", "C", "D", "E"]
    edges: list[Edge] = [
        (1, "A", "B"), (3, "A", "C"), (4, "B", "C"), (2, "B", "D"),
        (5, "C", "D"), (6, "C", "E"), (7, "D", "E"),
    ]
    for name, algorithm in (("クラスカル法", kruskal), ("プリム法", prim)):
        tree = algorithm(vertices, edges)
        total = sum(w for w, _, _ in tree)
        print(f"{name}: 重み {total}, 辺 {[(u, v) for _, u, v in tree]}")


if __name__ == "__main__":
    main()
