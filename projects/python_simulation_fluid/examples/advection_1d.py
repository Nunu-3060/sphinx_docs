"""1 次元移流方程式の差分解法。

周期境界条件のもとで移流方程式 du/dt + c du/dx = 0 を 3 種類の差分法で解き、
厳密解(初期波形が形を変えずに速さ c で移動する)と比較する。

実行方法::

    python advection_1d.py
"""
from collections.abc import Callable

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

FloatArray = npt.NDArray[np.float64]
# (現在の u, クーラン数) を受け取り、1 ステップ後の u を返す関数
Scheme = Callable[[FloatArray, float], FloatArray]


def upwind(u: FloatArray, cfl: float) -> FloatArray:
    """1 次精度風上差分(c > 0 なので、上流側 = 左隣との差を使う)。"""
    return u - cfl * (u - np.roll(u, 1))


def ftcs(u: FloatArray, cfl: float) -> FloatArray:
    """時間に前進差分、空間に中心差分を使う方法。無条件に不安定である。"""
    return u - 0.5 * cfl * (np.roll(u, -1) - np.roll(u, 1))


def lax_wendroff(u: FloatArray, cfl: float) -> FloatArray:
    """ラックス-ヴェンドロフ法(時間・空間とも 2 次精度)。"""
    up = np.roll(u, -1)  # 右隣 u[i + 1]
    um = np.roll(u, 1)  # 左隣 u[i - 1]
    return u - 0.5 * cfl * (up - um) + 0.5 * cfl**2 * (up - 2.0 * u + um)


def initial_profile(x: FloatArray) -> FloatArray:
    """初期波形: 矩形波とガウス関数を並べたもの。"""
    square = np.where((x > 0.1) & (x < 0.3), 1.0, 0.0)
    gauss = np.exp(-(((x - 0.65) / 0.06) ** 2))
    return square + gauss


def exact_solution(x: FloatArray, t: float, c: float) -> FloatArray:
    """厳密解: 初期波形を c t だけ平行移動したもの(周期 1)。"""
    return initial_profile((x - c * t) % 1.0)


def solve(scheme: Scheme, nx: int, c: float, cfl: float, t_end: float) -> tuple[FloatArray, FloatArray]:
    """格子点数 nx、クーラン数 cfl で t_end まで計算し、(x, u) を返す。"""
    dx = 1.0 / nx
    x = np.linspace(0.0, 1.0, nx, endpoint=False)
    dt = cfl * dx / c
    n_steps = round(t_end / dt)
    u = initial_profile(x)
    for _ in range(n_steps):
        u = scheme(u, cfl)
    return x, u


def main() -> None:
    c = 1.0
    nx = 200

    plt.rcParams["font.family"] = ["Meiryo", "sans-serif"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))

    # 安定な 2 つの方法で、ちょうど 1 周(t = 1)させた結果を比べる
    x, _ = solve(upwind, nx, c, 0.5, 0.0)
    ax1.plot(x, exact_solution(x, 1.0, c), "k--", label="厳密解")
    for name, scheme in (("風上差分", upwind), ("ラックス-ヴェンドロフ法", lax_wendroff)):
        x, u = solve(scheme, nx, c, 0.5, 1.0)
        ax1.plot(x, u, label=name)
    ax1.set_title("t = 1(1 周後)、クーラン数 0.5")
    ax1.set_xlabel("x")
    ax1.set_ylabel("u")
    ax1.legend()

    # 不安定になる例
    t_end = 0.05
    x, _ = solve(upwind, nx, c, 0.5, 0.0)
    ax2.plot(x, exact_solution(x, t_end, c), "k--", label="厳密解")
    x, u = solve(ftcs, nx, c, 0.5, t_end)
    ax2.plot(x, u, label="FTCS 法(クーラン数 0.5)")
    x, u = solve(upwind, nx, c, 1.2, t_end)
    ax2.plot(x, u, label="風上差分(クーラン数 1.2)")
    ax2.set_ylim(-2.0, 3.0)
    ax2.set_title(f"t = {t_end}")
    ax2.set_xlabel("x")
    ax2.legend()
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
