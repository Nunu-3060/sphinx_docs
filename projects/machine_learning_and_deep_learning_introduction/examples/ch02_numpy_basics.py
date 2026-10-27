"""第 2 章: NumPy によるベクトル・行列演算と数値微分の確認。

実行方法:
    python ch02_numpy_basics.py
"""
from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


def show_vector_and_matrix() -> None:
    """ベクトルの内積、行列とベクトルの積、ブロードキャストを確認する。"""
    x = np.array([1.0, 2.0, 3.0])
    w = np.array([0.5, -1.0, 2.0])
    print("内積 w・x =", w @ x)

    a = np.array([[1.0, 2.0, 3.0],
                  [4.0, 5.0, 6.0]])
    print("行列とベクトルの積 A x =", a @ x)

    # 各行 (サンプル) から列ごとの平均を引く。形状 (2, 3) と (3,) の演算がブロードキャストされる。
    centered = a - a.mean(axis=0)
    print("列ごとに平均を引いた行列:\n", centered)


def f(p: FloatArray) -> float:
    """f(x, y) = x^2 + 3y^2"""
    return float(p[0] ** 2 + 3.0 * p[1] ** 2)


def analytic_grad(p: FloatArray) -> FloatArray:
    """f の勾配を手計算した式 (2x, 6y)。"""
    return np.array([2.0 * p[0], 6.0 * p[1]])


def numerical_grad(func: Callable[[FloatArray], float], p: FloatArray, h: float = 1e-5) -> FloatArray:
    """中心差分で勾配を近似する。"""
    grad = np.zeros_like(p)
    for i in range(p.size):
        step = np.zeros_like(p)
        step[i] = h
        grad[i] = (func(p + step) - func(p - step)) / (2.0 * h)
    return grad


def main() -> None:
    show_vector_and_matrix()

    p = np.array([1.0, 2.0])
    print("解析的な勾配:", analytic_grad(p))
    print("数値微分による勾配:", numerical_grad(f, p))


if __name__ == "__main__":
    main()
