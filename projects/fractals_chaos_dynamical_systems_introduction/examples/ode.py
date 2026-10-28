"""常微分方程式 dx/dt = f(x) を数値的に解く、共通モジュール（第 3 章）.

* euler_step()   オイラー法で 1 ステップ進める
* rk4_step()     4 次のルンゲ＝クッタ法で 1 ステップ進める
* integrate()    指定した方法で n ステップ進め、途中の状態をすべて返す

状態 x は NumPy の配列で、最後の軸が状態の成分を表す。たとえばローレンツ方程式の
状態は形が (3,) の配列である。形が (1000, 3) の配列を渡せば、1000 個の初期値を
まとめて（ベクトル化して）計算できる。
"""

from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray

Vector = NDArray[np.float64]
VectorField = Callable[[Vector], Vector]
Stepper = Callable[[VectorField, Vector, float], Vector]


def euler_step(f: VectorField, x: Vector, dt: float) -> Vector:
    """オイラー法: 現在の傾き f(x) のまま dt だけ進む."""
    return x + dt * f(x)


def rk4_step(f: VectorField, x: Vector, dt: float) -> Vector:
    """4 次のルンゲ＝クッタ法: 区間内の 4 か所の傾きを重み付きで平均して進む."""
    k1 = f(x)
    k2 = f(x + 0.5 * dt * k1)
    k3 = f(x + 0.5 * dt * k2)
    k4 = f(x + dt * k3)
    return x + dt / 6.0 * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def integrate(f: VectorField, x0: Vector, dt: float, n: int, step: Stepper = rk4_step) -> Vector:
    """初期値 x0 から n ステップ進め、x0 を含む n + 1 個の状態を返す.

    戻り値の形は (n + 1,) + x0.shape である。
    """
    xs = np.empty((n + 1,) + x0.shape)
    xs[0] = x0
    x = x0.astype(np.float64)
    for i in range(n):
        x = step(f, x, dt)
        xs[i + 1] = x
    return xs
