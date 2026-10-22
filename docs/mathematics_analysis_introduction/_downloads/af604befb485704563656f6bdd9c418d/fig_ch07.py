"""第 7 章（積分）の図を生成する。

生成する図（source/images に保存する）:
    ch07_darboux_sums.png      上限和と下限和
    ch07_riemann_sum.png       リーマン和（代表点のとり方）
    ch07_trapezoid_simpson.png 台形公式とシンプソン公式の近似の様子
    ch07_quadrature_error.png  分割数と数値積分の誤差（両対数グラフ）

実行方法:
    python fig_ch07.py
"""

import math

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib.axes import Axes

from ch07_numerical_integration import simpson, trapezoid
from plot_style import save, setup_style

FloatArray = npt.NDArray[np.float64]


def sample_function(x: FloatArray) -> FloatArray:
    """図示に使う関数 f(x) = 1 + 0.6 sin(2x) + 0.2x（区間 [0, 3] で増減がある）。"""
    return 1.0 + 0.6 * np.sin(2.0 * x) + 0.2 * x


def draw_darboux(ax: Axes, n: int) -> None:
    """区間 [0, 3] を n 等分したときの上限和（枠）と下限和（塗り）を描く。"""
    a, b = 0.0, 3.0
    x = np.linspace(a, b, 600)
    ax.plot(x, sample_function(x), color="black", linewidth=1.5, label="$y = f(x)$")
    edges = np.linspace(a, b, n + 1)
    for left, right in zip(edges[:-1], edges[1:]):
        # 小区間上の上限・下限は、細かい格子点上の最大値・最小値で近似する
        values = sample_function(np.linspace(left, right, 200))
        lower, upper = float(values.min()), float(values.max())
        ax.fill_between([left, right], 0, lower, color="tab:blue", alpha=0.35, linewidth=0)
        ax.plot([left, left, right, right], [0, upper, upper, 0], color="tab:orange", linewidth=1.2)
    ax.plot([], [], color="tab:orange", label="上限和の長方形")
    ax.fill_between([], [], color="tab:blue", alpha=0.35, label="下限和の長方形")
    ax.set_title(f"分割数 n = {n}")
    ax.set_xlabel("$x$")
    ax.set_ylim(0, 2.2)
    ax.legend(loc="upper right", fontsize=9)


def make_darboux_sums() -> None:
    """上限和と下限和の図を作る。"""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    draw_darboux(axes[0], 6)
    draw_darboux(axes[1], 24)
    save(fig, "ch07_darboux_sums.png")


def make_riemann_sum() -> None:
    """代表点をばらばらにとったリーマン和の図を作る。"""
    a, b, n = 0.0, 3.0, 8
    rng = np.random.default_rng(seed=7)
    edges = np.linspace(a, b, n + 1)
    tags = edges[:-1] + rng.random(n) * (edges[1:] - edges[:-1])

    fig, ax = plt.subplots(figsize=(7, 4))
    x = np.linspace(a, b, 600)
    ax.plot(x, sample_function(x), color="black", linewidth=1.5, label="$y = f(x)$")
    heights = sample_function(tags)
    for left, right, height in zip(edges[:-1], edges[1:], heights):
        ax.fill_between([left, right], 0, height, color="tab:green", alpha=0.3, edgecolor="tab:green")
    ax.plot(tags, heights, "o", color="tab:red", label=r"代表点 $(\xi_i, f(\xi_i))$")
    ax.plot(edges, np.zeros_like(edges), "|", color="black", markersize=12)
    ax.set_xlabel("$x$")
    ax.set_ylim(0, 2.2)
    ax.legend(loc="upper right", fontsize=9)
    ax.set_title("リーマン和（分割数 8、代表点は小区間内の任意の点）")
    save(fig, "ch07_riemann_sum.png")


def make_trapezoid_simpson() -> None:
    """台形公式（折れ線で近似）とシンプソン公式（放物線で近似）の図を作る。"""
    a, b, n = 0.0, 3.0, 4
    edges = np.linspace(a, b, n + 1)
    x = np.linspace(a, b, 600)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    ax = axes[0]
    ax.plot(x, sample_function(x), color="black", linewidth=1.5, label="$y = f(x)$")
    ax.fill_between(edges, 0, sample_function(edges), color="tab:blue", alpha=0.3, label="台形の和")
    ax.plot(edges, sample_function(edges), "o-", color="tab:blue")
    ax.set_title("台形公式（n = 4）")

    ax = axes[1]
    ax.plot(x, sample_function(x), color="black", linewidth=1.5, label="$y = f(x)$")
    for i in range(0, n, 2):
        # 3 点 (x_i, x_{i+1}, x_{i+2}) を通る 2 次式（放物線）で近似する
        xs = edges[i:i + 3]
        coef = np.polyfit(xs, sample_function(xs), 2)
        xx = np.linspace(xs[0], xs[-1], 200)
        label = "放物線の下の面積" if i == 0 else None
        ax.fill_between(xx, 0, np.polyval(coef, xx), color="tab:purple", alpha=0.3, label=label)
        ax.plot(xx, np.polyval(coef, xx), color="tab:purple")
    ax.plot(edges, sample_function(edges), "o", color="tab:purple")
    ax.set_title("シンプソン公式（n = 4）")

    for ax in axes:
        ax.set_xlabel("$x$")
        ax.set_ylim(0, 2.2)
        ax.legend(loc="upper right", fontsize=9)
    save(fig, "ch07_trapezoid_simpson.png")


def make_quadrature_error() -> None:
    """∫_0^1 e^x dx に対する誤差を、刻み幅 h に対して両対数で描く。"""
    exact = math.e - 1.0
    ns = [2**k for k in range(1, 15)]
    hs = np.array([1.0 / n for n in ns])
    err_trap = np.array([abs(trapezoid(np.exp, 0.0, 1.0, n) - exact) for n in ns])
    err_simp = np.array([abs(simpson(np.exp, 0.0, 1.0, n) - exact) for n in ns])
    # 丸め誤差の影響で誤差がちょうど 0 になる点は対数軸に描けないので除く
    err_simp[err_simp == 0.0] = np.nan

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.loglog(hs, err_trap, "o-", label="台形公式")
    ax.loglog(hs, err_simp, "s-", label="シンプソン公式")
    ax.loglog(hs, 0.15 * hs**2, "--", color="gray", label="傾き 2（$h^2$ に比例）")
    ax.loglog(hs, 0.003 * hs**4, ":", color="gray", label="傾き 4（$h^4$ に比例）")
    ax.set_xlabel("刻み幅 $h$")
    ax.set_ylabel("誤差の絶対値")
    ax.set_ylim(1e-17, 1)
    ax.legend(fontsize=9)
    ax.set_title(r"$\int_0^1 e^x\,dx$ の数値積分の誤差")
    save(fig, "ch07_quadrature_error.png")


def main() -> None:
    """第 7 章の図をすべて生成する。"""
    setup_style()
    make_darboux_sums()
    make_riemann_sum()
    make_trapezoid_simpson()
    make_quadrature_error()


if __name__ == "__main__":
    main()
