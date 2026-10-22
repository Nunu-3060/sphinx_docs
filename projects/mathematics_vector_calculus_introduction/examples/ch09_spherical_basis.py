"""球座標 (r, θ, φ) の意味と、点 P での基底ベクトル e_r, e_θ, e_φ を描く.

使い方: python ch09_spherical_basis.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import vc_plot


def spherical_to_cartesian(r: float, theta: float, phi: float) -> NDArray[np.float64]:
    """球座標 (r, θ, φ) を直交座標 (x, y, z) に変換する."""
    return np.array([r * np.sin(theta) * np.cos(phi),
                     r * np.sin(theta) * np.sin(phi),
                     r * np.cos(theta)])


Basis = tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]


def spherical_basis(theta: float, phi: float) -> Basis:
    """角度 (θ, φ) の点での単位ベクトル e_r, e_θ, e_φ を返す."""
    e_r = np.array([np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)])
    e_theta = np.array([np.cos(theta) * np.cos(phi), np.cos(theta) * np.sin(phi), -np.sin(theta)])
    e_phi = np.array([-np.sin(phi), np.cos(phi), 0.0])
    return e_r, e_theta, e_phi


def create_figure() -> Figure:
    """点 P の位置を表す r, θ, φ と、P での基底ベクトルを描く."""
    r, theta, phi = 2.0, np.pi / 4, np.pi / 3
    p = spherical_to_cartesian(r, theta, phi)
    fig = plt.figure(figsize=(6.5, 6.0))
    ax = vc_plot.add_axes3d(fig)

    # 座標軸
    for axis, name in zip(np.eye(3), "xyz"):
        ax.plot(*np.vstack([np.zeros(3), 2.4 * axis]).T, color="0.5", linewidth=0.8)
        ax.text(*(2.55 * axis), f"${name}$", color="0.3", fontsize=12)

    # 原点から P への線分と、P を xy 平面に下ろした点 Q
    q = np.array([p[0], p[1], 0.0])
    ax.plot(*np.vstack([np.zeros(3), p]).T, color="k", linewidth=1.2)
    ax.plot(*np.vstack([np.zeros(3), q]).T, color="0.4", linestyle="--", linewidth=1.0)
    ax.plot(*np.vstack([q, p]).T, color="0.4", linestyle="--", linewidth=1.0)
    ax.scatter(*p, color="k", s=15)
    ax.text(*(p * 1.05 + np.array([0.0, 0.0, 0.15])), "P", fontsize=12)
    ax.text(*(0.55 * p + np.array([0.1, 0.1, -0.3])), "$r$", fontsize=13)

    # θ（z 軸から OP までの角）と φ（x 軸から OQ までの角）を円弧で示す
    s = np.linspace(0.0, theta, 30)
    arc_theta = np.array([spherical_to_cartesian(0.8, t, phi) for t in s])
    ax.plot(arc_theta[:, 0], arc_theta[:, 1], arc_theta[:, 2], color="C3")
    ax.text(*spherical_to_cartesian(0.95, theta / 2, phi), r"$\theta$", color="C3", fontsize=13)
    s = np.linspace(0.0, phi, 30)
    arc_phi = np.array([spherical_to_cartesian(0.8, np.pi / 2, t) for t in s])
    ax.plot(arc_phi[:, 0], arc_phi[:, 1], arc_phi[:, 2], color="C2")
    ax.text(*spherical_to_cartesian(1.0, np.pi / 2, phi / 2), r"$\phi$", color="C2", fontsize=13)

    # P での基底ベクトル
    e_r, e_theta, e_phi = spherical_basis(theta, phi)
    vc_plot.draw_vector3d(ax, 0.9 * e_r, origin=p, color="C0", label=r"$\mathbf{e}_r$")
    vc_plot.draw_vector3d(ax, 0.9 * e_theta, origin=p, color="C1", label=r"$\mathbf{e}_\theta$")
    vc_plot.draw_vector3d(ax, 0.9 * e_phi, origin=p, color="C4", label=r"$\mathbf{e}_\phi$")

    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.5, 2.5)
    ax.set_zlim(-0.5, 2.5)
    ax.set_box_aspect((1.0, 1.0, 1.0))
    ax.view_init(elev=20, azim=30)
    ax.set_axis_off()  # 目盛りの箱を消し、自分で描いた座標軸だけを見せる
    ax.set_title("球座標 $(r, \\theta, \\phi)$ と基底ベクトル")
    return fig


def main() -> None:
    vc_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
