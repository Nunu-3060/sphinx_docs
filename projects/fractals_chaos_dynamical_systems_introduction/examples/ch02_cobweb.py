"""1 次元写像の反復を、クモの巣図（cobweb plot）で調べる.

使い方: python ch02_cobweb.py [--save DIR]
"""

from collections.abc import Callable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy.typing import NDArray

import plot_util

Map = Callable[[NDArray[np.float64]], NDArray[np.float64]]


def logistic(r: float) -> Map:
    """パラメータ r のロジスティック写像 f(x) = r x (1 - x) を返す."""
    def f(x: NDArray[np.float64]) -> NDArray[np.float64]:
        return r * x * (1.0 - x)
    return f


def cobweb(ax: Axes, f: Map, x0: float, n: int, lo: float = 0.0, hi: float = 1.0) -> None:
    """写像 f のグラフ、対角線 y = x、x0 から n 回反復したクモの巣図を ax に描く.

    点 (x, x) から縦に動いてグラフ上の点 (x, f(x)) へ、そこから横に動いて
    対角線上の点 (f(x), f(x)) へ進む。これを繰り返すと、軌道 x0, x1, x2, ... が描ける。
    """
    grid = np.linspace(lo, hi, 400)
    ax.plot(grid, f(grid), color="C0", linewidth=1.5)
    ax.plot([lo, hi], [lo, hi], color="0.5", linewidth=1.0)
    x = np.array(x0)
    px, py = [x0], [x0]
    for _ in range(n):
        y = float(f(x))
        px += [float(x), y]
        py += [y, y]
        x = np.array(y)
    ax.plot(px, py, color="C3", linewidth=0.8)
    ax.plot(x0, x0, "o", color="C3", markersize=4)
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_aspect("equal")
    ax.set_xlabel("$x_n$")
    ax.set_ylabel("$x_{n+1}$")


def create_figures() -> dict[str, Figure]:
    """線形写像の安定性（linear）、ロジスティック写像（logistic）、2 回反復の写像（second）の図を作る."""
    fig1, axes1 = plt.subplots(1, 4, figsize=(13.0, 3.6))
    for ax, a in zip(axes1, (0.5, -0.5, 1.5, -1.5)):
        def linear(x: NDArray[np.float64], a: float = a) -> NDArray[np.float64]:
            return a * x
        cobweb(ax, linear, 0.8 if abs(a) < 1.0 else 0.05, 12, -1.0, 1.0)
        ax.set_title(f"$f(x) = {a}\\,x$")
    fig1.tight_layout()

    fig2, axes2 = plt.subplots(1, 3, figsize=(12.0, 4.2))
    for ax, r in zip(axes2, (2.8, 3.2, 3.9)):
        cobweb(ax, logistic(r), 0.1, 60 if r < 3.5 else 40)
        ax.set_title(f"$r = {r}$")
    fig2.tight_layout()

    r = 3.2
    f = logistic(r)
    grid = np.linspace(0.0, 1.0, 400)
    fig3, ax3 = plt.subplots(figsize=(7.4, 5.0))
    ax3.plot(grid, f(grid), label="$f(x)$")
    ax3.plot(grid, f(f(grid)), label="$f^2(x) = f(f(x))$")
    ax3.plot([0.0, 1.0], [0.0, 1.0], color="0.5", linewidth=1.0, label="$y = x$")
    p, q = period2_points(r)
    star = 1.0 - 1.0 / r
    ax3.plot([p, q], [p, q], "o", color="C3", label="周期 2 の点")
    ax3.plot([0.0, star], [0.0, star], "s", color="k", markersize=5, label="$f$ の固定点")
    ax3.set_xlim(0.0, 1.0)
    ax3.set_ylim(0.0, 1.0)
    ax3.set_aspect("equal")
    ax3.set_title(f"$r = {r}$")
    ax3.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0))
    fig3.tight_layout()
    return {"linear": fig1, "logistic": fig2, "second": fig3}


def period2_points(r: float) -> tuple[float, float]:
    """ロジスティック写像の周期 2 の点 p < q を返す（r > 3 で存在する）.

    f(f(x)) = x の 4 次方程式から固定点 0 と 1 - 1/r を除いた 2 次方程式
    r^2 x^2 - r (r + 1) x + (r + 1) = 0 の解である。
    """
    disc = (r + 1.0) * (r - 3.0)
    p = (r + 1.0 - np.sqrt(disc)) / (2.0 * r)
    q = (r + 1.0 + np.sqrt(disc)) / (2.0 * r)
    return float(p), float(q)


def report() -> None:
    """固定点と周期 2 の点、それらの安定性を判定する微分係数を表示する."""
    for r in (2.8, 3.2):
        star = 1.0 - 1.0 / r
        print(f"r = {r}: 固定点 x* = {star:.6f}, f'(x*) = {2.0 - r:+.6f}")
    r = 3.2
    p, q = period2_points(r)
    multiplier = r * (1.0 - 2.0 * p) * r * (1.0 - 2.0 * q)
    print(f"r = {r}: 周期 2 の点 p = {p:.6f}, q = {q:.6f}, f'(p) f'(q) = {multiplier:+.6f}")


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures, report)


if __name__ == "__main__":
    main()
