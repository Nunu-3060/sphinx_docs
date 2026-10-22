"""ハイパボリックツリーの考え方: 円板の等長変換で、木の注目する部分（焦点）を中央に移す.

使い方: python ch09_focus_context.py
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import ch07_tree
import hg
import hg_plot


def create_figure() -> Figure:
    """左は根を中央に置いた木、右は等長変換で根から 2 段下の頂点を中央に移した木."""
    edges = ch07_tree.hyperbolic_tree()
    focus = edges[3][1]  # 1 本目の枝の先の、さらに 1 段下の頂点（根から 2 段下）
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 5.2))
    hg_plot.setup_disk(axes[0], "根を中央に置いた表示")
    hg_plot.setup_disk(axes[1], "焦点の頂点を中央に移した表示")
    for p, q in edges:
        line = hg.disk_geodesic(p, q, 20)
        hg_plot.plot_complex(axes[0], line, color="C0", linewidth=0.8)
        moved = (line - focus) / (1.0 - focus.conjugate() * line)  # focus を原点に移す等長変換
        hg_plot.plot_complex(axes[1], moved, color="C0", linewidth=0.8)
    axes[0].plot([focus.real], [focus.imag], "o", color="C3", markersize=7)
    axes[1].plot([0.0], [0.0], "o", color="C3", markersize=7)
    root = hg.disk_translate(-focus, 0j)
    axes[0].plot([0.0], [0.0], "s", color="C2", markersize=7)
    axes[1].plot([root.real], [root.imag], "s", color="C2", markersize=7)
    fig.tight_layout()
    return fig


def main() -> None:
    hg_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
