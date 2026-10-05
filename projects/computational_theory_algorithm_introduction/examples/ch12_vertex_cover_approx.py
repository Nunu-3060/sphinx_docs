"""第 12 章: 頂点被覆問題の 2 近似アルゴリズム。

まだ覆われていない辺を 1 本選び、その両端点を被覆に加えることを繰り返す。
選んだ辺は互いに端点を共有しない (極大マッチング) ので、最適解はそれぞれの
辺から少なくとも 1 頂点を含む。よって得られる被覆は最適解の 2 倍以下になる。

実行例::

    python ch12_vertex_cover_approx.py
"""

from __future__ import annotations

from itertools import combinations

Edge = tuple[int, int]


def approx_vertex_cover(edges: list[Edge]) -> set[int]:
    """サイズが最適解の 2 倍以下の頂点被覆を O(E) で返す。"""
    cover: set[int] = set()
    for u, v in edges:
        if u not in cover and v not in cover:  # まだ覆われていない辺
            cover.add(u)
            cover.add(v)
    return cover


def exact_vertex_cover(edges: list[Edge]) -> set[int]:
    """小さい順に全ての頂点集合を試して最小の頂点被覆を返す (指数時間)。"""
    vertices = sorted({x for edge in edges for x in edge})
    for size in range(len(vertices) + 1):
        for group in combinations(vertices, size):
            chosen = set(group)
            if all(u in chosen or v in chosen for u, v in edges):
                return chosen
    return set(vertices)


def main() -> None:
    edges: list[Edge] = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (4, 5),
                         (4, 6), (5, 6)]
    approx = approx_vertex_cover(edges)
    exact = exact_vertex_cover(edges)
    print(f"近似解: {sorted(approx)} (サイズ {len(approx)})")
    print(f"最適解: {sorted(exact)} (サイズ {len(exact)})")
    print("近似比:", len(approx) / len(exact))


if __name__ == "__main__":
    main()
