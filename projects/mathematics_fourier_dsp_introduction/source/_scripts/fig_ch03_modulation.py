"""変調: 信号に余弦波を掛けると、スペクトルが ±f0 だけ移動する."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import fig_common

F0 = 5.0  # 搬送波の周波数 [Hz]


def create_figure() -> Figure:
    t = np.linspace(-2.0, 2.0, 4001)
    f = np.linspace(-9.0, 9.0, 1801)
    envelope = np.exp(-np.pi * t**2)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
    ax = axes[0]
    ax.plot(t, envelope, color="C0", label="x(t)")
    ax.plot(t, envelope * np.cos(2 * np.pi * F0 * t), color="C1", linewidth=0.8, label=r"$x(t)\cos(2\pi f_0 t)$")
    ax.set_xlabel("時間 t [s]")
    ax.set_title("時間領域")
    ax.legend(loc="lower right", fontsize=9)
    ax = axes[1]
    spectrum = np.exp(-np.pi * f**2)
    shifted = 0.5 * (np.exp(-np.pi * (f - F0) ** 2) + np.exp(-np.pi * (f + F0) ** 2))
    ax.plot(f, spectrum, color="C0", label="X(f)")
    ax.plot(f, shifted, color="C1", label=r"$\frac{1}{2}X(f - f_0) + \frac{1}{2}X(f + f_0)$")
    ax.set_xlabel("周波数 f [Hz]")
    ax.set_title(f"周波数領域（f0 = {F0:.0f} Hz）")
    ax.legend(loc="upper right", fontsize=9)
    ax.set_ylim(-0.05, 1.4)
    for ax in axes:
        fig_common.style_axes(ax)
    fig.tight_layout()
    return fig
