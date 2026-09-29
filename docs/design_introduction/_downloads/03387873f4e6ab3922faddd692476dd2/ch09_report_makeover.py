"""第 9 章: 月次報告の 1 枚資料を、本書で学んだ原則に沿って作り直す。

* ch09_report_before.png: 改善前 (円グラフ・多色・要点が不明)
* ch09_report_after.png: 改善後 (結論・指標カード・強調色 1 色)

実行例::

    python ch09_report_makeover.py --outdir output
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager
from matplotlib.axes import Axes
from matplotlib.patches import FancyBboxPatch

JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP"]

PRIMARY = "#1f5fbf"
MUTED = "#949494"
TEXT = "#222222"
SUBTEXT = "#555555"
SURFACE = "#f4f5f7"
GOOD = "#1e7b34"


@dataclass(frozen=True)
class Kpi:
    """指標カードに表示する値。"""

    name: str
    value: str
    change: str  # 前月からの変化
    is_good: bool  # 望ましい方向に変化したか (False なら強調しない)


KPIS = [
    Kpi("売上", "1.24 億円", "前月比 +8 %", True),
    Kpi("受注件数", "312 件", "前月比 +3 %", True),
    Kpi("解約率", "2.1 %", "前月差 −0.4 pt", True),
    Kpi("顧客満足度", "4.2 / 5", "前月差 ±0", False),
]

REGION_SALES = pd.Series(
    {"東日本": 4.1, "西日本": 3.2, "中部": 2.3, "九州": 1.6, "北海道": 1.2},
    name="売上 (千万円)")

MONTHLY_SALES = pd.Series(
    [1.02, 1.05, 1.01, 1.08, 1.10, 1.07, 1.12, 1.15, 1.24],
    index=[f"{m} 月" for m in range(1, 10)], name="売上 (億円)")


def use_japanese_font() -> None:
    """インストールされている日本語フォントを matplotlib に設定する。"""
    installed = {font.name for font in font_manager.fontManager.ttflist}
    available = [name for name in JAPANESE_FONTS if name in installed]
    plt.rcParams["font.family"] = available + ["sans-serif"]


def draw_before(path: Path) -> None:
    """改善前: 情報は同じだが、何を読み取ればよいかが分からない。"""
    fig = plt.figure(figsize=(10, 6))
    fig.suptitle("2026 年 9 月 月次報告書", fontsize=14)

    ax_pie = fig.add_subplot(2, 2, 1)
    ax_pie.pie(REGION_SALES, labels=REGION_SALES.index, autopct="%1.1f%%",
               explode=[0.05] * len(REGION_SALES), shadow=True,
               startangle=90)
    ax_pie.set_title("地域別売上")

    ax_bar = fig.add_subplot(2, 2, 2)
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    ax_bar.bar(MONTHLY_SALES.index, MONTHLY_SALES, color=colors[:9])
    ax_bar.set_title("月別売上")
    ax_bar.grid(True)
    ax_bar.tick_params(axis="x", rotation=90)

    ax_table = fig.add_subplot(2, 1, 2)
    ax_table.axis("off")
    ax_table.table(cellText=[[k.name, k.value, k.change] for k in KPIS],
                   colLabels=["項目", "値", "変化"], loc="center")
    fig.savefig(path, dpi=100, facecolor="white")
    plt.close(fig)


def draw_kpi_card(ax: Axes, kpi: Kpi) -> None:
    """指標カードを 1 枚描く。数値を最も大きく表示する。"""
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,"
                                "rounding_size=0.06", facecolor=SURFACE,
                                edgecolor="none", transform=ax.transAxes))
    ax.text(0.08, 0.78, kpi.name, fontsize=11, color=SUBTEXT,
            transform=ax.transAxes)
    ax.text(0.08, 0.40, kpi.value, fontsize=18, fontweight="bold",
            color=TEXT, transform=ax.transAxes)
    ax.text(0.08, 0.14, kpi.change, fontsize=10,
            color=GOOD if kpi.is_good else SUBTEXT, transform=ax.transAxes)


def draw_after(path: Path) -> None:
    """改善後: 結論 → 指標 → 根拠の順に、上から下へ読める構成。"""
    fig = plt.figure(figsize=(10, 6))
    grid = fig.add_gridspec(3, 4, height_ratios=[0.5, 0.9, 2.6],
                            left=0.06, right=0.97, top=0.95, bottom=0.08,
                            hspace=0.45, wspace=0.25)

    ax_head = fig.add_subplot(grid[0, :])
    ax_head.axis("off")
    ax_head.text(0, 0.75, "2026 年 9 月 月次報告", fontsize=11,
                 color=SUBTEXT, transform=ax_head.transAxes)
    ax_head.text(0, 0.05, "売上は前月比 8 % 増。東日本が全体の 3 分の 1 を占める",
                 fontsize=22, fontweight="bold", color=TEXT,
                 transform=ax_head.transAxes)

    for i, kpi in enumerate(KPIS):
        draw_kpi_card(fig.add_subplot(grid[1, i]), kpi)

    # 構成比を比べる場合も、円グラフより並べ替えた棒グラフの方が読みやすい
    ax_region = fig.add_subplot(grid[2, :2])
    region = REGION_SALES.sort_values()
    colors = [PRIMARY if name == "東日本" else MUTED for name in region.index]
    ax_region.barh(region.index, region, color=colors, height=0.6)
    for y, value in enumerate(region):
        ax_region.text(value + 0.05, y, f"{value:.1f}", va="center",
                       fontsize=10, color=SUBTEXT)
    ax_region.set_title("地域別売上 (千万円)", loc="left", fontsize=12)

    ax_month = fig.add_subplot(grid[2, 2:])
    x = range(len(MONTHLY_SALES))
    ax_month.plot(x, MONTHLY_SALES, color=PRIMARY, linewidth=2.5)
    ax_month.scatter([x[-1]], [MONTHLY_SALES.iloc[-1]], color=PRIMARY,
                     zorder=3)
    ax_month.annotate(f"{MONTHLY_SALES.iloc[-1]:.2f}", (x[-1],
                      MONTHLY_SALES.iloc[-1]), xytext=(-8, 8),
                      textcoords="offset points", ha="right",
                      color=PRIMARY, fontweight="bold")
    ax_month.set_xticks(list(x)[::2], MONTHLY_SALES.index[::2])
    ax_month.set_ylim(0.9, 1.3)
    ax_month.set_title("月別売上 (億円)", loc="left", fontsize=12)
    ax_month.grid(axis="y", color="#e5e5e5")

    for ax in (ax_region, ax_month):
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.tick_params(colors=SUBTEXT, length=0)
    ax_region.spines["bottom"].set_visible(False)
    ax_region.set_xticks([])
    fig.savefig(path, dpi=100, facecolor="white")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    use_japanese_font()
    draw_before(outdir / "ch09_report_before.png")
    draw_after(outdir / "ch09_report_after.png")
    print(f"画像を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
