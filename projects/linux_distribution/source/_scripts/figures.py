"""本文で使う matplotlib の図を生成する。

conf.py から ``generate()`` が呼び出され、ビルドの度に PNG を出力する。
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

# 日本語フォントの候補（先頭から順に、利用可能なものを使う）
FONT_FAMILY = ["Yu Gothic", "Meiryo", "Noto Sans CJK JP", "IPAexGothic"]

TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3df"
SURFACE = "#ffffff"

# 本文の基準日（情報の時点）
AS_OF = date(2026, 10, 23)

# 系統ごとの色（カテゴリ配色。順序は固定）
FAMILY_COLORS = {
    "Debian 系": "#2a78d6",
    "Red Hat 系": "#eb6834",
    "SUSE 系": "#1baf7a",
    "独立系": "#eda100",
}

# (名称, 系統, 開始年, 終了年 [継続中は None])
LIFESPANS: list[tuple[str, str, float, float | None]] = [
    ("Debian", "Debian 系", 1993.6, None),
    ("Ubuntu", "Debian 系", 2004.8, None),
    ("Linux Mint", "Debian 系", 2006.6, None),
    ("Red Hat Linux", "Red Hat 系", 1994.8, 2004.3),
    ("RHEL", "Red Hat 系", 2002.3, None),
    ("Fedora", "Red Hat 系", 2003.8, None),
    ("CentOS Linux", "Red Hat 系", 2004.4, 2024.5),
    ("Oracle Linux", "Red Hat 系", 2006.8, None),
    ("Amazon Linux", "Red Hat 系", 2010.9, None),
    ("CentOS Stream", "Red Hat 系", 2019.7, None),
    ("AlmaLinux", "Red Hat 系", 2021.2, None),
    ("Rocky Linux", "Red Hat 系", 2021.5, None),
    ("SUSE Linux", "SUSE 系", 1994.2, 2005.7),
    ("SLES", "SUSE 系", 2000.8, None),
    ("openSUSE", "SUSE 系", 2005.7, None),
    ("Slackware", "独立系", 1993.5, None),
    ("Gentoo", "独立系", 2002.2, None),
    ("Arch Linux", "独立系", 2002.2, None),
    ("Alpine Linux", "独立系", 2005.5, None),
]

# サポートの段階
STANDARD = "標準サポート"
MAINTENANCE = "保守サポート（セキュリティ修正中心）"
EXTENDED = "追加契約による延長サポート"

SUPPORT_COLORS = {
    STANDARD: "#1c5cab",
    MAINTENANCE: "#5b9be6",
    EXTENDED: "#b6d3f5",
}

# (名称, 公開日, [(段階, 終了日), ...])
SUPPORT_PERIODS: list[tuple[str, date, list[tuple[str, date]]]] = [
    ("Debian 13", date(2025, 8, 9),
     [(STANDARD, date(2028, 8, 9)), (MAINTENANCE, date(2030, 6, 30)), (EXTENDED, date(2035, 6, 30))]),
    ("Ubuntu 26.04 LTS", date(2026, 4, 23),
     [(STANDARD, date(2031, 5, 31)), (EXTENDED, date(2041, 5, 31))]),
    ("Linux Mint 22.3", date(2026, 1, 11),
     [(STANDARD, date(2029, 4, 30))]),
    ("RHEL 10", date(2025, 5, 20),
     [(STANDARD, date(2030, 5, 31)), (MAINTENANCE, date(2035, 5, 31)), (EXTENDED, date(2039, 5, 31))]),
    ("Fedora 44", date(2026, 4, 28),
     [(STANDARD, date(2027, 6, 2))]),
    ("CentOS Stream 10", date(2024, 12, 12),
     [(STANDARD, date(2030, 5, 31))]),
    ("Rocky Linux 10", date(2025, 6, 11),
     [(STANDARD, date(2030, 5, 31)), (MAINTENANCE, date(2035, 5, 31))]),
    ("AlmaLinux 10", date(2025, 5, 27),
     [(STANDARD, date(2030, 5, 31)), (MAINTENANCE, date(2035, 5, 31))]),
    ("Oracle Linux 10", date(2025, 6, 26),
     [(STANDARD, date(2035, 6, 30)), (EXTENDED, date(2038, 6, 30))]),
    ("Amazon Linux 2023", date(2023, 3, 15),
     [(STANDARD, date(2027, 6, 30)), (MAINTENANCE, date(2029, 6, 30))]),
    ("SLES 16", date(2025, 11, 4),
     [(STANDARD, date(2035, 11, 30)), (EXTENDED, date(2038, 11, 30))]),
    ("openSUSE Leap 16.0", date(2025, 10, 1),
     [(STANDARD, date(2027, 10, 31))]),
    ("Alpine Linux 3.24", date(2026, 6, 9),
     [(STANDARD, date(2028, 6, 1))]),
]


def _setup_style() -> None:
    available = {font.name for font in font_manager.fontManager.ttflist}
    families = [name for name in FONT_FAMILY if name in available] + ["sans-serif"]
    plt.rcParams.update({
        "font.family": families,
        "font.size": 10,
        "axes.edgecolor": GRID,
        "axes.labelcolor": TEXT_SECONDARY,
        "xtick.color": TEXT_SECONDARY,
        "ytick.color": TEXT_PRIMARY,
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
    })


def _plot_lifespans(path: Path) -> None:
    """主要ディストリビューションの存続期間を系統別の横棒で描く。"""
    now = AS_OF.year + (AS_OF.timetuple().tm_yday - 1) / 365
    fig, ax = plt.subplots(figsize=(10, 7.6))
    names = [row[0] for row in LIFESPANS]
    # 系統が変わる位置に隙間を空ける
    positions: list[float] = []
    y = 0.0
    for index, (_, family, _, _) in enumerate(LIFESPANS):
        if index > 0 and family != LIFESPANS[index - 1][1]:
            y += 0.6
        positions.append(y)
        y += 1.0
    for i, (_, family, start, end) in zip(positions, LIFESPANS):
        stop = now if end is None else end
        ax.barh(i, stop - start, left=start, height=0.6, color=FAMILY_COLORS[family],
                edgecolor=SURFACE, linewidth=2)
        ax.text(start - 0.3, i, f"{int(start)}", ha="right", va="center", fontsize=8, color=TEXT_SECONDARY)
        if end is not None:
            ax.text(stop + 0.3, i, f"{int(end)} 終了", ha="left", va="center", fontsize=8, color=TEXT_SECONDARY)

    ax.set_yticks(positions, names)
    ax.set_ylim(positions[-1] + 0.6, -1.4)
    ax.set_xlim(1990, 2028)
    ax.axvline(1991.7, color=TEXT_SECONDARY, linestyle=":", linewidth=1)
    ax.text(1991.9, -0.9, "1991 年 Linux 0.01 公開", fontsize=8, color=TEXT_SECONDARY, va="center")
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    ax.set_xlabel("西暦")
    handles = [Patch(facecolor=color, label=label) for label, color in FAMILY_COLORS.items()]
    ax.legend(handles=handles, loc="lower left", frameon=False, ncols=4, bbox_to_anchor=(0.0, 1.0))
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def _plot_support_periods(path: Path) -> None:
    """主要ディストリビューションの現行版のサポート期間を描く。"""
    fig, ax = plt.subplots(figsize=(10, 6.4))
    names = [row[0] for row in SUPPORT_PERIODS]
    for i, (_, released, phases) in enumerate(SUPPORT_PERIODS):
        start = released
        for phase, end in phases:
            left = float(mdates.date2num(start))
            width = float(mdates.date2num(end)) - left
            ax.barh(i, width, left=left, height=0.6, color=SUPPORT_COLORS[phase], edgecolor=SURFACE, linewidth=2)
            start = end
        ax.text(float(mdates.date2num(start)) + 60, i, f"{start.year}/{start.month:02d}", ha="left", va="center",
                fontsize=8, color=TEXT_SECONDARY)

    ax.set_yticks(range(len(names)), names)
    ax.set_ylim(len(names) - 0.4, -1.4)
    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.YearLocator(2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_xlim(float(mdates.date2num(date(2023, 1, 1))), float(mdates.date2num(date(2043, 1, 1))))
    as_of = float(mdates.date2num(AS_OF))
    ax.axvline(as_of, color=TEXT_PRIMARY, linestyle="--", linewidth=1)
    ax.text(as_of + 60, -0.9, "2026 年 10 月（本文書の時点）", fontsize=8, color=TEXT_PRIMARY, va="center")
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    handles = [Patch(facecolor=color, label=label) for label, color in SUPPORT_COLORS.items()]
    ax.legend(handles=handles, loc="lower left", frameon=False, ncols=3, bbox_to_anchor=(0.0, 1.0))
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def generate(out_dir: Path) -> None:
    """図をすべて生成して ``out_dir`` に保存する。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    _setup_style()
    _plot_lifespans(out_dir / "lifespans.png")
    _plot_support_periods(out_dir / "support_periods.png")


if __name__ == "__main__":
    generate(Path(__file__).resolve().parent.parent / "_generated")
