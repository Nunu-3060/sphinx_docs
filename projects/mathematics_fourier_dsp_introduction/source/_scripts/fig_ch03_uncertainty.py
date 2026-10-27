"""時間幅と帯域幅の関係: ガウス関数を時間方向に縮めると、スペクトルは広がる."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import fig_common


def create_figure() -> Figure:
    t = np.linspace(-3.0, 3.0, 1201)
    f = np.linspace(-3.0, 3.0, 1201)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
    for i, a in enumerate((0.5, 1.0, 2.0)):
        axes[0].plot(t, np.exp(-np.pi * (t / a) ** 2), color=f"C{i}", label=f"a = {a}")
        axes[1].plot(f, a * np.exp(-np.pi * (a * f) ** 2), color=f"C{i}", label=f"a = {a}")
    axes[0].set_title(r"$x(t) = e^{-\pi (t/a)^2}$")
    axes[0].set_xlabel("時間 t [s]")
    axes[1].set_title(r"$X(f) = a\, e^{-\pi (a f)^2}$")
    axes[1].set_xlabel("周波数 f [Hz]")
    for ax in axes:
        ax.legend(loc="upper right")
        fig_common.style_axes(ax)
    fig.tight_layout()
    return fig
