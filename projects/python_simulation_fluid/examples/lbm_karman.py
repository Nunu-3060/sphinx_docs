"""格子ボルツマン法による円柱まわりの流れ(カルマン渦列)。

D2Q9 モデルと BGK 衝突則を用いて、一様な流れの中に置いた円柱の後ろに
交互に渦が放出される様子を計算する。物理量はすべて格子単位
(格子間隔 1、時間刻み幅 1)で表す。

実行方法::

    python lbm_karman.py
"""
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib.animation import FuncAnimation
from matplotlib.artist import Artist

FloatArray = npt.NDArray[np.float64]
BoolArray = npt.NDArray[np.bool_]

# D2Q9 モデルの 9 個の離散速度 (cx, cy) と重み
C = np.array([[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, 1], [-1, -1], [1, -1]])
W = np.array([4 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 36, 1 / 36, 1 / 36, 1 / 36])
# 各離散速度と逆向きの離散速度の番号(跳ね返り境界で使う)
OPPOSITE = np.array([0, 3, 4, 1, 2, 7, 8, 5, 6])


@dataclass(frozen=True)
class Params:
    """シミュレーションのパラメーター(格子単位)。"""

    nx: int = 400  # x 方向の格子点数
    ny: int = 100  # y 方向の格子点数
    radius: float = 8.0  # 円柱の半径
    u_in: float = 0.08  # 流入速度
    reynolds: float = 100.0  # レイノルズ数(円柱の直径を代表長さとする)

    @property
    def viscosity(self) -> float:
        """レイノルズ数から決まる動粘性係数。"""
        return self.u_in * 2.0 * self.radius / self.reynolds

    @property
    def tau(self) -> float:
        """緩和時間。動粘性係数 nu と tau = 3 nu + 1/2 の関係がある。"""
        return 3.0 * self.viscosity + 0.5


@dataclass
class State:
    """流れの状態。"""

    f: FloatArray  # 分布関数(形状 (9, ny, nx))
    obstacle: BoolArray  # 円柱の内部なら True(形状 (ny, nx))
    steps: int = 0


def equilibrium(rho: FloatArray, ux: FloatArray, uy: FloatArray) -> FloatArray:
    """密度 rho と速度 (ux, uy)(いずれも 2 次元配列)に対応する平衡分布関数を返す。"""
    usq = 1.5 * (ux * ux + uy * uy)
    feq = np.empty((9, *ux.shape))
    for k in range(9):
        cu = 3.0 * (C[k, 0] * ux + C[k, 1] * uy)  # 3 (c_k · u)
        feq[k] = W[k] * rho * (1.0 + cu + 0.5 * cu * cu - usq)
    return feq


def macroscopic(f: FloatArray) -> tuple[FloatArray, FloatArray, FloatArray]:
    """分布関数から密度と速度を求める。"""
    rho = f.sum(axis=0)
    ux = (f[1] + f[5] + f[8] - f[3] - f[6] - f[7]) / rho  # Σ f_k c_kx / rho
    uy = (f[2] + f[5] + f[6] - f[4] - f[7] - f[8]) / rho  # Σ f_k c_ky / rho
    return rho, ux, uy


def create_state(prm: Params) -> State:
    """一様な流れの中に円柱を置いた初期状態を作る。"""
    y, x = np.mgrid[0:prm.ny, 0:prm.nx]
    cx, cy = prm.nx / 5, prm.ny / 2
    obstacle = (x - cx) ** 2 + (y - cy) ** 2 < prm.radius**2
    rho = np.ones((prm.ny, prm.nx))
    # 渦の放出が早く始まるように、流入速度にわずかな上下非対称の乱れを加える
    ux = prm.u_in * (1.0 + 1e-3 * np.sin(2.0 * np.pi * y / prm.ny))
    uy = np.zeros((prm.ny, prm.nx))
    return State(f=equilibrium(rho, ux, uy), obstacle=obstacle)


def step(s: State, prm: Params) -> None:
    """1 ステップ進める: 衝突 → 跳ね返り → 移動(ストリーミング)→ 流入・流出境界。"""
    f = s.f
    rho, ux, uy = macroscopic(f)
    feq = equilibrium(rho, ux, uy)
    f_new = np.empty_like(f)
    for k in range(9):
        # 1. 衝突: 分布関数を平衡分布関数に近づける(BGK 衝突則)
        post = f[k] + (feq[k] - f[k]) / prm.tau
        # 2. 円柱の内部では、粒子を来た向きへ跳ね返す(滑りなし条件)
        post[s.obstacle] = f[OPPOSITE[k]][s.obstacle]
        # 3. 移動: 離散速度 c_k の向きに隣の格子点へずらす(上下の端は周期境界になる)
        f_new[k] = np.roll(post, shift=(C[k, 1], C[k, 0]), axis=(0, 1))
    # 4. 流入境界(左端)は平衡分布関数で置き換え、流出境界(右端)は 1 つ内側の値を写す
    ones = np.ones((prm.ny, 1))
    f_new[:, :, :1] = equilibrium(ones, prm.u_in * ones, 0.0 * ones)
    f_new[:, :, -1] = f_new[:, :, -2]
    s.f = f_new
    s.steps += 1


def vorticity(ux: FloatArray, uy: FloatArray) -> FloatArray:
    """渦度 dv/dx - du/dy を中心差分で求める。"""
    omega: FloatArray = np.gradient(uy, axis=1) - np.gradient(ux, axis=0)
    return omega


def strouhal_number(signal: FloatArray, prm: Params) -> float:
    """円柱の後流で 1 ステップごとに記録した速度の時系列から、ストローハル数 St = f D / U を求める。

    信号が負から正に変わる時刻(上向きのゼロ交差)を線形補間で求め、
    その間隔の平均を渦放出の周期とする。
    """
    x = signal - signal.mean()
    k = np.flatnonzero((x[:-1] < 0.0) & (x[1:] >= 0.0))
    crossings = k + x[k] / (x[k] - x[k + 1])  # ゼロ交差の時刻(線形補間)
    period = float(np.mean(np.diff(crossings)))
    return 2.0 * prm.radius / (period * prm.u_in)


def main() -> None:
    prm = Params()
    print(f"動粘性係数 {prm.viscosity:.4f}、緩和時間 {prm.tau:.4f}")
    s = create_state(prm)
    steps_per_frame = 50

    plt.rcParams["font.family"] = ["Meiryo", "sans-serif"]
    fig, ax = plt.subplots(figsize=(10, 3))
    image = ax.imshow(np.zeros((prm.ny, prm.nx)), origin="lower", cmap="RdBu_r", vmin=-0.02, vmax=0.02)
    ax.contour(s.obstacle, levels=[0.5], colors="k")
    title = ax.set_title("")

    def animate(frame: int) -> tuple[Artist, Artist]:
        for _ in range(steps_per_frame):
            step(s, prm)
        _, ux, uy = macroscopic(s.f)
        omega = vorticity(ux, uy)
        omega[s.obstacle] = 0.0
        image.set_data(omega)
        title.set_text(f"格子ボルツマン法による円柱まわりの流れ(渦度) ステップ {s.steps}")
        return image, title

    # 戻り値を変数に保持しておかないと、アニメーションが途中で破棄される
    _ = FuncAnimation(fig, animate, frames=600, interval=20, blit=False, repeat=False)
    plt.show()


if __name__ == "__main__":
    main()
