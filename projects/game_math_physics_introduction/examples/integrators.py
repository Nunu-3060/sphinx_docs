"""第 10 章: 数値積分の方法（オイラー法、半陰的オイラー法、速度ベルレ法）を比べる。

ばねにつながれたおもり（単振動）と、重力による放物運動をシミュレーションし、誤差を表示する。

実行方法:
    py integrators.py
"""

import math
from collections.abc import Callable

OMEGA = math.tau  # 単振動の角振動数（周期 1 秒）
GRAVITY = -9.8  # 重力加速度（メートル毎秒毎秒。上向きを正とする）

Acceleration = Callable[[float], float]  # 位置から加速度を求める関数
Stepper = Callable[[float, float, Acceleration, float], tuple[float, float]]


def explicit_euler(x: float, v: float, accel: Acceleration, dt: float) -> tuple[float, float]:
    """オイラー法: 今の速度で位置を、今の加速度で速度を進める。"""
    a = accel(x)
    return x + v * dt, v + a * dt


def semi_implicit_euler(x: float, v: float, accel: Acceleration, dt: float) -> tuple[float, float]:
    """半陰的オイラー法: 先に速度を進め、新しい速度で位置を進める。"""
    v_new = v + accel(x) * dt
    return x + v_new * dt, v_new


def velocity_verlet(x: float, v: float, accel: Acceleration, dt: float) -> tuple[float, float]:
    """速度ベルレ法: 加速度の項まで含めて位置を進め、前後の加速度の平均で速度を進める。"""
    a0 = accel(x)
    x_new = x + v * dt + 0.5 * a0 * dt * dt
    a1 = accel(x_new)
    return x_new, v + 0.5 * (a0 + a1) * dt


STEPPERS: dict[str, Stepper] = {
    'オイラー法': explicit_euler,
    '半陰的オイラー法': semi_implicit_euler,
    '速度ベルレ法': velocity_verlet,
}


def spring_acceleration(x: float) -> float:
    """ばねの力による加速度（位置に比例し、逆向き）。"""
    return -OMEGA * OMEGA * x


def gravity_acceleration(x: float) -> float:
    """重力による加速度（位置によらず一定）。"""
    return GRAVITY


def spring_energy(x: float, v: float) -> float:
    """単位質量あたりの力学的エネルギー（運動エネルギー + ばねの位置エネルギー）。"""
    return 0.5 * v * v + 0.5 * OMEGA * OMEGA * x * x


def simulate(stepper: Stepper, accel: Acceleration, x0: float, v0: float, dt: float,
             duration: float) -> list[tuple[float, float, float]]:
    """時刻 0 から duration まで dt ずつ進め、各時刻の (時刻, 位置, 速度) のリストを返す。"""
    steps = round(duration / dt)
    x, v = x0, v0
    history = [(0.0, x, v)]
    for i in range(1, steps + 1):
        x, v = stepper(x, v, accel, dt)
        history.append((i * dt, x, v))
    return history


def main() -> None:
    print('--- 単振動: 振幅 1 m で 10 秒間。エネルギーは本来変わらない（最初は 19.739） ---')
    for dt in (1 / 60, 1 / 20):
        print(f'dt = 1/{round(1 / dt)} 秒')
        for name, stepper in STEPPERS.items():
            _, x, v = simulate(stepper, spring_acceleration, 1.0, 0.0, dt, 10.0)[-1]
            print(f'  {name:<10} 10 秒後のエネルギー: {spring_energy(x, v):12.3f}')

    print('--- 放物運動: 初速 4.9 m/s で真上に投げる。最高点は本来 1.225 m（0.5 秒後） ---')
    for name, stepper in STEPPERS.items():
        history = simulate(stepper, gravity_acceleration, 0.0, 4.9, 1 / 10, 1.0)
        print(f'  {name:<10} 最高点: {max(x for _, x, _ in history):.3f} m（dt = 0.1 秒）')


if __name__ == '__main__':
    main()
