"""第 2 章の図を生成する。

* ch02_epsilon_band.png：数列 a_n = 1 + (-1)^n / n と ε 帯
* ch02_monotone.png：単調増加で上に有界な数列 (1 + 1/n)^n
* ch02_newton_bisection.png：二分法とニュートン法の誤差の比較

実行方法::

    python fig_ch02.py
"""

from fractions import Fraction

import numpy as np

import matplotlib.pyplot as plt
from ch02_newton_sqrt2 import bisection_sequence, error, newton_sequence
from plot_style import save, setup_style


def plot_epsilon_band() -> None:
    """ε 帯に数列の項が入っていく様子を描く。"""
    n = np.arange(1, 41)
    a = 1.0 + (-1.0) ** n / n
    eps = 0.15
    # |a_n - 1| = 1/n < eps となる最小の n
    big_n = int(np.floor(1.0 / eps)) + 1

    fig, ax = plt.subplots(figsize=(8, 4))
    band_label = r"$\varepsilon$ 帯 $(1-\varepsilon, 1+\varepsilon)$"
    ax.axhspan(1.0 - eps, 1.0 + eps, color="tab:orange", alpha=0.2, label=band_label)
    ax.axhline(1.0, color="tab:orange", linewidth=1)
    inside = n >= big_n
    ax.plot(n[~inside], a[~inside], "o", color="tab:gray", label=r"$n < N$ の項")
    ax.plot(n[inside], a[inside], "o", color="tab:blue", label=r"$n \geq N$ の項（すべて帯の中）")
    ax.axvline(big_n - 0.5, color="tab:red", linestyle="--", linewidth=1)
    ax.text(big_n - 0.3, 1.75, rf"$N = {big_n}$", color="tab:red")
    ax.set_xlabel(r"$n$")
    ax.set_ylabel(r"$a_n$")
    ax.set_title(r"$a_n = 1 + (-1)^n / n$、$\varepsilon = 0.15$")
    ax.set_ylim(-0.1, 1.9)
    ax.legend(loc="lower right")
    save(fig, "ch02_epsilon_band.png")


def plot_monotone() -> None:
    """(1 + 1/n)^n が単調増加かつ上に有界で、e に収束する様子を描く。"""
    n = np.arange(1, 61)
    a = (1.0 + 1.0 / n) ** n

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(n, a, "o", color="tab:blue", markersize=4, label=r"$a_n = (1 + 1/n)^n$")
    ax.axhline(np.e, color="tab:orange", linestyle="--", label=r"$e = 2.71828\ldots$")
    ax.axhline(3.0, color="tab:red", linestyle=":", label="上界 3")
    ax.set_xlabel(r"$n$")
    ax.set_ylabel(r"$a_n$")
    ax.set_ylim(1.9, 3.1)
    ax.legend(loc="lower right")
    save(fig, "ch02_monotone.png")


def plot_newton_bisection() -> None:
    """√2 を求める二分法とニュートン法の誤差を片対数で比較する。"""
    steps = 6
    newton = [float(error(x)) for x in newton_sequence(Fraction(2), steps)]
    bisection = [float(error(x)) for x in bisection_sequence(Fraction(1), Fraction(2), 30)]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.semilogy(range(len(bisection)), bisection, "o-", color="tab:blue", markersize=4, label="二分法")
    ax.semilogy(range(len(newton)), newton, "s-", color="tab:orange", markersize=5, label="ニュートン法")
    ax.set_xlabel(r"反復回数 $n$")
    ax.set_ylabel(r"誤差 $|a_n - \sqrt{2}|$")
    ax.set_title(r"$\sqrt{2}$ に収束する 2 つの数列")
    ax.legend()
    save(fig, "ch02_newton_bisection.png")


def main() -> None:
    """第 2 章のすべての図を生成する。"""
    setup_style()
    plot_epsilon_band()
    plot_monotone()
    plot_newton_bisection()


if __name__ == "__main__":
    main()
