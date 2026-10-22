"""固有ベクトルの幾何学的意味: 変換しても向きが変わらないベクトル.

行列 A = [[4, 1], [2, 3]] で、単位円の上のベクトルを変換する。
左: 細い矢印が元のベクトル v、太い矢印が変換後の Av である。
    固有ベクトルの方向（点線）のベクトルだけは、変換後も同じ直線の上にある。
右: 単位円は楕円に移る。固有ベクトル (1, 1) は 5 倍、(1, -2) は 2 倍になる。

使い方: python ch10_eigen_geometry.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import la_plot

A = np.array([[4.0, 1.0],
              [2.0, 3.0]])


def create_figure() -> Figure:
    """ベクトルとその像、単位円とその像を描く."""
    eigenvectors = [np.array([1.0, 1.0]), np.array([1.0, -2.0])]
    fig, (ax_vec, ax_circle) = plt.subplots(1, 2, figsize=(10, 5))

    la_plot.setup_plane(ax_vec, (-5.5, 5.5), (-5.5, 5.5))
    for e in eigenvectors:
        t = np.array([-6.0, 6.0]) / np.linalg.norm(e)
        ax_vec.plot(t * e[0], t * e[1], color="0.5", linestyle=":")
    for degrees in range(0, 360, 30):
        theta = np.radians(degrees)
        v = np.array([np.cos(theta), np.sin(theta)])
        la_plot.draw_vector(ax_vec, v, color="C0")
        la_plot.draw_vector(ax_vec, A @ v, color="C1")
    for e in eigenvectors:
        v = e / np.linalg.norm(e)
        la_plot.draw_vector(ax_vec, A @ v, color="C3")
        la_plot.draw_vector(ax_vec, v, color="C2")
    ax_vec.set_title(r"$\mathbf{v}$（青）と $A\mathbf{v}$（橙）、固有ベクトル（緑と赤）")

    la_plot.setup_plane(ax_circle, (-5.5, 5.5), (-5.5, 5.5))
    theta = np.linspace(0, 2 * np.pi, 200)
    circle = np.vstack([np.cos(theta), np.sin(theta)])
    image = A @ circle
    ax_circle.plot(circle[0], circle[1], color="C0", label="単位円")
    ax_circle.plot(image[0], image[1], color="C1", label="単位円の像")
    for e, value in zip(eigenvectors, (5, 2)):
        v = e / np.linalg.norm(e)
        la_plot.draw_vector(ax_circle, value * v, color="C3",
                            label=rf"$\lambda = {value}$", offset=(0.1, 0.1))
        la_plot.draw_vector(ax_circle, v, color="C2")
    ax_circle.legend(loc="lower right")
    ax_circle.set_title("単位円の像")

    fig.tight_layout()
    return fig


def main() -> None:
    la_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
