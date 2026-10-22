"""第 1 章の図を生成する。

* ch01_sup.png：集合 {1 - 1/n} とその上界・上限
* ch01_float_spacing.png：浮動小数点数の間隔と数の大きさの関係

実行方法::

    python fig_ch01.py
"""

import numpy as np

import matplotlib.pyplot as plt
from plot_style import save, setup_style


def plot_sup() -> None:
    """集合 A = {1 - 1/n | n = 1, 2, ...} を数直線上に描き、上界と上限を示す。"""
    fig, ax = plt.subplots(figsize=(8, 2.2))
    n = np.arange(1, 40)
    points = 1.0 - 1.0 / n

    # 数直線
    ax.axhline(0.0, color="black", linewidth=1)
    ax.plot(points, np.zeros_like(points), "o", color="tab:blue", markersize=5, label=r"$A$ の要素 $1 - 1/n$")
    # 上界全体 [1, ∞) を帯で示す
    ax.axvspan(1.0, 1.6, color="tab:orange", alpha=0.2, label="上界の集合")
    ax.plot([1.0], [0.0], "o", markerfacecolor="white", markeredgecolor="tab:red", markersize=9,
            label=r"上限 $\sup A = 1$（$A$ には属さない）")

    ax.set_xlim(-0.1, 1.6)
    ax.set_ylim(-0.5, 0.5)
    ax.set_yticks([])
    ax.set_xticks([0.0, 0.5, 1.0, 1.5])
    ax.grid(False)
    ax.legend(loc="upper left", fontsize=9, ncol=3, bbox_to_anchor=(0.0, 1.35), frameon=False)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    save(fig, "ch01_sup.png")


def plot_float_spacing() -> None:
    """倍精度浮動小数点数の隣接間隔 spacing(x) を両対数で描く。"""
    x = np.logspace(-8, 8, 2000)
    spacing = np.spacing(x)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.loglog(x, spacing, color="tab:blue", label="隣の浮動小数点数までの間隔")
    eps = np.finfo(np.float64).eps
    ax.loglog(x, eps * x, "--", color="tab:orange", label=r"$\varepsilon_{\mathrm{mach}} \cdot x$")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel("間隔")
    ax.set_title("浮動小数点数は大きいほどまばらになる")
    ax.legend()
    save(fig, "ch01_float_spacing.png")


def main() -> None:
    """第 1 章のすべての図を生成する。"""
    setup_style()
    plot_sup()
    plot_float_spacing()


if __name__ == "__main__":
    main()
