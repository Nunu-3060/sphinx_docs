"""等高線図とカラーマップ: 平面上の量を描く.

2 変数関数 z = f(x, y) の値を、等高線図とカラーマップ（pcolormesh）の
2 通りで描く。

使い方: python ch09_contour.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont


def make_field() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """格子点の座標と、2 つの山と 1 つの谷を持つ関数の値を返す."""
    x = np.linspace(-3, 3, 121)
    y = np.linspace(-2, 2, 81)
    xx, yy = np.meshgrid(x, y)
    zz = (np.exp(-((xx + 1) ** 2 + yy ** 2))
          + 0.7 * np.exp(-((xx - 1.5) ** 2 + (yy - 0.8) ** 2) / 0.5)
          - 0.6 * np.exp(-((xx - 1) ** 2 + (yy + 1) ** 2) / 0.4))
    return xx, yy, zz


def create_figure() -> Figure:
    """等高線図とカラーマップを並べて描く."""
    xx, yy, zz = make_field()
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(10, 3.4))

    lines = ax_left.contour(xx, yy, zz, levels=10, colors="black",
                            linewidths=0.8)
    ax_left.clabel(lines, fontsize=8)  # 等高線に値を書く
    ax_left.set_title("等高線図")

    mesh = ax_right.pcolormesh(xx, yy, zz, cmap="RdBu_r", vmin=-1, vmax=1)
    ax_right.contour(xx, yy, zz, levels=10, colors="black",
                     linewidths=0.4, alpha=0.5)
    fig.colorbar(mesh, ax=ax_right, label="z")
    ax_right.set_title("カラーマップと等高線")

    for ax in (ax_left, ax_right):
        ax.set_aspect("equal")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
