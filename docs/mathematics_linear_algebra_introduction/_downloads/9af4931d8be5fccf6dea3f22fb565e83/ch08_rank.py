"""行列のランクと、零空間の基底を求める.

行基本変形で被約階段行列（RREF）を作り、ピボットのある列の数からランクを、
自由変数から零空間の基底を求める。

使い方: python ch08_rank.py
"""

import numpy as np
from numpy.typing import ArrayLike, NDArray

Matrix = NDArray[np.float64]


def rref(a: ArrayLike, tol: float = 1e-10) -> tuple[Matrix, list[int]]:
    """被約階段行列と、ピボットのある列の番号のリストを返す."""
    m = np.array(a, dtype=float)
    rows, cols = m.shape
    pivots: list[int] = []
    r = 0  # 次にピボットを置く行
    for c in range(cols):
        if r == rows:
            break
        p = r + int(np.argmax(np.abs(m[r:, c])))
        if abs(m[p, c]) < tol:
            continue  # この列にはピボットがない（自由変数の列）
        m[[r, p]] = m[[p, r]]
        m[r] /= m[r, c]  # ピボットを 1 にする
        for i in range(rows):
            if i != r:
                m[i] -= m[i, c] * m[r]  # ピボットの上下を 0 にする
        pivots.append(c)
        r += 1
    m[np.abs(m) < tol] = 0.0
    return m, pivots


def null_space_basis(a: ArrayLike) -> list[Matrix]:
    """零空間の基底を、自由変数を 1 つずつ 1 にした解として返す."""
    r, pivots = rref(a)
    cols = r.shape[1]
    free = [c for c in range(cols) if c not in pivots]
    basis = []
    for f in free:
        x = np.zeros(cols)
        x[f] = 1.0
        for row, p in enumerate(pivots):
            x[p] = -r[row, f] + 0.0  # + 0.0 で -0.0 を 0.0 にする
        basis.append(x)
    return basis


def report() -> None:
    """ランク、被約階段行列、4 つの基本部分空間の次元を表示する."""
    a = np.array([[1.0, 2.0, 1.0, 3.0],
                  [2.0, 4.0, 0.0, 2.0],
                  [3.0, 6.0, 1.0, 5.0]])
    r, pivots = rref(a)
    m, n = a.shape
    rank = len(pivots)
    print("被約階段行列 =")
    print(r)
    print("ピボットのある列（0 から数える）:", pivots)
    print("ランク =", rank, " np.linalg.matrix_rank =", np.linalg.matrix_rank(a))
    with np.printoptions(suppress=True):  # 丸め誤差の小さな値を 0 と表示する
        for x in null_space_basis(a):
            print("零空間の基底ベクトル", x, " a @ x =", a @ x)
    print(f"列空間の次元 {rank}、零空間の次元 {n - rank}（R^{n} の中）")
    print(f"行空間の次元 {rank}、左零空間の次元 {m - rank}（R^{m} の中）")
    y = np.array([1.0, 1.0, -1.0])
    print("左零空間の基底ベクトル", y, " y @ a =", y @ a)


def main() -> None:
    report()


if __name__ == "__main__":
    main()
