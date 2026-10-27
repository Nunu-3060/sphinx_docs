"""オイラーの公式: 単位円の上の点 e^{j theta} と、その実部と虚部を描く."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import fig_common

THETA = np.pi / 3  # 図に示す角度


def create_figure() -> Figure:
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), width_ratios=(1, 1.6))
    ax = axes[0]
    phi = np.linspace(0, 2 * np.pi, 361)
    ax.plot(np.cos(phi), np.sin(phi), color="0.6", linewidth=1.0)
    ax.axhline(0, color="0.5", linewidth=0.8)
    ax.axvline(0, color="0.5", linewidth=0.8)
    c, s = np.cos(THETA), np.sin(THETA)
    ax.annotate("", xy=(c, s), xytext=(0, 0), arrowprops={"arrowstyle": "-|>", "color": "C3", "linewidth": 2})
    ax.plot([c, c], [0, s], color="0.4", linestyle="--", linewidth=0.8)
    ax.plot([0, c], [0, 0], color="C0", linewidth=3)
    ax.plot([0, 0], [0, s], color="C1", linewidth=3)
    arc = np.linspace(0, THETA, 50)
    ax.plot(0.25 * np.cos(arc), 0.25 * np.sin(arc), color="k", linewidth=0.8)
    ax.text(0.3, 0.12, r"$\theta$", fontsize=13)
    ax.text(c + 0.05, s + 0.05, r"$e^{j\theta}$", fontsize=13, color="C3")
    ax.text(c / 2, -0.17, r"$\cos\theta$", fontsize=12, color="C0", ha="center")
    ax.text(-0.45, s / 2, r"$\sin\theta$", fontsize=12, color="C1", va="center")
    ax.text(1.1, -0.15, "実軸", fontsize=10)
    ax.text(0.05, 1.12, "虚軸", fontsize=10)
    ax.set_xlim(-1.3, 1.4)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect("equal")
    ax.set_title("複素平面の単位円")
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax = axes[1]
    ax.plot(phi, np.cos(phi), color="C0", label=r"実部 $\cos\theta$")
    ax.plot(phi, np.sin(phi), color="C1", label=r"虚部 $\sin\theta$")
    ax.axvline(THETA, color="C3", linestyle=":")
    ax.set_xticks(np.arange(0, 2.01, 0.5) * np.pi, ["0", r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$"])
    ax.set_xlabel(r"角度 $\theta$ [rad]")
    ax.set_title(r"$e^{j\theta}$ の実部と虚部")
    ax.legend(loc="lower left")
    fig_common.style_axes(ax)
    fig.tight_layout()
    return fig
