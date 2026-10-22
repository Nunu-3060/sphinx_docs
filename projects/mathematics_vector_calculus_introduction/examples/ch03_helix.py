"""らせんと、その上の単位接線ベクトル T と単位法線ベクトル N を描く.

使い方: python ch03_helix.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import vc_plot

A = 1.0  # らせんの半径 a
B = 0.25  # 1 ラジアンあたりに z 方向へ進む量 b


def helix(t: NDArray[np.float64]) -> NDArray[np.float64]:
    """らせん r(t) = (a cos t, a sin t, b t) の点を、3 行 N 列の配列で返す."""
    return np.array([A * np.cos(t), A * np.sin(t), B * t])


def unit_tangent(t: float) -> NDArray[np.float64]:
    """単位接線ベクトル T = r'(t) / |r'(t)| を返す."""
    v = np.array([-A * np.sin(t), A * np.cos(t), B])
    return v / float(np.linalg.norm(v))


def unit_normal(t: float) -> NDArray[np.float64]:
    """単位法線ベクトル N を返す（らせんでは z 軸に向かう水平な向きになる）."""
    return np.array([-np.cos(t), -np.sin(t), 0.0])


def create_figure() -> Figure:
    """らせんを 2 周分描き、いくつかの点で T と N を矢印で描く."""
    fig = plt.figure(figsize=(6.0, 5.5))
    ax = vc_plot.add_axes3d(fig)

    t = np.linspace(0.0, 4.0 * np.pi, 400)
    x, y, z = helix(t)
    ax.plot(x, y, z, color="0.3", linewidth=1.2)

    for i, ti in enumerate(np.linspace(0.5, 4.0 * np.pi - 0.5, 4)):
        p = helix(np.array([ti]))[:, 0]
        vc_plot.draw_vector3d(ax, 0.8 * unit_tangent(ti), origin=p, color="C0",
                              label=r"$\mathbf{T}$" if i == 0 else None)
        vc_plot.draw_vector3d(ax, 0.8 * unit_normal(ti), origin=p, color="C3",
                              label=r"$\mathbf{N}$" if i == 0 else None)

    ax.set_xticks([-1.0, 0.0, 1.0])
    ax.set_yticks([-1.0, 0.0, 1.0])
    ax.set_box_aspect((1, 1, 1.4))
    ax.view_init(elev=20, azim=-50)
    ax.set_title("らせんの単位接線ベクトル（青）と単位法線ベクトル（赤）")
    return fig


def main() -> None:
    vc_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
