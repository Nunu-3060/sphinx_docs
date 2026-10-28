"""本書のサンプルで共通に使う、図の表示と保存の補助関数.

* setup_font()   matplotlib で日本語を表示できるようにする
* run_sample()   サンプルのコマンドライン引数を解釈し、図を画面に表示するかファイルに保存する

各サンプルは、次の関数を持つ（どれも省略できる）。

* create_figures()     図の名前と matplotlib の Figure の辞書を返す
* report()             計算結果を標準出力に表示する
* create_animation()   GIF アニメーションをファイルに保存する
"""

import argparse
from collections.abc import Callable
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.figure import Figure

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
    # 日本語フォントの多くはマイナス記号（U+2212）を持たないため、負の数の目盛りにハイフンを使う
    plt.rcParams["axes.unicode_minus"] = False
    # 数式の文字は、本文の数式に近い STIX フォントで描く
    plt.rcParams["mathtext.fontset"] = "stix"


def run_sample(
    description: str,
    create_figures: Callable[[], dict[str, Figure]] | None = None,
    report: Callable[[], None] | None = None,
    create_animation: Callable[[Path], None] | None = None,
) -> None:
    """サンプルの main() から呼び出す.

    引数なしで実行すると、計算結果を表示し、図を画面に表示する。
    --save DIR を指定すると、図を DIR に PNG で、アニメーションを GIF で保存する。
    """
    # 説明文（サンプルの docstring）の改行を保ったまま表示する
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--save", metavar="DIR", type=Path,
                        help="図を画面に表示する代わりに、DIR フォルダーに保存する")
    args = parser.parse_args()
    setup_font()
    if report is not None:
        report()
    save_dir: Path | None = args.save
    if save_dir is not None:
        save_dir.mkdir(parents=True, exist_ok=True)
    if create_figures is not None:
        figures = create_figures()
        if save_dir is not None:
            for name, fig in figures.items():
                path = save_dir / f"{name}.png"
                fig.savefig(path, dpi=120, bbox_inches="tight")
                print(f"保存した: {path}")
            plt.close("all")
        else:
            plt.show()
    if create_animation is not None:
        if save_dir is not None:
            path = save_dir / "animation.gif"
            create_animation(path)
            print(f"保存した: {path}")
        else:
            print("アニメーションを保存するには --save DIR を指定する。")
