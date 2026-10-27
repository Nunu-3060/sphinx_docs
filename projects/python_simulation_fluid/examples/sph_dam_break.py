"""SPH(粒子法)によるダムブレイクのシミュレーション。

水槽の左端に置いた水柱が崩れて流れ出す様子を、弱圧縮性 SPH 法で計算する。
壁は動かない粒子(壁粒子)を並べて表現する。近傍探索には
neighbor_search.py のセル分割法を使うので、同じフォルダに置いて実行する。

実行方法::

    python sph_dam_break.py
"""
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib.animation import FuncAnimation
from matplotlib.artist import Artist

from neighbor_search import cell_list_pairs

FloatArray = npt.NDArray[np.float64]
BoolArray = npt.NDArray[np.bool_]
IntArray = npt.NDArray[np.int64]

GRAVITY = np.array([0.0, -9.81])  # 重力加速度 [m/s^2]


@dataclass(frozen=True)
class Params:
    """シミュレーションのパラメーター。長さの単位は m とする。"""

    spacing: float = 0.02  # 初期の粒子間隔
    tank_width: float = 1.6  # 水槽の幅
    tank_height: float = 1.0  # 水槽の壁の高さ
    water_width: float = 0.4  # 水柱の幅
    water_height: float = 0.8  # 水柱の高さ
    wall_layers: int = 3  # 壁粒子の層の数
    rho0: float = 1000.0  # 基準密度 [kg/m^3]
    alpha: float = 0.05  # 人工粘性の係数
    dt: float = 1e-4  # 時間刻み幅 [s]
    rebuild_interval: int = 8  # 近傍リストを作り直す間隔 [ステップ]

    @property
    def h(self) -> float:
        """カーネル関数の大きさを決める長さ(影響半径は 2h)。"""
        return 1.3 * self.spacing

    @property
    def sound_speed(self) -> float:
        """人工的な音速。流れの最大速度 sqrt(2 g H) の 10 倍とする。"""
        return float(10.0 * np.sqrt(2.0 * 9.81 * self.water_height))

    @property
    def search_radius(self) -> float:
        """近傍リストを作るときの探索半径。

        影響半径 2h に余裕(0.5h)を持たせておくことで、作り直すまでの
        rebuild_interval ステップの間に粒子が多少動いても、影響半径内の
        相手をすべて含んだままにする。
        """
        return 2.5 * self.h


@dataclass
class State:
    """粒子の状態。壁粒子も含めて 1 つの配列に格納する。"""

    pos: FloatArray  # 位置(形状 (N, 2))
    vel: FloatArray  # 速度(形状 (N, 2))
    is_fluid: BoolArray  # 流体粒子なら True、壁粒子なら False
    mass: float  # 粒子 1 個の質量
    pairs: tuple[IntArray, IntArray]  # 近傍リスト(距離が探索半径未満の粒子の組 (i, j))
    time: float = 0.0
    steps: int = 0


def kernel(r: FloatArray, h: float) -> FloatArray:
    """2 次元の 3 次スプラインカーネル W(r, h)。r < 2h の範囲で使う。"""
    q = r / h
    sigma = 10.0 / (7.0 * np.pi * h**2)
    w = np.where(q < 1.0, 1.0 - 1.5 * q * q + 0.75 * q * q * q, 0.25 * (2.0 - q) ** 3)
    return sigma * w


def kernel_derivative(r: FloatArray, h: float) -> FloatArray:
    """カーネル関数の r による微分 dW/dr。r < 2h の範囲で使う。"""
    q = r / h
    sigma = 10.0 / (7.0 * np.pi * h**2)
    dw = np.where(q < 1.0, -3.0 * q + 2.25 * q * q, -0.75 * (2.0 - q) ** 2)
    return sigma * dw / h


def lattice_positions(x0: float, x1: float, y0: float, y1: float, spacing: float) -> FloatArray:
    """長方形 [x0, x1] × [y0, y1] の中に、間隔 spacing で格子状に並べた点を返す。"""
    xs = np.arange(x0 + 0.5 * spacing, x1, spacing)
    ys = np.arange(y0 + 0.5 * spacing, y1, spacing)
    gx, gy = np.meshgrid(xs, ys)
    return np.stack([gx.ravel(), gy.ravel()], axis=1)


def create_state(prm: Params) -> State:
    """初期状態(水柱と水槽)を作る。"""
    s = prm.spacing
    fluid = lattice_positions(0.0, prm.water_width, 0.0, prm.water_height, s)
    t = prm.wall_layers * s  # 壁の厚さ
    walls = np.concatenate([
        lattice_positions(-t, prm.tank_width + t, -t, 0.0, s),  # 底
        lattice_positions(-t, 0.0, 0.0, prm.tank_height, s),  # 左の壁
        lattice_positions(prm.tank_width, prm.tank_width + t, 0.0, prm.tank_height, s),  # 右の壁
    ])
    pos = np.concatenate([fluid, walls])
    is_fluid = np.zeros(len(pos), dtype=np.bool_)
    is_fluid[:len(fluid)] = True

    # 格子状に並んだ粒子の密度がちょうど rho0 になるように質量を決める
    k = np.arange(-3, 4)
    kx, ky = np.meshgrid(k, k)
    r = s * np.hypot(kx, ky).ravel()  # 格子上の 1 点から周囲の点までの距離
    mass = prm.rho0 / float(np.sum(kernel(r[r < 2.0 * prm.h], prm.h)))
    pairs = cell_list_pairs(pos, prm.search_radius)
    return State(pos=pos, vel=np.zeros_like(pos), is_fluid=is_fluid, mass=mass, pairs=pairs)


def compute_density(s: State, i: IntArray, j: IntArray, r: FloatArray, h: float) -> FloatArray:
    """密度 ρ_i = Σ_j m W(r_ij, h) を求める(自分自身の寄与も含める)。"""
    n = len(s.pos)
    w = kernel(r, h)
    self_term = s.mass * kernel(np.zeros(1), h)
    return self_term + s.mass * (np.bincount(i, w, minlength=n) + np.bincount(j, w, minlength=n))


def compute_pressure(rho: FloatArray, prm: Params) -> FloatArray:
    """状態方程式(テイトの式)で密度から圧力を求める。負の圧力は 0 にする。"""
    b = prm.rho0 * prm.sound_speed**2 / 7.0
    return np.maximum(b * ((rho / prm.rho0) ** 7 - 1.0), 0.0)


def compute_acceleration(s: State, prm: Params) -> FloatArray:
    """各粒子の加速度(圧力勾配 + 人工粘性 + 重力)を求める。"""
    h = prm.h
    # 近傍リストから、現在の距離が影響半径 2h 未満の組だけを取り出す
    i, j = s.pairs
    d = s.pos[i] - s.pos[j]  # r_ij = x_i - x_j
    r = np.sqrt(d[:, 0] ** 2 + d[:, 1] ** 2)
    near = r < 2.0 * h
    i, j, d, r = i[near], j[near], d[near], r[near]
    rho = compute_density(s, i, j, r, h)
    p = compute_pressure(rho, prm)

    # ∇_i W_ij = (dW/dr) r_ij / |r_ij|
    grad_w = (kernel_derivative(r, h) / np.maximum(r, 1e-12))[:, np.newaxis] * d

    # 人工粘性: 近づき合う粒子の組にだけ働く
    dv = s.vel[i] - s.vel[j]
    vd = dv[:, 0] * d[:, 0] + dv[:, 1] * d[:, 1]  # v_ij · r_ij
    mu = h * vd / (r**2 + 0.01 * h**2)
    rho_mean = 0.5 * (rho[i] + rho[j])
    visc = np.where(vd < 0.0, -prm.alpha * prm.sound_speed * mu / rho_mean, 0.0)

    # 粒子 i が受ける加速度。粒子 j は同じ大きさで逆向きの加速度を受ける
    coeff = -s.mass * (p[i] / rho[i] ** 2 + p[j] / rho[j] ** 2 + visc)
    a_ij = coeff[:, np.newaxis] * grad_w
    n = len(s.pos)
    acc = np.zeros_like(s.pos)
    for axis in range(2):
        acc[:, axis] = np.bincount(i, a_ij[:, axis], minlength=n) - np.bincount(j, a_ij[:, axis], minlength=n)
    acc += GRAVITY
    acc[~s.is_fluid] = 0.0  # 壁粒子は動かさない
    return acc


def step(s: State, prm: Params) -> None:
    """半陰的オイラー法で 1 ステップ進める。"""
    if s.steps % prm.rebuild_interval == 0:
        s.pairs = cell_list_pairs(s.pos, prm.search_radius)
    acc = compute_acceleration(s, prm)
    s.vel += acc * prm.dt
    s.pos += s.vel * prm.dt
    s.time += prm.dt
    s.steps += 1


def front_position(s: State) -> float:
    """流れの先端の位置(流体粒子の x 座標の最大値)を返す。"""
    return float(s.pos[s.is_fluid, 0].max())


def main() -> None:
    prm = Params()
    s = create_state(prm)
    print(f"流体粒子 {np.count_nonzero(s.is_fluid)} 個、壁粒子 {np.count_nonzero(~s.is_fluid)} 個")
    steps_per_frame = 100  # 1 フレームあたり 0.01 s 進める

    plt.rcParams["font.family"] = ["Meiryo", "sans-serif"]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(-0.1, prm.tank_width + 0.1)
    ax.set_ylim(-0.1, prm.tank_height)
    ax.set_aspect("equal")
    ax.scatter(s.pos[~s.is_fluid, 0], s.pos[~s.is_fluid, 1], s=2, c="gray")
    fluid = ax.scatter(s.pos[s.is_fluid, 0], s.pos[s.is_fluid, 1], s=4)
    title = ax.set_title("")

    def animate(frame: int) -> tuple[Artist, Artist]:
        for _ in range(steps_per_frame):
            step(s, prm)
        fluid.set_offsets(s.pos[s.is_fluid])
        title.set_text(f"SPH によるダムブレイク t = {s.time:.2f} s")
        return fluid, title

    # 戻り値を変数に保持しておかないと、アニメーションが途中で破棄される
    _ = FuncAnimation(fig, animate, frames=150, interval=30, blit=False, repeat=False)
    plt.show()


if __name__ == "__main__":
    main()
