"""円板モデルで、直線 L の上にない点 P を通り L と交わらない直線が無数にあることを描く.

使い方: python ch04_parallels.py
"""

import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import hg
import hg_plot

H = 1.0  # 点 P と直線 L の距離


def parallel_angle(h: float) -> float:
    """平行角 Pi(h). tan(Pi(h) / 2) = e^{-h} から求める."""
    return 2.0 * math.atan(math.exp(-h))


def create_figure() -> Figure:
    """P を原点に置き、L を P から距離 H の位置で虚軸に垂直な測地線とする."""
    fig, ax = plt.subplots(figsize=(5.6, 5.6))
    hg_plot.setup_disk(ax)

    a = 1j * math.tanh(H / 2.0)  # 虚軸上で原点から距離 H の点（L と垂線の交点）
    line_l = hg.disk_line(a, hg.disk_translate(a, 0.5))  # 実軸を虚軸方向に距離 H だけ平行移動した測地線
    hg_plot.plot_complex(ax, line_l, color="k", linewidth=2.2)
    hg_plot.plot_complex(ax, hg.disk_geodesic(0j, a), color="0.4", linestyle=":")

    # 平行角を境に、L と交わる直線と交わらない直線に分かれる
    big_pi = parallel_angle(H)
    for delta in np.linspace(-big_pi, big_pi, 7)[1:-1]:  # L と交わる直線
        direction = 1j * complex(np.exp(1j * delta))
        hg_plot.plot_complex(ax, hg.disk_line(0j, direction * 0.5), color="C0", linewidth=0.9, linestyle="--")
    for sign in (1.0, -1.0):  # 極限平行線
        direction = 1j * complex(np.exp(1j * sign * big_pi))
        hg_plot.plot_complex(ax, hg.disk_line(0j, direction * 0.5), color="C3", linewidth=2.0)
    for delta in np.linspace(big_pi, math.pi - big_pi, 6)[1:-1]:  # L と交わらない直線（超平行線）
        direction = 1j * complex(np.exp(1j * delta))
        hg_plot.plot_complex(ax, hg.disk_line(0j, direction * 0.5), color="C2", linewidth=1.3)

    ax.plot([0.0], [0.0], "ko", markersize=5)
    ax.text(0.04, -0.09, "$P$", fontsize=14)
    ax.text(0.05, a.imag + 0.05, "$L$", fontsize=14)
    end = hg.disk_translate(a, 1.0)  # L の端（無限遠点）
    ax.plot([end.real, -end.real], [end.imag, end.imag], "o", color="C3", markersize=5)
    fig.tight_layout()
    return fig


def main() -> None:
    hg_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
