"""第 8 章: デザイントークンを定義し、matplotlib と tkinter の両方に適用する。

色・余白・文字の大きさを 1 か所で定義しておくと、グラフと UI の見た目を
まとめて揃えられます。次の画像を保存します。

* ch08_token_sheet.png: トークンの一覧 (色見本と余白の段階)
* ch08_token_chart.png: トークンを適用したグラフ

実行例::

    python ch08_design_tokens.py --outdir output
    python ch08_design_tokens.py --show-ui   # tkinter の画面も表示する
"""

from __future__ import annotations

import argparse
import tkinter as tk
from dataclasses import dataclass, field, fields
from pathlib import Path
from tkinter import ttk

import matplotlib.pyplot as plt
from cycler import cycler
from matplotlib import font_manager
from matplotlib.patches import Rectangle


@dataclass(frozen=True)
class ColorTokens:
    """用途ごとの色。値ではなく用途で名前を付ける。"""

    primary: str = "#1f5fbf"  # 主要な操作・強調するデータ
    text: str = "#222222"  # 本文
    subtext: str = "#555555"  # 補足・軸ラベル
    muted: str = "#949494"  # 強調しないデータ (白地と 3 : 1)
    border: str = "#d0d4db"  # 枠線・区切り線
    surface: str = "#f4f5f7"  # カードなどの背景
    background: str = "#ffffff"  # ページの背景
    error: str = "#c0392b"  # エラー
    success: str = "#1e7b34"  # 成功


@dataclass(frozen=True)
class SpaceTokens:
    """余白の段階。すべて基本単位 unit の倍数にする。"""

    unit: int = 8

    def __call__(self, steps: float) -> int:
        """unit の steps 倍の余白 (px) を返す。"""
        return round(self.unit * steps)


@dataclass(frozen=True)
class TypeTokens:
    """文字の大きさ (pt) と、使用するフォントの候補。"""

    families: tuple[str, ...] = ("Yu Gothic", "Meiryo", "Hiragino Sans",
                                 "Noto Sans CJK JP")
    small: int = 9
    body: int = 10
    heading: int = 13
    title: int = 16


@dataclass(frozen=True)
class DesignTokens:
    """デザイントークン一式。"""

    color: ColorTokens = field(default_factory=ColorTokens)
    space: SpaceTokens = field(default_factory=SpaceTokens)
    type: TypeTokens = field(default_factory=TypeTokens)

    def font_family(self) -> list[str]:
        """フォントの候補のうち、インストールされているものを返す。"""
        installed = {font.name for font in font_manager.fontManager.ttflist}
        found = [name for name in self.type.families if name in installed]
        return found + ["sans-serif"]


TOKENS = DesignTokens()


def apply_to_matplotlib(tokens: DesignTokens) -> None:
    """トークンを matplotlib の rcParams に反映する。"""
    c = tokens.color
    plt.rcParams.update({
        "font.family": tokens.font_family(),
        "font.size": tokens.type.body,
        "text.color": c.text,
        "figure.facecolor": c.background,
        "axes.facecolor": c.background,
        "axes.edgecolor": c.border,
        "axes.labelcolor": c.subtext,
        "axes.titlesize": tokens.type.heading,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.prop_cycle": cycler(color=[c.primary, c.muted]),
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": c.border,
        "grid.linewidth": 0.6,
        "xtick.color": c.subtext,
        "ytick.color": c.subtext,
        "legend.frameon": False,
    })


def apply_to_tkinter(root: tk.Tk, tokens: DesignTokens) -> ttk.Style:
    """トークンを tkinter (ttk) のスタイルに反映する。"""
    c = tokens.color
    family = tokens.font_family()[0]
    style = ttk.Style(root)
    style.theme_use("clam")
    root.configure(background=c.background)
    style.configure(".", background=c.background, foreground=c.text,
                    font=(family, tokens.type.body))
    style.configure("Title.TLabel", font=(family, tokens.type.title, "bold"))
    style.configure("Sub.TLabel", foreground=c.subtext,
                    font=(family, tokens.type.small))
    style.configure("TButton", padding=(tokens.space(2), tokens.space(0.5)))
    style.configure("Primary.TButton", background=c.primary,
                    foreground=c.background, bordercolor=c.primary)
    return style


def draw_token_sheet(tokens: DesignTokens, path: Path) -> None:
    """色トークンの見本と、余白の段階を 1 枚の画像にする。"""
    colors = [(f.name, str(getattr(tokens.color, f.name)))
              for f in fields(tokens.color)]
    fig, (ax_color, ax_space) = plt.subplots(
        1, 2, figsize=(9, 3.6), gridspec_kw={"width_ratios": [3, 2]})

    for i, (name, value) in enumerate(colors):
        x, y = (i % 3) * 1.1, 2 - (i // 3) * 1.1
        ax_color.add_patch(Rectangle((x, y), 1.0, 0.6, facecolor=value,
                                     edgecolor=tokens.color.border))
        ax_color.text(x, y - 0.08, f"{name}\n{value}", va="top",
                      fontsize=tokens.type.small)
    ax_color.set_xlim(-0.05, 3.3)
    ax_color.set_ylim(-0.6, 2.7)
    ax_color.set_title("color")
    ax_color.axis("off")

    steps = [0.5, 1, 2, 3, 4, 6]
    for i, step in enumerate(steps):
        px = tokens.space(step)
        ax_space.barh(i, px, color=tokens.color.primary, height=0.5)
        ax_space.text(px + 1, i, f"space({step:g}) = {px} px", va="center",
                      fontsize=tokens.type.small)
    ax_space.set_xlim(0, 90)
    ax_space.invert_yaxis()
    ax_space.set_title("space")
    ax_space.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=100)
    plt.close(fig)


def draw_chart(tokens: DesignTokens, path: Path) -> None:
    """トークンを適用した棒グラフ。強調する棒だけを primary にする。"""
    departments = ["開発部", "営業部", "総務部", "企画部", "品質保証部"]
    overtime = [21.5, 14.2, 8.3, 12.9, 10.4]
    focus = "開発部"
    colors = [tokens.color.primary if d == focus else tokens.color.muted
              for d in departments]

    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.barh(departments, overtime, color=colors, height=0.6)
    ax.invert_yaxis()
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("月平均の残業時間 (時間)")
    ax.set_title(f"{focus}の残業時間が突出している")
    for i, value in enumerate(overtime):
        ax.text(value + 0.3, i, f"{value:.1f}", va="center",
                fontsize=tokens.type.small, color=tokens.color.subtext)
    fig.tight_layout()
    fig.savefig(path, dpi=100)
    plt.close(fig)


def show_ui(tokens: DesignTokens) -> None:
    """同じトークンを適用した tkinter の画面を表示する。"""
    root = tk.Tk()
    root.title("デザイントークンの適用例")
    apply_to_tkinter(root, tokens)
    frame = ttk.Frame(root, padding=tokens.space(3))
    frame.pack(fill="both", expand=True)
    ttk.Label(frame, text="残業時間の集計", style="Title.TLabel").pack(
        anchor="w")
    ttk.Label(frame, text="グラフと同じ色・余白・文字の大きさを使っています。",
              style="Sub.TLabel").pack(anchor="w", pady=(0, tokens.space(2)))
    ttk.Button(frame, text="集計する", style="Primary.TButton",
               command=root.destroy).pack(anchor="e")
    root.mainloop()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    parser.add_argument("--show-ui", action="store_true",
                        help="トークンを適用した tkinter の画面を表示する")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    apply_to_matplotlib(TOKENS)
    draw_token_sheet(TOKENS, outdir / "ch08_token_sheet.png")
    draw_chart(TOKENS, outdir / "ch08_token_chart.png")
    print(f"画像を {outdir} に保存しました。")
    if args.show_ui:
        show_ui(TOKENS)


if __name__ == "__main__":
    main()
