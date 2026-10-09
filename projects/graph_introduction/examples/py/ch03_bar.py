"""棒グラフ: カテゴリごとの量を比較する.

架空の社内アンケート「主に使うプログラミング言語」の回答数を、
並べ替えない縦棒グラフと、値の大きい順に並べ替えた横棒グラフで描く。

使い方: python ch03_bar.py
"""

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

import jpfont

ANSWERS = {
    "C#": 18,
    "Go": 12,
    "Java": 25,
    "JavaScript": 31,
    "Python": 42,
    "Rust": 7,
    "TypeScript": 27,
}


def create_figure() -> Figure:
    """並べ替えない縦棒グラフと、並べ替えた横棒グラフを描く."""
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(10, 3.8))

    # 左: 名前の順（アルファベット順）の縦棒グラフ
    ax_left.bar(list(ANSWERS), list(ANSWERS.values()), color="C0")
    ax_left.set_title("名前の順の縦棒グラフ")
    ax_left.set_ylabel("回答数")
    ax_left.tick_params(axis="x", labelrotation=45)

    # 右: 値の大きい順の横棒グラフ。上から大きい順に並ぶように、
    # 小さい順に並べてから barh に渡す
    items = sorted(ANSWERS.items(), key=lambda item: item[1])
    names = [name for name, _ in items]
    counts = [count for _, count in items]
    bars = ax_right.barh(names, counts, color="C0")
    ax_right.bar_label(bars, padding=3)  # 棒の先に値を書く
    ax_right.set_title("値の大きい順の横棒グラフ")
    ax_right.set_xlabel("回答数")
    ax_right.set_xlim(0, 50)

    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
