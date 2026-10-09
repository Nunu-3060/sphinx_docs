"""円の大きさで量を表すときの誤り: 半径を値に比例させる.

値が 1、2、4 の 3 つの量を円で表す。半径を値に比例させると、面積は
値の 2 乗に比例し、差が誇張される。面積を値に比例させるのが正しい。

使い方: python ch14_area_scaling.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Circle

import jpfont

VALUES = [1.0, 2.0, 4.0]


def create_figure() -> Figure:
    """半径を比例させた円と、面積を比例させた円を並べて描く."""
    fig, (ax_bad, ax_good) = plt.subplots(1, 2, figsize=(10, 3.4))
    cases = (
        (ax_bad, [v for v in VALUES], "悪い例: 半径を値に比例させる"),
        (ax_good, [np.sqrt(v) for v in VALUES],
         "改善例: 面積を値に比例させる"),
    )
    for ax, radii, title in cases:
        x = 0.0
        for value, radius in zip(VALUES, radii):
            x += radius
            ax.add_patch(Circle((x, radius), radius, color="C0", alpha=0.7))
            ax.text(x, -0.4, f"値 {value:.0f}", ha="center", va="top")
            x += radius + 0.4
        ax.set_xlim(-0.2, 15)
        ax.set_ylim(-1.2, 8.2)
        ax.set_aspect("equal")
        ax.set_axis_off()
        ax.set_title(title, fontsize=11)
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
