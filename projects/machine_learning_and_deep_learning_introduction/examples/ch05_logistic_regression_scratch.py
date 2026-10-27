"""第 5 章: ロジスティック回帰を NumPy でスクラッチ実装する。

2 つの正規分布から生成した 2 次元データを、勾配降下法で学習したロジスティック回帰で分類する。

実行方法:
    python ch05_logistic_regression_scratch.py
"""
import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


def make_data(n_per_class: int, seed: int = 0) -> tuple[FloatArray, FloatArray]:
    """クラス 0 とクラス 1 のデータを作る。"""
    rng = np.random.default_rng(seed)
    x0 = rng.normal([-1.0, -1.0], 1.0, size=(n_per_class, 2))
    x1 = rng.normal([1.5, 1.0], 1.0, size=(n_per_class, 2))
    x = np.vstack([x0, x1])
    y = np.concatenate([np.zeros(n_per_class), np.ones(n_per_class)])
    return x, y


def sigmoid(z: FloatArray) -> FloatArray:
    """シグモイド関数。"""
    result: FloatArray = 1.0 / (1.0 + np.exp(-z))
    return result


def binary_cross_entropy(y: FloatArray, p: FloatArray, eps: float = 1e-12) -> float:
    """2 値交差エントロピー。log(0) を避けるため確率を [eps, 1 - eps] に収める。"""
    p = np.clip(p, eps, 1.0 - eps)
    return float(-np.mean(y * np.log(p) + (1.0 - y) * np.log(1.0 - p)))


def fit(x: FloatArray, y: FloatArray, lr: float = 0.5, epochs: int = 1000) -> tuple[FloatArray, float]:
    """重み w とバイアス b を勾配降下法で学習する。"""
    n, d = x.shape
    w = np.zeros(d)
    b = 0.0
    for epoch in range(epochs):
        p = sigmoid(x @ w + b)
        # 交差エントロピーをシグモイドの入力で微分すると (p - y) という単純な形になる
        error = p - y
        w -= lr * (x.T @ error) / n
        b -= lr * float(np.mean(error))
        if epoch % 200 == 0:
            print(f"epoch {epoch:4d}: loss = {binary_cross_entropy(y, p):.4f}")
    return w, b


def predict(x: FloatArray, w: FloatArray, b: float) -> FloatArray:
    """確率 0.5 をしきい値としてクラスを予測する。"""
    result: FloatArray = (sigmoid(x @ w + b) >= 0.5).astype(np.float64)
    return result


def main() -> None:
    x, y = make_data(100)
    w, b = fit(x, y)
    accuracy = float(np.mean(predict(x, w, b) == y))
    print(f"w = {w}, b = {b:.3f}")
    print(f"訓練データでの正解率 = {accuracy:.3f}")

    new_point = np.array([[0.0, 0.5]])
    print("点 (0.0, 0.5) がクラス 1 である確率:", sigmoid(new_point @ w + b))


if __name__ == "__main__":
    main()
