"""第 7 章: 幅優先探索・深さ優先探索・トポロジカルソート。

グラフは隣接リスト (頂点 -> 隣接する頂点のリスト) で表す。

実行例::

    python ch07_graph_search.py
"""

from __future__ import annotations

from collections import deque

Graph = dict[str, list[str]]


def bfs(graph: Graph, start: str) -> dict[str, int]:
    """start から各頂点への最短距離 (辺の本数) を返す。O(V + E)。"""
    dist = {start: 0}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in dist:  # 初めて見つけた頂点だけをキューに入れる
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist


def dfs(graph: Graph, start: str) -> list[str]:
    """start から深さ優先で訪問した順に頂点を返す。O(V + E)。"""
    order: list[str] = []
    visited: set[str] = set()

    def visit(u: str) -> None:
        visited.add(u)
        order.append(u)
        for v in graph[u]:
            if v not in visited:
                visit(v)

    visit(start)
    return order


def topological_sort(graph: Graph) -> list[str]:
    """有向非巡回グラフの頂点をトポロジカル順に並べる (カーンの方法)。"""
    indegree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            indegree[v] += 1
    queue = deque(u for u in graph if indegree[u] == 0)
    order: list[str] = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    if len(order) != len(graph):
        raise ValueError("グラフに閉路がある")
    return order


def main() -> None:
    undirected: Graph = {
        "A": ["B", "C"],
        "B": ["A", "D"],
        "C": ["A", "D", "E"],
        "D": ["B", "C", "F"],
        "E": ["C", "F"],
        "F": ["D", "E"],
    }
    print("BFS の距離:", bfs(undirected, "A"))
    print("DFS の訪問順:", dfs(undirected, "A"))

    # 授業の履修順序: 辺 u -> v は「u を v より先に履修する」ことを表す。
    courses: Graph = {
        "プログラミング": ["データ構造"],
        "離散数学": ["データ構造", "オートマトン"],
        "データ構造": ["アルゴリズム"],
        "アルゴリズム": ["計算複雑性"],
        "オートマトン": ["計算可能性"],
        "計算可能性": ["計算複雑性"],
        "計算複雑性": [],
    }
    print("履修順:", " -> ".join(topological_sort(courses)))


if __name__ == "__main__":
    main()
