"""正方キャビティ流れ(上の壁が動く正方形の容器内の流れ)。

一辺 1 の正方形の容器の上の壁を右向きに速さ 1 で動かし続けたときの
定常な流れを、射影法(フラクショナルステップ法)と中心差分で計算する。
レイノルズ数は Re = 1 / nu である。容器の中心を通る鉛直線上の x 方向の
速度を、Ghia ら(1982)のベンチマーク値と比較する。

実行方法::

    python cavity_flow.py
"""
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

FloatArray = npt.NDArray[np.float64]

LID_VELOCITY = 1.0  # 上の壁の速さ

# Ghia, Ghia and Shin (1982) の Re = 100 の結果
# 中心を通る鉛直線 (x = 0.5) 上の y と、x 方向の速度 u
GHIA_Y = np.array([0.0000, 0.0547, 0.0625, 0.0703, 0.1016, 0.1719, 0.2813, 0.4531, 0.5000,
                   0.6172, 0.7344, 0.8516, 0.9531, 0.9609, 0.9688, 0.9766, 1.0000])
GHIA_U = np.array([0.00000, -0.03717, -0.04192, -0.04775, -0.06434, -0.10150, -0.15662, -0.21090, -0.20581,
                   -0.13641, 0.00332, 0.23151, 0.68717, 0.73722, 0.78871, 0.84123, 1.00000])


@dataclass
class Result:
    """計算結果。配列の添字は [y 方向, x 方向] の順で、境界上の格子点を含む。"""

    x: FloatArray  # 格子点の x 座標(1 次元)
    y: FloatArray  # 格子点の y 座標(1 次元)
    u: FloatArray  # x 方向の速度
    v: FloatArray  # y 方向の速度
    p: FloatArray  # 圧力
    steps: int  # 定常に達するまでのステップ数


def apply_velocity_boundary(u: FloatArray, v: FloatArray) -> None:
    """速度の境界条件: 上の壁だけが動き、壁の上で流体は壁と同じ速度を持つ(滑りなし)。"""
    u[0, :] = 0.0
    u[:, 0] = 0.0
    u[:, -1] = 0.0
    u[-1, :] = LID_VELOCITY
    v[0, :] = 0.0
    v[-1, :] = 0.0
    v[:, 0] = 0.0
    v[:, -1] = 0.0


def apply_pressure_boundary(p: FloatArray) -> None:
    """圧力の境界条件: 壁に垂直な方向の圧力勾配を 0 とする。"""
    p[:, 0] = p[:, 1]
    p[:, -1] = p[:, -2]
    p[0, :] = p[1, :]
    p[-1, :] = p[-2, :]


def solve(n: int, nu: float, dt: float, poisson_iterations: int = 50, tol: float = 1e-6,
          max_steps: int = 100_000) -> Result:
    """格子点数 n × n で定常解を求める。

    1 ステップあたりの速度の変化量の最大値が tol × dt を下回ったら定常とみなす。
    """
    x = np.linspace(0.0, 1.0, n)
    y = np.linspace(0.0, 1.0, n)
    h = x[1] - x[0]
    u = np.zeros((n, n))
    v = np.zeros((n, n))
    p = np.zeros((n, n))
    apply_velocity_boundary(u, v)

    steps = max_steps
    for step in range(1, max_steps + 1):
        un, vn = u.copy(), v.copy()
        c = (slice(1, -1), slice(1, -1))  # 内部の格子点
        # 1. 圧力を無視して、移流と粘性だけで仮の速度 (u*, v*) を求める
        for f, fn in ((u, un), (v, vn)):
            dfdx = (fn[1:-1, 2:] - fn[1:-1, :-2]) / (2.0 * h)
            dfdy = (fn[2:, 1:-1] - fn[:-2, 1:-1]) / (2.0 * h)
            lap = (fn[1:-1, 2:] + fn[1:-1, :-2] + fn[2:, 1:-1] + fn[:-2, 1:-1] - 4.0 * fn[c]) / h**2
            f[c] = fn[c] + dt * (-(un[c] * dfdx + vn[c] * dfdy) + nu * lap)
        # 2. 仮の速度の発散を打ち消す圧力をポアソン方程式から求める(ヤコビ法)
        rhs = ((u[1:-1, 2:] - u[1:-1, :-2]) + (v[2:, 1:-1] - v[:-2, 1:-1])) / (2.0 * h * dt)
        for _ in range(poisson_iterations):
            p[c] = (p[1:-1, 2:] + p[1:-1, :-2] + p[2:, 1:-1] + p[:-2, 1:-1] - h**2 * rhs) / 4.0
            apply_pressure_boundary(p)
        p -= p.mean()  # 圧力は定数の差を除いて決まるので、平均を 0 にそろえる
        # 3. 圧力勾配で速度を修正する
        u[c] -= dt * (p[1:-1, 2:] - p[1:-1, :-2]) / (2.0 * h)
        v[c] -= dt * (p[2:, 1:-1] - p[:-2, 1:-1]) / (2.0 * h)
        apply_velocity_boundary(u, v)

        change = max(np.abs(u - un).max(), np.abs(v - vn).max())
        if change < tol * dt:
            steps = step
            break
    return Result(x=x, y=y, u=u, v=v, p=p, steps=steps)


def main() -> None:
    re = 100.0
    nu = 1.0 / re
    results = {n: solve(n, nu, dt=0.002) for n in (21, 41, 81)}
    for n, r in results.items():
        print(f"{n} × {n}: {r.steps} ステップで定常に達した")

    plt.rcParams["font.family"] = ["Meiryo", "sans-serif"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
    r = results[81]
    speed = np.hypot(r.u, r.v)
    ax1.streamplot(r.x, r.y, r.u, r.v, color=speed, cmap="viridis", density=1.5)
    ax1.set_aspect("equal")
    ax1.set_xlim(0.0, 1.0)
    ax1.set_ylim(0.0, 1.0)
    ax1.set_title("流線(81 × 81、Re = 100)")

    for n, r in results.items():
        ax2.plot(r.u[:, n // 2], r.y, label=f"{n} × {n}")
    ax2.plot(GHIA_U, GHIA_Y, "ko", label="Ghia ら(1982)")
    ax2.set_xlabel("u(x = 0.5)")
    ax2.set_ylabel("y")
    ax2.set_title("中心線上の速度の比較")
    ax2.legend()
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
