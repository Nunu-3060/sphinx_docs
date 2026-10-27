"""第 4 章: 線形回帰を NumPy でスクラッチ実装する。

正規方程式による解析解と、勾配降下法による解を比較する。

実行方法:
    python ch04_linear_regression_scratch.py
"""
import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


def make_data(n: int, seed: int = 0) -> tuple[FloatArray, FloatArray]:
    """y = 3x + 2 にノイズを加えたデータを作る。"""
    rng = np.random.default_rng(seed)
    x = rng.uniform(0.0, 2.0, size=(n, 1))
    y = 3.0 * x[:, 0] + 2.0 + rng.normal(0.0, 0.3, size=n)
    return x, y


def add_bias_column(x: FloatArray) -> FloatArray:
    """先頭に値が 1 の列を追加し、切片をパラメータの一部として扱えるようにする。"""
    return np.hstack([np.ones((x.shape[0], 1)), x])


def mse(y_true: FloatArray, y_pred: FloatArray) -> float:
    """平均二乗誤差。"""
    return float(np.mean((y_true - y_pred) ** 2))


def fit_normal_equation(x: FloatArray, y: FloatArray) -> FloatArray:
    """正規方程式 (X^T X) w = X^T y を解く。"""
    xb = add_bias_column(x)
    w: FloatArray = np.linalg.solve(xb.T @ xb, xb.T @ y)
    return w


def fit_gradient_descent(x: FloatArray, y: FloatArray, lr: float = 0.1, epochs: int = 500) -> FloatArray:
    """勾配降下法で平均二乗誤差を最小化する。"""
    xb = add_bias_column(x)
    n = xb.shape[0]
    w = np.zeros(xb.shape[1])
    for epoch in range(epochs):
        y_pred = xb @ w
        grad = (2.0 / n) * xb.T @ (y_pred - y)
        w -= lr * grad
        if epoch % 100 == 0:
            print(f"epoch {epoch:4d}: loss = {mse(y, y_pred):.4f}")
    return w


def main() -> None:
    x, y = make_data(100)

    w_exact = fit_normal_equation(x, y)
    print(f"正規方程式: 切片 = {w_exact[0]:.3f}, 傾き = {w_exact[1]:.3f}")

    w_gd = fit_gradient_descent(x, y)
    print(f"勾配降下法: 切片 = {w_gd[0]:.3f}, 傾き = {w_gd[1]:.3f}")

    y_pred = add_bias_column(x) @ w_gd
    print(f"訓練データでの MSE = {mse(y, y_pred):.4f}")


if __name__ == "__main__":
    main()
