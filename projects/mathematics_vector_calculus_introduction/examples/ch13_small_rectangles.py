"""領域を微小な長方形に分け、各長方形の循環を足すと内部の辺が打ち消し合う様子を描く.

使い方: python ch13_small_rectangles.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

import vc_plot


def draw_loop(ax: Axes, x0: float, y0: float, x1: float, y1: float, color: str) -> None:
    """長方形 [x0, x1] × [y0, y1] の周を反時計回りにたどる矢印を描く."""
    corners = np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])
    for start, end in zip(corners, np.roll(corners, -1, axis=0)):
        ax.plot([start[0], end[0]], [start[1], end[1]], color=color, linewidth=1.2)
        middle = (start + end) / 2
        direction = (end - start) * 0.15
        ax.annotate("", xy=(middle[0] + direction[0], middle[1] + direction[1]),
                    xytext=(middle[0] - direction[0], middle[1] - direction[1]),
                    arrowprops={"arrowstyle": "-|>", "color": color, "mutation_scale": 12})


def create_figure() -> Figure:
    """左に微小な長方形ごとの循環、右に足し合わせた結果（境界だけが残る）を描く."""
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.8))
    nx, ny = 4, 3
    gap = 0.07  # 隣り合う長方形の辺が重ならないように、少し内側にずらす
    for ax in axes:
        ax.set_xlim(-0.3, nx + 0.3)
        ax.set_ylim(-0.3, ny + 0.3)
        ax.set_aspect("equal")
        ax.axis("off")

    for i in range(nx):
        for j in range(ny):
            draw_loop(axes[0], i + gap, j + gap, i + 1 - gap, j + 1 - gap, "C0")
    axes[0].set_title("微小な長方形ごとの循環")

    axes[1].fill([0, nx, nx, 0], [0, 0, ny, ny], color="C0", alpha=0.1)
    draw_loop(axes[1], 0, 0, nx, ny, "C3")
    axes[1].text(nx / 2, ny / 2, "内部の辺は\n打ち消し合う", ha="center", va="center", fontsize=12)
    axes[1].set_title("足し合わせると境界の循環だけが残る")
    fig.tight_layout()
    return fig


def main() -> None:
    vc_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
