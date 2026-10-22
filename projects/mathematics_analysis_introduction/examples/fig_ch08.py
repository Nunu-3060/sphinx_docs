"""第 8 章（関数列と関数項級数）の図を生成する。

生成する図（source/images に保存する）:
    ch08_xn.png             x^n の各点収束（極限が不連続になる）
    ch08_uniform_band.png   一様収束の意味（ε 帯に関数全体が入る）
    ch08_spike.png          n x e^{-n x^2}（積分と極限を交換できない例）
    ch08_gibbs.png          矩形波のフーリエ部分和とギブズ現象

実行方法:
    python fig_ch08.py
"""

import math

import matplotlib.pyplot as plt
import numpy as np

from ch08_uniform_convergence import spike, square_wave_partial_sum
from plot_style import save, setup_style


def make_xn() -> None:
    """f_n(x) = x^n のグラフを重ねて描く。"""
    x = np.linspace(0.0, 1.0, 500)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for n in [1, 2, 5, 10, 30, 100]:
        ax.plot(x, x**n, label=f"$n = {n}$")
    # 極限関数：[0, 1) で 0、x = 1 で 1
    ax.plot([0, 1], [0, 0], color="black", linewidth=2.5, label="極限関数")
    ax.plot([1], [1], "o", color="black")
    ax.plot([1], [0], "o", color="black", markerfacecolor="white")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$x^n$")
    ax.legend(fontsize=9, loc="upper left")
    ax.set_title("$f_n(x) = x^n$ の各点収束")
    save(fig, "ch08_xn.png")


def make_uniform_band() -> None:
    """f(x) = sin x の ε 帯と、その中に収まる f_n(x) = sin x + sin(8x)/n を描く。"""
    x = np.linspace(0.0, 2.0 * math.pi, 1000)
    f = np.sin(x)
    eps = 0.3
    n = 4
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.fill_between(x, f - eps, f + eps, color="tab:orange", alpha=0.25,
                    label=r"$\varepsilon$ 帯 $f(x) \pm \varepsilon$")
    ax.plot(x, f, color="black", linewidth=1.5, label="$f(x) = \\sin x$")
    ax.plot(x, f + np.sin(8.0 * x) / n, color="tab:blue",
            label=r"$f_n(x) = \sin x + \sin(8x)/n$（$n = 4$）")
    ax.set_xlabel("$x$")
    ax.legend(fontsize=9, loc="lower left")
    ax.set_title(r"一様収束：$n \geq N$ ならグラフ全体が $\varepsilon$ 帯に入る（$\varepsilon = 0.3$）")
    save(fig, "ch08_uniform_band.png")


def make_spike() -> None:
    """g_n(x) = n x e^{-n x^2} のグラフを重ねて描く。"""
    x = np.linspace(0.0, 1.0, 2000)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for n in [1, 5, 20, 100, 400]:
        ax.plot(x, spike(n, x), label=f"$n = {n}$")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$g_n(x)$")
    ax.legend(fontsize=9)
    ax.set_title("$g_n(x) = n x e^{-n x^2}$（$n$ を大きくすると面積は 1/2 に近づく）")
    save(fig, "ch08_spike.png")


def make_gibbs() -> None:
    """矩形波とフーリエ部分和を、全体図と不連続点付近の拡大図で描く。"""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    x_all = np.linspace(-math.pi, math.pi, 4000)
    x_zoom = np.linspace(0.0, 0.6, 2000)
    for ax, x in [(axes[0], x_all), (axes[1], x_zoom)]:
        ax.plot(x, np.sign(x), color="black", linewidth=1.5, label="矩形波")
        for num_terms in [5, 20, 80]:
            ax.plot(x, square_wave_partial_sum(num_terms, x), linewidth=1.0, label=f"{num_terms} 項の部分和")
        ax.axhline(1.17898, color="gray", linestyle="--", linewidth=1.0, label="1.179")
        ax.set_xlabel("$x$")
        ax.legend(fontsize=8, loc="lower right")
    axes[0].set_title("全体（$-\\pi \\leq x \\leq \\pi$）")
    axes[1].set_title("不連続点 $x = 0$ の右側の拡大")
    axes[1].set_ylim(0.0, 1.3)
    save(fig, "ch08_gibbs.png")


def main() -> None:
    """第 8 章の図をすべて生成する。"""
    setup_style()
    make_xn()
    make_uniform_band()
    make_spike()
    make_gibbs()


if __name__ == "__main__":
    main()
