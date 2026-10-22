"""逆行列を求め、元の行列との積が単位行列になることを確かめる.

正則でない（行列式が 0 の）行列の逆行列を求めようとすると、
np.linalg.inv は LinAlgError を送出する。

使い方: python ch06_inverse.py
"""

import numpy as np


def report() -> None:
    """逆行列の計算結果を表示する."""
    a = np.array([[2.0, 1.0],
                  [5.0, 3.0]])
    a_inv = np.linalg.inv(a)
    with np.printoptions(precision=3, suppress=True):
        print(f"det(a) = {np.linalg.det(a):.3f}")
        print("a の逆行列 =")
        print(a_inv)
        print("a @ a_inv =")
        print(a @ a_inv)

        b = np.array([4.0, 11.0])
        print("a_inv @ b =", a_inv @ b)
        print("np.linalg.solve(a, b) =", np.linalg.solve(a, b))

    singular = np.array([[1.0, 2.0],
                         [2.0, 4.0]])
    try:
        np.linalg.inv(singular)
    except np.linalg.LinAlgError as error:
        print("正則でない行列の逆行列:", error)


def main() -> None:
    report()


if __name__ == "__main__":
    main()
