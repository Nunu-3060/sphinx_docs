"""本文で使う図（PNG）を生成する。

conf.py からビルド開始時に呼び出される。単体で実行すると source/_generated に図を出力する。
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

# 色（白い背景の上で読みやすい値）
SERIES_COLOR = "#2a78d6"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID_COLOR = "#e4e3df"
SURFACE_COLOR = "#ffffff"

# 日本語を表示できるフォント（Windows 標準のフォントを優先順に並べる）
FONT_CANDIDATES = [
    Path("C:/Windows/Fonts/YuGothM.ttc"),
    Path("C:/Windows/Fonts/meiryo.ttc"),
    Path("C:/Windows/Fonts/msgothic.ttc"),
]
BOLD_FONT_CANDIDATES = [
    Path("C:/Windows/Fonts/YuGothB.ttc"),
    Path("C:/Windows/Fonts/meiryob.ttc"),
]

DPI = 150


@dataclass(frozen=True)
class TimelineEvent:
    """年表の 1 つの出来事。"""

    year: int
    lane: int
    label: str
    offset: float


@dataclass(frozen=True)
class Brand:
    """香味の傾向図に載せる銘柄。"""

    name: str
    country: str
    body: float
    smoky: float
    dx: float
    dy: float


def _find_font(candidates: list[Path]) -> Path:
    """候補の中から最初に見つかったフォントファイルを返す。"""
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError("日本語フォントが見つからない: " + ", ".join(str(p) for p in candidates))


def _setup_matplotlib() -> None:
    """matplotlib で日本語を表示できるように設定する。"""
    font_path = _find_font(FONT_CANDIDATES)
    font_manager.fontManager.addfont(str(font_path))
    family = font_manager.FontProperties(fname=str(font_path)).get_name()
    plt.rcParams["font.family"] = family
    plt.rcParams["axes.edgecolor"] = GRID_COLOR
    plt.rcParams["axes.labelcolor"] = TEXT_SECONDARY
    plt.rcParams["xtick.color"] = TEXT_SECONDARY
    plt.rcParams["ytick.color"] = TEXT_SECONDARY
    plt.rcParams["text.color"] = TEXT_PRIMARY


def make_timeline(path: Path) -> None:
    """ウイスキーの歴史の年表を描く。"""
    lanes = ["スコットランド・\nアイルランド", "アメリカ", "日本"]
    events = [
        TimelineEvent(1494, 0, "1494 年\n最古の記録", 0.28),
        TimelineEvent(1725, 0, "1725 年\n麦芽税の強化", 0.28),
        TimelineEvent(1823, 0, "1823 年\n酒税法の改正", -0.30),
        TimelineEvent(1830, 0, "1830 年\n連続式蒸留機", 0.28),
        TimelineEvent(1860, 0, "1860 年\nブレンドの解禁", 0.75),
        TimelineEvent(1885, 0, "1860〜80 年代\nフィロキセラ禍", -0.30),
        TimelineEvent(1791, 1, "1791 年\nウイスキー税", 0.28),
        TimelineEvent(1920, 1, "1920 年\n禁酒法（〜1933 年）", 0.28),
        TimelineEvent(1964, 1, "1964 年\nバーボンを固有の製品に", -0.30),
        TimelineEvent(1923, 2, "1923 年\n山崎の建設開始", 0.28),
        TimelineEvent(1929, 2, "1929 年\n国産初の本格品", -0.30),
        TimelineEvent(1983, 2, "1983 年\n消費量のピーク", 0.28),
        TimelineEvent(2021, 2, "2021 年\n表示基準の制定", -0.30),
    ]

    fig, ax = plt.subplots(figsize=(11, 5.2), dpi=DPI)
    fig.patch.set_facecolor(SURFACE_COLOR)
    ax.set_facecolor(SURFACE_COLOR)

    x_min, x_max = 1470, 2045
    for lane in range(len(lanes)):
        y = len(lanes) - 1 - lane
        ax.hlines(y, x_min, x_max, color=GRID_COLOR, linewidth=2, zorder=1)

    for event in events:
        y = len(lanes) - 1 - event.lane
        ax.plot(event.year, y, "o", markersize=8, color=SERIES_COLOR,
                markeredgecolor=SURFACE_COLOR, markeredgewidth=2, zorder=3)
        ax.vlines(event.year, y, y + event.offset * 0.55, color=TEXT_SECONDARY, linewidth=0.8, zorder=2)
        va = "bottom" if event.offset > 0 else "top"
        ax.text(event.year, y + event.offset * 0.6, event.label, ha="center", va=va, fontsize=9,
                color=TEXT_PRIMARY, linespacing=1.3)

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-0.75, len(lanes) - 0.05)
    ax.set_yticks(range(len(lanes)))
    ax.set_yticklabels(list(reversed(lanes)), fontsize=10)
    ax.set_xticks(range(1500, 2050, 50))
    ax.tick_params(axis="x", labelsize=9, length=0)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=GRID_COLOR, linewidth=0.6)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xlabel("年", fontsize=10)

    fig.tight_layout()
    fig.savefig(path, facecolor=SURFACE_COLOR)
    plt.close(fig)


def make_flavor_map(path: Path) -> None:
    """主な銘柄の香味の傾向を 2 軸の図に描く。"""
    brands = [
        Brand("ザ・グレンリベット 12 年", "スコッチ", 2.6, 0.8, 0.0, -0.55),
        Brand("グレンフィディック 12 年", "スコッチ", 3.4, 1.6, 0.0, 0.45),
        Brand("ザ・マッカラン 12 年\nシェリーオーク", "スコッチ", 8.4, 1.4, 0.0, 0.45),
        Brand("タリスカー 10 年", "スコッチ", 6.4, 6.6, 0.0, 0.45),
        Brand("ラフロイグ 10 年", "スコッチ", 7.6, 9.0, 0.0, 0.45),
        Brand("ジョニーウォーカー\nブラックラベル 12 年", "スコッチ", 5.8, 4.4, 0.0, 0.45),
        Brand("バランタイン ファイネスト", "スコッチ", 2.2, 2.9, 0.0, 0.45),
        Brand("ジェムソン", "アイリッシュ", 1.2, 0.4, 0.0, 0.45),
        Brand("メーカーズマーク", "アメリカン", 6.0, 0.4, -0.2, -0.55),
        Brand("ワイルドターキー 8 年", "アメリカン", 8.2, 0.4, 0.0, -0.55),
        Brand("カナディアンクラブ", "カナディアン", 0.6, 1.4, 0.4, 0.45),
        Brand("山崎", "ジャパニーズ", 6.6, 1.6, -0.1, 0.45),
        Brand("白州", "ジャパニーズ", 3.6, 3.6, 0.0, 0.45),
        Brand("響 JAPANESE HARMONY", "ジャパニーズ", 4.6, 0.6, 0.0, 0.45),
        Brand("余市", "ジャパニーズ", 7.2, 5.6, 0.0, -0.6),
    ]
    markers = {
        "スコッチ": "o",
        "アイリッシュ": "D",
        "アメリカン": "s",
        "カナディアン": "v",
        "ジャパニーズ": "^",
    }

    fig, ax = plt.subplots(figsize=(10, 7.2), dpi=DPI)
    fig.patch.set_facecolor(SURFACE_COLOR)
    ax.set_facecolor(SURFACE_COLOR)

    for country, marker in markers.items():
        group = [b for b in brands if b.country == country]
        ax.scatter([b.body for b in group], [b.smoky for b in group], marker=marker, s=80,
                   color=SERIES_COLOR, edgecolors=SURFACE_COLOR, linewidths=2, zorder=3, label=country)
    for brand in brands:
        va = "bottom" if brand.dy > 0 else "top"
        ax.text(brand.body + brand.dx, brand.smoky + brand.dy * 0.5, brand.name, ha="center", va=va,
                fontsize=9, color=TEXT_PRIMARY, linespacing=1.2, zorder=4)

    ax.axhline(5, color=GRID_COLOR, linewidth=1, zorder=1)
    ax.axvline(5, color=GRID_COLOR, linewidth=1, zorder=1)
    ax.set_xlim(-0.6, 10.2)
    ax.set_ylim(-0.9, 10.2)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)
    ax.set_xlabel("軽快　←　ボディ（味わいの重さ）　→　重厚", fontsize=11)
    ax.set_ylabel("穏やか　←　スモーキーさ　→　強い", fontsize=11)
    ax.legend(loc="upper left", fontsize=9, frameon=False, labelcolor=TEXT_SECONDARY)

    fig.tight_layout()
    fig.savefig(path, facecolor=SURFACE_COLOR)
    plt.close(fig)


def make_abv_chart(path: Path) -> None:
    """飲み方ごとのアルコール度数の目安を棒グラフに描く。"""
    whisky_abv = 40.0
    # (飲み方, ウイスキー 1 に対する割り材の量)
    styles = [
        ("ストレート", 0.0),
        ("トワイスアップ（1：1）", 1.0),
        ("水割り（1：2.5）", 2.5),
        ("ハイボール（1：4）", 4.0),
    ]
    names = [name for name, _ in styles]
    values = [whisky_abv / (1.0 + ratio) for _, ratio in styles]

    fig, ax = plt.subplots(figsize=(8, 3.6), dpi=DPI)
    fig.patch.set_facecolor(SURFACE_COLOR)
    ax.set_facecolor(SURFACE_COLOR)

    positions = list(range(len(names)))
    ax.barh(positions, values, height=0.6, color=SERIES_COLOR, zorder=3)
    for pos, value in zip(positions, values):
        ax.text(value + 0.6, pos, f"{value:.1f} %", va="center", fontsize=10, color=TEXT_PRIMARY)

    ax.set_yticks(positions)
    ax.set_yticklabels(names, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlim(0, 46)
    ax.set_xlabel("アルコール度数（%）", fontsize=10)
    ax.tick_params(length=0)
    ax.grid(axis="x", color=GRID_COLOR, linewidth=0.6)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.tight_layout()
    fig.savefig(path, facecolor=SURFACE_COLOR)
    plt.close(fig)


def make_label(path: Path) -> None:
    """ラベルの読み方を説明するための架空のラベルを描く。"""
    scale = 2
    width, height = 560 * scale, 600 * scale
    image = Image.new("RGB", (width, height), SURFACE_COLOR)
    draw = ImageDraw.Draw(image)

    regular = _find_font(FONT_CANDIDATES)
    bold = _find_font(BOLD_FONT_CANDIDATES)

    # ラベルの台紙
    left, top, right, bottom = 70 * scale, 20 * scale, 540 * scale, 580 * scale
    draw.rectangle((left, top, right, bottom), fill="#f6efdf", outline="#8a6d3b", width=3 * scale)
    draw.rectangle((left + 10 * scale, top + 10 * scale, right - 10 * scale, bottom - 10 * scale),
                   outline="#b8995f", width=1 * scale)

    # (番号, 文字列, 文字の大きさ, 太字かどうか, 縦位置)
    lines = [
        (1, "THE GLEN SAMPLE", 34, True, 80),
        (2, "SINGLE MALT SCOTCH WHISKY", 20, True, 160),
        (3, "AGED 12 YEARS", 26, True, 235),
        (4, "MATURED IN BOURBON & SHERRY CASKS", 15, False, 315),
        (5, "NON CHILL-FILTERED", 15, False, 380),
        (6, "DISTILLED AND BOTTLED IN SCOTLAND", 15, False, 445),
        (7, "700 ml        46 % vol", 18, False, 515),
    ]
    center_x = (left + right) // 2
    for number, text, size, is_bold, y in lines:
        font = ImageFont.truetype(str(bold if is_bold else regular), size * scale)
        draw.text((center_x, y * scale), text, font=font, fill="#3b2a12", anchor="mm")

        # 番号付きの丸印を左側に置く
        cx, cy, r = 38 * scale, y * scale, 18 * scale
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=SERIES_COLOR)
        number_font = ImageFont.truetype(str(bold), 18 * scale)
        draw.text((cx, cy), str(number), font=number_font, fill=SURFACE_COLOR, anchor="mm")
        draw.line((cx + r, cy, left + 2 * scale, cy), fill=SERIES_COLOR, width=2 * scale)

    image.save(path)


def generate_all(out_dir: Path) -> None:
    """すべての図を out_dir に出力する。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    _setup_matplotlib()
    make_timeline(out_dir / "history_timeline.png")
    make_flavor_map(out_dir / "flavor_map.png")
    make_abv_chart(out_dir / "abv_by_style.png")
    make_label(out_dir / "label_example.png")


if __name__ == "__main__":
    generate_all(Path(__file__).resolve().parent.parent / "_generated")
