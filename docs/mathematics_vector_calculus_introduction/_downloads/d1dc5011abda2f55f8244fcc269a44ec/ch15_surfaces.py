"""同じ境界（単位円）を持つ円板と半球面、境界の向きと法線ベクトルの関係を描く.

使い方: python ch15_surfaces.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import vc_plot


def create_figure() -> Figure:
    """左に円板、右に半球面を描き、反時計回りの境界と上向きの法線ベクトルを示す."""
    fig = plt.figure(figsize=(9.0, 4.4))
    t = np.linspace(0, 2 * np.pi, 200)
    for position, title in ((121, "円板"), (122, "半球面")):
        ax = vc_plot.add_axes3d(fig, position)
        if position == 121:
            rho, phi = np.meshgrid(np.linspace(0, 1, 12), np.linspace(0, 2 * np.pi, 25))
            x, y, z = rho * np.cos(phi), rho * np.sin(phi), np.zeros_like(rho)
            normal_points = [(0.0, 0.0, 0.0), (0.6, 0.0, 0.0), (-0.3, 0.5, 0.0)]
            normals = [(0.0, 0.0, 0.6)] * 3
        else:
            theta, phi = np.meshgrid(np.linspace(0, np.pi / 2, 12), np.linspace(0, 2 * np.pi, 25))
            x, y, z = np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)
            normal_points = [(0.0, 0.0, 1.0), (0.6, 0.0, 0.8), (-0.3, 0.52, 0.8)]
            normals = [tuple(0.6 * np.array(p)) for p in normal_points]
        ax.plot_surface(x, y, z, color="C0", alpha=0.25, linewidth=0)
        # 境界の円と、反時計回りを示す矢印
        ax.plot(np.cos(t), np.sin(t), np.zeros_like(t), color="C3", linewidth=2)
        for s in (0.0, 2 * np.pi / 3, 4 * np.pi / 3):
            start = (np.cos(s), np.sin(s), 0.0)
            ax.quiver(*start, -0.4 * np.sin(s), 0.4 * np.cos(s), 0.0, color="C3", linewidth=2,
                      arrow_length_ratio=0.4)
        for p, n in zip(normal_points, normals):
            vc_plot.draw_vector3d(ax, n, origin=p, color="C1")
        ax.text(1.0, -1.1, 0.0, "$C$", color="C3", fontsize=13)
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        ax.set_zlim(0.0, 1.6)
        ax.set_box_aspect((1.0, 1.0, 0.75))
        ax.view_init(elev=25, azim=-60)
        ax.set_title(title)
    fig.tight_layout()
    return fig


def main() -> None:
    vc_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
