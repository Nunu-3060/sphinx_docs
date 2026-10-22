"""PageRank: リンク構造から、ページの重要度を固有ベクトルとして求める.

5 つのページ A から E のリンク構造（LINKS）から推移行列 M を作り、
ダンピング係数 d = 0.85 のグーグル行列 G = d M + (1 - d) / n を作る。
G の固有値 1 の固有ベクトルを、べき乗法で求める。

使い方: python ch14_pagerank.py
"""

import numpy as np
from numpy.typing import NDArray

Matrix = NDArray[np.float64]

PAGES = ["A", "B", "C", "D", "E"]
LINKS = {
    "A": ["B", "C"],
    "B": ["C"],
    "C": ["A"],
    "D": ["A", "C"],
    "E": ["A", "D"],
}
DAMPING = 0.85


def google_matrix() -> Matrix:
    """リンク構造からグーグル行列を作る."""
    n = len(PAGES)
    m = np.zeros((n, n))
    for source, targets in LINKS.items():
        j = PAGES.index(source)
        for target in targets:
            m[PAGES.index(target), j] = 1.0 / len(targets)  # j 列目はページ j からの遷移確率
    return DAMPING * m + (1.0 - DAMPING) / n * np.ones((n, n))


def power_iteration(g: Matrix, tol: float = 1e-10) -> tuple[Matrix, int]:
    """べき乗法で、固有値 1 の固有ベクトル（成分の和が 1）と反復回数を返す."""
    n = g.shape[0]
    x = np.full(n, 1.0 / n)
    for count in range(1, 1001):
        x_next = g @ x
        if np.abs(x_next - x).sum() < tol:
            return x_next, count
        x = x_next
    raise RuntimeError("収束しなかった")


def report() -> None:
    """べき乗法と固有値分解で求めた PageRank を表示する."""
    g = google_matrix()
    rank, count = power_iteration(g)
    values, vectors = np.linalg.eig(g)
    k = int(np.argmax(np.real(values)))
    v = np.real(vectors[:, k])
    with np.printoptions(precision=4, suppress=True):
        print("各列の和 =", g.sum(axis=0))
        print(f"べき乗法（{count} 回で収束）:", rank)
        print("固有値分解:", v / v.sum())
        print(f"最大の固有値 = {np.real(values[k]):.4f}")
    for page, value in sorted(zip(PAGES, rank), key=lambda item: -item[1]):
        print(f"{page}: {value:.4f}")


def main() -> None:
    report()


if __name__ == "__main__":
    main()
