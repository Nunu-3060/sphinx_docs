"""第 4 章 道と連結性 / 第 5 章 さまざまなグラフ.

連結成分、距離と直径、二部グラフの判定、切断点と橋を求める。
最後に NetworkX の結果と照合する。

実行方法:
    python connectivity.py
"""

from collections import deque
from typing import cast

import networkx as nx

AdjList = dict[int, list[int]]


def build(n: int, edges: list[tuple[int, int]]) -> AdjList:
    """辺リストから無向グラフの隣接リストを作る。"""
    adj: AdjList = {v: [] for v in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def bfs_distances(adj: AdjList, source: int) -> dict[int, int]:
    """source から到達できる各頂点までの距離（辺の本数）を幅優先探索で求める。"""
    dist = {source: 0}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist


def connected_components(adj: AdjList) -> list[set[int]]:
    """連結成分を頂点集合のリストとして返す。"""
    seen: set[int] = set()
    components: list[set[int]] = []
    for v in adj:
        if v not in seen:
            component = set(bfs_distances(adj, v))
            seen |= component
            components.append(component)
    return components


def diameter(adj: AdjList) -> int:
    """連結グラフの直径（2 頂点間の距離の最大値）を求める。"""
    return max(max(bfs_distances(adj, v).values()) for v in adj)


def bipartition(adj: AdjList) -> tuple[set[int], set[int]] | None:
    """二部グラフなら 2 つの頂点集合を、そうでなければ None を返す。

    各連結成分を幅優先探索し、隣り合う頂点に異なる色 (0 / 1) を塗る。
    同じ色の頂点同士が隣接していたら、奇数長の閉路があるので二部グラフではない。
    """
    color: dict[int, int] = {}
    for start in adj:
        if start in color:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if v not in color:
                    color[v] = 1 - color[u]
                    queue.append(v)
                elif color[v] == color[u]:
                    return None
    left = {v for v, c in color.items() if c == 0}
    return left, set(adj) - left


def articulation_points_and_bridges(adj: AdjList) -> tuple[set[int], set[tuple[int, int]]]:
    """深さ優先探索の訪問順 order と lowlink 値 low から切断点と橋を求める。

    low[v] は、v から深さ優先探索木の辺を 0 本以上下り、最後に後退辺を高々 1 本たどって
    到達できる頂点の order の最小値である。
    """
    order: dict[int, int] = {}
    low: dict[int, int] = {}
    points: set[int] = set()
    bridges: set[tuple[int, int]] = set()

    def dfs(u: int, parent: int | None) -> None:
        order[u] = low[u] = len(order)
        children = 0
        for v in adj[u]:
            if v not in order:
                children += 1
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if parent is not None and low[v] >= order[u]:
                    points.add(u)
                if low[v] > order[u]:
                    bridges.add((min(u, v), max(u, v)))
            elif v != parent:
                low[u] = min(low[u], order[v])
        if parent is None and children >= 2:
            points.add(u)

    for v in adj:
        if v not in order:
            dfs(v, None)
    return points, bridges


def main() -> None:
    # 2 つの三角形 {0, 1, 2} と {3, 4, 5} を辺 (2, 3) でつなぎ、頂点 5 に 6 をぶら下げたグラフ
    # と、それとは別の連結成分 {7, 8}
    n = 9
    edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 5), (5, 3), (5, 6), (7, 8)]
    adj = build(n, edges)

    print("連結成分:", connected_components(adj))
    print("頂点 0 からの距離:", bfs_distances(adj, 0))
    points, bridges = articulation_points_and_bridges(adj)
    print("切断点:", sorted(points))
    print("橋:", sorted(bridges))

    # 6 頂点の閉路 C6 は二部グラフ、5 頂点の閉路 C5 は二部グラフでない
    c6 = build(6, [(i, (i + 1) % 6) for i in range(6)])
    c5 = build(5, [(i, (i + 1) % 5) for i in range(5)])
    print("C6 の二部分割:", bipartition(c6))
    print("C5 の二部分割:", bipartition(c5))
    print("C6 の直径:", diameter(c6))

    # NetworkX との照合
    g: nx.Graph[int] = nx.Graph()
    g.add_nodes_from(range(n))
    g.add_edges_from(edges)
    print("連結成分が一致:",
          sorted(map(sorted, nx.connected_components(g))) == sorted(map(sorted, connected_components(adj))))
    print("切断点が一致:", set(nx.articulation_points(g)) == points)
    # 型スタブでは nx.bridges の戻り値の型が辺のタプルになっていないため cast で補う
    nx_bridges = cast(list[tuple[int, int]], list(nx.bridges(g)))
    print("橋が一致:", {(min(u, v), max(u, v)) for u, v in nx_bridges} == bridges)
    print("C5 は二部グラフか (NetworkX):", nx.is_bipartite(nx.cycle_graph(5)))


if __name__ == "__main__":
    main()
