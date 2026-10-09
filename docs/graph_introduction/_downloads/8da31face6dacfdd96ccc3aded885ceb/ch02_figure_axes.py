"""matplotlib の基本構造: Figure と Axes.

1 つの Figure（図全体）に 2 つの Axes（グラフ領域）を作り、それぞれに
グラフを描く。本書のサンプルは、すべてこの書き方を使う。

使い方: python ch02_figure_axes.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont


def create_figure() -> Figure:
    """1 行 2 列の Axes を持つ Figure を作る."""
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(8, 3))

    x = np.linspace(0, 2 * np.pi, 100)
    ax_left.plot(x, np.sin(x))
    ax_left.set_title("左の Axes: 折れ線グラフ")

    ax_right.bar(["A", "B", "C"], [3, 5, 2])
    ax_right.set_title("右の Axes: 棒グラフ")

    fig.suptitle("Figure（図全体）")
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
