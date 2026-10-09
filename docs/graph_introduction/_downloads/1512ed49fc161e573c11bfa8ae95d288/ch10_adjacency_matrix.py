"""隣接行列: グラフを行列として描く.

ch10_graph_from_edges.py と同じ呼び出し関係を隣接行列にし、
ヒートマップで描く。行が呼び出し元、列が呼び出し先で、エッジがある
マスを塗る。

使い方: python ch10_adjacency_matrix.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont
from ch10_graph_from_edges import EDGES, nodes


def adjacency_matrix(names: list[str]) -> np.ndarray:
    """エッジがあれば 1、なければ 0 の隣接行列を返す."""
    index = {name: i for i, name in enumerate(names)}
    matrix = np.zeros((len(names), len(names)))
    for source, target in EDGES:
        matrix[index[source], index[target]] = 1
    return matrix


def create_figure() -> Figure:
    """隣接行列のヒートマップを描く."""
    names = nodes()
    matrix = adjacency_matrix(names)
    fig, ax = plt.subplots(figsize=(4.8, 4.2))
    ax.imshow(matrix, cmap="Blues", vmin=0, vmax=1.3)
    # マスの境界に線を引く
    ax.set_xticks(np.arange(len(names) + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(len(names) + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="minor", length=0)
    ax.set_xticks(range(len(names)), names, rotation=45)
    ax.set_yticks(range(len(names)), names)
    ax.set_xlabel("呼び出し先")
    ax.set_ylabel("呼び出し元")
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
