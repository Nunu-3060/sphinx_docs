"""身近な力学系の例: 離散時間の 3 つの写像と、連続時間の減衰振り子.

使い方: python ch01_first_systems.py [--save DIR]
"""

import math
from collections.abc import Callable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import ode
import plot_util
from ode import Vector


def iterate(f: Callable[[float], float], x0: float, n: int) -> list[float]:
    """x0 に写像 f を n 回適用し、x0 を含む n + 1 個の値（軌道）を返す."""
    xs = [x0]
    for _ in range(n):
        xs.append(f(xs[-1]))
    return xs


def damped_pendulum(state: Vector, gamma: float = 0.3) -> Vector:
    """減衰のある振り子 θ'' = -sin θ - γ θ' を、1 階の連立方程式として表した右辺."""
    theta, omega = state[..., 0], state[..., 1]
    return np.stack([omega, -np.sin(theta) - gamma * omega], axis=-1)


def create_figures() -> dict[str, Figure]:
    """離散時間の例（orbits）と、連続時間の例（pendulum）の図を作る."""
    n = 30
    steps = np.arange(n + 1)
    fig1, axes = plt.subplots(1, 3, figsize=(12.0, 3.4))
    examples = [
        ("複利 $x_{n+1} = 1.1\\,x_n$", lambda x: 1.1 * x, 1.0),
        ("個体数 $x_{n+1} = 2.8\\,x_n(1 - x_n)$", lambda x: 2.8 * x * (1.0 - x), 0.05),
        ("$x_{n+1} = \\cos x_n$", math.cos, 0.0),
    ]
    for ax, (title, f, x0) in zip(axes, examples):
        ax.plot(steps, iterate(f, x0, n), "o-", markersize=3.5, linewidth=1.0)
        ax.set_title(title)
        ax.set_xlabel("$n$")
        ax.set_ylabel("$x_n$")
        ax.grid(True, color="0.9")
    fig1.tight_layout()

    dt = 0.02
    xs = ode.integrate(damped_pendulum, np.array([2.5, 0.0]), dt, 2000)
    t = np.arange(len(xs)) * dt
    fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.0))
    ax1.plot(t, xs[:, 0], label="角度 $\\theta$")
    ax1.plot(t, xs[:, 1], label="角速度 $\\omega$")
    ax1.set_xlabel("時刻 $t$")
    ax1.set_title("時系列")
    ax1.legend()
    ax1.grid(True, color="0.9")
    ax2.plot(xs[:, 0], xs[:, 1], linewidth=1.2)
    ax2.plot(xs[0, 0], xs[0, 1], "o", color="C3", label="初期状態")
    ax2.plot(0.0, 0.0, "*", color="k", markersize=12, label="平衡点")
    ax2.set_xlabel("$\\theta$")
    ax2.set_ylabel("$\\omega$")
    ax2.set_title("相空間（相平面）での軌道")
    ax2.legend()
    ax2.grid(True, color="0.9")
    fig2.tight_layout()
    return {"orbits": fig1, "pendulum": fig2}


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures)


if __name__ == "__main__":
    main()
