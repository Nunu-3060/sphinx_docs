"""Stable Fluids による 2 次元の煙のシミュレーション。

Stam の Stable Fluids 法で非圧縮性流体の速度場を計算し、その流れに乗って
運ばれる煙の濃度を表示する。1 ステップは「外力 → 移流 → 拡散 → 圧力投影」の
順に計算する。

格子は N × N 個のセルからなる一辺 1 の正方形の領域とし、外周に 1 層の
ゴーストセル(境界条件を表すための余分なセル)を加えた (N + 2) × (N + 2) の
配列で物理量を保持する。配列の添字は [y 方向, x 方向] の順である。

実行方法::

    python stable_fluids.py
"""
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib.animation import FuncAnimation
from matplotlib.artist import Artist

FloatArray = npt.NDArray[np.float64]

# set_boundary() に渡す物理量の種類
SCALAR, X_VELOCITY, Y_VELOCITY = 0, 1, 2


@dataclass(frozen=True)
class Params:
    """シミュレーションのパラメーター。"""

    n: int = 128  # 一辺のセル数
    dt: float = 0.05  # 時間刻み幅
    viscosity: float = 1e-5  # 動粘性係数
    diffusivity: float = 1e-5  # 煙の拡散係数
    buoyancy: float = 1.0  # 浮力の強さ(煙の濃度 1 あたりの上向きの加速度)
    source_rate: float = 4.0  # 煙を出す速さ(単位時間あたりの濃度の増加量)
    jacobi_iterations: int = 50  # ヤコビ法の反復回数


@dataclass
class State:
    """流体の状態。"""

    u: FloatArray  # x 方向の速度
    v: FloatArray  # y 方向の速度
    density: FloatArray  # 煙の濃度
    time: float = 0.0


def create_state(n: int) -> State:
    """静止した、煙の無い状態を作る。"""
    shape = (n + 2, n + 2)
    return State(u=np.zeros(shape), v=np.zeros(shape), density=np.zeros(shape))


def set_boundary(kind: int, f: FloatArray) -> None:
    """ゴーストセルに境界条件を設定する。

    領域の四方は壁とし、壁に垂直な速度成分は壁の上で 0 になるように符号を
    反転させ、それ以外の量は壁の内側の値をそのまま写す(勾配 0)。
    """
    sign_x = -1.0 if kind == X_VELOCITY else 1.0
    sign_y = -1.0 if kind == Y_VELOCITY else 1.0
    f[1:-1, 0] = sign_x * f[1:-1, 1]  # 左の壁
    f[1:-1, -1] = sign_x * f[1:-1, -2]  # 右の壁
    f[0, 1:-1] = sign_y * f[1, 1:-1]  # 下の壁
    f[-1, 1:-1] = sign_y * f[-2, 1:-1]  # 上の壁
    # 四隅は隣接する 2 つのゴーストセルの平均とする
    f[0, 0] = 0.5 * (f[1, 0] + f[0, 1])
    f[0, -1] = 0.5 * (f[1, -1] + f[0, -2])
    f[-1, 0] = 0.5 * (f[-2, 0] + f[-1, 1])
    f[-1, -1] = 0.5 * (f[-2, -1] + f[-1, -2])


def advect(kind: int, f0: FloatArray, u: FloatArray, v: FloatArray, dt: float) -> FloatArray:
    """セミラグランジュ法で物理量 f0 を速度場 (u, v) に沿って運ぶ。

    各セルの中心から流れを dt だけ逆にたどった位置(出発点)の値を、
    周囲 4 セルの値から双線形補間で求めて新しい値とする。
    """
    n = f0.shape[0] - 2
    j, i = np.mgrid[1:n + 1, 1:n + 1]  # 内部セルの添字 (y, x)
    # 出発点の位置(セル単位)。速度 1 は 1 単位時間に領域の一辺(n セル)進む速さ
    x = np.clip(i - dt * n * u[1:-1, 1:-1], 0.5, n + 0.5)
    y = np.clip(j - dt * n * v[1:-1, 1:-1], 0.5, n + 0.5)
    i0 = np.floor(x).astype(np.int64)
    j0 = np.floor(y).astype(np.int64)
    sx = x - i0  # x 方向の補間の重み
    sy = y - j0  # y 方向の補間の重み
    f = np.zeros_like(f0)
    f[1:-1, 1:-1] = (
        (1.0 - sy) * ((1.0 - sx) * f0[j0, i0] + sx * f0[j0, i0 + 1])
        + sy * ((1.0 - sx) * f0[j0 + 1, i0] + sx * f0[j0 + 1, i0 + 1])
    )
    set_boundary(kind, f)
    return f


def diffuse(kind: int, f0: FloatArray, coeff: float, dt: float, iterations: int) -> FloatArray:
    """拡散を陰解法で計算する。

    (1 + 4a) f[j, i] - a (周囲 4 セルの f の和) = f0[j, i] (a = coeff dt n^2)
    という連立 1 次方程式をヤコビ法で解く。
    """
    n = f0.shape[0] - 2
    a = coeff * dt * n * n
    f = f0.copy()
    for _ in range(iterations):
        neighbors = f[1:-1, :-2] + f[1:-1, 2:] + f[:-2, 1:-1] + f[2:, 1:-1]
        f[1:-1, 1:-1] = (f0[1:-1, 1:-1] + a * neighbors) / (1.0 + 4.0 * a)
        set_boundary(kind, f)
    return f


def divergence(u: FloatArray, v: FloatArray) -> FloatArray:
    """内部セルにおける速度の発散 du/dx + dv/dy を中心差分で求める。"""
    n = u.shape[0] - 2
    h = 1.0 / n
    div: FloatArray = (u[1:-1, 2:] - u[1:-1, :-2] + v[2:, 1:-1] - v[:-2, 1:-1]) / (2.0 * h)
    return div


def project(u: FloatArray, v: FloatArray, iterations: int) -> tuple[FloatArray, FloatArray]:
    """圧力投影: 速度場から発散を取り除き、非圧縮の条件を満たす速度場を返す。

    ポアソン方程式 ∇²p = ∇·u をヤコビ法で解き、u から ∇p を引く。
    ここでの p は、圧力に dt / ρ を掛けた量に相当する。
    """
    n = u.shape[0] - 2
    h = 1.0 / n
    div = np.zeros_like(u)
    div[1:-1, 1:-1] = divergence(u, v)
    p = np.zeros_like(u)
    for _ in range(iterations):
        p[1:-1, 1:-1] = (p[1:-1, :-2] + p[1:-1, 2:] + p[:-2, 1:-1] + p[2:, 1:-1] - h * h * div[1:-1, 1:-1]) / 4.0
        set_boundary(SCALAR, p)
    u = u.copy()
    v = v.copy()
    u[1:-1, 1:-1] -= (p[1:-1, 2:] - p[1:-1, :-2]) / (2.0 * h)
    v[1:-1, 1:-1] -= (p[2:, 1:-1] - p[:-2, 1:-1]) / (2.0 * h)
    set_boundary(X_VELOCITY, u)
    set_boundary(Y_VELOCITY, v)
    return u, v


def add_forces_and_sources(s: State, prm: Params) -> None:
    """煙の発生源から煙を出し、浮力と吹き出しの速度を与える。"""
    n = prm.n
    # 発生源: 下端中央の小さな領域。左右にゆっくり揺らして流れを乱す
    cx = n // 2
    w = max(n // 32, 1)
    src = (slice(2, 2 + 2 * w), slice(cx - w, cx + w))
    s.density[src] += prm.source_rate * prm.dt
    s.v[src] += 2.0 * prm.dt
    s.u[src] += 0.5 * np.sin(2.0 * np.pi * s.time / 3.0) * prm.dt
    # 浮力: 煙の濃い所ほど上向きの加速度を受ける
    s.v += prm.buoyancy * s.density * prm.dt


def step(s: State, prm: Params) -> None:
    """1 ステップ進める。"""
    # 速度場の更新: 外力 → 移流 → 拡散 → 圧力投影
    add_forces_and_sources(s, prm)
    u = advect(X_VELOCITY, s.u, s.u, s.v, prm.dt)
    v = advect(Y_VELOCITY, s.v, s.u, s.v, prm.dt)
    u = diffuse(X_VELOCITY, u, prm.viscosity, prm.dt, prm.jacobi_iterations)
    v = diffuse(Y_VELOCITY, v, prm.viscosity, prm.dt, prm.jacobi_iterations)
    s.u, s.v = project(u, v, prm.jacobi_iterations)
    # 煙の濃度の更新: 新しい速度場で運び、拡散させる
    d = advect(SCALAR, s.density, s.u, s.v, prm.dt)
    s.density = diffuse(SCALAR, d, prm.diffusivity, prm.dt, prm.jacobi_iterations)
    s.time += prm.dt


def main() -> None:
    prm = Params()
    s = create_state(prm.n)

    plt.rcParams["font.family"] = ["Meiryo", "sans-serif"]
    fig, ax = plt.subplots(figsize=(6, 6))
    image = ax.imshow(s.density[1:-1, 1:-1], origin="lower", extent=(0.0, 1.0, 0.0, 1.0),
                      cmap="inferno", vmin=0.0, vmax=1.0)
    ax.set_title("Stable Fluids による煙")

    def animate(frame: int) -> tuple[Artist]:
        step(s, prm)
        image.set_data(s.density[1:-1, 1:-1])
        return (image,)

    # 戻り値を変数に保持しておかないと、アニメーションが途中で破棄される
    _ = FuncAnimation(fig, animate, frames=400, interval=30, blit=True)
    plt.show()


if __name__ == "__main__":
    main()
