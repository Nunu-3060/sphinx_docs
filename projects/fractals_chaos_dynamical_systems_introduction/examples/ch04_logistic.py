"""ロジスティック写像の時系列、分岐図、ファイゲンバウム定数.

ロジスティック写像 x_{n+1} = r x_n (1 - x_n) を、パラメータ r を変えながら調べる。

使い方: python ch04_logistic.py [--save DIR]
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from numpy.typing import NDArray

import plot_util


def orbit(r: float, x0: float, n: int) -> NDArray[np.float64]:
    """パラメータ r、初期値 x0 の軌道 x0, x1, ..., xn を返す."""
    xs = np.empty(n + 1)
    xs[0] = x0
    for i in range(n):
        xs[i + 1] = r * xs[i] * (1.0 - xs[i])
    return xs


def bifurcation_points(r_min: float, r_max: float, n_r: int = 1500, transient: int = 500,
                       keep: int = 200) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """分岐図の点 (r, x) を返す.

    n_r 個の r の値について、軌道をまとめて（ベクトル化して）計算する。最初の transient 回の
    反復は、アトラクタに近づくまでの過渡状態として捨て、続く keep 回の値を記録する。
    """
    r = np.linspace(r_min, r_max, n_r)
    x = np.full(n_r, 0.5)
    for _ in range(transient):
        x = r * x * (1.0 - x)
    rs = np.empty((keep, n_r))
    xs = np.empty((keep, n_r))
    for i in range(keep):
        x = r * x * (1.0 - x)
        rs[i] = r
        xs[i] = x
    return rs.ravel(), xs.ravel()


def plot_bifurcation(ax: Axes, r_min: float, r_max: float, x_min: float = 0.0, x_max: float = 1.0,
                     transient: int = 500) -> None:
    """r の範囲 [r_min, r_max] の分岐図を ax に描く."""
    rs, xs = bifurcation_points(r_min, r_max, transient=transient, keep=300)
    ax.plot(rs, xs, ",", color="k", alpha=0.25)
    ax.set_xlim(r_min, r_max)
    ax.set_ylim(x_min, x_max)
    ax.set_xlabel("$r$")
    ax.set_ylabel("$x$")


def superstable_parameters(count: int) -> list[float]:
    """周期 2^n の超安定な軌道を持つパラメータ R_0, R_1, ... を count 個求める.

    超安定な軌道は、f の微分が 0 になる点 x = 1/2 を通る。そこで
    f_r を 2^n 回適用した値が 1/2 に戻る r を、割線法で解く。初期値は、
    それまでに求めた R から、間隔がほぼ一定の比で縮むことを使って予想する。
    """
    def g(r: float, n: int) -> float:
        x = 0.5
        for _ in range(2**n):
            x = r * x * (1.0 - x)
        return x - 0.5

    params = [2.0, 1.0 + np.sqrt(5.0)]
    while len(params) < count:
        n = len(params)
        guess = params[-1] + (params[-1] - params[-2]) / 4.7
        r0, r1 = guess, guess + 1e-6 * (params[-1] - params[-2])
        for _ in range(50):
            g0, g1 = g(r0, n), g(r1, n)
            if g1 == g0:
                break
            r0, r1 = r1, r1 - g1 * (r1 - r0) / (g1 - g0)
            if abs(r1 - r0) < 1e-15:
                break
        params.append(float(r1))
    return params[:count]


def create_figures() -> dict[str, Figure]:
    """時系列（timeseries）、分岐図（bifurcation）、周期 3 の窓の拡大（window）、間欠性（intermittency）の図を作る."""
    fig1, axes1 = plt.subplots(1, 4, figsize=(14.0, 3.0), sharey=True)
    for ax, r in zip(axes1, (2.8, 3.2, 3.5, 3.9)):
        ax.plot(orbit(r, 0.1, 60), "o-", markersize=2.5, linewidth=0.8)
        ax.set_title(f"$r = {r}$")
        ax.set_xlabel("$n$")
        ax.set_ylim(0.0, 1.0)
        ax.grid(True, color="0.9")
    axes1[0].set_ylabel("$x_n$")
    fig1.tight_layout()

    fig2, ax2 = plt.subplots(figsize=(10.0, 5.0))
    plot_bifurcation(ax2, 2.5, 4.0)
    for r in (3.0, 1.0 + np.sqrt(6.0)):
        ax2.axvline(r, color="C3", linewidth=0.8, linestyle="--")
    fig2.tight_layout()

    fig3, (ax3, ax4) = plt.subplots(1, 2, figsize=(11.0, 4.4))
    plot_bifurcation(ax3, 3.82, 3.86)
    ax3.set_title("周期 3 の窓")
    ax3.add_patch(Rectangle((3.841, 0.44), 0.016, 0.12, fill=False, edgecolor="C3", linewidth=1.2))
    plot_bifurcation(ax4, 3.841, 3.857, 0.44, 0.56, transient=2000)
    ax4.set_title("左の赤枠の拡大")
    fig3.tight_layout()

    fig4, ax5 = plt.subplots(figsize=(10.0, 3.0))
    r = 3.8282
    ax5.plot(orbit(r, 0.3, 400), linewidth=0.8)
    ax5.set_title(f"$r = {r}$（周期 3 の窓が始まる $r = 1 + \\sqrt{{8}} \\approx 3.82843$ のわずかに手前）")
    ax5.set_xlabel("$n$")
    ax5.set_ylabel("$x_n$")
    fig4.tight_layout()
    return {"timeseries": fig1, "bifurcation": fig2, "window": fig3, "intermittency": fig4}


def report() -> None:
    """超安定なパラメータ R_n と、間隔の比 δ_n = (R_{n-1} - R_{n-2}) / (R_n - R_{n-1}) を表示する."""
    params = superstable_parameters(9)
    print(" n  周期   R_n                 δ_n")
    for n, r in enumerate(params):
        if n >= 2:
            delta = (params[n - 1] - params[n - 2]) / (r - params[n - 1])
            print(f"{n:2d}  {2**n:4d}   {r:.12f}  {delta:.6f}")
        else:
            print(f"{n:2d}  {2**n:4d}   {r:.12f}")


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures, report)


if __name__ == "__main__":
    main()
