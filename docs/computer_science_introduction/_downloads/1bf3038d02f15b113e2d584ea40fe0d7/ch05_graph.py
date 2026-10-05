"""グラフ探索（幅優先探索・深さ優先探索・ダイクストラ法）のサンプル。

グラフは隣接リスト（頂点から隣接する頂点の一覧への辞書）で表す。

実行方法: python ch05_graph.py
関連する章: 第 5 章「アルゴリズムと計算量」
"""

import heapq
from collections import deque

Graph = dict[str, list[str]]
WeightedGraph = dict[str, list[tuple[str, int]]]


def bfs(graph: Graph, start: str) -> dict[str, int]:
    """start からの辺の数で数えた最短距離を返す（幅優先探索）。"""
    dist = {start: 0}
    queue = deque([start])
    while queue:
        u = queue.popleft()  # 先に見つけた頂点から順に取り出す
        for v in graph[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist


def dfs(graph: Graph, start: str) -> list[str]:
    """深さ優先探索で訪問した順に頂点を返す。"""
    order: list[str] = []
    visited: set[str] = set()
    stack = [start]
    while stack:
        u = stack.pop()  # 最後に見つけた頂点から取り出す
        if u in visited:
            continue
        visited.add(u)
        order.append(u)
        # 隣接リストの先頭の頂点から訪問するよう、逆順に積む
        for v in reversed(graph[u]):
            if v not in visited:
                stack.append(v)
    return order


def dijkstra(graph: WeightedGraph,
             start: str) -> tuple[dict[str, int], dict[str, str]]:
    """辺の重みが非負のグラフで、start からの最短距離と直前の頂点を返す。"""
    dist = {start: 0}
    prev: dict[str, str] = {}
    heap = [(0, start)]  # (暫定距離, 頂点) の優先度付きキュー
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue  # より短い距離で既に確定した古い候補は捨てる
        for v, w in graph[u]:
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, prev


def path_to(prev: dict[str, str], start: str, goal: str) -> list[str]:
    """直前の頂点の記録をたどって経路を復元する。"""
    path = [goal]
    while path[-1] != start:
        path.append(prev[path[-1]])
    return path[::-1]


def main() -> None:
    """3 つの探索の結果を表示する。"""
    graph: Graph = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "F"],
        "D": ["B"],
        "E": ["B", "F"],
        "F": ["C", "E"],
    }
    print("BFS の距離:", bfs(graph, "A"))
    print("DFS の訪問順:", dfs(graph, "A"))

    roads: WeightedGraph = {
        "S": [("A", 7), ("B", 2)],
        "A": [("G", 1)],
        "B": [("A", 3), ("C", 8)],
        "C": [("G", 2)],
        "G": [],
    }
    dist, prev = dijkstra(roads, "S")
    print("ダイクストラ法の距離:", dist)
    print("S から G への最短経路:", " -> ".join(path_to(prev, "S", "G")))


if __name__ == "__main__":
    main()
