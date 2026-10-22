"""本文で使う図（matplotlib）を生成するスクリプト.

conf.py から ``generate(output_dir)`` が呼ばれ、ビルドのたびに図を作り直す。
単体で ``python make_figures.py <出力ディレクトリ>`` として実行することもできる。
"""

import sys
from pathlib import Path
from typing import NamedTuple

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402  (バックエンドの指定後に読み込む必要がある)
from matplotlib.lines import Line2D  # noqa: E402


class Language(NamedTuple):
    """年表に載せる言語."""

    name: str
    year: int
    category: str


CATEGORY_COLORS: dict[str, str] = {
    "歴史的な言語": "#8c8c8c",
    "システム": "#1f6fb2",
    "アプリケーション": "#2a9d55",
    "スクリプト・Web": "#d9822b",
    "データベース": "#8e44ad",
}

LANGUAGES: list[Language] = [
    Language("FORTRAN", 1957, "歴史的な言語"),
    Language("LISP", 1958, "歴史的な言語"),
    Language("COBOL", 1959, "歴史的な言語"),
    Language("ALGOL 60", 1960, "歴史的な言語"),
    Language("Simula 67", 1967, "歴史的な言語"),
    Language("Pascal", 1970, "歴史的な言語"),
    Language("C", 1972, "システム"),
    Language("Smalltalk", 1972, "歴史的な言語"),
    Language("ML", 1973, "歴史的な言語"),
    Language("SQL", 1974, "データベース"),
    Language("C++", 1983, "システム"),
    Language("Objective-C", 1984, "歴史的な言語"),
    Language("Erlang", 1986, "歴史的な言語"),
    Language("Perl", 1987, "歴史的な言語"),
    Language("Haskell", 1990, "歴史的な言語"),
    Language("Python", 1991, "スクリプト・Web"),
    Language("Java", 1995, "アプリケーション"),
    Language("JavaScript", 1995, "スクリプト・Web"),
    Language("PHP", 1995, "スクリプト・Web"),
    Language("Ruby", 1995, "スクリプト・Web"),
    Language("C#", 2000, "アプリケーション"),
    Language("Go", 2009, "システム"),
    Language("Rust", 2010, "システム"),
    Language("Kotlin", 2011, "アプリケーション"),
    Language("TypeScript", 2012, "スクリプト・Web"),
    Language("Swift", 2014, "アプリケーション"),
]


def make_timeline(path: Path) -> None:
    """言語の登場年を示す年表を描いて保存する."""
    plt.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "sans-serif"]
    fig, ax = plt.subplots(figsize=(10, 8), dpi=120)

    for row, lang in enumerate(LANGUAGES):
        color = CATEGORY_COLORS[lang.category]
        ax.hlines(row, 1950, lang.year, colors="#e0e0e0", linewidth=1, zorder=1)
        ax.scatter(lang.year, row, s=60, color=color, zorder=2)
        ax.text(lang.year + 0.8, row, f"{lang.name}（{lang.year}）", va="center", fontsize=10)

    ax.set_xlim(1950, 2030)
    ax.set_ylim(len(LANGUAGES), -1)
    ax.set_yticks([])
    ax.set_xlabel("登場年")
    ax.set_xticks(range(1950, 2031, 10))
    ax.grid(axis="x", color="#d0d0d0", linewidth=0.5)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)

    handles = [
        Line2D([0], [0], marker="o", linestyle="", color=color, label=category)
        for category, color in CATEGORY_COLORS.items()
    ]
    ax.legend(handles=handles, loc="upper right", frameon=False)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def generate(output_dir: Path) -> None:
    """すべての図を output_dir に生成する."""
    output_dir.mkdir(parents=True, exist_ok=True)
    make_timeline(output_dir / "timeline.png")


if __name__ == "__main__":
    generate(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("."))
