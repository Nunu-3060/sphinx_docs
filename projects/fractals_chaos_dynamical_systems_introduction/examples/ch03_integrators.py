"""オイラー法と 4 次のルンゲ＝クッタ法の精度を、単振動で比べる.

単振動 x'' = -x は、初期値 (x, v) = (1, 0) のとき厳密解 x = cos t, v = -sin t を持つ。
エネルギー x^2 + v^2 は常に 1 に保たれる。

使い方: python ch03_integrators.py [--save DIR]
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import ode
import plot_util
from ode import Vector


def oscillator(state: Vector) -> Vector:
    """単振動 x'' = -x を 1 階の連立方程式 x' = v, v' = -x として表した右辺."""
    return np.stack([state[..., 1], -state[..., 0]], axis=-1)


def final_error(step: ode.Stepper, dt: float, t_end: float = 10.0) -> float:
    """時刻 t_end での数値解と厳密解の距離を返す."""
    n = round(t_end / dt)
    xs = ode.integrate(oscillator, np.array([1.0, 0.0]), dt, n, step)
    exact = np.array([np.cos(n * dt), -np.sin(n * dt)])
    return float(np.linalg.norm(xs[-1] - exact))


def create_figures() -> dict[str, Figure]:
    """相平面上の軌道（orbits）と、刻み幅と誤差の関係（errors）の図を作る."""
    dt = 0.1
    x0 = np.array([1.0, 0.0])
    euler = ode.integrate(oscillator, x0, dt, 300, ode.euler_step)
    rk4 = ode.integrate(oscillator, x0, dt, 300, ode.rk4_step)
    fig1, ax1 = plt.subplots(figsize=(5.4, 5.0))
    t = np.linspace(0.0, 2.0 * np.pi, 200)
    ax1.plot(np.cos(t), -np.sin(t), color="0.6", linewidth=4.0, label="厳密解")
    ax1.plot(euler[:, 0], euler[:, 1], color="C3", linewidth=1.0, label="オイラー法")
    ax1.plot(rk4[:, 0], rk4[:, 1], color="C0", linewidth=1.0, linestyle="--", label="ルンゲ＝クッタ法")
    ax1.set_aspect("equal")
    ax1.set_xlabel("$x$")
    ax1.set_ylabel("$v$")
    ax1.set_title(f"$\\Delta t = {dt}$, 300 ステップ")
    ax1.legend(loc="upper right", fontsize=9)
    fig1.tight_layout()

    dts = np.array([0.2, 0.1, 0.05, 0.02, 0.01, 0.005])
    fig2, ax2 = plt.subplots(figsize=(5.6, 4.4))
    for step, label, marker in ((ode.euler_step, "オイラー法", "o"), (ode.rk4_step, "ルンゲ＝クッタ法", "s")):
        errors = [final_error(step, float(dt)) for dt in dts]
        ax2.loglog(dts, errors, marker=marker, label=label)
    ax2.set_xlabel("刻み幅 $\\Delta t$")
    ax2.set_ylabel("$t = 10$ での誤差")
    ax2.grid(True, which="both", color="0.9")
    ax2.legend()
    fig2.tight_layout()
    return {"orbits": fig1, "errors": fig2}


def report() -> None:
    """刻み幅を半分にしたときに、誤差が何分の 1 になるかを表示する."""
    print("  dt      オイラー法   比     ルンゲ＝クッタ法  比")
    prev: tuple[float, float] | None = None
    for dt in (0.1, 0.05, 0.025, 0.0125):
        e1 = final_error(ode.euler_step, dt)
        e4 = final_error(ode.rk4_step, dt)
        if prev is None:
            print(f"{dt:7.4f}  {e1:.3e}         {e4:.3e}")
        else:
            print(f"{dt:7.4f}  {e1:.3e}  {prev[0] / e1:5.1f}  {e4:.3e}       {prev[1] / e4:5.1f}")
        prev = (e1, e4)


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures, report)


if __name__ == "__main__":
    main()
