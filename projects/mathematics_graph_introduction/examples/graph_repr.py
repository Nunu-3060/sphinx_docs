"""第 3 章 グラフの表現.

同じ無向グラフを辺リスト・隣接行列・接続行列・隣接リストの 4 通りで表し、
相互に変換する。最後に NetworkX の結果と照合する。

実行方法:
    python graph_repr.py
"""

import networkx as nx
import numpy as np
import numpy.typing as npt

# 頂点を 0, 1, ..., n-1 の整数で表す。
Edge = tuple[int, int]
AdjList = dict[int, list[int]]
IntMatrix = npt.NDArray[np.int64]


def to_adjacency_matrix(n: int, edges: list[Edge]) -> IntMatrix:
    """辺リストから隣接行列を作る。A[u, v] は u と v を結ぶ辺の本数。"""
    a = np.zeros((n, n), dtype=np.int64)
    for u, v in edges:
        a[u, v] += 1
        a[v, u] += 1
    return a


def to_incidence_matrix(n: int, edges: list[Edge]) -> IntMatrix:
    """辺リストから接続行列を作る。B[v, j] は頂点 v が辺 j の端点なら 1。"""
    b = np.zeros((n, len(edges)), dtype=np.int64)
    for j, (u, v) in enumerate(edges):
        b[u, j] = 1
        b[v, j] = 1
    return b


def to_adjacency_list(n: int, edges: list[Edge]) -> AdjList:
    """辺リストから隣接リストを作る。"""
    adj: AdjList = {v: [] for v in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def degrees(adj: AdjList) -> dict[int, int]:
    """隣接リストから各頂点の次数を求める。"""
    return {v: len(neighbors) for v, neighbors in adj.items()}


def main() -> None:
    n = 5
    edges: list[Edge] = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4)]

    a = to_adjacency_matrix(n, edges)
    b = to_incidence_matrix(n, edges)
    adj = to_adjacency_list(n, edges)
    deg = degrees(adj)

    print("隣接行列 A:")
    print(a)
    print("接続行列 B:")
    print(b)
    print("隣接リスト:", adj)
    print("次数:", deg)

    # 握手補題: 次数の総和は辺数の 2 倍
    print("次数の総和 =", sum(deg.values()), " 2|E| =", 2 * len(edges))

    # 隣接行列の行和は次数に等しく、B B^T = D + A が成り立つ
    print("A の行和:", a.sum(axis=1).tolist())
    d = np.diag(a.sum(axis=1))
    print("B B^T == D + A:", bool(np.array_equal(b @ b.T, d + a)))

    # NetworkX との照合
    g: nx.Graph[int] = nx.Graph()
    g.add_nodes_from(range(n))
    g.add_edges_from(edges)
    a_nx = nx.to_numpy_array(g, nodelist=list(range(n)))
    print("NetworkX の隣接行列と一致:", bool(np.array_equal(a, a_nx)))
    print("NetworkX の次数と一致:", dict(g.degree()) == deg)


if __name__ == "__main__":
    main()
