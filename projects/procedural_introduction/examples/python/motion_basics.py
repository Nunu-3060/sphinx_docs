"""第 12 章「プロシージャルアニメーション」: 時間の関数としての動きと、ばねによる追従の図を作る。

* periodic_noise.png: 周期関数、1 次元ノイズ、2 次元ノイズによる揺れのグラフ
* spring_response.png: ばねと減衰による追従のステップ応答（減衰比と固有振動数を変える）
* spring_framerate.png: フレームレートを変えたときの追従の違い
"""

from __future__ import annotations

import math

import numpy as np

from common import FloatArray, output_dir, save_figure, setup_matplotlib
from noise import fbm, perlin2
from spring import smooth_toward, spring_step


def noise1(t: FloatArray, frequency: float, octaves: int = 1, seed: int = 0) -> FloatArray:
    """時刻 t の 1 次元ノイズ（-1〜1 程度）。

    2 次元ノイズの y = 0.5 の線上を使う。格子点の上（y が整数）を通ると、勾配ノイズは
    t × frequency が整数になるたびに 0 になり、動きが周期的に止まって見える。
    """
    return fbm(perlin2, t * frequency, np.full_like(t, 0.5), octaves=octaves, seed=seed)


def draw_periodic_noise(file_name: str) -> None:
    import matplotlib.pyplot as plt

    t = np.linspace(0.0, 3.0, 1200)
    figure, axes = plt.subplots(1, 3, figsize=(13, 3.6), gridspec_kw={"width_ratios": [1.4, 1.4, 1.0]})

    ax = axes[0]
    ax.plot(t, np.sin(2.0 * math.pi * 1.0 * t), label="sin（1 Hz）")
    ax.plot(t, 2.0 * (t * 1.0 % 1.0) - 1.0, label="のこぎり波 fract(t)")
    ax.plot(t, 2.0 * np.abs(np.sin(math.pi * 1.0 * t)) - 1.0, label="|sin|（弾む）")
    ax.plot(t, 2.0 * np.exp(-6.0 * (t % 1.0)) - 1.0, label="exp(-6 fract(t))（脈動）")
    ax.set_title("周期関数")

    ax = axes[1]
    ax.plot(t, noise1(t, 1.0, seed=1), label="ノイズ 1 Hz")
    ax.plot(t, noise1(t, 4.0, seed=2), label="ノイズ 4 Hz", alpha=0.8)
    ax.plot(t, noise1(t, 1.0, octaves=4, seed=3), label="fBm（4 オクターブ）")
    ax.set_title("1 次元ノイズ")

    for ax in axes[:2]:
        ax.set_xlabel("時刻 t [s]")
        ax.set_ylim(-1.3, 1.6)
        ax.grid(alpha=0.3)
        ax.legend(fontsize=8, loc="upper right", ncol=2)

    ax = axes[2]
    long_t = np.linspace(0.0, 10.0, 2000)
    for octaves, color in [(1, "#4c72b0"), (4, "#dd8452")]:
        x = noise1(long_t, 0.5, octaves, seed=10)
        y = noise1(long_t, 0.5, octaves, seed=20)
        ax.plot(x, y, color=color, lw=1.0, label=f"{octaves} オクターブ")
    ax.set_aspect("equal")
    ax.set_title("2 次元の揺れ（10 秒間の軌跡）")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def simulate_spring(frequency: float, damping: float, dt: float, duration: float) -> tuple[FloatArray, FloatArray]:
    """時刻 0 に目標値が 0 から 1 に変わったときの位置の変化（ステップ応答）を返す。"""
    steps = int(round(duration / dt))
    times = np.arange(steps + 1, dtype=np.float64) * dt
    x = np.zeros(1)
    v = np.zeros(1)
    target = np.ones(1)
    positions = [0.0]
    for _ in range(steps):
        x, v = spring_step(x, v, target, frequency, damping, dt)
        positions.append(float(x[0]))
    return times, np.array(positions)


def draw_spring_response(file_name: str) -> None:
    import matplotlib.pyplot as plt

    dt = 1.0 / 240.0
    figure, axes = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)
    for damping in [0.1, 0.3, 0.6, 1.0, 2.0]:
        times, x = simulate_spring(2.0, damping, dt, 2.0)
        axes[0].plot(times, x, label=f"ζ = {damping:g}")
    axes[0].set_title("減衰比 ζ を変える（f = 2 Hz）")
    for frequency in [1.0, 2.0, 4.0]:
        times, x = simulate_spring(frequency, 0.5, dt, 2.0)
        axes[1].plot(times, x, label=f"f = {frequency:g} Hz")
    axes[1].set_title("固有振動数 f を変える（ζ = 0.5）")
    for ax in axes:
        ax.axhline(1.0, color="gray", lw=0.8, ls="--")
        ax.set_xlabel("時刻 t [s]")
        ax.grid(alpha=0.3)
        ax.legend(fontsize=9, loc="lower right")
    axes[0].set_ylabel("位置 x（目標値は 1）")
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_spring_framerate(file_name: str) -> None:
    import matplotlib.pyplot as plt

    duration = 1.0
    figure, axes = plt.subplots(1, 3, figsize=(13, 3.6), sharey=True)
    for fps in [30, 60, 144]:
        dt = 1.0 / fps
        steps = int(duration * fps)
        times = np.arange(steps + 1, dtype=np.float64) * dt
        naive = [0.0]
        smooth = [0.0]
        for _ in range(steps):
            naive.append(naive[-1] + (1.0 - naive[-1]) * 0.1)
            smooth.append(float(smooth_toward(np.array(smooth[-1]), np.array(1.0), 6.0, dt)))
        axes[0].plot(times, naive, marker=".", ms=3, label=f"{fps} fps")
        axes[1].plot(times, smooth, marker=".", ms=3, label=f"{fps} fps")
        spring_times, spring_x = simulate_spring(2.0, 0.4, dt, duration)
        axes[2].plot(spring_times, spring_x, marker=".", ms=3, label=f"{fps} fps")
    axes[0].set_title("毎フレーム x += (目標 - x) × 0.1")
    axes[1].set_title("x += (目標 - x)(1 - exp(-6 Δt))")
    axes[2].set_title("ばね（f = 2 Hz、ζ = 0.4）、刻み Δt")
    for ax in axes:
        ax.set_xlabel("時刻 t [s]")
        ax.grid(alpha=0.3)
        ax.legend(fontsize=9, loc="lower right")
    axes[0].set_ylabel("位置 x（目標値は 1）")
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_periodic_noise("periodic_noise.png")
    draw_spring_response("spring_response.png")
    draw_spring_framerate("spring_framerate.png")


if __name__ == "__main__":
    main()
