"""発散が正・負・0 の 2 次元のベクトル場を並べて描く.

使い方: python ch06_divergence_fields.py
"""

from collections.abc import Callable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from numpy.typing import NDArray

import vc_plot

Field = Callable[[NDArray[np.float64], NDArray[np.float64]],
                 tuple[NDArray[np.float64], NDArray[np.float64]]]


def source(x: NDArray[np.float64], y: NDArray[np.float64]) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """湧き出し F = (x, y). 発散は 2."""
    return x, y


def sink(x: NDArray[np.float64], y: NDArray[np.float64]) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """吸い込み F = (-x, -y). 発散は -2."""
    return -x, -y


def stagnation(x: NDArray[np.float64], y: NDArray[np.float64]) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """よどみ点流れ F = (x, -y). 発散は 0."""
    return x, -y


def stretch(x: NDArray[np.float64], y: NDArray[np.float64]) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """一方向の流れで、下流ほど速くなる場 F = (x + 2, 0). 発散は 1."""
    return x + 2.0, np.zeros_like(y)


def draw_box(ax: Axes, field: Field) -> None:
    """原点の周りの正方形の各辺で、外向きの流れ（青）と内向きの流れ（赤）を矢印で示す."""
    a = 0.5
    ax.add_patch(Rectangle((-a, -a), 2 * a, 2 * a, fill=False, edgecolor="k", linewidth=1.2))
    # 各辺の中点と、その辺の外向き法線ベクトル
    for mx, my, nx, ny in ((a, 0.0, 1.0, 0.0), (-a, 0.0, -1.0, 0.0), (0.0, a, 0.0, 1.0), (0.0, -a, 0.0, -1.0)):
        fx, fy = field(np.array([mx]), np.array([my]))
        flow = float(fx[0]) * nx + float(fy[0]) * ny  # 外向きの成分
        if abs(flow) < 1.0e-12:
            continue
        length = 0.6 * abs(flow)
        if flow > 0:  # 辺から外へ向かう矢印
            start, end, color = (mx, my), (mx + length * nx, my + length * ny), "C0"
        else:  # 外から辺へ向かう矢印
            start, end, color = (mx + length * nx, my + length * ny), (mx, my), "C3"
        ax.annotate("", xy=end, xytext=start,
                    arrowprops={"arrowstyle": "-|>", "color": color, "linewidth": 2.5, "mutation_scale": 18})


def create_figure() -> Figure:
    """4 つのベクトル場を矢印図で描き、原点の周りの正方形を出入りする流れを重ねる."""
    fields: list[tuple[Field, str]] = [
        (source, r"$\mathbf{F} = (x, y)$、$\nabla\cdot\mathbf{F} = 2$"),
        (sink, r"$\mathbf{F} = (-x, -y)$、$\nabla\cdot\mathbf{F} = -2$"),
        (stagnation, r"$\mathbf{F} = (x, -y)$、$\nabla\cdot\mathbf{F} = 0$"),
        (stretch, r"$\mathbf{F} = (x + 2, 0)$、$\nabla\cdot\mathbf{F} = 1$"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(8.0, 8.0))
    qx, qy = vc_plot.mesh((-1.8, 1.8), (-1.8, 1.8), 11)
    for ax, (field, title) in zip(axes.flat, fields):
        fx, fy = field(qx, qy)
        ax.quiver(qx, qy, fx, fy, color="0.45", angles="xy", scale_units="xy", scale=6.0, width=0.005)
        draw_box(ax, field)
        ax.set_xlim(-2.1, 2.1)
        ax.set_ylim(-2.1, 2.1)
        ax.set_aspect("equal")
        ax.set_xticks([-2, -1, 0, 1, 2])
        ax.set_yticks([-2, -1, 0, 1, 2])
        ax.set_title(title, fontsize=11)
    fig.tight_layout()
    return fig


def main() -> None:
    vc_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
