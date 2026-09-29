"""第 2 章: 基準色から配色パターンを生成する。

色相環上の位置関係 (補色・類似色・トライアド) を使って配色を作り、
色見本を ch02_color_scheme.png として保存します。
あわせて、配色比率 70:25:5 の見本 ch02_color_ratio.png も保存します。

実行例::

    python ch02_color_scheme.py --outdir output --base "#1f5fbf"
"""

from __future__ import annotations

import argparse
import colorsys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle

JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP"]


def use_japanese_font() -> None:
    """インストールされている日本語フォントを matplotlib に設定する。"""
    installed = {font.name for font in font_manager.fontManager.ttflist}
    available = [name for name in JAPANESE_FONTS if name in installed]
    plt.rcParams["font.family"] = available + ["sans-serif"]


def rotate_hue(color: str, degrees: float) -> str:
    """色相を degrees 度回転させた色を '#rrggbb' 形式で返す。

    HLS の明るさ (L) と彩度 (S) は元の色のまま保つ。
    ただし、知覚される明るさは色相によって変わる。
    """
    r, g, b = (int(color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, lightness, s = colorsys.rgb_to_hls(r, g, b)
    h = (h + degrees / 360) % 1.0
    r, g, b = colorsys.hls_to_rgb(h, lightness, s)
    return "#{:02x}{:02x}{:02x}".format(
        round(r * 255), round(g * 255), round(b * 255))


def make_schemes(base: str) -> dict[str, list[str]]:
    """配色パターンの名前と色のリストを返す。"""
    return {
        "補色": [base, rotate_hue(base, 180)],
        "類似色": [rotate_hue(base, -30), base, rotate_hue(base, 30)],
        "トライアド": [base, rotate_hue(base, 120), rotate_hue(base, 240)],
        "スプリット補色": [base, rotate_hue(base, 150),
                    rotate_hue(base, 210)],
    }


def draw_schemes(schemes: dict[str, list[str]], path: Path) -> None:
    """配色パターンごとに色見本を 1 行ずつ描画して保存する。"""
    row_step = 1.3  # 色見本の高さ 0.8 + 色コードの表示領域
    fig, ax = plt.subplots(figsize=(7, 1.1 * len(schemes)))
    for row, (name, colors) in enumerate(schemes.items()):
        y = (len(schemes) - 1 - row) * row_step
        ax.text(-0.1, y + 0.4, name, ha="right", va="center", fontsize=12)
        for col, color in enumerate(colors):
            ax.add_patch(Rectangle((col * 1.6, y), 1.5, 0.8, color=color))
            ax.text(col * 1.6 + 0.75, y - 0.1, color, ha="center",
                    va="top", fontsize=9)
    ax.set_xlim(-2.2, 5.0)
    ax.set_ylim(-0.5, len(schemes) * row_step)
    ax.axis("off")
    fig.savefig(path, dpi=100, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def draw_ratio(base: str, path: Path) -> None:
    """ベースカラー 70 %、メインカラー 25 %、アクセントカラー 5 % の見本。"""
    accent = rotate_hue(base, 180)
    fig, ax = plt.subplots(figsize=(7, 1.4))
    ax.barh(0, 70, left=0, color="#f4f5f7", edgecolor="#cccccc")
    ax.barh(0, 25, left=70, color=base)
    ax.barh(0, 5, left=95, color=accent)
    ax.text(35, 0, "ベースカラー 70 %", ha="center", va="center",
            fontsize=11, color="#222222")
    ax.text(82.5, 0, "メインカラー 25 %", ha="center", va="center",
            fontsize=10, color="white")
    # 5 % の帯は狭いので、ラベルは帯の外に置いて線で結ぶ
    ax.annotate("アクセントカラー 5 %", xy=(97.5, -0.4), xytext=(97.5, -0.9),
                ha="center", va="top", fontsize=11,
                arrowprops={"arrowstyle": "-", "color": "#555555"})
    ax.set_xlim(0, 100)
    ax.set_ylim(-1.5, 0.5)
    ax.axis("off")
    fig.savefig(path, dpi=100, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    parser.add_argument("--base", default="#1f5fbf",
                        help="基準色 ('#rrggbb' 形式)")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    use_japanese_font()
    schemes = make_schemes(args.base)
    for name, colors in schemes.items():
        print(f"{name}: {', '.join(colors)}")
    draw_schemes(schemes, outdir / "ch02_color_scheme.png")
    draw_ratio(args.base, outdir / "ch02_color_ratio.png")
    print(f"画像を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
