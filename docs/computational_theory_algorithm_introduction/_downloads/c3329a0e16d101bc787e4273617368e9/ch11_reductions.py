"""第 11 章: 3-SAT からクリーク問題への多項式時間還元。

k 個の節を持つ 3-CNF 式 φ から、次のグラフ G を作る。

* 頂点: 各節の各リテラルの出現 (節の番号, リテラル)。
* 辺: 異なる節に属し、かつ互いに矛盾しない (x と ¬x でない) 2 頂点を結ぶ。

このとき「φ が充足可能」と「G がサイズ k のクリークを持つ」は同値である。
main() では、小さな式について両者の答えが一致することを総当たりで確かめる。

実行例::

    python ch11_reductions.py
"""

from __future__ import annotations

from itertools import combinations, product

CNF = list[list[int]]
Vertex = tuple[int, int]  # (節の番号, リテラル)


def reduce_3sat_to_clique(
    cnf: CNF,
) -> tuple[list[Vertex], set[frozenset[Vertex]], int]:
    """3-CNF 式から (頂点のリスト, 辺の集合, クリークのサイズ k) を作る。"""
    vertices = [(i, lit) for i, clause in enumerate(cnf) for lit in clause]
    edges: set[frozenset[Vertex]] = set()
    for (i, a), (j, b) in combinations(vertices, 2):
        if i != j and a != -b:
            edges.add(frozenset({(i, a), (j, b)}))
    return vertices, edges, len(cnf)


def has_clique(
    vertices: list[Vertex], edges: set[frozenset[Vertex]], k: int
) -> bool:
    """サイズ k のクリークがあるかを総当たりで調べる。"""
    return any(
        all(frozenset({u, v}) in edges for u, v in combinations(group, 2))
        for group in combinations(vertices, k)
    )


def is_satisfiable(cnf: CNF) -> bool:
    """全ての割り当てを試して充足可能性を判定する。"""
    names = sorted({abs(lit) for clause in cnf for lit in clause})
    for values in product([False, True], repeat=len(names)):
        a = dict(zip(names, values))
        if all(any(a[abs(lit)] == (lit > 0) for lit in c) for c in cnf):
            return True
    return False


def main() -> None:
    examples: list[CNF] = [
        [[1, 2, 3], [-1, -2, 3], [1, -2, -3]],
        [[1, 1, 1], [-1, -1, -1]],  # x1 ∧ ¬x1 と同じで充足不能
        [[1, 2, 2], [-1, 2, 2], [1, -2, -2], [-1, -2, -2]],
    ]
    for cnf in examples:
        vertices, edges, k = reduce_3sat_to_clique(cnf)
        sat = is_satisfiable(cnf)
        clique = has_clique(vertices, edges, k)
        print(f"{cnf}\n  頂点 {len(vertices)}, 辺 {len(edges)}, k = {k}:"
              f" 充足可能 {sat}, クリークあり {clique}")


if __name__ == "__main__":
    main()
