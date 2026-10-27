"""第 13 章 ネットワークフロー.

エドモンズ・カープ法（幅優先探索で増加路を選ぶフォード・ファルカーソン法）で最大フローを求め、
残余グラフから最小カットを取り出す。

実行方法:
    python max_flow.py
"""

from collections import deque

import networkx as nx

Capacity = dict[str, dict[str, int]]


def edmonds_karp(capacity: Capacity, s: str, t: str) -> tuple[int, Capacity]:
    """最大フローの値と、各辺の流量を返す。

    簡単のため、u -> v と v -> u の両方の辺を持つ頂点の組は無いものとする。
    """
    # 残余容量: 順方向は容量、逆方向は 0 から始める
    residual: Capacity = {u: {} for u in capacity}
    for u in capacity:
        for v, c in capacity[u].items():
            residual.setdefault(v, {})
            residual[u][v] = residual[u].get(v, 0) + c
            residual[v].setdefault(u, 0)

    total = 0
    while True:
        # 幅優先探索で、残余容量が正の辺だけを通る s-t 路を探す
        parent: dict[str, str] = {s: s}
        queue = deque([s])
        while queue and t not in parent:
            u = queue.popleft()
            for v, r in residual[u].items():
                if r > 0 and v not in parent:
                    parent[v] = u
                    queue.append(v)
        if t not in parent:
            break
        # 増加路上の残余容量の最小値だけ流す
        path = [t]
        while path[-1] != s:
            path.append(parent[path[-1]])
        path.reverse()
        delta = min(residual[u][v] for u, v in zip(path, path[1:]))
        for u, v in zip(path, path[1:]):
            residual[u][v] -= delta
            residual[v][u] += delta
        total += delta

    flow = {u: {v: c - residual[u][v] for v, c in capacity[u].items()} for u in capacity}
    return total, flow


def min_cut(capacity: Capacity, flow: Capacity, s: str) -> tuple[set[str], list[tuple[str, str]]]:
    """最大フローの残余グラフで s から到達できる頂点集合 S と、S から出る辺（カット）を返す。"""
    reach = {s}
    stack = [s]
    while stack:
        u = stack.pop()
        candidates = [(v, capacity[u][v] - flow[u][v]) for v in capacity.get(u, {})]
        candidates += [(w, flow[w][u]) for w in capacity if u in capacity[w]]  # 逆向きに戻せる流量
        for v, r in candidates:
            if r > 0 and v not in reach:
                reach.add(v)
                stack.append(v)
    cut = [(u, v) for u in reach for v in capacity.get(u, {}) if v not in reach]
    return reach, cut


def main() -> None:
    capacity: Capacity = {
        "s": {"a": 10, "b": 10},
        "a": {"b": 2, "c": 4, "d": 8},
        "b": {"d": 9},
        "c": {"t": 10},
        "d": {"c": 6, "t": 10},
        "t": {},
    }
    value, flow = edmonds_karp(capacity, "s", "t")
    print("最大フローの値:", value)
    for u in flow:
        for v, f in flow[u].items():
            print(f"  {u} -> {v}: {f} / {capacity[u][v]}")
    reach, cut = min_cut(capacity, flow, "s")
    print("S =", sorted(reach), " カット:", sorted(cut), " 容量 =", sum(capacity[u][v] for u, v in cut))

    g: nx.DiGraph[str] = nx.DiGraph()
    for u in capacity:
        for v, c in capacity[u].items():
            g.add_edge(u, v, capacity=c)
    print("NetworkX の最大フローの値:", nx.maximum_flow_value(g, "s", "t"))


if __name__ == "__main__":
    main()
