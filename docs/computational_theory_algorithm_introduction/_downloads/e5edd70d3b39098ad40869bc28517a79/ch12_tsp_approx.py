"""第 12 章: 巡回セールスマン問題の近似と局所探索。

平面上の点 (距離が三角不等式を満たす) について、次の 3 つを比べる。

* mst_tour: 最小全域木を深さ優先でたどった順に回る 2 近似アルゴリズム。
* two_opt: 経路の 2 辺をつなぎ替えて短くなる限り改善を続ける局所探索。
* exact_tour: 全ての順列を試す厳密解法 (点が少ないときだけ使える)。

実行例::

    python ch12_tsp_approx.py
"""

from __future__ import annotations

import math
import random
from itertools import permutations

Point = tuple[float, float]


def tour_length(points: list[Point], tour: list[int]) -> float:
    """巡回路 tour (最後に出発点へ戻る) の長さを返す。"""
    return sum(math.dist(points[tour[i]], points[tour[i - 1]])
               for i in range(len(tour)))


def mst_tour(points: list[Point]) -> list[int]:
    """プリム法で最小全域木を作り、その前順 (行きがけ順) を巡回路とする。"""
    n = len(points)
    in_tree = [False] * n
    best = [math.inf] * n  # 木に最も近い頂点までの距離
    parent = [-1] * n
    children: list[list[int]] = [[] for _ in range(n)]
    best[0] = 0.0
    for _ in range(n):
        u = min((i for i in range(n) if not in_tree[i]), key=lambda i: best[i])
        in_tree[u] = True
        if parent[u] >= 0:
            children[parent[u]].append(u)
        for v in range(n):
            d = math.dist(points[u], points[v])
            if not in_tree[v] and d < best[v]:
                best[v], parent[v] = d, u
    order: list[int] = []
    stack = [0]
    while stack:  # 深さ優先でたどり、初めて訪れた順に並べる
        u = stack.pop()
        order.append(u)
        stack.extend(reversed(children[u]))
    return order


def two_opt(points: list[Point], tour: list[int]) -> list[int]:
    """辺 (a, b) と (c, d) を (a, c) と (b, d) に替えて短くなれば採用する。"""
    tour = list(tour)
    improved = True
    while improved:
        improved = False
        for i in range(1, len(tour) - 1):
            for j in range(i + 1, len(tour)):
                a, b = points[tour[i - 1]], points[tour[i]]
                c, d = points[tour[j]], points[tour[(j + 1) % len(tour)]]
                delta = (math.dist(a, c) + math.dist(b, d)
                         - math.dist(a, b) - math.dist(c, d))
                if delta < -1e-12:
                    tour[i:j + 1] = reversed(tour[i:j + 1])
                    improved = True
    return tour


def exact_tour(points: list[Point]) -> list[int]:
    """点 0 を出発点に固定し、残りの (n - 1)! 通りの順序を全て試す。"""
    rest = range(1, len(points))
    best = min(permutations(rest),
               key=lambda p: tour_length(points, [0, *p]))
    return [0, *best]


def main() -> None:
    random.seed(3)
    points = [(random.random(), random.random()) for _ in range(9)]
    approx = mst_tour(points)
    improved = two_opt(points, approx)
    exact = exact_tour(points)
    print(f"2 近似 (最小全域木): {tour_length(points, approx):.4f}")
    print(f"2-opt で改善      : {tour_length(points, improved):.4f}")
    print(f"厳密解            : {tour_length(points, exact):.4f}")


if __name__ == "__main__":
    main()
