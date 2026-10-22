"""部分空間への正射影と射影行列.

行列 a の列空間（平面）への正射影の行列 P = a (a^T a)^-1 a^T を作り、
P^2 = P、P^T = P であることと、誤差 b - Pb が列空間と直交することを確かめる。

使い方: python ch09_projection_matrix.py
"""

import numpy as np


def report() -> None:
    """射影行列と、b の正射影を表示する."""
    a = np.array([[1.0, 0.0],
                  [0.0, 1.0],
                  [1.0, 1.0]])  # 列ベクトル a1 = (1, 0, 1)、a2 = (0, 1, 1)
    b = np.array([1.0, 2.0, 5.0])
    p_matrix = a @ np.linalg.inv(a.T @ a) @ a.T
    p = p_matrix @ b
    e = b - p
    with np.printoptions(precision=4, suppress=True):
        print("射影行列 P =")
        print(p_matrix)
        print("P @ P == P:", np.allclose(p_matrix @ p_matrix, p_matrix))
        print("P.T == P:", np.allclose(p_matrix.T, p_matrix))
        print("正射影 p = P @ b =", p)
        print("誤差 e = b - p =", e)
        print("a.T @ e =", a.T @ e)  # 各列ベクトルとの内積が 0


def main() -> None:
    report()


if __name__ == "__main__":
    main()
