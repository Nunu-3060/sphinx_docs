"""ヒストグラム: 階級の幅によって分布の見え方が変わる.

2 つの山を持つ架空の測定値（試験の点数）を、階級の数を変えて 3 回描く。

使い方: python ch04_histogram.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont


def make_scores() -> np.ndarray:
    """2 つの山を持つ架空の点数を 300 人分作る."""
    rng = np.random.default_rng(1)
    low = rng.normal(45, 8, 120)
    high = rng.normal(72, 7, 180)
    scores: np.ndarray = np.clip(np.concatenate([low, high]), 0, 100)
    return scores


def create_figure() -> Figure:
    """階級の数が 5、20、80 のヒストグラムを並べて描く."""
    scores = make_scores()
    fig, axes = plt.subplots(1, 3, figsize=(10, 3), sharey=False)
    for ax, bins in zip(axes, [5, 20, 80]):
        ax.hist(scores, bins=bins, range=(0, 100), color="C0",
                edgecolor="white", linewidth=0.5)
        ax.set_title(f"階級の数: {bins}")
        ax.set_xlabel("点数")
    axes[0].set_ylabel("人数")
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
