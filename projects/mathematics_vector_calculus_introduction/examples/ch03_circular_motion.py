"""等速円運動の速度ベクトルと加速度ベクトルを描く.

使い方: python ch03_circular_motion.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import vc_plot

RADIUS = 2.0  # 円の半径 R
OMEGA = 1.0  # 角速度 ω


def create_figure() -> Figure:
    """円周上のいくつかの点で、速度（接線方向）と加速度（中心向き）を矢印で描く."""
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    vc_plot.setup_plane(ax, (-3.6, 3.6), (-3.6, 3.6))

    t = np.linspace(0.0, 2.0 * np.pi, 200)
    ax.plot(RADIUS * np.cos(t), RADIUS * np.sin(t), color="0.4", linewidth=1)

    scale = 0.6  # 矢印を見やすい長さにするための倍率
    for i, ti in enumerate(np.linspace(0.0, 2.0 * np.pi, 6, endpoint=False) + 0.3):
        r = RADIUS * np.array([np.cos(OMEGA * ti), np.sin(OMEGA * ti)])
        v = RADIUS * OMEGA * np.array([-np.sin(OMEGA * ti), np.cos(OMEGA * ti)])
        a = -OMEGA**2 * r
        ax.plot(r[0], r[1], "o", color="k", markersize=4)
        vc_plot.draw_vector(ax, scale * v, origin=r, color="C0",
                            label=r"$\mathbf{v}$" if i == 0 else None, offset=(0.05, 0.1))
        vc_plot.draw_vector(ax, scale * a, origin=r, color="C3",
                            label=r"$\mathbf{a}$" if i == 0 else None, offset=(-0.1, 0.15))

    ax.set_title("等速円運動の速度（青）と加速度（赤）")
    fig.tight_layout()
    return fig


def main() -> None:
    vc_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
