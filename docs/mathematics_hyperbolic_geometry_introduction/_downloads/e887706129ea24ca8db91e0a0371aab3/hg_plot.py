"""本書のサンプルで共通に使う、図の描画の補助関数.

* setup_font()               matplotlib で日本語を表示できるようにする
* setup_disk()               ポアンカレ円板モデル（またはクラインモデル）の円板を描く
* plot_complex()             複素数の点列を折れ線で描く
* setup_half_plane()         上半平面モデルの座標平面を用意する
* half_plane_line()          上半平面モデルで 2 点を通る測地線全体の点列を返す
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.axes import Axes
from matplotlib.patches import Circle
from numpy.typing import NDArray

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


def setup_disk(ax: Axes, title: str | None = None) -> None:
    """単位円板の境界（無限遠）を描き、縦横の目盛りを等しくして軸を消す."""
    ax.add_patch(Circle((0.0, 0.0), 1.0, facecolor="0.97", edgecolor="0.2", linewidth=1.2))
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.set_aspect("equal")
    ax.axis("off")
    if title is not None:
        ax.set_title(title)


def plot_complex(ax: Axes, points: NDArray[np.complex128], color: str = "C0", linewidth: float = 1.5,
                 linestyle: str = "-", label: str | None = None) -> None:
    """複素数の点列 points を、実部を横軸、虚部を縦軸とする折れ線で描く."""
    ax.plot(points.real, points.imag, color=color, linewidth=linewidth, linestyle=linestyle, label=label)


def setup_half_plane(ax: Axes, xlim: tuple[float, float], ylim: tuple[float, float],
                     title: str | None = None) -> None:
    """上半平面モデルの座標平面を用意する. 実軸（無限遠）を太線で描く."""
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axhline(0.0, color="0.2", linewidth=1.2)
    ax.grid(True, color="0.92")
    ax.set_axisbelow(True)
    ax.set_xlabel(r"$\mathrm{Re}\,z$")
    ax.set_ylabel(r"$\mathrm{Im}\,z$")
    if title is not None:
        ax.set_title(title)


def half_plane_line(z: complex, w: complex, n: int = 400, height: float = 100.0) -> NDArray[np.complex128]:
    """上半平面モデルで点 z と点 w を通る測地線全体の点列を返す.

    実部が等しければ垂直な半直線（高さ height まで）、そうでなければ中心が実軸上にある半円になる。
    """
    if abs(z.real - w.real) < 1e-12:
        y = np.linspace(0.0, height, n)
        return (z.real + 1j * y).astype(np.complex128)
    center = (abs(z) ** 2 - abs(w) ** 2) / (2.0 * (z.real - w.real))
    radius = abs(z - center)
    t = np.linspace(0.0, np.pi, n)
    return (center + radius * np.exp(1j * t)).astype(np.complex128)
