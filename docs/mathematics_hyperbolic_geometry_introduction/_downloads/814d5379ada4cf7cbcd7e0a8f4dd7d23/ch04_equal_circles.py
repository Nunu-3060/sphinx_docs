"""双曲的な半径が等しい円を、上半平面モデルと円板モデルのいろいろな位置に描く.

使い方: python ch04_equal_circles.py
"""

import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Circle

import hg
import hg_plot

RADIUS = 0.5  # 双曲的な半径


def create_figure() -> Figure:
    """左に上半平面モデル、右に円板モデルで、半径 RADIUS の円を並べる.

    上半平面モデルで中心 x + iy、双曲的な半径 r の円は、
    中心 x + i y cosh r、半径 y sinh r のユークリッドの円になる。
    """
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.6))

    ax = axes[0]
    hg_plot.setup_half_plane(ax, (-3.2, 3.2), (-0.2, 5.0), "上半平面モデル")
    # 中心の高さ y を 2 倍ずつ変え、横の間隔も y に比例させる（z -> 2z は等長変換である）
    for y in (0.25, 0.5, 1.0, 2.0):
        for m in range(-6, 7):
            x = 1.5 * y * m
            if abs(x) < 3.0:
                ax.add_patch(Circle((x, y * math.cosh(RADIUS)), y * math.sinh(RADIUS), facecolor="C0", alpha=0.35,
                                    edgecolor="C0"))

    ax = axes[1]
    hg_plot.setup_disk(ax, "ポアンカレ円板モデル")
    t = np.linspace(0.0, 2.0 * np.pi, 120)
    circle0 = hg.disk_point(RADIUS, 0.0).real * np.exp(1j * t)  # 原点を中心とする円
    for r in (0.0, 1.2, 2.4, 3.6):
        count = 1 if r == 0.0 else 8
        for j in range(count):
            center = hg.disk_point(r, 2.0 * np.pi * j / count)
            moved = (circle0 + center) / (1.0 + np.conj(center) * circle0)  # 原点を center に移す
            ax.fill(moved.real, moved.imag, color="C0", alpha=0.35)
    fig.tight_layout()
    return fig


def main() -> None:
    hg_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
