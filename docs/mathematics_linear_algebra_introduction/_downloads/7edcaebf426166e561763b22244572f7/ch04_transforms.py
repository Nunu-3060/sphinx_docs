"""2 次元の基本的な線形変換で、方眼と F の字がどう変形するかを描く.

赤と青の矢印は、基本ベクトル e1 = (1, 0) と e2 = (0, 1) の行き先である。
行き先はそれぞれ行列の 1 列目と 2 列目に等しい。

使い方: python ch04_transforms.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import la_plot


def rotation(degrees: float) -> NDArray[np.float64]:
    """原点を中心に degrees 度だけ回転する行列を返す."""
    theta = np.radians(degrees)
    return np.array([[np.cos(theta), -np.sin(theta)],
                     [np.sin(theta), np.cos(theta)]])


TRANSFORMS: dict[str, NDArray[np.float64]] = {
    "恒等変換（変換前）": np.eye(2),
    "拡大縮小": np.array([[1.5, 0.0], [0.0, 0.5]]),
    "回転（30 度）": rotation(30),
    "反射（y 軸に関して）": np.array([[-1.0, 0.0], [0.0, 1.0]]),
    "せん断": np.array([[1.0, 1.0], [0.0, 1.0]]),
    "射影（x 軸へ）": np.array([[1.0, 0.0], [0.0, 0.0]]),
}


def create_figure() -> Figure:
    """変換ごとに、変換後の方眼、F の字、基本ベクトルを描く."""
    fig, axes = plt.subplots(2, 3, figsize=(10, 7))
    shape = la_plot.letter_f()
    for ax, (title, a) in zip(axes.flat, TRANSFORMS.items()):
        la_plot.setup_plane(ax, (-2.5, 2.5), (-2.5, 2.5))
        la_plot.draw_grid(ax, a, color="0.4")
        moved = a @ shape
        ax.fill(moved[0], moved[1], color="C2", alpha=0.5)
        ax.plot(moved[0], moved[1], color="C2")
        la_plot.draw_vector(ax, a[:, 0], color="C3")
        la_plot.draw_vector(ax, a[:, 1], color="C0")
        ax.set_title(title)
    fig.tight_layout()
    return fig


def main() -> None:
    la_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
