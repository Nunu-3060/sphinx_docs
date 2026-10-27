"""投げ上げたボールの運動。

重力と空気抵抗(速度に比例する抵抗)を受けるボールの軌道を数値計算し、
厳密解と比較する。さらに、床で跳ね返るボールの運動も計算する。

実行方法::

    python projectile.py
"""
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

FloatArray = npt.NDArray[np.float64]

GRAVITY = np.array([0.0, -9.81])  # 重力加速度 [m/s^2]


def acceleration(vel: FloatArray, drag: float) -> FloatArray:
    """重力と線形の空気抵抗による加速度 g - b v を返す(b = drag)。"""
    return GRAVITY - drag * vel


def simulate_flight(pos0: FloatArray, vel0: FloatArray, drag: float, dt: float, t_end: float) -> FloatArray:
    """半陰的オイラー法で t_end まで計算し、位置の履歴(形状 (n + 1, 2))を返す。"""
    n_steps = round(t_end / dt)
    pos = pos0.copy()
    vel = vel0.copy()
    history = np.empty((n_steps + 1, 2))
    history[0] = pos
    for n in range(n_steps):
        vel = vel + acceleration(vel, drag) * dt
        pos = pos + vel * dt
        history[n + 1] = pos
    return history


def analytic_flight(pos0: FloatArray, vel0: FloatArray, drag: float, t: FloatArray) -> FloatArray:
    """線形の空気抵抗がある場合の厳密解(drag > 0)を、時刻 t の各点で返す。"""
    v_term = GRAVITY / drag  # 終端速度
    decay = (1.0 - np.exp(-drag * t))[:, np.newaxis] / drag
    return pos0 + v_term * t[:, np.newaxis] + (vel0 - v_term) * decay


def simulate_bounce(height: float, restitution: float, dt: float, t_end: float) -> FloatArray:
    """床(y = 0)で跳ね返るボールの高さの履歴を返す。空気抵抗は無視する。"""
    n_steps = round(t_end / dt)
    y, vy = height, 0.0
    history = np.empty(n_steps + 1)
    history[0] = y
    for n in range(n_steps):
        vy += GRAVITY[1] * dt
        y += vy * dt
        if y < 0.0:
            # 床にめり込んだら床の上へ押し戻し、速度を反転させて反発係数を掛ける
            y = -y
            vy = -restitution * vy
        history[n + 1] = y
    return history


def main() -> None:
    pos0 = np.array([0.0, 0.0])
    vel0 = np.array([10.0, 10.0])
    dt = 0.01
    t_end = 2.0
    t = np.linspace(0.0, t_end, round(t_end / dt) + 1)

    plt.rcParams["font.family"] = ["Meiryo", "sans-serif"]
    fig, (ax_fly, ax_bounce) = plt.subplots(1, 2, figsize=(11, 4))
    for drag in (0.0, 0.5, 1.0):
        traj = simulate_flight(pos0, vel0, drag, dt, t_end)
        ax_fly.plot(traj[:, 0], traj[:, 1], label=f"数値解 b = {drag}")
        if drag > 0.0:
            exact = analytic_flight(pos0, vel0, drag, t)
            ax_fly.plot(exact[:, 0], exact[:, 1], "k--", lw=1)
    ax_fly.set_xlabel("x [m]")
    ax_fly.set_ylabel("y [m]")
    ax_fly.set_ylim(bottom=0.0)
    ax_fly.legend()
    ax_fly.set_title("空気抵抗の有無による軌道の違い(破線は厳密解)")

    heights = simulate_bounce(height=2.0, restitution=0.8, dt=0.001, t_end=4.0)
    ax_bounce.plot(np.linspace(0.0, 4.0, heights.size), heights)
    ax_bounce.set_xlabel("時刻 t [s]")
    ax_bounce.set_ylabel("高さ y [m]")
    ax_bounce.set_title("床で跳ね返るボール(反発係数 0.8)")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
