"""第 12 章 最短経路問題.

ダイクストラ法、ベルマン・フォード法、ワーシャル・フロイド法、A* 探索を実装し、
NetworkX の結果と照合する。

実行方法:
    python shortest_path.py
"""

import heapq
import math

import networkx as nx

# 重み付き有向グラフ: 頂点 -> [(隣接頂点, 重み)]
WeightedAdj = dict[str, list[tuple[str, float]]]


def dijkstra(adj: WeightedAdj, source: str) -> tuple[dict[str, float], dict[str, str]]:
    """ダイクストラ法（優先度付きキュー版）。重みはすべて非負とする。

    戻り値は (距離, 最短経路木における親)。
    """
    dist = {v: math.inf for v in adj}
    parent: dict[str, str] = {}
    dist[source] = 0.0
    heap = [(0.0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:  # 古いエントリは読み飛ばす
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                parent[v] = u
                heapq.heappush(heap, (dist[v], v))
    return dist, parent


def restore_path(parent: dict[str, str], source: str, target: str) -> list[str]:
    """親の情報から source -> target の経路を復元する。"""
    path = [target]
    while path[-1] != source:
        path.append(parent[path[-1]])
    return path[::-1]


def bellman_ford(adj: WeightedAdj, source: str) -> dict[str, float] | None:
    """ベルマン・フォード法。source から到達できる負閉路があれば None を返す。"""
    dist = {v: math.inf for v in adj}
    dist[source] = 0.0
    edges = [(u, v, w) for u in adj for v, w in adj[u]]
    for _ in range(len(adj) - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break
    # n - 1 回の反復後もまだ短くできる辺があれば負閉路が存在する
    if any(dist[u] + w < dist[v] for u, v, w in edges):
        return None
    return dist


def floyd_warshall(adj: WeightedAdj) -> dict[str, dict[str, float]]:
    """ワーシャル・フロイド法で全点対の最短距離を求める。"""
    nodes = list(adj)
    dist = {u: {v: (0.0 if u == v else math.inf) for v in nodes} for u in nodes}
    for u in adj:
        for v, w in adj[u]:
            dist[u][v] = min(dist[u][v], float(w))
    for k in nodes:  # 経由してよい頂点を 1 つずつ増やす
        for i in nodes:
            for j in nodes:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


Cell = tuple[int, int]


def astar_grid(grid: list[str], start: Cell, goal: Cell, use_heuristic: bool = True) -> tuple[int, int] | None:
    """格子上の A* 探索。'#' は壁。マンハッタン距離をヒューリスティックに用いる。

    use_heuristic が False ならヒューリスティックを常に 0 とし、ダイクストラ法と同じ動作になる。
    戻り値は (最短距離, 展開した頂点数)。到達できなければ None。
    """
    def h(c: Cell) -> int:
        return abs(c[0] - goal[0]) + abs(c[1] - goal[1]) if use_heuristic else 0

    g_cost = {start: 0}
    heap = [(h(start), start)]
    closed: set[Cell] = set()
    while heap:
        _, c = heapq.heappop(heap)
        if c in closed:
            continue
        closed.add(c)
        if c == goal:
            return g_cost[c], len(closed)
        r, col = c
        for nr, nc in ((r + 1, col), (r - 1, col), (r, col + 1), (r, col - 1)):
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != "#":
                ng = g_cost[c] + 1
                if ng < g_cost.get((nr, nc), math.inf):
                    g_cost[(nr, nc)] = ng
                    heapq.heappush(heap, (ng + h((nr, nc)), (nr, nc)))
    return None


def main() -> None:
    adj: WeightedAdj = {
        "s": [("a", 4), ("b", 1)],
        "a": [("c", 1)],
        "b": [("a", 2), ("c", 5)],
        "c": [("t", 3)],
        "t": [],
    }
    dist, parent = dijkstra(adj, "s")
    print("ダイクストラ法:", dist, "経路:", restore_path(parent, "s", "t"))
    print("ベルマン・フォード法:", bellman_ford(adj, "s"))

    negative: WeightedAdj = {"s": [("a", 1)], "a": [("b", -2)], "b": [("a", 1), ("t", 1)], "t": []}
    print("負閉路を含むグラフ:", bellman_ford(negative, "s"))

    fw = floyd_warshall(adj)
    print("ワーシャル・フロイド法 (a からの距離):", fw["a"])

    g: nx.DiGraph[str] = nx.DiGraph()
    for u in adj:
        for v, w in adj[u]:
            g.add_edge(u, v, weight=w)
    print("NetworkX:", nx.single_source_dijkstra_path_length(g, "s"))

    grid = [
        "..........",
        "..######..",
        "........#.",
        "######..#.",
        "........#.",
    ]
    print("A* 探索 (距離, 展開数):", astar_grid(grid, (0, 0), (4, 0)))
    print("ダイクストラ法 (距離, 展開数):", astar_grid(grid, (0, 0), (4, 0), use_heuristic=False))


if __name__ == "__main__":
    main()
