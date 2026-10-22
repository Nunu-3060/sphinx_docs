"""本書のサンプルで共通に使う、図の描画の補助関数.

* setup_font()   matplotlib で日本語を表示できるようにする
* setup_plane()  2 次元の座標平面（縦横の目盛りが等しい方眼）を用意する
* draw_vector()  矢印でベクトルを描く
* draw_grid()    方眼を行列で変換した図を描く
* letter_f()     向きの分かる図形（F の字）の頂点を返す
"""

from collections.abc import Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.axes import Axes
from numpy.typing import ArrayLike, NDArray

# Windows、macOS、Linux で日本語を表示できる代表的なフォント
FONT_CANDIDATES = [
    "Yu Gothic",
    "Meiryo",
    "Hiragino Sans",
    "Noto Sans CJK JP",
    "Noto Sans JP",
    "IPAexGothic",
]


def setup_font() -> None:
    """日本語を表示できるフォントを matplotlib に設定する.

    候補のフォントのうち、最初に見つかったものを使う。どれも見つからない
    場合は既定のフォントのままになり、日本語の文字は豆腐（□）で表示される。
    """
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in FONT_CANDIDATES:
        if name in available:
            plt.rcParams["font.family"] = name
            break
    # 日本語フォントの多くはマイナス記号（U+2212）を持たないため、
    # 負の数の目盛りにハイフンを使う
    plt.rcParams["axes.unicode_minus"] = False
    # 数式の文字は、本文の数式に近い STIX フォントで描く
    plt.rcParams["mathtext.fontset"] = "stix"


def setup_plane(ax: Axes, xlim: tuple[float, float], ylim: tuple[float, float]) -> None:
    """縦横の目盛りが等しい座標平面を用意し、x 軸と y 軸を描く."""
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.grid(True, color="0.9")
    ax.axhline(0, color="0.5", linewidth=0.8)
    ax.axvline(0, color="0.5", linewidth=0.8)
    ax.set_axisbelow(True)


def draw_vector(ax: Axes, vector: ArrayLike, origin: ArrayLike = (0.0, 0.0), color: str = "C0",
                label: str | None = None, offset: tuple[float, float] = (0.1, 0.1),
                linestyle: str = "-") -> None:
    """origin を始点とする矢印でベクトルを描き、終点の近くに label を書く."""
    start = np.asarray(origin, dtype=float)
    end = start + np.asarray(vector, dtype=float)
    ax.annotate("", xy=(end[0], end[1]), xytext=(start[0], start[1]),
                arrowprops={"arrowstyle": "-|>", "color": color, "linewidth": 2,
                            "linestyle": linestyle, "shrinkA": 0, "shrinkB": 0,
                            "mutation_scale": 15})
    if label is not None:
        ax.text(end[0] + offset[0], end[1] + offset[1], label, color=color, fontsize=12)


def draw_grid(ax: Axes, matrix: ArrayLike, extent: int = 3, color: str = "C0") -> None:
    """-extent から extent までの方眼の直線を、行列 matrix で変換して描く."""
    a = np.asarray(matrix, dtype=float)
    t = np.linspace(-extent, extent, 2)
    for k in range(-extent, extent + 1):
        for line in (np.vstack([t, np.full(2, k)]), np.vstack([np.full(2, k), t])):
            moved = a @ line
            ax.plot(moved[0], moved[1], color=color, linewidth=0.6, alpha=0.5)


def letter_f() -> NDArray[np.float64]:
    """F の字の形をした多角形の頂点を、2 行 N 列の配列で返す.

    左右や上下が反転すると形が変わるので、変換の向きを確かめるのに使う。
    """
    points: Sequence[tuple[float, float]] = [
        (0.0, 0.0), (0.3, 0.0), (0.3, 0.6), (0.7, 0.6), (0.7, 0.9), (0.3, 0.9),
        (0.3, 1.2), (0.9, 1.2), (0.9, 1.5), (0.0, 1.5), (0.0, 0.0),
    ]
    return np.array(points, dtype=float).T
