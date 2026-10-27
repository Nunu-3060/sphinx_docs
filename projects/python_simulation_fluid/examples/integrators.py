"""時間積分法の比較。

ばね振動子(質量 1、ばね定数 1)の運動を 3 種類の時間積分法で解き、
位置の時間変化と力学的エネルギーの変化を厳密解と比較する。

実行方法::

    python integrators.py
"""
from collections.abc import Callable

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

FloatArray = npt.NDArray[np.float64]

# 位置 x を受け取り、加速度を返す関数
Acceleration = Callable[[float], float]
# (x, v, dt, 加速度関数) を受け取り、1 ステップ後の (x, v) を返す関数
Stepper = Callable[[float, float, float, Acceleration], tuple[float, float]]


def spring_acceleration(x: float) -> float:
    """ばね振動子の加速度 a = -(k / m) x を返す(k = m = 1)。"""
    return -x


def explicit_euler(x: float, v: float, dt: float, accel: Acceleration) -> tuple[float, float]:
    """陽的オイラー法: 現在の速度と加速度だけを使って更新する。"""
    a = accel(x)
    return x + v * dt, v + a * dt


def semi_implicit_euler(x: float, v: float, dt: float, accel: Acceleration) -> tuple[float, float]:
    """半陰的オイラー法: 先に速度を更新し、新しい速度で位置を更新する。"""
    v_new = v + accel(x) * dt
    x_new = x + v_new * dt
    return x_new, v_new


def velocity_verlet(x: float, v: float, dt: float, accel: Acceleration) -> tuple[float, float]:
    """速度ベルレ法: 更新前後の 2 つの加速度の平均で速度を更新する。"""
    a = accel(x)
    x_new = x + v * dt + 0.5 * a * dt**2
    v_new = v + 0.5 * (a + accel(x_new)) * dt
    return x_new, v_new


def simulate(stepper: Stepper, x0: float, v0: float, dt: float, n_steps: int) -> tuple[FloatArray, FloatArray]:
    """指定した積分法で n_steps ステップ進め、位置と速度の履歴を返す。"""
    xs = np.empty(n_steps + 1)
    vs = np.empty(n_steps + 1)
    xs[0], vs[0] = x0, v0
    x, v = x0, v0
    for n in range(n_steps):
        x, v = stepper(x, v, dt, spring_acceleration)
        xs[n + 1], vs[n + 1] = x, v
    return xs, vs


def energy(x: FloatArray, v: FloatArray) -> FloatArray:
    """力学的エネルギー(運動エネルギー + ばねのエネルギー)を返す。"""
    return 0.5 * v**2 + 0.5 * x**2


METHODS: dict[str, Stepper] = {
    "陽的オイラー法": explicit_euler,
    "半陰的オイラー法": semi_implicit_euler,
    "速度ベルレ法": velocity_verlet,
}


def main() -> None:
    dt = 0.1
    n_steps = 300
    t = np.arange(n_steps + 1) * dt

    plt.rcParams["font.family"] = ["Meiryo", "sans-serif"]
    fig, (ax_x, ax_e) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    ax_x.plot(t, np.cos(t), "k--", label="厳密解")
    for name, stepper in METHODS.items():
        xs, vs = simulate(stepper, 1.0, 0.0, dt, n_steps)
        ax_x.plot(t, xs, label=name)
        ax_e.plot(t, energy(xs, vs), label=name)
    ax_x.set_ylabel("位置 x")
    ax_x.legend(loc="upper left")
    ax_e.set_xlabel("時刻 t")
    ax_e.set_ylabel("エネルギー E")
    ax_e.set_ylim(0.0, 2.0)
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
