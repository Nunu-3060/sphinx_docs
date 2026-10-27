"""図生成スクリプトで共通に使う設定と関数。"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

# 図の出力先 (source/figures)
FIGURE_DIR: Path = Path(__file__).resolve().parent.parent / "figures"

# サンプルコードの置き場所 (examples)
EXAMPLES_DIR: Path = Path(__file__).resolve().parents[2] / "examples"

# 日本語を表示できるフォントを優先順に指定する
JAPANESE_FONTS: list[str] = ["Yu Gothic", "Meiryo", "MS Gothic", "sans-serif"]

# 図で共通に使う色
BLUE = "#4878a8"
ORANGE = "#e07b39"
GREEN = "#5a9e6f"
GRAY = "#9a9a9a"
LIGHT_BLUE = "#c9daea"
NAVY = "#2f4b6e"


def setup_style() -> None:
    """日本語フォントと全体の見た目を設定する。"""
    plt.rcParams["font.family"] = JAPANESE_FONTS
    plt.rcParams["font.size"] = 11
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.right"] = False


def save_figure(fig: Figure, name: str) -> Path:
    """図を PNG として保存し、保存先のパスを返す。"""
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURE_DIR / name
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path
