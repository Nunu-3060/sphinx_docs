"""グラム・シュミットの直交化で、行列を QR 分解する.

a の列ベクトルを順に直交化して正規直交基底 q1、q2、q3 を作る。
Q は q を列に並べた行列、R = Q^T a は上三角行列になり、a = QR が成り立つ。

使い方: python ch09_gram_schmidt.py
"""

import numpy as np
from numpy.typing import NDArray

Matrix = NDArray[np.float64]


def gram_schmidt(a: Matrix) -> Matrix:
    """a の列ベクトルを直交化し、正規直交基底を列に並べた行列を返す."""
    q = np.zeros_like(a, dtype=float)
    for j in range(a.shape[1]):
        v = a[:, j].astype(float)
        for i in range(j):
            v -= (q[:, i] @ a[:, j]) * q[:, i]  # 求めた基底の方向の成分を除く
        q[:, j] = v / np.linalg.norm(v)  # 長さを 1 にする
    return q


def report() -> None:
    """Q、R と、NumPy の QR 分解の結果を表示する."""
    a = np.array([[1.0, 1.0, 0.0],
                  [1.0, 0.0, 1.0],
                  [0.0, 1.0, 1.0]])
    q = gram_schmidt(a)
    r = q.T @ a
    with np.printoptions(precision=4, suppress=True):
        print("Q =")
        print(q)
        print("Q.T @ Q =")
        print(q.T @ q)
        print("R = Q.T @ a =")
        print(r)
        print("Q @ R == a:", np.allclose(q @ r, a))
        q_np, r_np = np.linalg.qr(a)
        print("np.linalg.qr の R =")
        print(r_np)  # 列の符号が反対になることがある


def main() -> None:
    report()


if __name__ == "__main__":
    main()
