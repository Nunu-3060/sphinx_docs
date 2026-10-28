"""ロジスティック写像のリアプノフ指数を計算し、分岐図と並べる.

リアプノフ指数 λ は、軌道に沿った微分の絶対値の対数の平均
λ = lim (1/N) Σ log|f'(x_n)| で、f'(x) = r (1 - 2x) である。

使い方: python ch05_lyapunov.py [--save DIR]
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import plot_util
from ch04_logistic import plot_bifurcation


def lyapunov_exponents(r: NDArray[np.float64], n: int = 2000, transient: int = 500) -> NDArray[np.float64]:
    """配列 r の各要素について、リアプノフ指数をまとめて計算する."""
    x = np.full(r.shape, 0.4)
    for _ in range(transient):
        x = r * x * (1.0 - x)
    total = np.zeros(r.shape)
    for _ in range(n):
        x = r * x * (1.0 - x)
        # 微分が 0 になる点（x = 1/2）を通ると log 0 になるので、ごく小さな値で下から抑える
        total += np.log(np.maximum(np.abs(r * (1.0 - 2.0 * x)), 1e-300))
    result: NDArray[np.float64] = total / n
    return result


def create_figures() -> dict[str, Figure]:
    """分岐図（上）とリアプノフ指数（下）を、横軸をそろえて描く（lyapunov）."""
    r_min, r_max = 2.5, 4.0
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10.0, 6.4), sharex=True)
    plot_bifurcation(ax1, r_min, r_max)
    ax1.set_xlabel("")
    r = np.linspace(r_min, r_max, 3000)
    lam = lyapunov_exponents(r)
    ax2.plot(r, lam, linewidth=0.6)
    ax2.axhline(0.0, color="C3", linewidth=0.8)
    ax2.set_ylim(-2.0, 1.0)
    ax2.set_xlabel("$r$")
    ax2.set_ylabel("リアプノフ指数 $\\lambda$")
    ax2.grid(True, color="0.9")
    fig.tight_layout()
    return {"lyapunov": fig}


def report() -> None:
    """いくつかの r でのリアプノフ指数を表示する。r = 4 の理論値は log 2 である."""
    r = np.array([2.8, 3.2, 3.5, 3.83, 3.9, 4.0])
    lam = lyapunov_exponents(r, n=100000)
    for ri, li in zip(r, lam):
        print(f"r = {ri:.2f}: λ = {li:+.4f}")
    print(f"log 2 = {np.log(2.0):.4f}")


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures, report)


if __name__ == "__main__":
    main()
