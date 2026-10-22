"""球面のパラメーター表示 r(θ, φ) と、接ベクトル r_θ, r_φ、外向きの法線ベクトル r_θ × r_φ を描く.

使い方: python ch12_sphere_normals.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import vc_plot

Vec = NDArray[np.float64]


def sphere(theta: float, phi: float, radius: float = 1.0) -> Vec:
    """半径 radius の球面 r(θ, φ) = R (sinθ cosφ, sinθ sinφ, cosθ)."""
    return radius * np.array([np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)])


def tangents(theta: float, phi: float, radius: float = 1.0) -> tuple[Vec, Vec]:
    """接ベクトル r_θ = ∂r/∂θ と r_φ = ∂r/∂φ を返す."""
    r_theta = radius * np.array([np.cos(theta) * np.cos(phi), np.cos(theta) * np.sin(phi), -np.sin(theta)])
    r_phi = radius * np.array([-np.sin(theta) * np.sin(phi), np.sin(theta) * np.cos(phi), 0.0])
    return r_theta, r_phi


def create_figure() -> Figure:
    """球面の座標曲線（経線と緯線）、法線ベクトル、1 点での接ベクトルを描く."""
    fig = plt.figure(figsize=(6.5, 6.0))
    ax = vc_plot.add_axes3d(fig)

    # 座標曲線：θ 一定の緯線と φ 一定の経線
    s = np.linspace(0.0, 2.0 * np.pi, 100)
    for theta in np.linspace(np.pi / 8, 7 * np.pi / 8, 7):
        pts = np.array([sphere(theta, p) for p in s])
        ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color="0.75", linewidth=0.7)
    s = np.linspace(0.0, np.pi, 60)
    for phi in np.linspace(0.0, 2.0 * np.pi, 12, endpoint=False):
        pts = np.array([sphere(t, phi) for t in s])
        ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color="0.75", linewidth=0.7)

    # 上半分のいくつかの点での外向きの単位法線ベクトル
    for polar in (np.pi / 6, np.pi / 3):
        for azimuth in np.linspace(0.0, 2.0 * np.pi, 8, endpoint=False):
            p = sphere(polar, azimuth)
            ax.quiver(*p, *(0.35 * p), color="C0", linewidth=1.0, arrow_length_ratio=0.25)

    # 1 点での接ベクトルと、その外積（法線ベクトル）
    theta0, phi0 = np.pi / 2.2, 0.42 * np.pi
    p0 = sphere(theta0, phi0)
    r_theta, r_phi = tangents(theta0, phi0)
    vc_plot.draw_vector3d(ax, 0.6 * r_theta, origin=p0, color="C1", label=r"$\mathbf{r}_\theta$")
    vc_plot.draw_vector3d(ax, 0.6 * r_phi, origin=p0, color="C2", label=r"$\mathbf{r}_\phi$")
    vc_plot.draw_vector3d(ax, 0.6 * np.cross(r_theta, r_phi), origin=p0, color="C3",
                          label=r"$\mathbf{r}_\theta \times \mathbf{r}_\phi$")

    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_zlim(-1.2, 1.2)
    ax.set_box_aspect((1.0, 1.0, 1.0))
    ax.view_init(elev=20, azim=30)
    ax.set_title("球面の接ベクトルと外向きの法線ベクトル")
    return fig


def main() -> None:
    vc_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
