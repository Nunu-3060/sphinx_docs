"""本文の図を作るスクリプトで共通に使う補助関数.

* setup_font()  matplotlib で日本語を表示できるようにする
* style_axes()  目盛り線などの体裁を整える
* to_db()       振幅をデシベル（dB）に変換する
* stem()        離散時間信号を棒（ステム）で描く
"""

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
    # 数式の文字は STIX フォントで描く
    plt.rcParams["mathtext.fontset"] = "stix"


def style_axes(ax: Axes) -> None:
    """薄い目盛り線を引き、グラフの線より奥に置く."""
    ax.grid(True, color="0.88")
    ax.set_axisbelow(True)


def to_db(amplitude: ArrayLike, floor: float = 1e-12) -> NDArray[np.float64]:
    """振幅をデシベルに変換する（20 log10 |a|）.

    log10(0) を避けるため、floor より小さい値は floor として扱う。
    """
    a = np.abs(np.asarray(amplitude))
    result: NDArray[np.float64] = 20.0 * np.log10(np.maximum(a, floor))
    return result


def stem(ax: Axes, x: ArrayLike, y: ArrayLike, color: str = "C0", label: str | None = None,
         markersize: float = 4.0) -> None:
    """離散時間信号を棒（ステム）で描く."""
    markerline, stemlines, baseline = ax.stem(x, y, basefmt=" ", label=label)
    markerline.set_color(color)
    markerline.set_markersize(markersize)
    stemlines.set_color(color)
    stemlines.set_linewidth(1.0)
