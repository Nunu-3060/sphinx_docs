"""極座標の微小な領域（r から r+Δr、θ から θ+Δθ）の面積がおよそ r Δr Δθ になる様子を描く.

使い方: python ch10_polar_cell.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import vc_plot


def create_figure() -> Figure:
    """極座標の格子と、1 つの微小な領域を描く."""
    r0, dr = 2.0, 0.5
    t0, dt = np.pi / 6, np.pi / 12
    fig, ax = plt.subplots(figsize=(5.5, 5.0))
    vc_plot.setup_plane(ax, (-0.2, 3.2), (-0.2, 3.0))

    # 極座標の格子
    s = np.linspace(0.0, np.pi / 2, 100)
    for r in np.arange(0.5, 3.01, 0.5):
        ax.plot(r * np.cos(s), r * np.sin(s), color="0.8", linewidth=0.8)
    for t in np.arange(0.0, np.pi / 2 + 0.01, np.pi / 12):
        ax.plot([0.0, 3.0 * np.cos(t)], [0.0, 3.0 * np.sin(t)], color="0.8", linewidth=0.8)

    # 微小な領域（扇形の一部）を塗る
    arc = np.linspace(t0, t0 + dt, 30)
    xs = np.concatenate([r0 * np.cos(arc), (r0 + dr) * np.cos(arc[::-1])])
    ys = np.concatenate([r0 * np.sin(arc), (r0 + dr) * np.sin(arc[::-1])])
    ax.fill(xs, ys, color="C1", alpha=0.5)

    # 辺の長さの注記
    mid = t0 + dt / 2
    ax.annotate(r"$\Delta r$", xy=((r0 + dr / 2) * np.cos(t0), (r0 + dr / 2) * np.sin(t0)),
                xytext=(2.6, 0.75), fontsize=13, arrowprops={"arrowstyle": "-", "color": "0.3"})
    ax.annotate(r"$r \, \Delta\theta$", xy=(r0 * np.cos(mid), r0 * np.sin(mid)),
                xytext=(1.0, 1.55), fontsize=13, arrowprops={"arrowstyle": "-", "color": "0.3"})
    # 角度 θ と Δθ を円弧で示す
    s = np.linspace(0.0, t0, 30)
    ax.plot(0.6 * np.cos(s), 0.6 * np.sin(s), color="C0", linewidth=1.5)
    ax.text(0.68 * np.cos(t0 / 2), 0.68 * np.sin(t0 / 2) - 0.05, r"$\theta$", color="C0", fontsize=13)
    s = np.linspace(t0, t0 + dt, 30)
    ax.plot(1.0 * np.cos(s), 1.0 * np.sin(s), color="C3", linewidth=1.5)
    ax.text(1.05 * np.cos(mid) + 0.02, 1.05 * np.sin(mid), r"$\Delta\theta$", color="C3", fontsize=13)
    ax.set_title(r"面積 $\approx r \, \Delta r \, \Delta\theta$")
    fig.tight_layout()
    return fig


def main() -> None:
    vc_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
