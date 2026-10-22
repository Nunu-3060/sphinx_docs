"""特異値分解の計算と、擬似逆行列による最小ノルム解.

2 行 3 列の行列 a を a = U Σ V^T と分解し、a^T a の固有値が
特異値の 2 乗になることを確かめる。また、擬似逆行列を使って、
解が無数にある方程式 a x = b のうちノルムが最小の解を求める。

使い方: python ch12_svd.py
"""

import numpy as np


def report() -> None:
    """特異値分解と擬似逆行列の結果を表示する."""
    a = np.array([[3.0, 2.0, 2.0],
                  [2.0, 3.0, -2.0]])
    u, s, vt = np.linalg.svd(a)
    with np.printoptions(precision=4, suppress=True):
        print("特異値 =", s)
        print("U =")
        print(u)
        print("V^T =")
        print(vt)
        sigma = np.zeros(a.shape)
        sigma[:2, :2] = np.diag(s)
        print("U Σ V^T == a:", np.allclose(u @ sigma @ vt, a))
        print("a^T a の固有値 =", np.linalg.eigvalsh(a.T @ a)[::-1])

        b = np.array([5.0, 5.0])
        x = np.linalg.pinv(a) @ b
        print("擬似逆行列による解 x =", x, " a @ x =", a @ x)
        print(f"|x| = {np.linalg.norm(x):.4f}")
        x_other = x + vt[2]  # 零空間のベクトルを加えても解である
        print("別の解 x + v3 =", x_other, " a @ (x + v3) =", a @ x_other)
        print(f"|x + v3| = {np.linalg.norm(x_other):.4f}")


def main() -> None:
    report()


if __name__ == "__main__":
    main()
