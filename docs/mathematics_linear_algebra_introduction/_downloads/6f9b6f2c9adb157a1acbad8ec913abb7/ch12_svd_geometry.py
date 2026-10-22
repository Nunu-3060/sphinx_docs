"""特異値分解の幾何学的意味: A = U Σ V^T は「回転 → 拡大縮小 → 回転」.

行列 A = [[3, 0], [4, 5]] で単位円を変換する過程を、V^T、Σ、U の
3 段階に分けて描く。緑と赤の矢印は、右特異ベクトル v1、v2 とその行き先である。

使い方: python ch12_svd_geometry.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import la_plot

A = np.array([[3.0, 0.0],
              [4.0, 5.0]])


def create_figure() -> Figure:
    """単位円が V^T、Σ、U の順に変換される様子を描く."""
    u, s, vt = np.linalg.svd(A)
    sigma = np.diag(s)
    steps = [
        ("単位円", np.eye(2)),
        (r"$V^\top$ を掛ける（回転・反射）", vt),
        (r"$\Sigma$ を掛ける（拡大縮小）", sigma @ vt),
        (r"$U$ を掛ける（回転・反射）$= A$", u @ sigma @ vt),
    ]
    theta = np.linspace(0, 2 * np.pi, 200)
    circle = np.vstack([np.cos(theta), np.sin(theta)])
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.8))
    for ax, (title, m) in zip(axes, steps):
        la_plot.setup_plane(ax, (-7.5, 7.5), (-7.5, 7.5))
        image = m @ circle
        ax.fill(image[0], image[1], color="C0", alpha=0.2)
        ax.plot(image[0], image[1], color="C0")
        la_plot.draw_vector(ax, m @ vt[0], color="C2")  # v1 の行き先
        la_plot.draw_vector(ax, m @ vt[1], color="C3")  # v2 の行き先
        ax.set_title(title, fontsize=10)
    fig.tight_layout()
    return fig


def main() -> None:
    la_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
