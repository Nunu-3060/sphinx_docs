"""測地線、円、ホロサイクル、等距離線を、上半平面モデルと円板モデルで描く.

使い方: python ch07_curves.py
"""

import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import hg_plot

ComplexArray = NDArray[np.complex128]


def curves_in_half_plane() -> dict[str, list[ComplexArray]]:
    """上半平面モデルでの 4 種類の曲線. 測地線は虚軸とする."""
    t = np.linspace(0.0, 2.0 * np.pi, 300)
    y = np.linspace(0.0, 60.0, 600)
    x = np.linspace(-60.0, 60.0, 600)
    return {
        "測地線": [(1j * y).astype(np.complex128)],
        # 中心 2i、半径 0.8 の円（中心 x + i y cosh r、半径 y sinh r のユークリッドの円）
        "円": [(2j * math.cosh(0.8) + 2.0 * math.sinh(0.8) * np.exp(1j * t)).astype(np.complex128)],
        # 無限遠点 ∞ を中心とする水平な直線と、無限遠点 1.5 を中心とする実軸に接する円
        "ホロサイクル": [(x + 3.0j).astype(np.complex128), (1.5 + 0.6j + 0.6j * np.exp(1j * t)).astype(np.complex128)],
        # 虚軸から距離 d の等距離線は、原点を通る半直線 |x| / y = sinh d
        "等距離線": [(math.sinh(0.6) * y + 1j * y).astype(np.complex128),
                 (-math.sinh(0.6) * y + 1j * y).astype(np.complex128)],
    }


def create_figure() -> Figure:
    """上半平面モデルの曲線と、ケーリー変換でそれを円板に移したものを並べる."""
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.8))
    hg_plot.setup_half_plane(axes[0], (-3.5, 3.5), (-0.2, 5.0), "上半平面モデル")
    hg_plot.setup_disk(axes[1], "ポアンカレ円板モデル")
    colors = {"測地線": "k", "円": "C0", "ホロサイクル": "C3", "等距離線": "C2"}
    for name, lines in curves_in_half_plane().items():
        for k, line in enumerate(lines):
            label = name if k == 0 else None
            hg_plot.plot_complex(axes[0], line, color=colors[name], linewidth=1.8, label=label)
            disk = (line - 1j) / (line + 1j)
            hg_plot.plot_complex(axes[1], disk, color=colors[name], linewidth=1.8)
    axes[0].legend(loc="upper right", fontsize=10)
    fig.tight_layout()
    return fig


def main() -> None:
    hg_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
