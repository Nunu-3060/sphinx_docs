"""第 9 章 グラフ彩色.

貪欲彩色、バックトラックによる彩色数の計算、削除縮約による彩色多項式の計算を行う。

実行方法:
    python coloring.py
"""

import networkx as nx

AdjList = dict[int, set[int]]


def to_adj(g: "nx.Graph[int]") -> AdjList:
    """NetworkX のグラフを隣接集合の辞書に変換する。"""
    return {v: set(g.neighbors(v)) for v in g.nodes}


def greedy_coloring(adj: AdjList, order: list[int]) -> dict[int, int]:
    """与えられた順に、隣接頂点が使っていない最小の色 (0, 1, 2, ...) を割り当てる。"""
    color: dict[int, int] = {}
    for v in order:
        used = {color[u] for u in adj[v] if u in color}
        c = 0
        while c in used:
            c += 1
        color[v] = c
    return color


def is_colorable(adj: AdjList, k: int) -> bool:
    """k 色で彩色できるかをバックトラックで判定する。"""
    order = sorted(adj, key=lambda v: -len(adj[v]))  # 次数の大きい頂点から決める
    color: dict[int, int] = {}

    def assign(i: int) -> bool:
        if i == len(order):
            return True
        v = order[i]
        used = {color[u] for u in adj[v] if u in color}
        for c in range(k):
            if c not in used:
                color[v] = c
                if assign(i + 1):
                    return True
                del color[v]
        return False

    return assign(0)


def chromatic_number(adj: AdjList) -> int:
    """彩色数を求める（小さなグラフ向け）。"""
    k = 1
    while not is_colorable(adj, k):
        k += 1
    return k


def chromatic_polynomial(edges: frozenset[frozenset[int]], n: int) -> list[int]:
    """削除縮約公式 P(G) = P(G - e) - P(G / e) で彩色多項式の係数を求める。

    戻り値の i 番目の要素が k^i の係数である。辺を持たない n 頂点のグラフは k^n。
    """
    if not edges:
        return [0] * n + [1]
    e = next(iter(edges))
    u, v = sorted(e)
    deleted = edges - {e}
    # 縮約: v を u に併合する。生じる自己ループは e 自身なので除かれ、多重辺は集合なので 1 本になる
    contracted = frozenset(frozenset(u if x == v else x for x in f) for f in deleted)
    p1 = chromatic_polynomial(deleted, n)
    p2 = chromatic_polynomial(contracted, n - 1)
    return [a - (p2[i] if i < len(p2) else 0) for i, a in enumerate(p1)]


def format_poly(coeffs: list[int]) -> str:
    """係数リストを "k^4 - 4k^3 + 6k^2 - 3k" のような文字列にする。"""
    text = ""
    for i in range(len(coeffs) - 1, -1, -1):
        c = coeffs[i]
        if c == 0:
            continue
        sign = "-" if c < 0 else "+"
        mag = "" if abs(c) == 1 and i > 0 else str(abs(c))
        var = "" if i == 0 else ("k" if i == 1 else f"k^{i}")
        text += (f" {sign} " if text else ("-" if c < 0 else "")) + mag + var
    return text


def main() -> None:
    # 王冠グラフ: 二部グラフなのに、頂点の順序によっては貪欲彩色が多くの色を使う
    n = 4
    crown: nx.Graph[int] = nx.Graph()
    for i in range(n):
        for j in range(n):
            if i != j:
                crown.add_edge(2 * i, 2 * j + 1)  # 偶数番号と奇数番号の頂点を結ぶ
    adj = to_adj(crown)
    bad_order = [v for i in range(n) for v in (2 * i, 2 * i + 1)]  # 0, 1, 2, 3, ...
    good_order = sorted(adj, key=lambda v: v % 2)  # 偶数をすべて先に塗る
    print("王冠グラフ (悪い順序):", len(set(greedy_coloring(adj, bad_order).values())), "色")
    print("王冠グラフ (良い順序):", len(set(greedy_coloring(adj, good_order).values())), "色")

    petersen = to_adj(nx.petersen_graph())
    print("ピーターセングラフの彩色数:", chromatic_number(petersen))
    nx_coloring = nx.greedy_color(nx.petersen_graph(), strategy="largest_first")
    print("NetworkX の貪欲彩色 (largest_first):", len(set(nx_coloring.values())), "色")

    # 彩色多項式: 閉路 C4 は (k-1)^4 + (k-1) = k^4 - 4k^3 + 6k^2 - 3k
    c4 = frozenset(frozenset((i, (i + 1) % 4)) for i in range(4))
    print("C4 の彩色多項式:", format_poly(chromatic_polynomial(c4, 4)))
    k4 = frozenset(frozenset((i, j)) for i in range(4) for j in range(i + 1, 4))
    print("K4 の彩色多項式:", format_poly(chromatic_polynomial(k4, 4)))


if __name__ == "__main__":
    main()
