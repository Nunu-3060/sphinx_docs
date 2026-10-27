"""第 5 章 グラフ理論入門のサンプルコード。

無向グラフを隣接リストで表し、次数・幅優先探索・二部グラフ判定・
オイラー路の存在判定を実装する。
"""

from collections import deque


class Graph:
    """無向グラフ（多重辺を許す）を隣接リストで表すクラス。"""

    def __init__(self, edges: list[tuple[str, str]]) -> None:
        self.adjacency: dict[str, list[str]] = {}
        for u, v in edges:
            self.adjacency.setdefault(u, []).append(v)
            self.adjacency.setdefault(v, []).append(u)
        self.edge_count = len(edges)

    def vertices(self) -> list[str]:
        """頂点の一覧を返す。"""
        return sorted(self.adjacency)

    def degree(self, v: str) -> int:
        """頂点 v の次数を返す。"""
        return len(self.adjacency[v])

    def bfs_distances(self, start: str) -> dict[str, int]:
        """幅優先探索で start から各頂点への最短距離（辺の本数）を求める。"""
        distances = {start: 0}
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for w in self.adjacency[u]:
                if w not in distances:
                    distances[w] = distances[u] + 1
                    queue.append(w)
        return distances

    def shortest_path(self, start: str, goal: str) -> list[str]:
        """幅優先探索で start から goal への最短路を 1 つ求める。到達できなければ空リストを返す。"""
        parent: dict[str, str | None] = {start: None}
        queue = deque([start])
        while queue:
            u = queue.popleft()
            if u == goal:
                break
            for w in self.adjacency[u]:
                if w not in parent:
                    parent[w] = u
                    queue.append(w)
        if goal not in parent:
            return []
        path: list[str] = []
        node: str | None = goal
        while node is not None:
            path.append(node)
            node = parent[node]
        return path[::-1]

    def is_connected(self) -> bool:
        """連結かどうかを返す。"""
        vertices = self.vertices()
        return len(self.bfs_distances(vertices[0])) == len(vertices)

    def is_bipartite(self) -> bool:
        """幅優先探索で隣接する頂点を異なる色に塗り分けられるかを調べる（連結グラフを仮定）。"""
        start = self.vertices()[0]
        color = {start: 0}
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for w in self.adjacency[u]:
                if w not in color:
                    color[w] = 1 - color[u]
                    queue.append(w)
                elif color[w] == color[u]:
                    return False
        return True

    def has_euler_path(self) -> bool:
        """オイラー路が存在するか（連結かつ奇数次数の頂点が 0 個または 2 個か）を返す。"""
        odd = sum(1 for v in self.vertices() if self.degree(v) % 2 == 1)
        return self.is_connected() and odd in (0, 2)


def main() -> None:
    print("--- 握手補題 ---")
    g = Graph([("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "E"), ("D", "E"), ("E", "F")])
    degrees = {v: g.degree(v) for v in g.vertices()}
    print(f"次数: {degrees}")
    print(f"次数の総和={sum(degrees.values())}, 辺の本数 x 2={2 * g.edge_count}")

    print("--- 幅優先探索 ---")
    print(f"A からの距離: {g.bfs_distances('A')}")
    print(f"A から F への最短路: {g.shortest_path('A', 'F')}")

    print("--- 二部グラフ判定 ---")
    square = Graph([("1", "2"), ("2", "3"), ("3", "4"), ("4", "1")])
    triangle = Graph([("1", "2"), ("2", "3"), ("3", "1")])
    print(f"長さ 4 の閉路: {square.is_bipartite()}, 長さ 3 の閉路: {triangle.is_bipartite()}")

    print("--- オイラー路 ---")
    konigsberg = Graph([
        ("北岸", "島"), ("北岸", "島"), ("南岸", "島"), ("南岸", "島"),
        ("北岸", "東"), ("南岸", "東"), ("島", "東"),
    ])
    konigsberg_degrees = {v: konigsberg.degree(v) for v in konigsberg.vertices()}
    print(f"ケーニヒスベルク: 次数={konigsberg_degrees}")
    print(f"オイラー路の存在: {konigsberg.has_euler_path()}")
    print(f"グラフ g のオイラー路の存在: {g.has_euler_path()}")


if __name__ == "__main__":
    main()
