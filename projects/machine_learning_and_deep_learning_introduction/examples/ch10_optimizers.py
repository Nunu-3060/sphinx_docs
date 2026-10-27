"""第 10 章: 最適化手法 (SGD、モメンタム、Adam) を NumPy で実装して比較する。

細長い谷の形をした関数 f(x, y) = 0.05 x^2 + 2 y^2 の最小値 (0, 0) を探す。

実行方法:
    python ch10_optimizers.py
"""
import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]


def f(p: FloatArray) -> float:
    return float(0.05 * p[0] ** 2 + 2.0 * p[1] ** 2)


def grad_f(p: FloatArray) -> FloatArray:
    return np.array([0.1 * p[0], 4.0 * p[1]])


class SGD:
    """確率的勾配降下法: p <- p - lr * g"""

    def __init__(self, lr: float) -> None:
        self.lr = lr

    def step(self, p: FloatArray, g: FloatArray) -> FloatArray:
        return p - self.lr * g


class Momentum:
    """モメンタム: 過去の更新方向 (速度) を引き継ぐ。"""

    def __init__(self, lr: float, beta: float = 0.9) -> None:
        self.lr = lr
        self.beta = beta
        self.v: FloatArray | None = None

    def step(self, p: FloatArray, g: FloatArray) -> FloatArray:
        if self.v is None:
            self.v = np.zeros_like(p)
        self.v = self.beta * self.v - self.lr * g
        return p + self.v


class Adam:
    """Adam: 勾配の移動平均 (1 次モーメント) と勾配の 2 乗の移動平均 (2 次モーメント) を使う。"""

    def __init__(self, lr: float, beta1: float = 0.9, beta2: float = 0.999, eps: float = 1e-8) -> None:
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m: FloatArray | None = None
        self.v: FloatArray | None = None
        self.t = 0

    def step(self, p: FloatArray, g: FloatArray) -> FloatArray:
        if self.m is None or self.v is None:
            self.m = np.zeros_like(p)
            self.v = np.zeros_like(p)
        self.t += 1
        self.m = self.beta1 * self.m + (1.0 - self.beta1) * g
        self.v = self.beta2 * self.v + (1.0 - self.beta2) * g ** 2
        # 初期値を 0 にしたことによる偏りを補正する
        m_hat = self.m / (1.0 - self.beta1 ** self.t)
        v_hat = self.v / (1.0 - self.beta2 ** self.t)
        result: FloatArray = p - self.lr * m_hat / (np.sqrt(v_hat) + self.eps)
        return result


def run(optimizer: SGD | Momentum | Adam, steps: int = 100) -> FloatArray:
    p = np.array([-8.0, 2.0])
    for _ in range(steps):
        p = optimizer.step(p, grad_f(p))
    return p


def main() -> None:
    optimizers: dict[str, SGD | Momentum | Adam] = {
        "SGD (lr=0.4)": SGD(lr=0.4),
        "モメンタム (lr=0.1)": Momentum(lr=0.1),
        "Adam (lr=0.5)": Adam(lr=0.5),
    }
    for name, opt in optimizers.items():
        p = run(opt)
        print(f"{name}: 100 ステップ後の位置 = ({p[0]: .4f}, {p[1]: .4f}), f = {f(p):.6f}")


if __name__ == "__main__":
    main()
