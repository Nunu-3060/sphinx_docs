"""第 10 章（多変数関数の積分）の図を生成する。

生成する図（source/images に保存する）:
    ch10_riemann_sum.png    長方形の分割と小長方形
    ch10_region.png         縦線集合と積分順序の交換
    ch10_polar.png          極座標の小領域の面積
    ch10_gauss.png          ガウス積分の評価に使う円板と正方形
    ch10_monte_carlo.png    格子点とモンテカルロ積分の誤差

実行方法:
    python fig_ch10.py
"""

import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Rectangle, Wedge
from matplotlib.ticker import NullFormatter

from ch10_monte_carlo import SEED, compare_dimensions, rms_error
from plot_style import save, setup_style


def plot_riemann_sum() -> None:
    """長方形 [a, b] x [c, d] の分割と、代表点を描く。"""
    xs = [0.0, 0.7, 1.5, 2.0, 3.0]
    ys = [0.0, 0.6, 1.0, 1.8, 2.2]
    fig, ax = plt.subplots(figsize=(5.5, 4.4))
    for x in xs:
        ax.plot([x, x], [ys[0], ys[-1]], color="black", linewidth=1.0)
    for y in ys:
        ax.plot([xs[0], xs[-1]], [y, y], color="black", linewidth=1.0)
    ax.add_patch(Rectangle((xs[1], ys[2]), xs[2] - xs[1], ys[3] - ys[2], color="tab:orange", alpha=0.4))
    ax.plot([1.2], [1.6], marker="o", color="tab:red")
    ax.text(0.78, 1.38, r"$(\xi_{ij}, \eta_{ij})$", color="tab:red")
    ax.text(1.25, 1.08, r"$R_{ij}$")
    ax.set_xticks(xs, ["$a=x_0$", "$x_1$", "$x_2$", "$x_3$", "$b=x_4$"])
    ax.set_yticks(ys, ["$c=y_0$", "$y_1$", "$y_2$", "$y_3$", "$d=y_4$"])
    ax.grid(False)
    ax.set_title("長方形の分割と小長方形 $R_{ij}$")
    save(fig, "ch10_riemann_sum.png")


def plot_region() -> None:
    """三角形領域を縦線集合と横線集合の 2 通りに見る図を描く。"""
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 4.2))
    tri_x = [0.0, 1.0, 1.0, 0.0]
    tri_y = [0.0, 0.0, 1.0, 0.0]
    for ax in axes:
        ax.fill(tri_x, tri_y, color="tab:blue", alpha=0.2)
        ax.plot(tri_x, tri_y, color="tab:blue")
        ax.set_xlim(-0.1, 1.2)
        ax.set_ylim(-0.1, 1.2)
        ax.set_aspect("equal")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
    for x in np.linspace(0.1, 0.9, 9):
        axes[0].plot([x, x], [0.0, x], color="tab:red", linewidth=1.0)
    axes[0].set_title("先に $y$ で積分：$0 \\leq y \\leq x$")
    for y in np.linspace(0.1, 0.9, 9):
        axes[1].plot([y, 1.0], [y, y], color="tab:green", linewidth=1.0)
    axes[1].set_title("先に $x$ で積分：$y \\leq x \\leq 1$")
    save(fig, "ch10_region.png")


def plot_polar() -> None:
    """極座標の格子と、小領域の面積がおよそ r Δr Δθ になる様子を描く。"""
    fig, ax = plt.subplots(figsize=(5.2, 5.0))
    for r in np.arange(0.25, 2.01, 0.25):
        ax.add_patch(Circle((0.0, 0.0), r, fill=False, color="gray", linewidth=0.6))
    for t in np.arange(0.0, 90.1, 10.0):
        rad = math.radians(t)
        ax.plot([0.0, 2.0 * math.cos(rad)], [0.0, 2.0 * math.sin(rad)], color="gray", linewidth=0.6)
    ax.add_patch(Wedge((0.0, 0.0), 1.75, 30.0, 40.0, width=0.25, color="tab:orange", alpha=0.7))
    ax.annotate(r"面積 $\approx r\,\Delta r\,\Delta\theta$", xy=(1.3, 0.95), xytext=(1.4, 1.6),
                arrowprops={"arrowstyle": "->"})
    ax.set_xlim(0.0, 2.1)
    ax.set_ylim(0.0, 2.1)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("極座標の小領域")
    save(fig, "ch10_polar.png")


def plot_gauss() -> None:
    """円板 D_R ⊂ 正方形 [-R, R]^2 ⊂ 円板 D_{√2 R} の包含関係を描く。"""
    big_r = 1.0
    fig, ax = plt.subplots(figsize=(5.0, 5.0))
    ax.add_patch(Circle((0.0, 0.0), math.sqrt(2.0) * big_r, color="tab:green", alpha=0.15,
                        label=r"円板 $D_{\sqrt{2}R}$"))
    ax.add_patch(Rectangle((-big_r, -big_r), 2.0 * big_r, 2.0 * big_r, color="tab:blue", alpha=0.25,
                           label=r"正方形 $[-R, R]^2$"))
    ax.add_patch(Circle((0.0, 0.0), big_r, color="tab:red", alpha=0.3, label=r"円板 $D_R$"))
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(loc="upper right", fontsize=9)
    ax.set_title("ガウス積分の評価に使う領域")
    save(fig, "ch10_gauss.png")


def plot_monte_carlo() -> None:
    """次元と誤差の関係、およびモンテカルロ積分の誤差と標本数の関係を描く。"""
    dims = [1, 2, 3, 4, 6, 12]
    rows = compare_dimensions(4096, dims)
    grid_errors = [row[2] for row in rows]
    mc_errors = [row[3] for row in rows]

    rng = np.random.default_rng(SEED)
    sample_sizes = [10**k for k in range(2, 6)]
    rms = [rms_error(6, n, 50, rng) for n in sample_sizes]

    fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.2))
    axes[0].semilogy(dims, grid_errors, marker="o", label="格子点（中点則）")
    axes[0].semilogy(dims, mc_errors, marker="s", label="モンテカルロ")
    axes[0].set_xlabel("次元 d")
    axes[0].set_ylabel("相対誤差")
    axes[0].set_title("点の総数 N = 4096 のときの誤差")
    axes[0].legend()

    axes[1].loglog(sample_sizes, rms, marker="s", label="モンテカルロ（d = 6）")
    ref = [rms[0] * math.sqrt(sample_sizes[0] / n) for n in sample_sizes]
    axes[1].loglog(sample_sizes, ref, linestyle="--", color="gray", label=r"$N^{-1/2}$ に比例")
    axes[1].set_xlabel("標本数 N")
    axes[1].set_ylabel("相対誤差（二乗平均平方根）")
    axes[1].set_title("モンテカルロ積分の誤差")
    axes[1].yaxis.set_minor_formatter(NullFormatter())
    axes[1].legend()
    fig.tight_layout()
    save(fig, "ch10_monte_carlo.png")


def main() -> None:
    """第 10 章の図をすべて生成する。"""
    setup_style()
    plot_riemann_sum()
    plot_region()
    plot_polar()
    plot_gauss()
    plot_monte_carlo()


if __name__ == "__main__":
    main()
