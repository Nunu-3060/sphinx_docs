"""本書のサンプルで共通に使う、図の描画の補助関数.

* setup_font()     matplotlib で日本語を表示できるようにする
* setup_plane()    2 次元の座標平面（縦横の目盛りが等しい方眼）を用意する
* draw_vector()    2 次元のベクトルを矢印で描く
* add_axes3d()     3 次元のグラフを描く Axes を追加する
* draw_vector3d()  3 次元のベクトルを矢印で描く
* mesh()           2 次元の格子点の座標を作る
"""

from typing import cast

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
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
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")


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


def add_axes3d(fig: Figure, position: int = 111) -> Axes3D:
    """fig に 3 次元のグラフを描く Axes を追加し、軸の名前を付けて返す.

    position は fig.add_subplot() と同じ 3 桁の整数（例：121 は 1 行 2 列の 1 番目）で指定する。
    """
    ax = cast(Axes3D, fig.add_subplot(position, projection="3d"))
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_zlabel("$z$")
    return ax


def draw_vector3d(ax: Axes3D, vector: ArrayLike, origin: ArrayLike = (0.0, 0.0, 0.0),
                  color: str = "C0", label: str | None = None) -> None:
    """origin を始点とする矢印で 3 次元のベクトルを描き、終点の近くに label を書く."""
    start = np.asarray(origin, dtype=float)
    vec = np.asarray(vector, dtype=float)
    ax.quiver(*start, *vec, color=color, linewidth=2, arrow_length_ratio=0.15)
    if label is not None:
        end = start + vec * 1.08
        ax.text(*end, label, color=color, fontsize=12)


def mesh(xlim: tuple[float, float], ylim: tuple[float, float],
         n: int = 15) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """xlim と ylim の範囲を n 等分した格子点の x 座標と y 座標を、2 次元配列で返す."""
    x = np.linspace(xlim[0], xlim[1], n)
    y = np.linspace(ylim[0], ylim[1], n)
    xx, yy = np.meshgrid(x, y)
    return xx, yy
