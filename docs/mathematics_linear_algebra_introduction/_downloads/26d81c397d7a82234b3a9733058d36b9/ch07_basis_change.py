"""基底の取り替え: 同じベクトルを 2 つの基底で表す.

標準基底では (4, 5) と表されるベクトル x を、基底 b1 = (2, 1)、
b2 = (1, 2) で表すと、x = 1 b1 + 2 b2 なので座標は (1, 2) になる。

使い方: python ch07_basis_change.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import la_plot

B = np.array([[2.0, 1.0],
              [1.0, 2.0]])  # 基底ベクトル b1、b2 を列に並べた行列
X = np.array([4.0, 5.0])


def report() -> None:
    """x の、基底 b1、b2 に関する座標を求める."""
    c = np.linalg.solve(B, X)  # B c = x を解く
    print("b1、b2 に関する座標 c =", c)
    print("B @ c =", B @ c)  # 標準基底の座標に戻す


def create_figure() -> Figure:
    """標準基底の方眼と、基底 b1、b2 の方眼の上に x を描く."""
    fig, (ax_std, ax_new) = plt.subplots(1, 2, figsize=(9, 4.4))

    la_plot.setup_plane(ax_std, (-1, 6), (-1, 6))
    la_plot.draw_vector(ax_std, (1, 0), color="C3", label=r"$\mathbf{e}_1$", offset=(0.0, -0.5))
    la_plot.draw_vector(ax_std, (0, 1), color="C0", label=r"$\mathbf{e}_2$", offset=(-0.6, 0.0))
    la_plot.draw_vector(ax_std, X, color="C2", label=r"$\mathbf{x}$")
    ax_std.set_title(r"標準基底では $\mathbf{x} = (4, 5)$")

    la_plot.setup_plane(ax_new, (-1, 6), (-1, 6))
    ax_new.grid(False)
    la_plot.draw_grid(ax_new, B, extent=4, color="0.4")
    la_plot.draw_vector(ax_new, B[:, 0], color="C3", label=r"$\mathbf{b}_1$", offset=(0.0, -0.5))
    la_plot.draw_vector(ax_new, B[:, 1], color="C0", label=r"$\mathbf{b}_2$", offset=(-0.6, 0.0))
    la_plot.draw_vector(ax_new, 2 * B[:, 1], origin=B[:, 0], color="C0", linestyle="--")
    la_plot.draw_vector(ax_new, X, color="C2", label=r"$\mathbf{x}$")
    ax_new.set_title(r"基底 $\mathbf{b}_1, \mathbf{b}_2$ では $\mathbf{x} = (1, 2)$")

    fig.tight_layout()
    return fig


def main() -> None:
    report()
    la_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
