"""上半平面モデルで、楕円型、放物型、双曲型の等長変換が点をどう動かすかを描く.

使い方: python ch05_isometries.py
"""

import math
from collections.abc import Callable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy.typing import NDArray

import hg_plot

Matrix = NDArray[np.float64]


def mobius(m: Matrix, z: NDArray[np.complex128]) -> NDArray[np.complex128]:
    """行列 m = [[a, b], [c, d]] が表すメビウス変換 (a z + b) / (c z + d)."""
    result: NDArray[np.complex128] = (m[0, 0] * z + m[0, 1]) / (m[1, 0] * z + m[1, 1])
    return result


def elliptic(t: float) -> Matrix:
    """点 i のまわりの回転（回転角 2t）."""
    return np.array([[math.cos(t), math.sin(t)], [-math.sin(t), math.cos(t)]])


def parabolic(t: float) -> Matrix:
    """実軸方向の平行移動 z -> z + t."""
    return np.array([[1.0, t], [0.0, 1.0]])


def hyperbolic(t: float) -> Matrix:
    """虚軸に沿った移動 z -> e^t z."""
    return np.array([[math.exp(t / 2.0), 0.0], [0.0, math.exp(-t / 2.0)]])


def draw_flow(ax: Axes, family: Callable[[float], Matrix], starts: list[complex], t_max: float,
              step: float) -> None:
    """starts の各点を family(t) で動かした軌跡（線）と、t = step ごとの位置（点）を描く."""
    z0 = np.array(starts, dtype=np.complex128)
    t_line = np.linspace(-t_max, t_max, 400)
    paths = np.array([mobius(family(t), z0) for t in t_line])
    for j in range(len(starts)):
        hg_plot.plot_complex(ax, paths[:, j], color="0.5", linewidth=0.9)
    n = int(t_max / step)
    for k in range(-n, n + 1):
        z = mobius(family(k * step), z0)
        ax.plot(z.real, z.imag, "o", color="C3" if k == 0 else "C0", markersize=3.5)


def create_figure() -> Figure:
    """3 種類の等長変換の軌跡を横に並べる."""
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 4.0))
    xlim, ylim = (-3.0, 3.0), (-0.2, 4.0)

    hg_plot.setup_half_plane(axes[0], xlim, ylim, "楕円型（$i$ のまわりの回転）")
    starts = [1j * math.exp(s) for s in (0.3, 0.6, 0.9, 1.2)]
    draw_flow(axes[0], elliptic, starts, math.pi / 2.0, math.pi / 12.0)
    axes[0].plot([0.0], [1.0], "k*", markersize=9)

    hg_plot.setup_half_plane(axes[1], xlim, ylim, r"放物型（$z \mapsto z + t$）")
    draw_flow(axes[1], parabolic, [0.5j, 1.0j, 2.0j, 3.0j], 3.0, 0.5)

    hg_plot.setup_half_plane(axes[2], xlim, ylim, r"双曲型（$z \mapsto e^{t} z$）")
    starts = [complex(np.exp(1j * phi)) for phi in (0.35, 0.8, math.pi / 2.0, math.pi - 0.8, math.pi - 0.35)]
    draw_flow(axes[2], hyperbolic, starts, 3.0, 0.5)
    fig.tight_layout()
    return fig


def main() -> None:
    hg_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
