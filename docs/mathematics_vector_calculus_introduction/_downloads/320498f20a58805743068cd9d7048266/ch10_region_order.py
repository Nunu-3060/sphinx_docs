"""領域 D: x^2 <= y <= x を、縦の帯（先に y で積分）と横の帯（先に x で積分）に分ける様子を描く.

使い方: python ch10_region_order.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

import vc_plot


def create_figure() -> Figure:
    """左に縦の帯、右に横の帯で領域 D を分けた図を描く."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.0, 4.5))
    s = np.linspace(0.0, 1.0, 200)
    for ax in (ax1, ax2):
        vc_plot.setup_plane(ax, (-0.1, 1.15), (-0.1, 1.15))
        ax.fill_between(s, s**2, s, color="C0", alpha=0.15)
        ax.plot(s, s, color="C0")
        ax.plot(s, s**2, color="C0")
        ax.text(0.62, 0.78, "$y = x$", color="C0", fontsize=12)
        ax.text(0.78, 0.45, "$y = x^2$", color="C0", fontsize=12)

    # 縦の帯：x を固定し、y を x^2 から x まで動かす
    for x in np.linspace(0.1, 0.9, 9):
        ax1.add_patch(Rectangle((x - 0.02, x**2), 0.04, x - x**2, color="C1", alpha=0.6))
    ax1.set_title("縦の帯：$\\int_0^1 \\left( \\int_{x^2}^{x} f \\, dy \\right) dx$")

    # 横の帯：y を固定し、x を y から √y まで動かす
    for y in np.linspace(0.1, 0.9, 9):
        ax2.add_patch(Rectangle((y, y - 0.02), np.sqrt(y) - y, 0.04, color="C2", alpha=0.6))
    ax2.set_title("横の帯：$\\int_0^1 \\left( \\int_{y}^{\\sqrt{y}} f \\, dx \\right) dy$")
    fig.tight_layout()
    return fig


def main() -> None:
    vc_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
