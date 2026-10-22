"""図生成スクリプトで共通に使う設定。

日本語フォントの指定と、図の保存先（source/images）をまとめる。
"""

import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

# 図の保存先（このファイルから見て ../source/images）
IMAGE_DIR: Path = Path(__file__).resolve().parent.parent / "source" / "images"

# 日本語フォント（先頭から順に、見つかったものを使う）
# Noto Sans JP が可変フォント版しか無い環境では matplotlib が細字（Thin）として扱うため、
# 游ゴシックを先頭に置く。
JAPANESE_FONTS: list[str] = ["Yu Gothic", "Noto Sans JP", "Meiryo"]

# 可変フォント版の Noto Sans JP について「weight normal が見つからない」という警告が
# 大量に出るが、実際の描画には先頭の游ゴシックが使われるので表示しない。
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)


def setup_style() -> None:
    """日本語フォントと図の共通スタイルを設定する。"""
    plt.rcParams["font.family"] = JAPANESE_FONTS
    plt.rcParams["mathtext.fontset"] = "cm"
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["savefig.dpi"] = 150
    plt.rcParams["axes.grid"] = True
    plt.rcParams["grid.alpha"] = 0.3


def save(fig: Figure, name: str) -> Path:
    """図を source/images/<name> に保存して閉じる。"""
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    path = IMAGE_DIR / name
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"saved: {path}")
    return path
