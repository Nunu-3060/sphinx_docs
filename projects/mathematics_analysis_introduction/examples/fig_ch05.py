"""第 5 章「微分」の図を生成する。

生成する図（source/images に保存）:
    ch05_tangent.png       割線が接線に近づく様子
    ch05_mvt.png           平均値の定理
    ch05_numdiff_error.png 数値微分の誤差と刻み幅の関係

実行方法:
    python fig_ch05.py
"""

import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

from plot_style import save, setup_style

FloatArray = npt.NDArray[np.float64]


def plot_tangent() -> None:
    """f(x) = x^2 / 2 + 1 について、割線が接線に近づく様子を描く。"""
    def f(x: FloatArray) -> FloatArray:
        return 0.5 * x ** 2 + 1.0

    a = 1.0
    fa = 0.5 * a ** 2 + 1.0
    slope = a  # f'(a) = a
    x = np.linspace(-0.5, 3.0, 300)

    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    ax.plot(x, f(x), color="black", linewidth=2, label=r"$y = f(x)$")
    for h, color in [(1.5, "tab:blue"), (0.8, "tab:green"), (0.3, "tab:orange")]:
        fah = 0.5 * (a + h) ** 2 + 1.0
        s = (fah - fa) / h
        ax.plot(x, fa + s * (x - a), color=color, linestyle="--", linewidth=1,
                label=f"割線（$h = {h}$）")
        ax.plot([a + h], [fah], "o", color=color)
    ax.plot(x, fa + slope * (x - a), color="tab:red", linewidth=2, label="接線")
    ax.plot([a], [fa], "o", color="black")
    ax.annotate(r"$(a, f(a))$", (a, fa), textcoords="offset points", xytext=(-45, 10))
    ax.set_xlim(-0.5, 3.0)
    ax.set_ylim(0.0, 5.5)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.legend(loc="upper left")
    save(fig, "ch05_tangent.png")


def plot_mvt() -> None:
    """f(x) = sin(x) + 0.3x の区間 [0.5, 3] における平均値の定理を描く。"""
    def f(x: FloatArray) -> FloatArray:
        return np.sin(x) + 0.3 * x

    a, b = 0.5, 3.0
    fa = float(np.sin(a) + 0.3 * a)
    fb = float(np.sin(b) + 0.3 * b)
    slope = (fb - fa) / (b - a)

    # f'(c) = cos(c) + 0.3 = slope となる c を格子上で探す
    grid = np.linspace(a, b, 100001)
    c = float(grid[np.argmin(np.abs(np.cos(grid) + 0.3 - slope))])
    fc = float(np.sin(c) + 0.3 * c)

    x = np.linspace(0.0, 3.5, 300)
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    ax.plot(x, f(x), color="black", linewidth=2, label=r"$y = f(x)$")
    ax.plot([a, b], [fa, fb], color="tab:blue", linewidth=1.5, label="割線（傾き $\\frac{f(b) - f(a)}{b - a}$）")
    ax.plot(x, fc + slope * (x - c), color="tab:red", linestyle="--", linewidth=1.5,
            label="点 $c$ における接線")
    ax.plot([a, b], [fa, fb], "o", color="tab:blue")
    ax.plot([c], [fc], "o", color="tab:red")
    for xv, name in [(a, "a"), (c, "c"), (b, "b")]:
        ax.axvline(xv, color="gray", linewidth=0.8, linestyle=":")
        ax.annotate(f"${name}$", (xv, 0.0), textcoords="offset points", xytext=(3, 5))
    ax.set_xlim(0.0, 3.5)
    ax.set_ylim(0.0, 2.5)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.legend(loc="upper left")
    save(fig, "ch05_mvt.png")


def plot_numdiff_error() -> None:
    """exp(x) の x = 1 における数値微分の誤差を両対数グラフで描く。"""
    x0 = 1.0
    exact = np.exp(x0)
    h = 10.0 ** np.linspace(-16, -1, 151)
    forward = np.abs((np.exp(x0 + h) - np.exp(x0)) / h - exact)
    central = np.abs((np.exp(x0 + h) - np.exp(x0 - h)) / (2.0 * h) - exact)
    eps = float(np.finfo(np.float64).eps)

    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    ax.loglog(h, forward, ".", color="tab:blue", markersize=4, label="前進差分")
    ax.loglog(h, central, ".", color="tab:orange", markersize=4, label="中心差分")
    # 誤差の上界の目安（M = exp(1) とおいた理論曲線）
    ax.loglog(h, exact * h / 2.0 + 2.0 * eps * exact / h, color="tab:blue", linewidth=1,
              label=r"上界の目安 $\frac{M h}{2} + \frac{2 \varepsilon_f}{h}$")
    ax.loglog(h, exact * h ** 2 / 6.0 + eps * exact / h, color="tab:orange", linewidth=1,
              label=r"上界の目安 $\frac{M h^2}{6} + \frac{\varepsilon_f}{h}$")
    ax.set_xlabel(r"刻み幅 $h$")
    ax.set_ylabel("誤差の絶対値")
    ax.set_ylim(1e-12, 1e1)
    ax.legend(loc="upper center", fontsize=9)
    save(fig, "ch05_numdiff_error.png")


def main() -> None:
    """第 5 章の図をすべて生成する。"""
    setup_style()
    plot_tangent()
    plot_mvt()
    plot_numdiff_error()


if __name__ == "__main__":
    main()
