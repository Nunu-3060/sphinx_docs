"""第 6 章「テイラーの定理と近似」の図を生成する。

生成する図（source/images に保存）:
    ch06_taylor_sin.png  sin(x) とマクローリン多項式
    ch06_flat.png        exp(-1/x^2) のグラフ
    ch06_newton.png      ニュートン法の幾何学的な意味

実行方法:
    python fig_ch06.py
"""

import math

import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

from plot_style import save, setup_style

FloatArray = npt.NDArray[np.float64]


def sin_taylor(x: FloatArray, n: int) -> FloatArray:
    """sin(x) の n 次マクローリン多項式の値を返す（n は奇数）。"""
    total = np.zeros_like(x)
    for k in range(0, n // 2 + 1):
        total += (-1) ** k * x ** (2 * k + 1) / math.factorial(2 * k + 1)
    return total


def plot_taylor_sin() -> None:
    """sin(x) と 1, 3, 5, 7, 9 次のマクローリン多項式を描く。"""
    x = np.linspace(-2.0 * np.pi, 2.0 * np.pi, 600)
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    ax.plot(x, np.sin(x), color="black", linewidth=2.5, label=r"$\sin x$")
    for n in [1, 3, 5, 7, 9]:
        ax.plot(x, sin_taylor(x, n), linewidth=1.2, label=f"{n} 次")
    ax.set_xlim(-2.0 * np.pi, 2.0 * np.pi)
    ax.set_ylim(-2.0, 2.0)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.legend(loc="lower left", fontsize=9, ncol=2)
    save(fig, "ch06_taylor_sin.png")


def plot_flat() -> None:
    """f(x) = exp(-1/x^2)（f(0) = 0）のグラフを描く。"""
    x = np.linspace(-3.0, 3.0, 1201)
    y = np.zeros_like(x)
    nonzero = x != 0.0
    y[nonzero] = np.exp(-1.0 / x[nonzero] ** 2)

    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.plot(x, y, color="tab:blue", linewidth=2, label=r"$y = f(x)$")
    ax.axhline(0.0, color="tab:red", linestyle="--", linewidth=1.2, label="原点でのテイラー級数（恒等的に 0）")
    ax.set_xlim(-3.0, 3.0)
    ax.set_ylim(-0.1, 1.0)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.legend(loc="upper center", fontsize=9)
    save(fig, "ch06_flat.png")


def plot_newton() -> None:
    """f(x) = x^2 - 2 に対するニュートン法の反復を接線で描く。"""
    def f(x: FloatArray) -> FloatArray:
        return x ** 2 - 2.0

    x = np.linspace(1.0, 3.2, 300)
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    ax.plot(x, f(x), color="black", linewidth=2, label=r"$y = x^2 - 2$")
    ax.axhline(0.0, color="gray", linewidth=0.8)

    xn = 3.0
    colors = ["tab:blue", "tab:green", "tab:orange"]
    for n, color in enumerate(colors):
        fx = xn ** 2 - 2.0
        x_next = xn - fx / (2.0 * xn)
        ax.plot([xn, xn], [0.0, fx], color="gray", linestyle=":", linewidth=1)
        ax.plot([xn, x_next], [fx, 0.0], color=color, linewidth=1.5, label=f"$x_{n}$ における接線")
        ax.plot([xn], [fx], "o", color=color)
        ax.annotate(f"$x_{n}$", (xn, 0.0), textcoords="offset points", xytext=(-4, -16))
        xn = x_next
    ax.plot([np.sqrt(2.0)], [0.0], "*", color="tab:red", markersize=12, label=r"解 $\sqrt{2}$")
    ax.set_xlim(1.0, 3.2)
    ax.set_ylim(-1.5, 8.5)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.legend(loc="upper left", fontsize=9)
    save(fig, "ch06_newton.png")


def main() -> None:
    """第 6 章の図をすべて生成する。"""
    setup_style()
    plot_taylor_sin()
    plot_flat()
    plot_newton()


if __name__ == "__main__":
    main()
