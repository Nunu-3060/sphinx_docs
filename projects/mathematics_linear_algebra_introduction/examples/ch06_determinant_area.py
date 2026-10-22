"""行列式の幾何学的意味: 単位正方形が移る平行四辺形の符号付き面積.

点線の正方形が単位正方形、色を塗った図形がその行き先である。
赤と青の矢印は、e1 と e2 の行き先（行列の 1 列目と 2 列目）である。

使い方: python ch06_determinant_area.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import la_plot

MATRICES = [
    np.array([[2.0, 1.0], [0.5, 1.5]]),
    np.array([[1.0, 1.0], [0.0, 1.0]]),
    np.array([[0.5, 1.0], [1.5, 0.5]]),
    np.array([[1.0, 2.0], [0.5, 1.0]]),
]


def create_figure() -> Figure:
    """4 つの行列について、単位正方形の行き先と行列式を描く."""
    square = np.array([[0.0, 1.0, 1.0, 0.0, 0.0],
                       [0.0, 0.0, 1.0, 1.0, 0.0]])
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.6))
    for ax, a in zip(axes, MATRICES):
        la_plot.setup_plane(ax, (-0.5, 3.2), (-0.5, 3.2))
        ax.plot(square[0], square[1], color="0.4", linestyle=":")
        moved = a @ square
        # 丸め誤差を除くため、行列式を小数点以下 10 桁に丸める（+ 0.0 で -0.0 を 0.0 にする）
        det = round(float(np.linalg.det(a)), 10) + 0.0
        # 行列式が負なら向きが反転しているので、色を変える
        color = "C2" if det >= 0 else "C1"
        ax.fill(moved[0], moved[1], color=color, alpha=0.4)
        ax.plot(moved[0], moved[1], color=color)
        la_plot.draw_vector(ax, a[:, 0], color="C3")
        la_plot.draw_vector(ax, a[:, 1], color="C0")
        ax.set_title(f"[[{a[0, 0]:g}, {a[0, 1]:g}], [{a[1, 0]:g}, {a[1, 1]:g}]]\ndet = {det:g}")
    fig.tight_layout()
    return fig


def main() -> None:
    la_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
