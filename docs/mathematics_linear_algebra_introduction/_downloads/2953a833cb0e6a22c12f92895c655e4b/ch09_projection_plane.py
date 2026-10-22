"""3 次元空間のベクトル b を、平面（列空間）へ正射影する様子を描く.

平面は a1 = (1, 0, 1) と a2 = (0, 1, 1) が張る。b = (1, 2, 5) の
正射影 p は平面の上にあり、誤差 e = b - p は平面に垂直である。

使い方: python ch09_projection_plane.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.axes3d import Axes3D

import la_plot


def create_figure() -> Figure:
    """平面、b、正射影 p、誤差 e を 3 次元のグラフに描く."""
    a = np.array([[1.0, 0.0],
                  [0.0, 1.0],
                  [1.0, 1.0]])
    b = np.array([1.0, 2.0, 5.0])
    x_hat = np.linalg.solve(a.T @ a, a.T @ b)  # 正規方程式の解
    p = a @ x_hat

    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(projection="3d")
    assert isinstance(ax, Axes3D)

    # 平面 s a1 + t a2
    s, t = np.meshgrid(np.linspace(-0.5, 2.5, 7), np.linspace(-0.5, 3.0, 7))
    ax.plot_surface(s, t, s + t, color="C0", alpha=0.2)

    vectors = [
        (np.zeros(3), b, "C3", r"$\mathbf{b}$"),
        (np.zeros(3), p, "C2", r"$\mathbf{p}$"),
        (p, b - p, "C1", r"$\mathbf{e}$"),
        (np.zeros(3), a[:, 0], "C0", r"$\mathbf{a}_1$"),
        (np.zeros(3), a[:, 1], "C0", r"$\mathbf{a}_2$"),
    ]
    for origin, v, color, label in vectors:
        ax.quiver(*origin, *v, color=color, arrow_length_ratio=0.08, linewidth=2)
        end = origin + v
        ax.text(end[0], end[1], end[2] + 0.15, label, color=color, fontsize=12)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.view_init(elev=20, azim=-50)
    ax.set_title("平面への正射影")
    fig.tight_layout()
    return fig


def main() -> None:
    la_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
