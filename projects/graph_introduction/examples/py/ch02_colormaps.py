"""カラーマップの 3 つの種類: 質的、連続、発散.

カテゴリを区別する質的カラーマップ、量の大小を表す連続カラーマップ、
基準値からの上下を表す発散カラーマップを並べて表示する。

使い方: python ch02_colormaps.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont

COLORMAPS = [
    ("質的（tab10）: カテゴリの区別", "tab10", 10),
    ("連続（viridis）: 量の大小", "viridis", 256),
    ("発散（RdBu）: 基準値からの上下", "RdBu", 256),
]


def create_figure() -> Figure:
    """3 種類のカラーマップを帯として並べる."""
    fig, axes = plt.subplots(3, 1, figsize=(7, 2.6))
    for ax, (title, name, count) in zip(axes, COLORMAPS):
        gradient = np.linspace(0, 1, count).reshape(1, -1)
        ax.imshow(gradient, cmap=plt.get_cmap(name, count), aspect="auto")
        ax.set_title(title, loc="left", fontsize=10)
        ax.set_axis_off()
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
