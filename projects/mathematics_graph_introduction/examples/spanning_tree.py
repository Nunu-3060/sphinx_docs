"""第 6 章 木と全域木.

Union-Find、クラスカル法、プリム法で最小全域木を求める。
また、プリューファー符号で木と数列を相互に変換し、ケイリーの公式を確かめる。

実行方法:
    python spanning_tree.py
"""

import heapq
import itertools
from collections import Counter

import networkx as nx

# 重み付き辺 (重み, 端点 u, 端点 v)
WeightedEdge = tuple[float, int, int]


class UnionFind:
    """互いに素な集合を管理するデータ構造（経路圧縮とランクによる併合付き）。"""

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        """x が属する集合の代表元を返す。"""
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # 経路圧縮（経路半分化）
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> bool:
        """x と y の集合を併合する。既に同じ集合なら False を返す。"""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


def kruskal(n: int, edges: list[WeightedEdge]) -> list[WeightedEdge]:
    """クラスカル法: 重みの小さい辺から順に、閉路を作らないものを採用する。"""
    uf = UnionFind(n)
    tree: list[WeightedEdge] = []
    for w, u, v in sorted(edges):
        if uf.union(u, v):
            tree.append((w, u, v))
            if len(tree) == n - 1:
                break
    return tree


def prim(n: int, edges: list[WeightedEdge], root: int = 0) -> list[WeightedEdge]:
    """プリム法: 木に含まれる頂点集合から外へ出る最小の辺を繰り返し採用する。"""
    adj: dict[int, list[tuple[float, int]]] = {v: [] for v in range(n)}
    for w, u, v in edges:
        adj[u].append((w, v))
        adj[v].append((w, u))
    in_tree = {root}
    heap = [(w, root, v) for w, v in adj[root]]
    heapq.heapify(heap)
    tree: list[WeightedEdge] = []
    while heap and len(in_tree) < n:
        w, u, v = heapq.heappop(heap)
        if v in in_tree:
            continue
        in_tree.add(v)
        tree.append((w, u, v))
        for w2, x in adj[v]:
            if x not in in_tree:
                heapq.heappush(heap, (w2, v, x))
    return tree


def prufer_encode(n: int, tree_edges: list[tuple[int, int]]) -> list[int]:
    """頂点 0..n-1 の木をプリューファー符号（長さ n-2 の数列）に変換する。"""
    adj: dict[int, set[int]] = {v: set() for v in range(n)}
    for u, v in tree_edges:
        adj[u].add(v)
        adj[v].add(u)
    code: list[int] = []
    for _ in range(n - 2):
        leaf = min(v for v in adj if len(adj[v]) == 1)  # 番号最小の葉
        neighbor = adj[leaf].pop()
        code.append(neighbor)
        adj[neighbor].discard(leaf)
        del adj[leaf]
    return code


def prufer_decode(code: list[int]) -> list[tuple[int, int]]:
    """プリューファー符号から木の辺リストを復元する。"""
    n = len(code) + 2
    remaining = Counter(code)  # 残りの符号に各頂点が何回現れるか
    edges: list[tuple[int, int]] = []
    used: set[int] = set()
    for x in code:
        leaf = min(v for v in range(n) if v not in used and remaining[v] == 0)
        edges.append((leaf, x))
        used.add(leaf)
        remaining[x] -= 1
    u, v = (w for w in range(n) if w not in used)
    edges.append((u, v))
    return edges


def main() -> None:
    n = 6
    edges: list[WeightedEdge] = [
        (7, 0, 1), (5, 0, 3), (8, 1, 2), (9, 1, 3), (7, 1, 4),
        (5, 2, 4), (15, 3, 4), (6, 3, 5), (8, 4, 5), (11, 2, 5),
    ]
    tk = kruskal(n, edges)
    tp = prim(n, edges)
    print("クラスカル法:", tk, "重み合計 =", sum(w for w, _, _ in tk))
    print("プリム法    :", tp, "重み合計 =", sum(w for w, _, _ in tp))

    g: nx.Graph[int] = nx.Graph()
    for w, u, v in edges:
        g.add_edge(u, v, weight=w)
    mst = nx.minimum_spanning_tree(g)
    print("NetworkX    : 重み合計 =", mst.size(weight="weight"))

    # プリューファー符号の往復変換
    tree = [(0, 3), (1, 3), (2, 3), (3, 4), (4, 5)]
    code = prufer_encode(6, tree)
    print("プリューファー符号:", code)
    print("復元した木:", sorted(tuple(sorted(e)) for e in prufer_decode(code)))

    # ケイリーの公式: 頂点数 n のラベル付き木は n^(n-2) 個
    # 長さ n-2 の数列すべてを復元し、異なる木が n^(n-2) 個得られることを確かめる
    for m in range(2, 7):
        trees = {frozenset(frozenset(e) for e in prufer_decode(list(c)))
                 for c in itertools.product(range(m), repeat=m - 2)}
        print(f"n = {m}: 木の個数 = {len(trees)}, n^(n-2) = {m ** (m - 2)}")


if __name__ == "__main__":
    main()
