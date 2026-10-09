"""matplotlib で日本語を表示するための設定.

各サンプルの main() から setup() を呼び出す。候補のフォントのうち、
最初に見つかったものを使う。どれも見つからない場合は既定のフォントのまま
になり、日本語の文字は豆腐（□）で表示される。
"""

import matplotlib.pyplot as plt
from matplotlib import font_manager

# Windows、macOS、Linux で日本語を表示できる代表的なフォント
CANDIDATES = [
    "Yu Gothic",
    "Meiryo",
    "Hiragino Sans",
    "Noto Sans CJK JP",
    "Noto Sans JP",
    "IPAexGothic",
]


def setup() -> None:
    """日本語を表示できるフォントを matplotlib に設定する."""
    available = {font.name for font in font_manager.fontManager.ttflist}
    for name in CANDIDATES:
        if name in available:
            plt.rcParams["font.family"] = name
            break
    # 日本語フォントの多くはマイナス記号（U+2212）を持たないため、
    # 負の数の目盛りにハイフンを使う
    plt.rcParams["axes.unicode_minus"] = False
