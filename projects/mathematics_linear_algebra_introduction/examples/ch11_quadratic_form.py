"""二次形式 q(x) = x^T A x の等高線と、主軸（固有ベクトル）を描く.

左: 正定値（固有値 3, 1）。等高線は楕円で、原点が最小値になる。
中: 不定値（固有値 3, -1）。等高線は双曲線で、原点は鞍点になる。
右: 半正定値（固有値 2, 0）。固有値 0 の方向では値が変わらない。

使い方: python ch11_quadratic_form.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import la_plot

CASES = [
    ("正定値", np.array([[2.0, 1.0], [1.0, 2.0]])),
    ("不定値", np.array([[1.0, 2.0], [2.0, 1.0]])),
    ("半正定値", np.array([[1.0, 1.0], [1.0, 1.0]])),
]


def create_figure() -> Figure:
    """3 つの対称行列について、二次形式の等高線と主軸を描く."""
    s = np.linspace(-2.0, 2.0, 201)
    x, y = np.meshgrid(s, s)
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.2))
    for ax, (title, a) in zip(axes, CASES):
        q = a[0, 0] * x**2 + 2 * a[0, 1] * x * y + a[1, 1] * y**2
        contour = ax.contour(x, y, q, levels=np.arange(-6.0, 7.0, 1.0), cmap="RdBu_r")
        ax.clabel(contour, fontsize=7)
        values, vectors = np.linalg.eigh(a)
        for value, v in zip(values, vectors.T):
            la_plot.draw_vector(ax, 1.5 * v, color="k", label=rf"$\lambda={value:g}$",
                                offset=(0.05, 0.05))
        ax.set_aspect("equal")
        ax.set_title(f"{title}: [[{a[0, 0]:g}, {a[0, 1]:g}], [{a[1, 0]:g}, {a[1, 1]:g}]]")
    fig.tight_layout()
    return fig


def main() -> None:
    la_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
