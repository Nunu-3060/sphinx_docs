"""同じ図形（三角形と測地線の網目）を、上半平面、ポアンカレ円板、クラインの 3 つのモデルで描く.

使い方: python ch03_models.py
"""

import math
from collections.abc import Callable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy.typing import NDArray

import hg
import hg_plot

ComplexArray = NDArray[np.complex128]


def grid_lines() -> list[ComplexArray]:
    """円板モデルで、実軸と、実軸に垂直な測地線（間隔 0.6）を返す."""
    t = np.tanh(np.linspace(-12.0, 12.0, 300) / 2.0)
    lines = [t.astype(np.complex128)]  # 実軸
    for s in np.arange(-3.0, 3.01, 0.6):
        a = math.tanh(s / 2.0)  # 実軸上で原点から距離 s の点
        lines.append((1j * t + a) / (1.0 + a * 1j * t))  # 虚軸を実軸方向に距離 s だけ平行移動した測地線
    return lines


def triangle() -> list[ComplexArray]:
    """円板モデルで、原点からの距離 1.2 の 3 点を頂点とする正三角形の辺を返す."""
    vertices = [hg.disk_point(1.2, math.pi / 2.0 + 2.0 * math.pi * k / 3.0) for k in range(3)]
    return [hg.disk_geodesic(vertices[k], vertices[(k + 1) % 3]) for k in range(3)]


def draw(ax: Axes, transform: Callable[[ComplexArray], ComplexArray]) -> None:
    """円板モデルの図形を transform でほかのモデルに移して描く."""
    for line in grid_lines():
        hg_plot.plot_complex(ax, transform(line), color="0.55", linewidth=0.8)
    for side in triangle():
        hg_plot.plot_complex(ax, transform(side), color="C3", linewidth=2.0)


def create_figure() -> Figure:
    """3 つのモデルを横に並べて描く."""
    fig, axes = plt.subplots(1, 3, figsize=(11.0, 4.0))

    def to_half_plane(z: ComplexArray) -> ComplexArray:
        return 1j * (1.0 + z) / (1.0 - z)

    def identity(z: ComplexArray) -> ComplexArray:
        return z

    def to_klein(z: ComplexArray) -> ComplexArray:
        return 2.0 * z / (1.0 + np.abs(z) ** 2)

    hg_plot.setup_half_plane(axes[0], (-4.0, 4.0), (-0.3, 5.0), "上半平面モデル")
    draw(axes[0], to_half_plane)
    hg_plot.setup_disk(axes[1], "ポアンカレ円板モデル")
    draw(axes[1], identity)
    hg_plot.setup_disk(axes[2], "クラインモデル")
    draw(axes[2], to_klein)
    fig.tight_layout()
    return fig


def main() -> None:
    hg_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
