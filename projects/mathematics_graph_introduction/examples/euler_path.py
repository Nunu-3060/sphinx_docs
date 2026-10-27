"""第 7 章 オイラー路とハミルトン路.

次数の条件からオイラー路の有無を判定し、ヒールホルツァーのアルゴリズムで
オイラー路を構成する。また、バックトラックでハミルトン閉路を探す。

実行方法:
    python euler_path.py
"""

import networkx as nx

Edge = tuple[int, int]


def odd_vertices(n: int, edges: list[Edge]) -> list[int]:
    """次数が奇数の頂点の一覧を返す。"""
    deg = [0] * n
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1
    return [v for v in range(n) if deg[v] % 2 == 1]


def euler_path(n: int, edges: list[Edge]) -> list[int] | None:
    """ヒールホルツァーのアルゴリズムでオイラー路（またはオイラー閉路）を求める。

    多重辺を扱えるよう、辺を番号で区別する。オイラー路が存在しなければ None を返す。
    """
    odd = odd_vertices(n, edges)
    if len(odd) not in (0, 2):
        return None
    adj: dict[int, list[tuple[int, int]]] = {v: [] for v in range(n)}  # 頂点 -> [(隣接頂点, 辺番号)]
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i))
        adj[v].append((u, i))
    used = [False] * len(edges)
    start = odd[0] if odd else edges[0][0]

    stack = [start]
    path: list[int] = []
    while stack:
        u = stack[-1]
        # u から出る未使用の辺を 1 本たどる。行き止まりになったら path に確定させる。
        while adj[u] and used[adj[u][-1][1]]:
            adj[u].pop()
        if adj[u]:
            v, i = adj[u].pop()
            used[i] = True
            stack.append(v)
        else:
            path.append(stack.pop())
    if len(path) != len(edges) + 1:  # 辺を持つ部分が連結でない
        return None
    return path[::-1]


def hamiltonian_cycle(g: "nx.Graph[int]") -> list[int] | None:
    """バックトラックでハミルトン閉路を 1 つ探す。見つからなければ None を返す。"""
    nodes = list(g.nodes)
    n = len(nodes)
    start = nodes[0]
    path = [start]
    visited = {start}

    def extend() -> bool:
        if len(path) == n:
            return g.has_edge(path[-1], start)
        for v in g.neighbors(path[-1]):
            if v not in visited:
                path.append(v)
                visited.add(v)
                if extend():
                    return True
                path.pop()
                visited.remove(v)
        return False

    return path + [start] if extend() else None


def main() -> None:
    # ケーニヒスベルクの橋: 陸地 0 (北岸), 1 (南岸), 2 (中洲), 3 (東の陸地) と 7 本の橋
    konigsberg: list[Edge] = [(0, 2), (0, 2), (1, 2), (1, 2), (0, 3), (1, 3), (2, 3)]
    print("ケーニヒスベルク: 奇数次の頂点 =", odd_vertices(4, konigsberg))
    print("ケーニヒスベルク: オイラー路 =", euler_path(4, konigsberg))

    # 橋を 1 本取り除くと、奇数次の頂点が 2 個になりオイラー路が存在する
    print("橋を 1 本除いた場合:", euler_path(4, konigsberg[1:]))

    # 「家の形」の一筆書き: 正方形 0-1-2-3 と屋根の頂点 4、および対角線 0-2, 1-3
    house: list[Edge] = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3), (2, 4), (3, 4)]
    path = euler_path(5, house)
    print("家の形: オイラー路 =", path)

    g: nx.MultiGraph[int] = nx.MultiGraph(house)
    print("NetworkX: オイラー路が存在するか =", nx.has_eulerian_path(g))

    # 正十二面体グラフはハミルトン閉路を持ち、ピーターセングラフは持たない
    print("正十二面体:", hamiltonian_cycle(nx.dodecahedral_graph()))
    print("ピーターセン:", hamiltonian_cycle(nx.petersen_graph()))


if __name__ == "__main__":
    main()
