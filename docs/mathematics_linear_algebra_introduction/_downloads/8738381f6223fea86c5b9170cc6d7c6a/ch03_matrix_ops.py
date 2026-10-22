"""行列の演算: 行列とベクトルの積の 2 つの見方、行列の積、転置.

使い方: python ch03_matrix_ops.py
"""

import numpy as np


def report() -> None:
    """行列の演算の結果を表示する."""
    a = np.array([[1.0, 2.0],
                  [3.0, 4.0]])
    b = np.array([[0.0, 1.0],
                  [1.0, 0.0]])
    x = np.array([5.0, 6.0])

    print("a @ x =", a @ x)
    # 見方 1: 列の線形結合
    print("x[0] * a[:, 0] + x[1] * a[:, 1] =", x[0] * a[:, 0] + x[1] * a[:, 1])
    # 見方 2: 各行とベクトルの内積
    print("[a[0] @ x, a[1] @ x] =", [float(a[0] @ x), float(a[1] @ x)])

    print("a @ b =")
    print(a @ b)  # 右から b を掛けると a の列が入れ替わる
    print("b @ a =")
    print(b @ a)  # 左から b を掛けると a の行が入れ替わる
    print("a @ b == b @ a:", np.array_equal(a @ b, b @ a))

    print("(a @ b).T == b.T @ a.T:", np.array_equal((a @ b).T, b.T @ a.T))
    i = np.eye(2)  # 単位行列
    print("a @ i == a:", np.array_equal(a @ i, a))


def main() -> None:
    report()


if __name__ == "__main__":
    main()
