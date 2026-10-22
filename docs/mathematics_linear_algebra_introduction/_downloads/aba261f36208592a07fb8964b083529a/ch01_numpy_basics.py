"""NumPy の配列の基本: ベクトルと行列を作り、形状と演算を確かめる.

使い方: python ch01_numpy_basics.py
"""

import numpy as np


def report() -> None:
    """ベクトルと行列を作り、形状、成分、演算の結果を表示する."""
    v = np.array([1.0, 2.0, 3.0])  # 3 次元のベクトル
    a = np.array([[1.0, 2.0, 3.0],
                  [4.0, 5.0, 6.0]])  # 2 行 3 列の行列

    print("v =", v)
    print("v.shape =", v.shape)
    print("a =")
    print(a)
    print("a.shape =", a.shape)
    print("a[1, 2] =", a[1, 2])  # 2 行 3 列目の成分（添字は 0 から数える）
    print("a[:, 0] =", a[:, 0])  # 1 列目
    print("a @ v =", a @ v)  # 行列とベクトルの積
    print("2 * a =")
    print(2 * a)  # スカラー倍
    print("a.T =")
    print(a.T)  # 転置


def main() -> None:
    report()


if __name__ == "__main__":
    main()
