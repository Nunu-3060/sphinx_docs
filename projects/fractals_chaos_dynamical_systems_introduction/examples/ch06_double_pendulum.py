"""二重振り子: 摩擦のない（エネルギーが保存される）系のカオス.

2 つのおもりの質量と棒の長さをすべて 1、重力加速度を g とする。状態は
2 本の棒の角度 θ1, θ2（真下から測る）と角速度 ω1, ω2 である。

使い方: python ch06_double_pendulum.py [--save DIR]
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from PIL import Image, ImageDraw

import ode
import plot_util
from ode import Vector

G = 9.81


def double_pendulum(state: Vector) -> Vector:
    """二重振り子の運動方程式（質量と長さがすべて 1 の場合）の右辺."""
    t1, t2, w1, w2 = state[..., 0], state[..., 1], state[..., 2], state[..., 3]
    d = t1 - t2
    den = 3.0 - np.cos(2.0 * d)
    a1 = (-3.0 * G * np.sin(t1) - G * np.sin(t1 - 2.0 * t2)
          - 2.0 * np.sin(d) * (w2**2 + w1**2 * np.cos(d))) / den
    a2 = 2.0 * np.sin(d) * (2.0 * w1**2 + 2.0 * G * np.cos(t1) + w2**2 * np.cos(d)) / den
    return np.stack([w1, w2, a1, a2], axis=-1)


def energy(state: Vector) -> Vector:
    """力学的エネルギー（運動エネルギーと位置エネルギーの和）."""
    t1, t2, w1, w2 = state[..., 0], state[..., 1], state[..., 2], state[..., 3]
    kinetic = w1**2 + 0.5 * w2**2 + w1 * w2 * np.cos(t1 - t2)
    potential = -G * (2.0 * np.cos(t1) + np.cos(t2))
    result: Vector = kinetic + potential
    return result


def simulate(theta1: float, theta2: float, dt: float, n: int) -> Vector:
    """静止した状態から振り子を離し、n ステップの状態を返す."""
    return ode.integrate(double_pendulum, np.array([theta1, theta2, 0.0, 0.0]), dt, n)


def tip_positions(states: Vector) -> tuple[Vector, Vector]:
    """2 つ目のおもりの座標 (x, y) を返す（支点を原点とし、上向きを y の正とする）."""
    t1, t2 = states[:, 0], states[:, 1]
    x = np.sin(t1) + np.sin(t2)
    y = -np.cos(t1) - np.cos(t2)
    return x, y


def create_figures() -> dict[str, Figure]:
    """2 つ目のおもりの軌跡（tip）と、初期角度がわずかに違う 2 つの振り子の角度の時系列（divergence）を作る."""
    dt = 0.002
    a = simulate(2.0, 2.0, dt, 10000)
    b = simulate(2.0, 2.0 + 1e-6, dt, 10000)
    x, y = tip_positions(a)
    fig1, ax1 = plt.subplots(figsize=(5.0, 5.0))
    ax1.plot(x, y, linewidth=0.4)
    ax1.plot(0.0, 0.0, "o", color="k")
    ax1.set_xlim(-2.1, 2.1)
    ax1.set_ylim(-2.1, 2.1)
    ax1.set_aspect("equal")
    ax1.set_title("2 つ目のおもりの軌跡（20 秒間）")
    fig1.tight_layout()

    t = np.arange(len(a)) * dt
    fig2, ax2 = plt.subplots(figsize=(10.0, 3.4))
    ax2.plot(t, a[:, 1], linewidth=0.9, label="$\\theta_2(0) = 2$")
    ax2.plot(t, b[:, 1], linewidth=0.9, linestyle="--", label="$\\theta_2(0) = 2 + 10^{-6}$")
    ax2.set_xlabel("時刻 $t$")
    ax2.set_ylabel("$\\theta_2$")
    ax2.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0))
    ax2.grid(True, color="0.9")
    fig2.tight_layout()
    return {"tip": fig1, "divergence": fig2}


def report() -> None:
    """数値計算でエネルギーがどれだけ保たれているかを表示する."""
    states = simulate(2.0, 2.0, 0.002, 10000)
    e = energy(states)
    print(f"エネルギーの初期値: {e[0]:.6f}")
    print(f"20 秒間のエネルギーの変化の最大値: {np.max(np.abs(e - e[0])):.2e}")


def create_animation(path: Path) -> None:
    """初期角度が 0.001 ラジアンだけ違う 3 つの振り子を重ねた GIF アニメーションを保存する."""
    size = 240
    scale = size / 4.6
    center = size / 2.0
    dt = 0.002
    frame_step = 20  # 20 ステップ（0.04 秒）ごとに 1 コマ
    colors = [(31, 119, 180), (214, 39, 40), (44, 160, 44)]
    runs = [simulate(2.0, 2.0 + k * 1e-3, dt, 7500) for k in range(3)]
    frames = []
    for i in range(0, 7501, frame_step):
        image = Image.new("RGB", (size, size), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        for states, color in zip(runs, colors):
            t1, t2 = states[i, 0], states[i, 1]
            p1 = (center + scale * np.sin(t1), center + scale * np.cos(t1))
            p2 = (p1[0] + scale * np.sin(t2), p1[1] + scale * np.cos(t2))
            draw.line([(center, center), p1, p2], fill=color, width=2)
            for px, py in (p1, p2):
                draw.ellipse((px - 4, py - 4, px + 4, py + 4), fill=color)
        draw.ellipse((center - 3, center - 3, center + 3, center + 3), fill=(0, 0, 0))
        draw.text((6, 6), f"t = {i * dt:4.1f}", fill=(0, 0, 0))
        frames.append(image.quantize(colors=16))
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=40, loop=0, optimize=True)


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures, report, create_animation)


if __name__ == "__main__":
    main()
