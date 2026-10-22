"""第 4 章「関数の極限と連続性」の図を生成する。

生成する図（source/images に保存する）:

* ch04_epsilon_delta.png   : ε-δ 論法の図解
* ch04_discontinuous.png   : 不連続な関数・振動する関数の例
* ch04_bisection.png       : 中間値の定理と二分法
* ch04_uniform.png         : y = 1/x が一様連続でないことの図解

実行方法::

    python fig_ch04.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from plot_style import save, setup_style


def draw_epsilon_delta(ax: Axes, a: float, delta: float, epsilon: float) -> None:
    """関数 y = x^2 / 2 + 0.5 の点 a における ε 帯と δ 帯を描く。"""
    x = np.linspace(0.0, 2.5, 400)
    y = x**2 / 2.0 + 0.5
    fa = a**2 / 2.0 + 0.5
    ax.plot(x, y, color="black")
    # 横の帯：f(a) - ε < y < f(a) + ε
    ax.axhspan(fa - epsilon, fa + epsilon, color="tab:orange", alpha=0.25, label=r"$|y - f(a)| < \varepsilon$")
    # 縦の帯：a - δ < x < a + δ
    ax.axvspan(a - delta, a + delta, color="tab:blue", alpha=0.25, label=r"$|x - a| < \delta$")
    # δ 帯の中のグラフを太く描く
    xs = np.linspace(a - delta, a + delta, 100)
    ax.plot(xs, xs**2 / 2.0 + 0.5, color="tab:red", linewidth=3)
    ax.plot([a], [fa], "o", color="tab:red")
    ax.set_xticks([a - delta, a, a + delta], [r"$a-\delta$", r"$a$", r"$a+\delta$"])
    ax.set_yticks([fa - epsilon, fa, fa + epsilon], [r"$f(a)-\varepsilon$", r"$f(a)$", r"$f(a)+\varepsilon$"])
    ax.set_xlim(0.0, 2.5)
    ax.set_ylim(0.0, 3.5)


def plot_epsilon_delta() -> None:
    """ε-δ 論法の図を描く。δ が十分小さければグラフは ε 帯に収まる。"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    a, epsilon = 1.2, 0.4
    draw_epsilon_delta(ax1, a, 0.6, epsilon)
    ax1.set_title(r"$\delta$ が大きすぎる（はみ出す）")
    draw_epsilon_delta(ax2, a, 0.25, epsilon)
    ax2.set_title(r"$\delta$ を小さくすると帯に収まる")
    ax2.legend(loc="upper left")
    save(fig, "ch04_epsilon_delta.png")


def plot_discontinuous() -> None:
    """階段関数、sin(1/x)、x sin(1/x) のグラフを並べる。"""
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.8))

    ax = axes[0]
    ax.plot([-1.0, 0.0], [0.0, 0.0], color="tab:blue")
    ax.plot([0.0, 1.0], [1.0, 1.0], color="tab:blue")
    ax.plot([0.0], [1.0], "o", color="tab:blue")
    ax.plot([0.0], [0.0], "o", markerfacecolor="white", color="tab:blue")
    ax.set_ylim(-0.5, 1.5)
    ax.set_title("(a) 階段関数（0 で不連続）")

    x = np.linspace(-0.5, 0.5, 20001)
    x = x[x != 0.0]
    ax = axes[1]
    ax.plot(x, np.sin(1.0 / x), linewidth=0.6, color="tab:blue")
    ax.set_title(r"(b) $\sin(1/x)$（0 で極限なし）")

    ax = axes[2]
    ax.plot(x, x * np.sin(1.0 / x), linewidth=0.6, color="tab:blue")
    ax.plot(x, np.abs(x), "--", color="gray", linewidth=0.8)
    ax.plot(x, -np.abs(x), "--", color="gray", linewidth=0.8)
    ax.set_title(r"(c) $x \sin(1/x)$（0 で極限 0）")
    for ax in axes:
        ax.set_xlabel(r"$x$")
    save(fig, "ch04_discontinuous.png")


def plot_bisection() -> None:
    """f(x) = x^3 - 2 に二分法を適用したときの区間の縮み方を描く。"""
    x = np.linspace(0.9, 2.1, 400)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(x, x**3 - 2.0, color="black", label=r"$y = x^3 - 2$")
    ax.axhline(0.0, color="gray", linewidth=0.8)
    a, b = 1.0, 2.0
    for k in range(5):
        level = -1.5 - 0.8 * k
        ax.plot([a, b], [level, level], "|-", color="tab:blue", linewidth=2, markersize=10)
        ax.text(2.12, level, rf"$[a_{k}, b_{k}]$", va="center")
        c = (a + b) / 2.0
        if c**3 - 2.0 > 0:
            b = c
        else:
            a = c
    root = 2.0 ** (1.0 / 3.0)
    ax.plot([root], [0.0], "o", color="tab:red", label=r"解 $2^{1/3}$")
    ax.set_xlim(0.9, 2.4)
    ax.set_ylim(-5.5, 6.5)
    ax.set_xlabel(r"$x$")
    ax.legend(loc="upper left")
    save(fig, "ch04_bisection.png")


def plot_uniform() -> None:
    """y = 1/x で、同じ ε に対して必要な δ が x → 0 で小さくなる様子を描く。"""
    x = np.linspace(0.12, 2.0, 400)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(x, 1.0 / x, color="black", label=r"$y = 1/x$")
    epsilon = 0.5
    for a, color in [(1.2, "tab:blue"), (0.3, "tab:red")]:
        fa = 1.0 / a
        # |1/x - 1/a| < ε となる x の範囲は a の左側の方が狭いので、左側の幅を δ とする
        delta = a - 1.0 / (fa + epsilon)
        ax.axhspan(fa - epsilon, fa + epsilon, color=color, alpha=0.15)
        ax.axvspan(a - delta, a + delta, color=color, alpha=0.3)
        ax.plot([a], [fa], "o", color=color, label=rf"$a = {a}$ では $\delta \approx {delta:.3f}$")
    ax.set_xlim(0.0, 2.0)
    ax.set_ylim(0.0, 6.0)
    ax.set_xlabel(r"$x$")
    ax.set_title(r"同じ $\varepsilon = 0.5$ でも、$a$ が 0 に近いほど $\delta$ を小さくとる必要がある")
    ax.legend()
    save(fig, "ch04_uniform.png")


def main() -> None:
    """第 4 章の図をすべて生成する。"""
    setup_style()
    plot_epsilon_delta()
    plot_discontinuous()
    plot_bisection()
    plot_uniform()


if __name__ == "__main__":
    main()
