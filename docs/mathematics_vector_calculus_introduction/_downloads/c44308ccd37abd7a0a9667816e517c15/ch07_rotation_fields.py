"""剛体回転、自由渦、せん断流の 3 つの流れに羽根車を流したとき、羽根車が自転するかを描く.

使い方: python ch07_rotation_fields.py
"""

import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

import vc_plot


def draw_paddle(ax: Axes, x: float, y: float, angle: float, size: float = 0.28) -> None:
    """点 (x, y) に、角度 angle [rad] だけ回った十字形の羽根車を描く. 赤い羽根で向きが分かる."""
    for k in range(4):
        a = angle + k * math.pi / 2
        color = "C3" if k == 0 else "k"
        ax.plot([x, x + size * math.cos(a)], [y, y + size * math.sin(a)], color=color, linewidth=2.0)
    ax.plot(x, y, "o", color="k", markersize=3)


def create_figure() -> Figure:
    """3 つの流れの矢印図に、時間とともに流される羽根車の位置と向きを重ねる."""
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.4))
    qx, qy = vc_plot.mesh((-2.0, 2.0), (-2.0, 2.0), 11)
    radius = 1.3
    times = np.linspace(0.0, 2.0 * math.pi, 7)[:-1]

    # 剛体回転 v = (-y, x)：回転は (0, 0, 2) で、羽根車は角速度 1 で自転する
    ax = axes[0]
    ax.quiver(qx, qy, -qy, qx, color="0.6", angles="xy", scale_units="xy", scale=4.0, width=0.005)
    for t in times:
        draw_paddle(ax, radius * math.cos(t), radius * math.sin(t), angle=t)
    ax.set_title("剛体回転 $\\mathbf{v} = (-y, x, 0)$\n$\\nabla\\times\\mathbf{v} = (0, 0, 2)$")

    # 自由渦 v = (-y, x) / (x^2 + y^2)：原点以外で回転は 0 なので、羽根車は自転しない
    ax = axes[1]
    r2 = qx**2 + qy**2
    mask = r2 > 0.5  # 原点の近くは速さが大きすぎるので描かない
    ax.quiver(qx[mask], qy[mask], -qy[mask] / r2[mask], qx[mask] / r2[mask], color="0.6",
              angles="xy", scale_units="xy", scale=4.0, width=0.005)
    for t in times:
        draw_paddle(ax, radius * math.cos(t), radius * math.sin(t), angle=0.0)
    ax.set_title("自由渦 $\\mathbf{v} = (-y, x, 0)/(x^2 + y^2)$\n$\\nabla\\times\\mathbf{v} = \\mathbf{0}$（原点以外）")

    # せん断流 v = (y, 0)：流れは直線だが回転は (0, 0, -1) で、羽根車は時計回りに自転する
    ax = axes[2]
    ax.quiver(qx, qy, qy, np.zeros_like(qy), color="0.6", angles="xy", scale_units="xy", scale=4.0,
              width=0.005)
    for t in range(5):
        draw_paddle(ax, -2.0 + t, 1.0, angle=-t / 2.0)
    ax.set_title("せん断流 $\\mathbf{v} = (y, 0, 0)$\n$\\nabla\\times\\mathbf{v} = (0, 0, -1)$")

    for ax in axes:
        ax.set_xlim(-2.4, 2.4)
        ax.set_ylim(-2.4, 2.4)
        ax.set_aspect("equal")
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
    fig.tight_layout()
    return fig


def main() -> None:
    vc_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
