"""第 7 章: 最大流 (エドモンズ-カープ法)。

フォード-ファルカーソン法のうち、増加路を幅優先探索で選ぶものを
エドモンズ-カープ法と呼ぶ。計算量は O(VE^2)。

実行例::

    python ch07_max_flow.py
"""

from __future__ import annotations

from collections import deque


def max_flow(capacity: dict[str, dict[str, int]], s: str, t: str) -> int:
    """容量 capacity[u][v] のネットワークで s から t への最大流量を返す。"""
    # 残余グラフ: 逆向きの辺も容量 0 で用意しておく。
    residual: dict[str, dict[str, int]] = {}
    for u, targets in capacity.items():
        for v, c in targets.items():
            residual.setdefault(u, {})
            residual.setdefault(v, {})
            residual[u][v] = residual[u].get(v, 0) + c
            residual[v].setdefault(u, 0)

    flow = 0
    while True:
        # 残余容量が正の辺だけを通って s から t への経路を探す。
        parent: dict[str, str] = {}
        queue = deque([s])
        while queue and t not in parent:
            u = queue.popleft()
            for v, c in residual[u].items():
                if c > 0 and v != s and v not in parent:
                    parent[v] = u
                    queue.append(v)
        if t not in parent:
            return flow  # 増加路が無ければ現在の流量が最大
        # 経路上の残余容量の最小値だけ流す。
        bottleneck = min(residual[parent[v]][v] for v in path_to(parent, t))
        for v in path_to(parent, t):
            u = parent[v]
            residual[u][v] -= bottleneck
            residual[v][u] += bottleneck  # 逆辺を増やして「押し戻し」を許す
        flow += bottleneck


def path_to(parent: dict[str, str], t: str) -> list[str]:
    """parent をたどって得られる経路上の頂点 (始点を除く) を返す。"""
    path: list[str] = []
    v = t
    while v in parent:
        path.append(v)
        v = parent[v]
    return path


def main() -> None:
    capacity = {
        "s": {"a": 10, "b": 10},
        "a": {"b": 2, "c": 4, "d": 8},
        "b": {"d": 9},
        "c": {"t": 10},
        "d": {"c": 6, "t": 10},
    }
    print("最大流量:", max_flow(capacity, "s", "t"))  # 19


if __name__ == "__main__":
    main()
