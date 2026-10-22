"""第 9 章の数値実験：2 次関数に対する勾配降下法。

f(x) = (1/2) x^T A x - b^T x（A は対称正定値行列）を勾配降下法で最小化し、
ステップ幅 eta によって収束の速さがどう変わるかを調べる。

実行方法:
    python ch09_gradient_descent.py
"""

import numpy as np
from numpy.typing import NDArray

Vector = NDArray[np.float64]
Matrix = NDArray[np.float64]

# 目的関数 f(x) = (1/2) x^T A x - b^T x の係数（固有値は 1 と 10）
A_MATRIX: Matrix = np.array([[1.0, 0.0], [0.0, 10.0]])
B_VECTOR: Vector = np.array([1.0, 1.0])

# 初期点
X0: Vector = np.array([-4.0, 2.0])


def objective(x: Vector) -> float:
    """目的関数 f(x) の値を返す。"""
    return float(0.5 * x @ A_MATRIX @ x - B_VECTOR @ x)


def gradient(x: Vector) -> Vector:
    """勾配 ∇f(x) = Ax - b を返す。"""
    result: Vector = A_MATRIX @ x - B_VECTOR
    return result


def gradient_descent(x0: Vector, eta: float, num_steps: int) -> list[Vector]:
    """ステップ幅 eta の勾配降下法を num_steps 回行い、点列 x_0, x_1, ... を返す。"""
    points = [x0.copy()]
    x = x0.copy()
    for _ in range(num_steps):
        x = x - eta * gradient(x)
        points.append(x.copy())
    return points


def contraction_rate(eta: float) -> float:
    """誤差の縮小率 max |1 - eta * lambda_i|（lambda_i は A の固有値）を返す。"""
    eigenvalues = np.linalg.eigvalsh(A_MATRIX)
    return float(np.max(np.abs(1.0 - eta * eigenvalues)))


def main() -> None:
    """いくつかのステップ幅で勾配降下法を実行し、最小点との距離を表示する。"""
    x_star: Vector = np.linalg.solve(A_MATRIX, B_VECTOR)
    eigenvalues = np.linalg.eigvalsh(A_MATRIX)
    mu = float(eigenvalues[0])
    big_l = float(eigenvalues[-1])
    print(f"最小点 x* = {x_star}, 固有値 mu = {mu}, L = {big_l}")
    print(f"収束する条件: 0 < eta < 2/L = {2.0 / big_l}")
    print(f"最適なステップ幅: 2/(mu+L) = {2.0 / (mu + big_l):.4f}")
    print()

    etas = [0.05, 0.15, 2.0 / (mu + big_l), 0.21]
    checkpoints = [0, 10, 20, 30, 40, 50]
    header = "eta      rate   " + "".join(f"k={k:<9d}" for k in checkpoints)
    print(header)
    for eta in etas:
        points = gradient_descent(X0, eta, checkpoints[-1])
        errors = [float(np.linalg.norm(points[k] - x_star)) for k in checkpoints]
        row = f"{eta:<8.4f} {contraction_rate(eta):<6.3f} "
        row += "".join(f"{e:<11.2e}" for e in errors)
        print(row)


if __name__ == "__main__":
    main()
