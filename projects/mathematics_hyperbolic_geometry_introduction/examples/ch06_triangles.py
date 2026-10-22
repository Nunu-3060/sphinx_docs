"""円板モデルで、大きさの異なる正三角形を描き、内角の和が大きさによって変わることを示す.

使い方: python ch06_triangles.py
"""

import math

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import hg
import hg_plot


def create_figure() -> Figure:
    """原点を中心とし、頂点までの距離が R の正三角形を、R を変えて描く. R が大きいものは理想三角形に近い."""
    fig, ax = plt.subplots(figsize=(6.0, 6.0))
    hg_plot.setup_disk(ax)
    for radius, color in ((0.4, "C0"), (1.0, "C1"), (1.8, "C2"), (16.0, "C3")):
        vs = [hg.disk_point(radius, math.pi / 2.0 + 2.0 * math.pi * k / 3.0) for k in range(3)]
        for k in range(3):
            hg_plot.plot_complex(ax, hg.disk_geodesic(vs[k], vs[(k + 1) % 3], 200), color=color, linewidth=1.8)
        angle_sum = 3.0 * hg.disk_angle(vs[0], vs[1], vs[2])
        name = "理想三角形" if radius > 10.0 else f"$R = {radius}$"
        ax.plot([], [], color=color, label=f"{name}：内角の和 {math.degrees(angle_sum):.1f} 度")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 0.02), ncol=2, fontsize=10, frameon=False)
    fig.tight_layout()
    return fig


def main() -> None:
    hg_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
