"""第 9 章（多変数関数の微分）の図を生成する。

生成する図（source/images に保存する）:
    ch09_path_limit.png        経路によって極限が異なる関数 xy/(x^2+y^2) の等高線
    ch09_gradient.png          等高線と勾配ベクトル
    ch09_critical_points.png   臨界点（極小点と鞍点）
    ch09_lagrange.png          ラグランジュの未定乗数法
    ch09_gradient_descent.png  勾配降下法の軌跡

実行方法:
    python fig_ch09.py
"""

import matplotlib.pyplot as plt
import numpy as np

from ch09_gradient_descent import A_MATRIX, B_VECTOR, X0, gradient_descent, objective
from plot_style import save, setup_style


def plot_path_limit() -> None:
    """f(x, y) = xy/(x^2+y^2) の等高線を描く。原点を通る直線上で値が一定になる。"""
    x, y = np.meshgrid(np.linspace(-1.0, 1.0, 401), np.linspace(-1.0, 1.0, 401))
    r2 = x**2 + y**2
    z = np.where(r2 > 0.0, x * y / np.where(r2 > 0.0, r2, 1.0), 0.0)

    fig, ax = plt.subplots(figsize=(5.5, 4.8))
    levels = np.linspace(-0.5, 0.5, 21)
    cs = ax.contourf(x, y, z, levels=levels, cmap="coolwarm")
    fig.colorbar(cs, ax=ax, label="f(x, y)")
    for m in [0.0, 0.5, 1.0, -1.0]:
        t = np.linspace(-1.0, 1.0, 2)
        ax.plot(t, m * t, color="black", linewidth=1.0, linestyle="--")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal")
    ax.set_title(r"$f(x,y)=xy/(x^2+y^2)$" + "\n" + r"直線 $y=mx$ 上で値 $m/(1+m^2)$ が一定")
    save(fig, "ch09_path_limit.png")


def plot_gradient() -> None:
    """f(x, y) = x^2 + 2y^2 の等高線と勾配ベクトルを描く。"""
    x, y = np.meshgrid(np.linspace(-2.0, 2.0, 201), np.linspace(-1.5, 1.5, 201))
    z = x**2 + 2.0 * y**2

    qx, qy = np.meshgrid(np.linspace(-1.8, 1.8, 10), np.linspace(-1.3, 1.3, 8))
    gx = 2.0 * qx
    gy = 4.0 * qy

    fig, ax = plt.subplots(figsize=(6.0, 4.6))
    cs = ax.contour(x, y, z, levels=[0.25, 0.75, 1.5, 2.5, 3.5], colors="tab:blue")
    ax.clabel(cs, fontsize=8)
    ax.quiver(qx, qy, gx, gy, color="tab:red", angles="xy", scale_units="xy", scale=12.0, width=0.004)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal")
    ax.set_title(r"$f(x,y)=x^2+2y^2$ の等高線（青）と勾配 $\nabla f$（赤）")
    save(fig, "ch09_gradient.png")


def plot_critical_points() -> None:
    """f(x, y) = x^3 - 3x + y^2 の等高線と臨界点を描く。"""
    x, y = np.meshgrid(np.linspace(-2.2, 2.2, 301), np.linspace(-2.0, 2.0, 301))
    z = x**3 - 3.0 * x + y**2

    fig, ax = plt.subplots(figsize=(6.0, 5.0))
    cs = ax.contour(x, y, z, levels=np.linspace(-3.0, 5.0, 17), cmap="viridis")
    ax.clabel(cs, fontsize=7)
    ax.plot([1.0], [0.0], marker="o", color="tab:red", markersize=8, label="極小点 (1, 0)")
    ax.plot([-1.0], [0.0], marker="X", color="tab:orange", markersize=9, label="鞍点 (-1, 0)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal")
    ax.legend(loc="upper left")
    ax.set_title(r"$f(x,y)=x^3-3x+y^2$ の等高線と臨界点")
    save(fig, "ch09_critical_points.png")


def plot_lagrange() -> None:
    """円 x^2 + y^2 = 1 上で f(x, y) = x + y を最大化する様子を描く。"""
    x, y = np.meshgrid(np.linspace(-1.6, 1.6, 201), np.linspace(-1.6, 1.6, 201))
    z = x + y
    theta = np.linspace(0.0, 2.0 * np.pi, 400)
    p = 1.0 / np.sqrt(2.0)

    fig, ax = plt.subplots(figsize=(5.4, 5.0))
    cs = ax.contour(x, y, z, levels=np.linspace(-2.0, 2.0, 9), colors="tab:blue", linewidths=0.8)
    ax.clabel(cs, fontsize=8)
    # 最大点で制約曲線に接する等高線 x + y = √2 を太線で描く
    ax.contour(x, y, z, levels=[np.sqrt(2.0)], colors="tab:blue", linewidths=2.0)
    ax.plot(np.cos(theta), np.sin(theta), color="black", linewidth=2.0, label=r"制約 $x^2+y^2=1$")
    ax.plot([p], [p], marker="o", color="tab:red", markersize=7, label="最大点")
    ax.annotate("", xy=(p + 0.45, p + 0.45), xytext=(p, p),
                arrowprops={"arrowstyle": "->", "color": "tab:red", "linewidth": 2.0})
    ax.annotate("", xy=(p + 0.65, p + 0.65), xytext=(p, p),
                arrowprops={"arrowstyle": "->", "color": "tab:green", "linewidth": 1.2})
    ax.text(p + 0.5, p + 0.2, r"$\nabla f$", color="tab:red")
    ax.text(p + 0.05, p + 0.6, r"$\nabla g$", color="tab:green")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal")
    ax.legend(loc="lower left")
    ax.set_title(r"$f(x,y)=x+y$ の等高線と制約曲線")
    save(fig, "ch09_lagrange.png")


def plot_gradient_descent() -> None:
    """2 種類のステップ幅で勾配降下法の軌跡を描く。"""
    x, y = np.meshgrid(np.linspace(-4.5, 2.5, 301), np.linspace(-2.2, 2.4, 301))
    z = 0.5 * (A_MATRIX[0, 0] * x**2 + A_MATRIX[1, 1] * y**2) - B_VECTOR[0] * x - B_VECTOR[1] * y
    f_min = objective(np.linalg.solve(A_MATRIX, B_VECTOR))

    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    ax.contour(x, y, z, levels=f_min + np.array([0.1, 0.5, 1.5, 3.0, 6.0, 10.0, 15.0]),
               colors="gray", linewidths=0.8)
    for eta, color in [(0.05, "tab:blue"), (0.18, "tab:red")]:
        points = np.array(gradient_descent(X0, eta, 30))
        ax.plot(points[:, 0], points[:, 1], marker="o", markersize=3, color=color,
                linewidth=1.0, label=rf"$\eta={eta}$")
    ax.plot([1.0], [0.1], marker="*", color="black", markersize=12, label="最小点")
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.set_aspect("equal")
    ax.legend(loc="upper right")
    ax.set_title("勾配降下法の軌跡（30 反復）")
    save(fig, "ch09_gradient_descent.png")


def main() -> None:
    """第 9 章の図をすべて生成する。"""
    setup_style()
    plot_path_limit()
    plot_gradient()
    plot_critical_points()
    plot_lagrange()
    plot_gradient_descent()


if __name__ == "__main__":
    main()
