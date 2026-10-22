"""本文で使う図を matplotlib で生成するスクリプト。

conf.py から ``make_all()`` を呼び出し、ビルドのたびに図を出力する。
"""

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

# Windows 標準の日本語フォントを優先し、無い環境では他の日本語フォントを使う。
JAPANESE_FONTS = ["Meiryo", "Yu Gothic", "Noto Sans CJK JP", "IPAexGothic"]
_installed = {font.name for font in font_manager.fontManager.ttflist}
plt.rcParams["font.family"] = [name for name in JAPANESE_FONTS if name in _installed] + ["sans-serif"]

# 月の位置は「月 + 日 / 31」で表す。例えば 2 月 11 日は 2 + 11 / 31。
EARLY = 0.0
MID = 1 / 3
LATE = 2 / 3

CATEGORY_COLORS = {
    "花": "#d9668c",
    "紅葉": "#d9822b",
    "行事": "#3b78c2",
    "味覚": "#4c9a6a",
}


@dataclass(frozen=True)
class SeasonItem:
    """カレンダーに載せる見どころ 1 件分のデータ。"""

    label: str
    category: str
    start: float
    end: float


SEASON_ITEMS: list[SeasonItem] = [
    SeasonItem("偕楽園・弘道館の梅", "花", 2 + EARLY, 3 + LATE),
    SeasonItem("真壁のひなまつり", "行事", 2 + 4 / 31, 3 + 3 / 31),
    SeasonItem("水戸の梅まつり", "行事", 2 + 11 / 31, 3 + 22 / 31),
    SeasonItem("古河公方公園の花桃", "花", 3 + MID, 4 + LATE),
    SeasonItem("日立の桜", "花", 4 + EARLY, 4 + MID),
    SeasonItem("ネモフィラ", "花", 4 + MID, 5 + MID),
    SeasonItem("笠間の陶炎祭", "行事", 4 + 29 / 31, 5 + 5 / 31),
    SeasonItem("潮来あやめまつり", "行事", 5 + 22 / 31, 6 + 21 / 31),
    SeasonItem("コキアの紅葉", "紅葉", 10 + MID, 11 + EARLY),
    SeasonItem("袋田の滝・筑波山の紅葉", "紅葉", 11 + EARLY, 12 + EARLY),
    SeasonItem("花貫渓谷の紅葉", "紅葉", 11 + MID, 12 + EARLY),
    SeasonItem("土浦全国花火競技大会", "行事", 11 + 7 / 31, 11 + 8 / 31),
    SeasonItem("あんこう鍋の旬 (11 月から)", "味覚", 11 + EARLY, 13.0),
    SeasonItem("あんこう鍋の旬 (3 月まで)", "味覚", 1.0, 4.0),
]


def make_season_calendar(path: Path) -> None:
    """季節の見どころカレンダーを横棒グラフとして出力する。"""
    fig, ax = plt.subplots(figsize=(10, 6.4))

    labels = list(dict.fromkeys(item.label.split(" (")[0] for item in SEASON_ITEMS))
    rows = {label: index for index, label in enumerate(labels)}

    for item in SEASON_ITEMS:
        row = rows[item.label.split(" (")[0]]
        width = max(item.end - item.start, 0.08)
        ax.barh(row, width, left=item.start, height=0.6, color=CATEGORY_COLORS[item.category])

    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()

    ax.set_xlim(1, 13)
    ax.set_xticks([month + 0.5 for month in range(1, 13)])
    ax.set_xticklabels([f"{month} 月" for month in range(1, 13)])
    ax.set_xticks(range(1, 14), minor=True)
    ax.tick_params(axis="x", which="major", length=0)
    ax.grid(axis="x", which="minor", color="#cccccc", linewidth=0.8)
    ax.set_axisbelow(True)

    handles = [Patch(color=color, label=name) for name, color in CATEGORY_COLORS.items()]
    ax.legend(handles=handles, loc="lower left", ncols=len(handles), frameon=False, bbox_to_anchor=(0, -0.13))

    ax.set_title("茨城県の主な見どころカレンダー")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=110)
    plt.close(fig)


def make_all(output_dir: Path) -> None:
    """本文で使うすべての図を ``output_dir`` に出力する。"""
    make_season_calendar(output_dir / "season_calendar.png")


if __name__ == "__main__":
    make_all(Path(__file__).resolve().parent.parent / "_figures")
