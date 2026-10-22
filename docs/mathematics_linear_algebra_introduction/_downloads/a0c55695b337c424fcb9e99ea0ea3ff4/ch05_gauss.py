"""ガウスの消去法で連立一次方程式を解く.

前進消去で拡大係数行列を上三角の形にし、後退代入で解を求める。
pivoting=True のときは、各列で絶対値が最大の行をピボットの行に選ぶ
（部分ピボット選択。第 13 章で扱う）。

使い方: python ch05_gauss.py
"""

import numpy as np
from numpy.typing import ArrayLike, NDArray

Vector = NDArray[np.float64]


def gaussian_elimination(a: ArrayLike, b: ArrayLike, pivoting: bool = False,
                         verbose: bool = False) -> Vector:
    """ガウスの消去法で a x = b を解き、x を返す."""
    # 拡大係数行列 [a | b] を作る（元の配列は書き換えない）
    m = np.hstack([np.array(a, dtype=float), np.array(b, dtype=float).reshape(-1, 1)])
    n = m.shape[0]

    # 前進消去: k 列目の、k 行目より下の成分を 0 にする
    for k in range(n - 1):
        if pivoting:
            p = k + int(np.argmax(np.abs(m[k:, k])))
            if p != k:
                m[[k, p]] = m[[p, k]]  # 行を入れ替える
                if verbose:
                    print(f"行 {k + 1} と行 {p + 1} を入れ替える")
        if m[k, k] == 0.0:
            raise ZeroDivisionError(f"ピボットが 0 になった（{k + 1} 列目）")
        for i in range(k + 1, n):
            factor = m[i, k] / m[k, k]
            m[i] -= factor * m[k]  # 行 i から、行 k の factor 倍を引く
        if verbose:
            print(f"{k + 1} 列目の消去の後:")
            print(m)

    # 後退代入: 下の行から順に未知数を求める
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (m[i, -1] - m[i, i + 1:n] @ x[i + 1:]) / m[i, i]
    return x


def report() -> None:
    """3 元連立一次方程式を消去法で解き、途中経過と解を表示する."""
    a = [[2.0, 1.0, -1.0],
         [-3.0, -1.0, 2.0],
         [-2.0, 1.0, 2.0]]
    b = [8.0, -11.0, -3.0]
    with np.printoptions(precision=3, suppress=True):
        x = gaussian_elimination(a, b, verbose=True)
        print("解 x =", x)
        print("np.linalg.solve の解 =", np.linalg.solve(a, b))


def main() -> None:
    report()


if __name__ == "__main__":
    main()
