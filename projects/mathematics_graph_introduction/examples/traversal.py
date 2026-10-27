"""第 11 章 グラフの探索.

幅優先探索、深さ優先探索、トポロジカルソート（カーンのアルゴリズム）、
強連結成分分解（タージャンのアルゴリズム）を実装し、NetworkX の結果と照合する。

実行方法:
    python traversal.py
"""

from collections import deque

import networkx as nx

AdjList = dict[str, list[str]]


def bfs_order(adj: AdjList, source: str) -> list[str]:
    """幅優先探索で頂点を訪問した順序を返す。"""
    visited = {source}
    order: list[str] = []
    queue = deque([source])
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            if v not in visited:
                visited.add(v)
                queue.append(v)
    return order


def dfs_order(adj: AdjList, source: str) -> list[str]:
    """深さ優先探索（再帰）で頂点を訪問した順序（行きがけ順）を返す。"""
    visited: set[str] = set()
    order: list[str] = []

    def visit(u: str) -> None:
        visited.add(u)
        order.append(u)
        for v in adj[u]:
            if v not in visited:
                visit(v)

    visit(source)
    return order


def topological_sort(adj: AdjList) -> list[str] | None:
    """カーンのアルゴリズム: 入次数 0 の頂点を順に取り出す。閉路があれば None を返す。"""
    indeg = {v: 0 for v in adj}
    for u in adj:
        for v in adj[u]:
            indeg[v] += 1
    queue = deque(v for v in adj if indeg[v] == 0)
    order: list[str] = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    return order if len(order) == len(adj) else None


def strongly_connected_components(adj: AdjList) -> list[set[str]]:
    """タージャンのアルゴリズムで強連結成分を求める。"""
    index: dict[str, int] = {}
    low: dict[str, int] = {}
    stack: list[str] = []
    on_stack: set[str] = set()
    components: list[set[str]] = []

    def visit(u: str) -> None:
        index[u] = low[u] = len(index)
        stack.append(u)
        on_stack.add(u)
        for v in adj[u]:
            if v not in index:
                visit(v)
                low[u] = min(low[u], low[v])
            elif v in on_stack:
                low[u] = min(low[u], index[v])
        if low[u] == index[u]:  # u は強連結成分の根
            component: set[str] = set()
            while True:
                w = stack.pop()
                on_stack.remove(w)
                component.add(w)
                if w == u:
                    break
            components.append(component)

    for v in adj:
        if v not in index:
            visit(v)
    return components


def main() -> None:
    undirected: AdjList = {
        "A": ["B", "C"], "B": ["A", "D", "E"], "C": ["A", "F"],
        "D": ["B"], "E": ["B", "F"], "F": ["C", "E"],
    }
    print("BFS:", bfs_order(undirected, "A"))
    print("DFS:", dfs_order(undirected, "A"))

    # 授業の履修順序（先修科目 -> 後続科目）
    courses: AdjList = {
        "プログラミング基礎": ["データ構造", "離散数学"],
        "離散数学": ["アルゴリズム", "グラフ理論"],
        "データ構造": ["アルゴリズム"],
        "アルゴリズム": ["コンパイラ"],
        "グラフ理論": [],
        "コンパイラ": [],
    }
    print("トポロジカル順序:", topological_sort(courses))

    directed: AdjList = {
        "a": ["b"], "b": ["c", "e"], "c": ["a", "d"], "d": ["h"],
        "e": ["f"], "f": ["g"], "g": ["e", "h"], "h": [],
    }
    sccs = strongly_connected_components(directed)
    print("強連結成分:", [sorted(c) for c in sccs])

    g: nx.DiGraph[str] = nx.DiGraph([(u, v) for u in directed for v in directed[u]])
    nx_sccs = [set(c) for c in nx.strongly_connected_components(g)]
    print("NetworkX と一致:", sorted(map(sorted, sccs)) == sorted(map(sorted, nx_sccs)))


if __name__ == "__main__":
    main()
