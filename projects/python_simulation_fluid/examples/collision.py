"""ばね-ダッシュポットモデルによる粒子の衝突。

円形の粒子が重なった量に応じて反発力(ばね)と減衰力(ダッシュポット)を
受けるモデルで、箱の中に落下して積み重なる粒子群を計算する。
2 粒子の正面衝突を計算して、設定した反発係数が再現されることも確かめる。

実行方法::

    python collision.py
"""
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib.animation import FuncAnimation
from matplotlib.artist import Artist

FloatArray = npt.NDArray[np.float64]

GRAVITY = np.array([0.0, -9.81])  # 重力加速度 [m/s^2]


@dataclass(frozen=True)
class ContactModel:
    """接触力のパラメーター。"""

    radius: float = 0.02  # 粒子の半径 [m]
    mass: float = 0.01  # 粒子の質量 [kg]
    stiffness: float = 2000.0  # ばね定数 [N/m]
    restitution: float = 0.5  # 反発係数

    @property
    def damping(self) -> float:
        """反発係数から求めたダッシュポットの減衰係数 [N s/m]。"""
        m_eff = self.mass / 2.0  # 同じ質量の 2 粒子の換算質量
        log_e = np.log(self.restitution)
        zeta = -log_e / np.sqrt(np.pi**2 + log_e**2)  # 減衰比
        return float(2.0 * zeta * np.sqrt(m_eff * self.stiffness))

    @property
    def contact_time(self) -> float:
        """1 回の衝突で粒子どうしが接触している時間 [s]。"""
        m_eff = self.mass / 2.0
        omega0 = np.sqrt(self.stiffness / m_eff)
        zeta = self.damping / (2.0 * np.sqrt(m_eff * self.stiffness))
        return float(np.pi / (omega0 * np.sqrt(1.0 - zeta**2)))


def particle_forces(pos: FloatArray, vel: FloatArray, model: ContactModel) -> FloatArray:
    """粒子どうしの接触力を総当たりで計算し、各粒子が受ける力の合計を返す。"""
    i, j = np.triu_indices(len(pos), k=1)  # i < j となるすべての粒子の組
    d = pos[j] - pos[i]
    dist = np.linalg.norm(d, axis=1)
    overlap = 2.0 * model.radius - dist  # 重なり量(正のとき接触している)
    contact = overlap > 0.0
    i, j, d, dist, overlap = i[contact], j[contact], d[contact], dist[contact], overlap[contact]
    n = d / dist[:, np.newaxis]  # i から j へ向かう単位ベクトル
    approach = -np.sum((vel[j] - vel[i]) * n, axis=1)  # 法線方向に近づく速さ
    f = (model.stiffness * overlap + model.damping * approach)[:, np.newaxis] * n
    # 粒子 j は n の向きに押され、粒子 i は逆向きに押される(作用・反作用)
    force = np.zeros_like(pos)
    np.add.at(force, j, f)
    np.add.at(force, i, -f)
    return force


def wall_forces(pos: FloatArray, vel: FloatArray, model: ContactModel, box: float) -> FloatArray:
    """箱の壁(0 <= x <= box, 0 <= y)から受ける力を返す。壁は質量無限大の物体として扱う。"""
    force = np.zeros_like(pos)
    k = model.stiffness
    c = model.damping
    for axis, wall, normal in ((0, 0.0, 1.0), (0, box, -1.0), (1, 0.0, 1.0)):
        overlap = model.radius - normal * (pos[:, axis] - wall)
        contact = overlap > 0.0
        f = k * overlap[contact] - c * normal * vel[contact, axis]
        force[contact, axis] += normal * f
    return force


def step(pos: FloatArray, vel: FloatArray, model: ContactModel, box: float, dt: float) -> None:
    """半陰的オイラー法で 1 ステップ進める。"""
    force = particle_forces(pos, vel, model) + wall_forces(pos, vel, model, box) + model.mass * GRAVITY
    vel += force / model.mass * dt
    pos += vel * dt


def measure_restitution(model: ContactModel, dt: float) -> float:
    """2 粒子を正面衝突させ、衝突前後の相対速度の比から反発係数を測る。"""
    pos = np.array([[0.0, 0.0], [3.0 * model.radius, 0.0]])
    vel = np.array([[0.5, 0.0], [-0.5, 0.0]])
    rel_before = vel[1, 0] - vel[0, 0]
    for _ in range(round(10.0 * model.contact_time / dt)):
        force = particle_forces(pos, vel, model)  # 重力と壁は考えない
        vel += force / model.mass * dt
        pos += vel * dt
    rel_after = vel[1, 0] - vel[0, 0]
    return float(-rel_after / rel_before)


def initial_state(n_side: int, model: ContactModel, box: float, seed: int = 0) -> tuple[FloatArray, FloatArray]:
    """粒子を箱の上部に格子状に並べ、少しずらした初期状態を返す。"""
    rng = np.random.default_rng(seed)
    spacing = 2.5 * model.radius
    ix, iy = np.meshgrid(np.arange(n_side), np.arange(n_side))
    x0 = 0.5 * box - 0.5 * spacing * (n_side - 1)
    pos = np.stack([x0 + spacing * ix.ravel(), 0.3 + spacing * iy.ravel()], axis=1)
    pos += rng.uniform(-0.2, 0.2, pos.shape) * model.radius
    vel = rng.normal(0.0, 0.1, (n_side**2, 2))
    return pos, vel


def main() -> None:
    model = ContactModel()
    dt = model.contact_time / 20.0  # 1 回の衝突を 20 ステップ程度で解像する
    print(f"接触時間 {model.contact_time * 1e3:.2f} ms, 時間刻み幅 {dt * 1e3:.3f} ms")
    print(f"設定した反発係数 {model.restitution:.3f}, 測定した反発係数 {measure_restitution(model, dt):.3f}")

    box = 0.6
    pos, vel = initial_state(12, model, box)
    steps_per_frame = round((1.0 / 60.0) / dt)

    plt.rcParams["font.family"] = ["Meiryo", "sans-serif"]
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0.0, box)
    ax.set_ylim(0.0, 1.5 * box)  # 初期状態の粒子は箱の高さより上にもある
    ax.set_aspect("equal")
    ax.set_title("ばね-ダッシュポットモデルによる粒子の衝突")
    # 点の大きさの単位はポイントなので、粒子の直径がデータ座標と一致するように換算する
    fig.canvas.draw()
    diameter_pt = 2.0 * model.radius / box * ax.get_window_extent().width * 72.0 / fig.dpi
    scatter = ax.scatter(pos[:, 0], pos[:, 1], s=diameter_pt**2)

    def animate(frame: int) -> tuple[Artist]:
        for _ in range(steps_per_frame):
            step(pos, vel, model, box, dt)
        scatter.set_offsets(pos)
        return (scatter,)

    # 戻り値を変数に保持しておかないと、アニメーションが途中で破棄される
    _ = FuncAnimation(fig, animate, frames=300, interval=16, blit=True)
    plt.show()


if __name__ == "__main__":
    main()
