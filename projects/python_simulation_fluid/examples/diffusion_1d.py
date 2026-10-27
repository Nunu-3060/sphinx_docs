"""1 次元拡散方程式の差分解法。

両端の値を 0 に固定した区間 [0, 1] で拡散方程式 du/dt = nu d^2u/dx^2 を
陽解法(FTCS 法)で解き、厳密解と比較する。拡散数 r = nu dt / dx^2 が
1/2 を超えると計算が不安定になることも確かめる。

実行方法::

    python diffusion_1d.py
"""
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

FloatArray = npt.NDArray[np.float64]

# 初期条件を構成する正弦波の (波数 k, 振幅)
MODES = ((1, 1.0), (6, 0.3))


def exact_solution(x: FloatArray, t: float, nu: float) -> FloatArray:
    """厳密解: 各正弦波は、それぞれ exp(-nu (k pi)^2 t) の割合で減衰する。"""
    u = np.zeros_like(x)
    for k, amp in MODES:
        u += amp * np.sin(k * np.pi * x) * np.exp(-nu * (k * np.pi) ** 2 * t)
    return u


def solve(nx: int, nu: float, r: float, t_end: float) -> tuple[FloatArray, FloatArray]:
    """格子点数 nx、拡散数 r で t_end まで計算し、(x, u) を返す。"""
    x = np.linspace(0.0, 1.0, nx)
    dx = x[1] - x[0]
    dt = r * dx**2 / nu
    n_steps = round(t_end / dt)
    u = exact_solution(x, 0.0, nu)
    for _ in range(n_steps):
        # 内部の点だけを更新する(両端 u[0] と u[-1] は 0 のまま)
        u[1:-1] = u[1:-1] + r * (u[2:] - 2.0 * u[1:-1] + u[:-2])
    return x, u


def main() -> None:
    nu = 1.0
    nx = 51

    plt.rcParams["font.family"] = ["Meiryo", "sans-serif"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    x_fine = np.linspace(0.0, 1.0, 400)
    for t in (0.0, 0.005, 0.02, 0.05):
        ax1.plot(x_fine, exact_solution(x_fine, t, nu), "k--", lw=1)
        x, u = solve(nx, nu, 0.4, t)
        ax1.plot(x, u, "o", ms=3, label=f"t = {t}")
    ax1.set_title("拡散数 r = 0.4(破線は厳密解)")
    ax1.set_xlabel("x")
    ax1.set_ylabel("u")
    ax1.legend()

    t_end = 0.045
    ax2.plot(x_fine, exact_solution(x_fine, t_end, nu), "k--", lw=1, label="厳密解")
    for r in (0.5, 0.55):
        x, u = solve(nx, nu, r, t_end)
        ax2.plot(x, u, "o-", ms=3, label=f"r = {r}")
    ax2.set_ylim(-0.2, 1.0)
    ax2.set_title(f"t = {t_end}")
    ax2.set_xlabel("x")
    ax2.legend()
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
