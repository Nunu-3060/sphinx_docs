"""本文で使用する図を matplotlib で生成する。

conf.py から generate() を呼び出し、ビルドのたびに図を出力する。
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Polygon, Rectangle  # noqa: E402

plt.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "sans-serif"]

DPI = 150


def make_diataxis(path: Path) -> None:
    """Diátaxis の 4 象限の図を出力する。"""
    fig, ax = plt.subplots(figsize=(8, 6.4))
    quadrants = [
        # (x, y, 色, 名前, 性質, 例)
        (0, 1, "#dbe9f6", "チュートリアル", "学習志向", "例：はじめての○○"),
        (1, 1, "#dff0d8", "ハウツーガイド", "課題志向", "例：○○を設定する"),
        (0, 0, "#fcf3cf", "解説", "理解志向", "例：○○の設計思想"),
        (1, 0, "#f9e0e0", "リファレンス", "情報志向", "例：API リファレンス"),
    ]
    for x, y, color, name, nature, example in quadrants:
        ax.add_patch(Rectangle((x, y), 1, 1, facecolor=color, edgecolor="#555555", linewidth=1.5))
        ax.text(x + 0.5, y + 0.62, name, ha="center", va="center", fontsize=17, fontweight="bold")
        ax.text(x + 0.5, y + 0.42, nature, ha="center", va="center", fontsize=12)
        ax.text(x + 0.5, y + 0.25, example, ha="center", va="center", fontsize=10.5, color="#444444")

    ax.text(1, 2.08, "行動（手を動かす）", ha="center", va="bottom", fontsize=12)
    ax.text(1, -0.08, "認識（理解する）", ha="center", va="top", fontsize=12)
    ax.text(-0.05, 1, "習得\n（学ぶとき）", ha="right", va="center", fontsize=12)
    ax.text(2.05, 1, "適用\n（仕事を\nするとき）", ha="left", va="center", fontsize=12)

    ax.set_xlim(-0.45, 2.45)
    ax.set_ylim(-0.3, 2.3)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def make_inverted_pyramid(path: Path) -> None:
    """逆ピラミッド型の構成の図を出力する。"""
    fig, ax = plt.subplots(figsize=(9, 4.6))
    # 上辺の幅 6、高さ 3 の逆三角形を 3 段に分ける
    bands = [
        (3.0, 2.0, "#2e6da4", "white", "結論", "読者が最初に知るべきこと"),
        (2.0, 1.0, "#7aa6d6", "black", "根拠・重要な詳細", "結論を支える事実やデータ"),
        (1.0, 0.0, "#d6e4f2", "black", "補足・背景", "必要な読者だけが読む情報"),
    ]
    for top, bottom, color, text_color, title, note in bands:
        # 中心から左右の端までの距離は高さと等しい
        polygon = Polygon(
            [(-top, top), (top, top), (bottom, bottom), (-bottom, bottom)],
            closed=True, facecolor=color, edgecolor="white", linewidth=2,
        )
        ax.add_patch(polygon)
        center = (top + bottom) / 2
        # 最下段は先端が細いため、文字を上寄せにして小さくする
        is_tip = bottom == 0.0
        title_y = center + 0.18 if is_tip else center
        fontsize = 12 if is_tip else 14
        ax.text(0, title_y, title, ha="center", va="center", fontsize=fontsize, fontweight="bold", color=text_color)
        ax.text(3.4, title_y, note, ha="left", va="center", fontsize=11)
        ax.plot([title_y + 0.3, 3.3], [title_y, title_y], color="#999999", linewidth=1, linestyle=":")

    arrow = FancyArrowPatch(
        (-3.6, 3.0), (-3.6, 0.1), arrowstyle="-|>", mutation_scale=20, linewidth=1.5, color="#555555",
    )
    ax.add_patch(arrow)
    ax.text(-3.75, 2.9, "重要度：高", ha="right", va="center", fontsize=11)
    ax.text(-3.75, 0.2, "重要度：低", ha="right", va="center", fontsize=11)
    ax.text(0, 3.15, "文書の先頭", ha="center", va="bottom", fontsize=11, color="#555555")

    ax.set_xlim(-5.4, 6.6)
    ax.set_ylim(-0.2, 3.5)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def generate(output_dir: Path) -> None:
    """すべての図を output_dir に出力する。"""
    output_dir.mkdir(parents=True, exist_ok=True)
    make_diataxis(output_dir / "diataxis.png")
    make_inverted_pyramid(output_dir / "inverted_pyramid.png")
