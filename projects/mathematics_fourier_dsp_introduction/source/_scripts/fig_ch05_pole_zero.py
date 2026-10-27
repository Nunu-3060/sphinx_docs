"""2 次の共振器の極と零点の配置（左）と、振幅特性（右）を描く.

H(z) = (1 - z^-2) / (1 - 2 r cos(theta) z^-1 + r^2 z^-2) は、
極が r e^{±j theta}、零点が z = ±1 にある。極を単位円に近づける（r を 1 に近づける）と、
角度 theta に対応する周波数の付近の利得が大きくなる。
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from scipy import signal

import fig_common

THETA = np.pi / 4  # 極の角度 [rad]


def create_figure() -> Figure:
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), width_ratios=(1, 1.5))
    ax = axes[0]
    phi = np.linspace(0, 2 * np.pi, 361)
    ax.plot(np.cos(phi), np.sin(phi), color="0.6", linewidth=1.0)
    ax.axhline(0, color="0.5", linewidth=0.8)
    ax.axvline(0, color="0.5", linewidth=0.8)
    ax.plot([1, -1], [0, 0], "o", markersize=9, markerfacecolor="none", markeredgecolor="k", label="零点")
    for i, r in enumerate((0.7, 0.9, 0.97)):
        poles = r * np.exp(np.array([1j, -1j]) * THETA)
        ax.plot(poles.real, poles.imag, "x", color=f"C{i}", markersize=9, markeredgewidth=2, label=f"極（r = {r}）")
    ax.set_aspect("equal")
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_xlabel("実部")
    ax.set_ylabel("虚部")
    ax.set_title("z 平面")
    ax.legend(loc="lower left", fontsize=8)
    ax = axes[1]
    for i, r in enumerate((0.7, 0.9, 0.97)):
        b = [1.0, 0.0, -1.0]
        a = [1.0, -2 * r * np.cos(THETA), r**2]
        w, h = signal.freqz(b, a, worN=2048)
        ax.plot(w, fig_common.to_db(h), color=f"C{i}", label=f"r = {r}")
    ax.axvline(THETA, color="0.4", linestyle=":")
    ax.set_xticks(np.arange(0, 1.01, 0.25) * np.pi, ["0", r"$\pi/4$", r"$\pi/2$", r"$3\pi/4$", r"$\pi$"])
    ax.set_xlabel(r"正規化角周波数 $\hat{\omega}$ [rad/標本]")
    ax.set_ylabel("利得 [dB]")
    ax.set_ylim(-40, 35)
    ax.set_title("振幅特性")
    ax.legend(loc="upper right")
    for ax in axes:
        fig_common.style_axes(ax)
    fig.tight_layout()
    return fig
