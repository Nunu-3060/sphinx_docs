"""LU 分解: 係数行列を下三角行列 L と上三角行列 U の積に分解して解く.

一度分解しておけば、右辺 b が変わっても、前進代入と後退代入だけで
解を求められる。ここでは簡単のため、ピボット選択をしない。

使い方: python ch05_lu.py
"""

import numpy as np
from numpy.typing import ArrayLike, NDArray

Matrix = NDArray[np.float64]


def lu_decompose(a: ArrayLike) -> tuple[Matrix, Matrix]:
    """a = L U となる単位下三角行列 L と上三角行列 U を返す."""
    u = np.array(a, dtype=float)
    n = u.shape[0]
    lower = np.eye(n)
    for k in range(n - 1):
        for i in range(k + 1, n):
            lower[i, k] = u[i, k] / u[k, k]  # 消去に使った倍率を L に記録する
            u[i] -= lower[i, k] * u[k]
    return lower, u


def lu_solve(lower: Matrix, upper: Matrix, b: ArrayLike) -> Matrix:
    """LU 分解の結果を使って a x = b を解く."""
    n = lower.shape[0]
    rhs = np.array(b, dtype=float)
    # 前進代入: L y = b
    y = np.zeros(n)
    for i in range(n):
        y[i] = rhs[i] - lower[i, :i] @ y[:i]
    # 後退代入: U x = y
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - upper[i, i + 1:] @ x[i + 1:]) / upper[i, i]
    return x


def report() -> None:
    """LU 分解の結果と、2 つの右辺に対する解を表示する."""
    a = np.array([[2.0, 1.0, -1.0],
                  [-3.0, -1.0, 2.0],
                  [-2.0, 1.0, 2.0]])
    lower, upper = lu_decompose(a)
    with np.printoptions(precision=3, suppress=True):
        print("L =")
        print(lower)
        print("U =")
        print(upper)
        print("L @ U == a:", np.allclose(lower @ upper, a))
        for b in ([8.0, -11.0, -3.0], [1.0, 0.0, 0.0]):
            print(f"b = {b} の解 x =", lu_solve(lower, upper, b))


def main() -> None:
    report()


if __name__ == "__main__":
    main()
