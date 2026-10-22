"""スミスチャートを双曲幾何の目で見る.

正規化インピーダンス z = r + jx（r > 0）は右半平面の点であり、反射係数 Gamma = (z - 1) / (z + 1) は
右半平面を単位円板に移すメビウス変換である。このとき
    抵抗 r が一定の円   = Gamma = 1 を中心とするホロサイクル
    リアクタンス x が一定の弧 = Gamma = 1 を端点とする測地線
になる。また、円板の中心からの双曲的な距離 d と電圧定在波比 VSWR の間に VSWR = e^d が成り立つ。

使い方: python ch09_smith_chart.py
"""

import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import ArrayLike, NDArray

import hg
import hg_plot


def gamma(z: complex) -> complex:
    """正規化インピーダンス z の反射係数."""
    return (z - 1.0) / (z + 1.0)


def gamma_array(z: ArrayLike) -> NDArray[np.complex128]:
    """配列で与えた正規化インピーダンスの反射係数."""
    w = np.asarray(z, dtype=np.complex128)
    return (w - 1.0) / (w + 1.0)


def create_figure() -> Figure:
    """抵抗一定の円、リアクタンス一定の弧と、直列リアクタンスと伝送線路による点の動きを描く."""
    fig, ax = plt.subplots(figsize=(6.0, 6.0))
    hg_plot.setup_disk(ax)
    t = np.linspace(-200.0, 200.0, 4000)
    for r in (0.2, 0.5, 1.0, 2.0, 5.0):  # 抵抗一定の円
        hg_plot.plot_complex(ax, gamma_array(r + 1j * t), color="C0", linewidth=0.8)
    for x in (0.2, 0.5, 1.0, 2.0, 5.0, -0.2, -0.5, -1.0, -2.0, -5.0):  # リアクタンス一定の弧
        hg_plot.plot_complex(ax, gamma_array(np.exp(np.linspace(-8.0, 8.0, 800)) + 1j * x), color="C2",
                             linewidth=0.8)
    hg_plot.plot_complex(ax, gamma_array(np.exp(np.linspace(-8.0, 8.0, 800)) + 0j), color="C2", linewidth=0.8)

    # 負荷 z = 2 + j に直列にリアクタンス -j を加えると、r = 2 の円（ホロサイクル）に沿って動く
    path = gamma_array(2.0 + 1j * np.linspace(1.0, 0.0, 50))
    hg_plot.plot_complex(ax, path, color="C3", linewidth=2.5)
    # 続いて伝送線路を通すと、中心のまわりに回転する（中心からの距離、つまり VSWR は変わらない）
    g0 = gamma(2.0 + 0j)
    rotation = g0 * np.exp(-1j * np.linspace(0.0, math.pi, 60))
    hg_plot.plot_complex(ax, rotation, color="C1", linewidth=2.5)
    for z, label in ((2.0 + 1j, "$z = 2 + j$"), (2.0 + 0j, "$z = 2$")):
        g = gamma(z)
        ax.plot([g.real], [g.imag], "ko", markersize=5)
        ax.text(g.real + 0.03, g.imag + 0.04, label, fontsize=11)
    ax.plot([1.0], [0.0], "o", color="C3", markersize=6)
    ax.text(1.02, -0.08, r"$\Gamma = 1$", fontsize=11)
    fig.tight_layout()
    return fig


def report() -> None:
    """いくつかの負荷について、VSWR と e^d を比べる."""
    print("負荷 z        |Gamma|   VSWR      e^d")
    for z in (2.0 + 0j, 0.5 + 0j, 1.0 + 1j, 3.0 - 2j):
        g = gamma(z)
        vswr = (1.0 + abs(g)) / (1.0 - abs(g))
        d = hg.disk_distance(0j, g)
        print(f"{str(z):<13} {abs(g):.5f}   {vswr:.5f}   {math.exp(d):.5f}")


def main() -> None:
    hg_plot.setup_font()
    report()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
