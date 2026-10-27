"""パーティクルシステムによる噴水。

多数の粒子を NumPy の配列でまとめて管理し、発生・移動・床での反発・消滅を
ベクトル化した処理で計算する。あわせて、Python の for 文で 1 粒子ずつ
更新する場合との速度を比較する。

実行方法::

    python particle_system.py
"""
import time
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib.animation import FuncAnimation
from matplotlib.artist import Artist

FloatArray = npt.NDArray[np.float64]
BoolArray = npt.NDArray[np.bool_]

GRAVITY = np.array([0.0, -9.81])  # 重力加速度 [m/s^2]
RESTITUTION = 0.5  # 床との反発係数
LIFETIME = 3.0  # 粒子の寿命 [s]


@dataclass
class Particles:
    """全粒子の状態。i 番目の要素が i 番目の粒子に対応する。"""

    pos: FloatArray  # 位置(形状 (N, 2))
    vel: FloatArray  # 速度(形状 (N, 2))
    age: FloatArray  # 発生してからの経過時間(形状 (N,))
    alive: BoolArray  # 生存しているかどうか(形状 (N,))


def create_particles(capacity: int) -> Particles:
    """最大 capacity 個の粒子を格納できる空の(全粒子が消滅した)状態を作る。"""
    return Particles(
        pos=np.zeros((capacity, 2)),
        vel=np.zeros((capacity, 2)),
        age=np.zeros(capacity),
        alive=np.zeros(capacity, dtype=np.bool_),
    )


def emit(p: Particles, count: int, rng: np.random.Generator) -> None:
    """消滅している粒子を最大 count 個選び、原点から上向きに発射する。"""
    free = np.flatnonzero(~p.alive)[:count]
    n = free.size
    angle = np.deg2rad(90.0 + rng.normal(0.0, 8.0, n))  # 真上から少しばらつかせる
    speed = rng.uniform(6.0, 8.0, n)
    p.pos[free] = 0.0
    p.vel[free, 0] = speed * np.cos(angle)
    p.vel[free, 1] = speed * np.sin(angle)
    p.age[free] = 0.0
    p.alive[free] = True


def update(p: Particles, dt: float) -> None:
    """全粒子を 1 ステップ進める(半陰的オイラー法)。"""
    p.vel += GRAVITY * dt
    p.pos += p.vel * dt
    # 床(y = 0)より下に出た粒子を床の上へ戻し、鉛直方向の速度を反転させる
    hit = p.pos[:, 1] < 0.0
    p.pos[hit, 1] *= -1.0
    p.vel[hit, 1] *= -RESTITUTION
    p.age += dt
    p.alive &= p.age < LIFETIME


def update_with_loop(pos: list[list[float]], vel: list[list[float]], dt: float) -> None:
    """update() と同じ計算(寿命の処理は除く)を、for 文で 1 粒子ずつ行う。"""
    for i in range(len(pos)):
        vel[i][1] += GRAVITY[1] * dt
        pos[i][0] += vel[i][0] * dt
        pos[i][1] += vel[i][1] * dt
        if pos[i][1] < 0.0:
            pos[i][1] *= -1.0
            vel[i][1] *= -RESTITUTION


def benchmark(n: int, repeat: int = 10) -> tuple[float, float]:
    """n 個の粒子を 1 ステップ更新する時間 [s] を、for 文版と NumPy 版で測る。"""
    rng = np.random.default_rng(0)
    p = create_particles(n)
    p.pos[:] = rng.uniform(0.0, 1.0, (n, 2))
    p.vel[:] = rng.normal(0.0, 1.0, (n, 2))
    pos_list = p.pos.tolist()
    vel_list = p.vel.tolist()

    start = time.perf_counter()
    for _ in range(repeat):
        update_with_loop(pos_list, vel_list, 0.001)
    t_loop = (time.perf_counter() - start) / repeat

    start = time.perf_counter()
    for _ in range(repeat):
        update(p, 0.001)
    t_numpy = (time.perf_counter() - start) / repeat
    return t_loop, t_numpy


def main() -> None:
    for n in (1_000, 10_000, 100_000):
        t_loop, t_numpy = benchmark(n)
        print(f"N = {n:>7}: for 文 {t_loop * 1e3:8.3f} ms, NumPy {t_numpy * 1e3:7.3f} ms")

    dt = 1.0 / 60.0
    rng = np.random.default_rng(1)
    p = create_particles(3000)

    plt.rcParams["font.family"] = ["Meiryo", "sans-serif"]
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_xlim(-3.0, 3.0)
    ax.set_ylim(0.0, 4.0)
    ax.set_aspect("equal")
    ax.set_title("パーティクルシステムによる噴水")
    scatter = ax.scatter([], [], s=4)

    def animate(frame: int) -> tuple[Artist]:
        emit(p, 15, rng)
        update(p, dt)
        scatter.set_offsets(p.pos[p.alive])
        return (scatter,)

    # 戻り値を変数に保持しておかないと、アニメーションが途中で破棄される
    _ = FuncAnimation(fig, animate, frames=600, interval=16, blit=True)
    plt.show()


if __name__ == "__main__":
    main()
