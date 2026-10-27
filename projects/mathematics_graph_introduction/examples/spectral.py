"""第 14 章 代数的グラフ理論.

隣接行列のべき乗による歩道の数え上げ、ラプラシアン行列の固有値、行列木定理、
フィードラーベクトルによるグラフの 2 分割、べき乗法による PageRank を計算する。

実行方法:
    python spectral.py
"""

import networkx as nx
import numpy as np
import numpy.typing as npt

FloatMatrix = npt.NDArray[np.float64]
FloatVector = npt.NDArray[np.float64]


def adjacency(g: "nx.Graph[int]") -> FloatMatrix:
    """頂点 0..n-1 のグラフの隣接行列を返す。"""
    n = g.number_of_nodes()
    a = np.zeros((n, n))
    for u, v in g.edges:
        a[u, v] = a[v, u] = 1.0
    return a


def laplacian(a: FloatMatrix) -> FloatMatrix:
    """ラプラシアン行列 L = D - A を返す。"""
    return np.diag(a.sum(axis=1)) - a


def count_spanning_trees(a: FloatMatrix) -> int:
    """行列木定理: ラプラシアン行列から 1 行 1 列を除いた行列式が全域木の個数に等しい。"""
    reduced = laplacian(a)[1:, 1:]
    return round(float(np.linalg.det(reduced)))


def fiedler_partition(a: FloatMatrix) -> tuple[float, list[int], list[int]]:
    """2 番目に小さい固有値（代数的連結度）と、フィードラーベクトルの符号による 2 分割を返す。"""
    eigenvalues, eigenvectors = np.linalg.eigh(laplacian(a))  # 固有値は昇順に並ぶ
    fiedler = eigenvectors[:, 1]
    plus = [i for i in range(len(fiedler)) if fiedler[i] >= 0]
    minus = [i for i in range(len(fiedler)) if fiedler[i] < 0]
    return float(eigenvalues[1]), plus, minus


def pagerank(links: dict[int, list[int]], damping: float = 0.85, tol: float = 1e-10) -> FloatVector:
    """べき乗法で PageRank を求める。リンクを持たないページからは全ページへ均等に移るものとする。"""
    n = len(links)
    p = np.zeros((n, n))  # p[j, i] は i から j へ移る確率
    for i, outs in links.items():
        if outs:
            for j in outs:
                p[j, i] = 1.0 / len(outs)
        else:
            p[:, i] = 1.0 / n
    x = np.full(n, 1.0 / n)
    while True:
        x_new: FloatVector = damping * p @ x + (1.0 - damping) / n
        if np.abs(x_new - x).sum() < tol:
            return x_new
        x = x_new


def main() -> None:
    # 隣接行列のべき乗: (A^k)[u, v] は u から v への長さ k の歩道の数
    k4 = adjacency(nx.complete_graph(4))
    a3 = np.linalg.matrix_power(k4, 3)
    print("K4 の A^3:")
    print(a3.astype(int))
    print("三角形の個数 = trace(A^3) / 6 =", int(np.trace(a3)) // 6)

    # ラプラシアン行列の固有値 0 の重複度は連結成分の個数に等しい
    two_parts: nx.Graph[int] = nx.disjoint_union(nx.path_graph(3), nx.cycle_graph(4))
    eig = np.linalg.eigvalsh(laplacian(adjacency(two_parts)))
    print("P3 と C4 の非交和のラプラシアン固有値:", np.round(eig, 3) + 0.0)  # + 0.0 で -0. を 0. にする

    # 行列木定理とケイリーの公式
    for n in range(2, 7):
        print(f"K{n} の全域木の個数: {count_spanning_trees(adjacency(nx.complete_graph(n)))} (n^(n-2) = {n ** (n - 2)})")
    petersen = nx.petersen_graph()
    print("ピーターセングラフの全域木の個数:", count_spanning_trees(adjacency(petersen)),
          "NetworkX:", round(nx.number_of_spanning_trees(petersen)))

    # フィードラーベクトルによる 2 分割: 2 つの K5 を 1 本の辺でつないだバーベルグラフ
    barbell = nx.barbell_graph(5, 0)
    lam2, plus, minus = fiedler_partition(adjacency(barbell))
    print(f"代数的連結度 = {lam2:.4f}, 分割: {plus} / {minus}")

    # PageRank
    links = {0: [1, 2], 1: [2], 2: [0], 3: [2]}
    pr = pagerank(links)
    print("PageRank:", np.round(pr, 4))
    nx_pr = nx.pagerank(nx.DiGraph([(i, j) for i, outs in links.items() for j in outs]), alpha=0.85, tol=1e-12)
    print("NetworkX:", [round(nx_pr[i], 4) for i in range(4)])


if __name__ == "__main__":
    main()
