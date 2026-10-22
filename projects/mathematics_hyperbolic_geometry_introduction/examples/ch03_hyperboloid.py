"""双曲面モデルと、そこから円板モデル、クラインモデルへの射影を 3 次元で描く.

使い方: python ch03_hyperboloid.py
"""

from typing import cast

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

import hg
import hg_plot


def create_figure() -> Figure:
    """双曲面 x0^2 - x1^2 - x2^2 = 1 の上の点 X を、2 通りの方法で円板に射影する様子を描く.

    縦軸を x0 とする。円板モデルは平面 x0 = 0 の上に、点 S = (-1, 0, 0) から射影して得る。
    クラインモデルは平面 x0 = 1 の上に、原点 O から射影して得る。
    """
    fig = plt.figure(figsize=(6.5, 6.0))
    ax = cast(Axes3D, fig.add_subplot(111, projection="3d"))

    # 双曲面（x0 >= 1 の部分）
    rho = np.linspace(0.0, 1.7, 30)
    phi = np.linspace(0.0, 2.0 * np.pi, 60)
    rr, pp = np.meshgrid(rho, phi)
    ax.plot_surface(np.sinh(rr) * np.cos(pp), np.sinh(rr) * np.sin(pp), np.cosh(rr), color="C0", alpha=0.25,
                    linewidth=0.0)

    # 円板（x0 = 0）とクラインの円板（x0 = 1）の境界
    t = np.linspace(0.0, 2.0 * np.pi, 200)
    ax.plot(np.cos(t), np.sin(t), np.zeros_like(t), color="C2", linewidth=1.5)
    ax.plot(np.cos(t), np.sin(t), np.ones_like(t), color="C1", linewidth=1.5)

    # 双曲面上の点 X と、2 通りの射影
    x = hg.disk_to_hyperboloid(hg.disk_point(1.5, 0.0))
    disk = hg.hyperboloid_to_disk(x)
    klein = x[1:] / x[0]
    ax.plot([-1.0, x[1]], [0.0, x[2]], [0.0, x[0]], color="C2", linestyle="--")  # S から X へ
    ax.plot([0.0, x[1]], [0.0, x[2]], [0.0, x[0]], color="C1", linestyle="--")  # O から X へ
    ax.scatter([x[1]], [x[2]], [x[0]], color="k", s=25)
    ax.scatter([disk.real], [disk.imag], [0.0], color="C2", s=25)
    ax.scatter([klein[0]], [klein[1]], [1.0], color="C1", s=25)
    ax.scatter([-1.0, 0.0], [0.0, 0.0], [0.0, 0.0], color="0.3", s=15)
    ax.text(x[1] + 0.1, x[2], x[0], "$X$", fontsize=13)
    ax.text(disk.real, disk.imag - 0.25, -0.25, "円板モデル", color="C2", fontsize=11)
    ax.text(klein[0] + 0.1, klein[1], 1.05, "クライン", color="C1", fontsize=11)
    ax.text(-1.0, 0.0, -0.25, "$S$", fontsize=12)
    ax.text(0.05, 0.0, -0.25, "$O$", fontsize=12)

    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.set_zlabel("$x_0$")
    ax.set_box_aspect((1.0, 1.0, 1.0))
    ax.view_init(elev=12.0, azim=-70.0)
    fig.tight_layout()
    return fig


def main() -> None:
    hg_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
