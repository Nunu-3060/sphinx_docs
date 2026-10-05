"""第 7 章: 最短経路アルゴリズム。

* dijkstra: 辺の重みが非負のときの単一始点最短経路。O((V + E) log V)
* bellman_ford: 負の重みを許す単一始点最短経路と負閉路の検出。O(VE)
* floyd_warshall: 全点対最短経路。O(V^3)

重み付き有向グラフは「頂点 -> (隣接頂点, 重み) のリスト」で表す。

実行例::

    python ch07_shortest_path.py
"""

from __future__ import annotations

import heapq
import math

WeightedGraph = dict[str, list[tuple[str, float]]]


def dijkstra(graph: WeightedGraph, start: str) -> dict[str, float]:
    """start から各頂点への最短距離を返す。重みは非負でなければならない。"""
    dist = {u: math.inf for u in graph}
    dist[start] = 0.0
    heap: list[tuple[float, str]] = [(0.0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue  # 既により短い距離で確定済みの古い情報は捨てる
        for v, w in graph[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    return dist


def bellman_ford(graph: WeightedGraph, start: str) -> dict[str, float]:
    """負の重みを許す最短距離。start から到達できる負閉路があれば例外。"""
    dist = {u: math.inf for u in graph}
    dist[start] = 0.0
    for _ in range(len(graph) - 1):  # 最短経路の辺数は高々 V - 1
        for u in graph:
            for v, w in graph[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
    for u in graph:  # V 回目でも更新できるなら負閉路がある
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                raise ValueError("負閉路がある")
    return dist


def floyd_warshall(graph: WeightedGraph) -> dict[str, dict[str, float]]:
    """全ての頂点の組の最短距離を返す。"""
    dist = {u: {v: math.inf for v in graph} for u in graph}
    for u in graph:
        dist[u][u] = 0.0
        for v, w in graph[u]:
            dist[u][v] = min(dist[u][v], float(w))
    for k in graph:  # 経由してよい頂点を 1 つずつ増やす
        for i in graph:
            for j in graph:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


def main() -> None:
    graph: WeightedGraph = {
        "s": [("a", 4), ("b", 1)],
        "a": [("c", 1)],
        "b": [("a", 2), ("c", 5)],
        "c": [("t", 3)],
        "t": [],
    }
    print("ダイクストラ法      :", dijkstra(graph, "s"))
    print("ベルマン-フォード法 :", bellman_ford(graph, "s"))
    all_pairs = floyd_warshall(graph)
    print("ワーシャル-フロイド法 (b から):", all_pairs["b"])

    negative: WeightedGraph = {
        "s": [("a", 2)],
        "a": [("b", 3)],
        "b": [("a", -4)],
    }
    try:
        bellman_ford(negative, "s")
    except ValueError as error:
        print("負の重みを含むグラフ:", error)


if __name__ == "__main__":
    main()
