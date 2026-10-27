"""三角関数の直交性: 積を 1 周期で積分すると、異なる周波数なら 0 になる."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import fig_common


def create_figure() -> Figure:
    t = np.linspace(0.0, 1.0, 1001)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.4), sharey=True)
    cases = [
        (np.sin(2 * np.pi * t), np.sin(2 * np.pi * 2 * t), r"$\sin(2\pi t)\,\sin(4\pi t)$", "積分 = 0"),
        (np.sin(2 * np.pi * t), np.sin(2 * np.pi * t), r"$\sin^2(2\pi t)$", "積分 = 1/2"),
    ]
    for ax, (a, b, label, result) in zip(axes, cases):
        product = a * b
        ax.plot(t, a, color="0.6", linewidth=0.8)
        ax.plot(t, b, color="0.6", linewidth=0.8, linestyle="--")
        ax.plot(t, product, color="C0", linewidth=1.5)
        ax.fill_between(t, product, 0, where=product >= 0, color="C0", alpha=0.3)
        ax.fill_between(t, product, 0, where=product < 0, color="C3", alpha=0.3)
        ax.set_title(f"{label}（{result}）")
        ax.set_xlabel("時間 t [s]（T = 1 s）")
        ax.set_ylim(-1.2, 1.2)
        fig_common.style_axes(ax)
    fig.tight_layout()
    return fig
