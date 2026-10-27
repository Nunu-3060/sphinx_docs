"""ばね-質点系によるロープの運動。

質点をばねでつないだロープの一端を固定し、水平に張った状態から放して
重力で振れ落ちる様子を計算する。時間刻み幅が大きすぎると計算が発散する
ことも確認する。

実行方法::

    python spring_mass.py
"""
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib.animation import FuncAnimation
from matplotlib.artist import Artist

FloatArray = npt.NDArray[np.float64]
IntArray = npt.NDArray[np.int64]

GRAVITY = np.array([0.0, -9.81])  # 重力加速度 [m/s^2]


@dataclass(frozen=True)
class Rope:
    """ロープのパラメーター。"""

    n_nodes: int = 20  # 質点の数
    rest_length: float = 0.05  # ばねの自然長 [m]
    mass: float = 0.01  # 質点 1 個の質量 [kg]
    stiffness: float = 500.0  # ばね定数 [N/m]
    damping: float = 0.05  # ばねの伸縮に対する減衰係数 [N s/m]


def make_springs(n_nodes: int) -> IntArray:
    """隣り合う質点をつなぐばねの一覧(形状 (n_nodes - 1, 2))を返す。"""
    i = np.arange(n_nodes - 1)
    return np.stack([i, i + 1], axis=1)


def spring_forces(pos: FloatArray, vel: FloatArray, springs: IntArray, rope: Rope) -> FloatArray:
    """すべてのばねが各質点に及ぼす力の合計を返す。"""
    i, j = springs[:, 0], springs[:, 1]
    d = pos[j] - pos[i]
    length = np.linalg.norm(d, axis=1)
    n = d / length[:, np.newaxis]  # i から j へ向かう単位ベクトル
    stretch_rate = np.sum((vel[j] - vel[i]) * n, axis=1)  # 伸びる速さ
    magnitude = rope.stiffness * (length - rope.rest_length) + rope.damping * stretch_rate
    f = magnitude[:, np.newaxis] * n  # 質点 i が受ける力(質点 j は逆向きの力を受ける)
    force = np.zeros_like(pos)
    np.add.at(force, i, f)
    np.add.at(force, j, -f)
    return force


def simulate(rope: Rope, dt: float, t_end: float, n_frames: int) -> FloatArray:
    """ロープの運動を計算し、n_frames 枚分の位置(形状 (n_frames, n_nodes, 2))を返す。

    計算が発散した場合は、それ以降の位置を NaN とする。
    """
    springs = make_springs(rope.n_nodes)
    pos = np.zeros((rope.n_nodes, 2))
    pos[:, 0] = np.arange(rope.n_nodes) * rope.rest_length  # 水平に並べる
    vel = np.zeros_like(pos)

    n_steps = round(t_end / dt)
    save_every = max(n_steps // (n_frames - 1), 1)
    frames = np.full((n_frames, rope.n_nodes, 2), np.nan)
    frames[0] = pos
    for step in range(1, n_steps + 1):
        force = spring_forces(pos, vel, springs, rope) + rope.mass * GRAVITY
        vel += force / rope.mass * dt
        vel[0] = 0.0  # 先頭の質点は固定する
        pos += vel * dt
        if not np.all(np.abs(pos) < 1e3):
            break  # 発散した
        if step % save_every == 0 and step // save_every < n_frames:
            frames[step // save_every] = pos
    return frames


def critical_time_step(rope: Rope) -> float:
    """半陰的オイラー法が安定に計算できる時間刻み幅の目安 2 / ω_max を返す。

    ω_max は質点列の固有振動数の最大値で、およそ 2 sqrt(k / m) となる。
    """
    omega_max = 2.0 * np.sqrt(rope.stiffness / rope.mass)
    return float(2.0 / omega_max)


def main() -> None:
    rope = Rope()
    dt_crit = critical_time_step(rope)
    print(f"時間刻み幅の上限の目安: {dt_crit * 1e3:.2f} ms")

    frames = simulate(rope, dt=0.0005, t_end=3.0, n_frames=181)

    plt.rcParams["font.family"] = ["Meiryo", "sans-serif"]
    fig, ax = plt.subplots(figsize=(6, 6))
    length = rope.rest_length * (rope.n_nodes - 1)
    ax.set_xlim(-1.3 * length, 1.3 * length)
    ax.set_ylim(-1.5 * length, 0.5 * length)
    ax.set_aspect("equal")
    ax.set_title("ばね-質点系によるロープ")
    (line,) = ax.plot([], [], "o-", ms=4)

    def animate(frame: int) -> tuple[Artist]:
        line.set_data(frames[frame, :, 0], frames[frame, :, 1])
        return (line,)

    # 戻り値を変数に保持しておかないと、アニメーションが途中で破棄される
    _ = FuncAnimation(fig, animate, frames=len(frames), interval=1000 * 3.0 / 180, blit=True)
    plt.show()


if __name__ == "__main__":
    main()
