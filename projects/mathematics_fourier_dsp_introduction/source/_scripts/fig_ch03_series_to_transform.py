"""周期を長くすると、フーリエ級数の線スペクトルが密になり、フーリエ変換に近づく.

幅 1 の矩形パルスを周期 T で繰り返した信号の複素フーリエ係数は
c_k = sinc(k / T) / T である。T c_k を周波数 k / T の位置に描くと、
包絡線はいつも sinc(f) になり、T を長くすると線の間隔 1 / T が狭くなる。
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import fig_common


def create_figure() -> Figure:
    periods = (2.0, 4.0, 16.0)
    t = np.linspace(-9.0, 9.0, 4001)
    f = np.linspace(-4.0, 4.0, 1001)
    fig, axes = plt.subplots(len(periods), 2, figsize=(10, 6.5), width_ratios=(1, 1.3))
    for row, period in enumerate(periods):
        ax = axes[row, 0]
        phase = np.mod(t + period / 2, period) - period / 2
        ax.plot(t, np.where(np.abs(phase) < 0.5, 1.0, 0.0))
        ax.set_ylabel(f"T = {period:.0f} s")
        ax.set_ylim(-0.2, 1.3)
        fig_common.style_axes(ax)
        ax = axes[row, 1]
        k = np.arange(-int(4 * period), int(4 * period) + 1)
        ax.plot(f, np.sinc(f), color="0.7", linewidth=1.0)
        fig_common.stem(ax, k / period, np.sinc(k / period), color="C1", markersize=3)
        ax.axhline(0, color="0.5", linewidth=0.8)
        ax.set_ylim(-0.35, 1.15)
        fig_common.style_axes(ax)
    axes[0, 0].set_title("周期的な矩形パルス（幅 1 s）")
    axes[0, 1].set_title(r"$T c_k$（周波数 $k/T$ の位置）と包絡線 sinc(f)")
    axes[-1, 0].set_xlabel("時間 t [s]")
    axes[-1, 1].set_xlabel("周波数 f [Hz]")
    fig.tight_layout()
    return fig
