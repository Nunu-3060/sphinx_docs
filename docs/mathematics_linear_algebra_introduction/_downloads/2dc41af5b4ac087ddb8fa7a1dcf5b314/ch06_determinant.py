"""行列式の計算と性質を確かめる.

余因子展開による計算（定義どおりだが遅い）と、消去法による
np.linalg.det の結果を比べ、行列式の性質を数値で確かめる。

使い方: python ch06_determinant.py
"""

import numpy as np
from numpy.typing import NDArray

Matrix = NDArray[np.float64]


def det_cofactor(a: Matrix) -> float:
    """1 行目に沿った余因子展開で行列式を求める（n! に比例する計算量）."""
    n = a.shape[0]
    if n == 1:
        return float(a[0, 0])
    total = 0.0
    for j in range(n):
        minor = np.delete(np.delete(a, 0, axis=0), j, axis=1)  # 1 行目と j 列目を除く
        total += (-1) ** j * a[0, j] * det_cofactor(minor)
    return total


def report() -> None:
    """行列式の値と性質を表示する."""
    a = np.array([[2.0, 1.0, -1.0],
                  [-3.0, -1.0, 2.0],
                  [-2.0, 1.0, 2.0]])
    b = np.array([[1.0, 2.0, 0.0],
                  [0.0, 1.0, 3.0],
                  [4.0, 0.0, 1.0]])
    print("余因子展開:     det(a) =", det_cofactor(a))
    print("np.linalg.det: det(a) =", np.linalg.det(a))
    print(f"det(b) = {np.linalg.det(b):.6f}")
    print(f"det(a @ b) = {np.linalg.det(a @ b):.6f}")
    print(f"det(a) * det(b) = {np.linalg.det(a) * np.linalg.det(b):.6f}")
    print(f"det(a.T) = {np.linalg.det(a.T):.6f}")
    swapped = a[[1, 0, 2]]  # 1 行目と 2 行目を入れ替える
    print(f"行を入れ替えた行列の det = {np.linalg.det(swapped):.6f}")
    scaled = a.copy()
    scaled[0] *= 3  # 1 行目を 3 倍する
    print(f"1 行目を 3 倍した行列の det = {np.linalg.det(scaled):.6f}")


def main() -> None:
    report()


if __name__ == "__main__":
    main()
