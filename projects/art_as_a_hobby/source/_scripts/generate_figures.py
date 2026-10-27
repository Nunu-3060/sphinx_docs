"""本文で使う図を生成する.

Sphinx のビルド開始時に conf.py から main() が呼び出される。
単独で実行しても図を生成できる。
"""

import colorsys
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).resolve().parent.parent / "images"

FONT_PATHS = [
    "C:/Windows/Fonts/meiryo.ttc",
    "C:/Windows/Fonts/YuGothM.ttc",
]

plt.switch_backend("Agg")  # 画面に表示せず、ファイルにだけ描画する
plt.rcParams["font.family"] = ["Meiryo", "Yu Gothic", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """日本語を表示できるフォントを読み込む. 見つからなければ既定のフォントを使う."""
    for path in FONT_PATHS:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def hue_to_rgb(hue_deg: float) -> tuple[int, int, int]:
    """色相 [度] を、彩度・明度が最大の RGB に変換する."""
    r, g, b = colorsys.hsv_to_rgb(hue_deg / 360.0, 1.0, 1.0)
    return int(r * 255), int(g * 255), int(b * 255)


def fig_color_wheel() -> None:
    """12 色の色相環と補色の関係."""
    size = 560
    center = size / 2
    outer = 220
    inner = 110
    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)
    font = load_font(18)

    # 赤を真上に置き、時計回りに 30 度ずつ色相を変える
    for i in range(12):
        hue = i * 30
        start = -90 + hue - 15
        draw.pieslice(
            (center - outer, center - outer, center + outer, center + outer),
            start, start + 30, fill=hue_to_rgb(hue), outline="white", width=3,
        )
    draw.ellipse((center - inner, center - inner, center + inner, center + inner), fill="white")

    # 補色の組（向かい合う色）を線で結ぶ
    for hue in (0, 60, 120):
        rad = math.radians(-90 + hue)
        x1 = center + inner * 0.95 * math.cos(rad)
        y1 = center + inner * 0.95 * math.sin(rad)
        x2 = center - inner * 0.95 * math.cos(rad)
        y2 = center - inner * 0.95 * math.sin(rad)
        draw.line((x1, y1, x2, y2), fill=(90, 90, 90), width=2)
    draw.text((center, center), "補色", fill="black", font=font, anchor="mm",
              stroke_width=4, stroke_fill="white")

    labels = {0: "赤", 60: "黄", 120: "緑", 180: "青緑", 240: "青", 300: "赤紫"}
    for hue, label in labels.items():
        rad = math.radians(-90 + hue)
        x = center + (outer + 25) * math.cos(rad)
        y = center + (outer + 25) * math.sin(rad)
        draw.text((x, y), label, fill="black", font=font, anchor="mm")
    img.save(OUT_DIR / "color_wheel.png")


def fig_composition() -> None:
    """代表的な 3 つの構図（三分割法、日の丸構図、対角線構図）."""
    panel_w, panel_h = 300, 200
    margin = 20
    title_h = 40
    width = panel_w * 3 + margin * 4
    height = panel_h + title_h + margin * 2
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    font = load_font(18)
    sky = (205, 228, 245)
    ground = (196, 222, 180)
    subject = (220, 80, 60)
    guide = (90, 90, 90)
    titles = ["三分割法", "日の丸構図", "対角線構図"]

    for i, title in enumerate(titles):
        left = margin + i * (panel_w + margin)
        top = margin + title_h
        right = left + panel_w
        bottom = top + panel_h
        draw.text((left + panel_w / 2, margin + title_h / 2), title, fill="black", font=font, anchor="mm")

        if i == 0:
            # 地平線を下の 1/3 の線に、主題を交点に置く
            horizon = top + panel_h * 2 / 3
            draw.rectangle((left, top, right, horizon), fill=sky)
            draw.rectangle((left, horizon, right, bottom), fill=ground)
            cx, cy = left + panel_w * 2 / 3, top + panel_h * 2 / 3 - 22
            draw.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), fill=subject)
            for k in (1, 2):
                x = left + panel_w * k / 3
                y = top + panel_h * k / 3
                draw.line((x, top, x, bottom), fill=guide, width=1)
                draw.line((left, y, right, y), fill=guide, width=1)
        elif i == 1:
            # 主題を画面の中央に大きく置く
            draw.rectangle((left, top, right, bottom), fill=sky)
            cx, cy = left + panel_w / 2, top + panel_h / 2
            draw.ellipse((cx - 50, cy - 50, cx + 50, cy + 50), fill=subject)
            draw.line((cx - 12, cy, cx + 12, cy), fill=guide, width=1)
            draw.line((cx, cy - 12, cx, cy + 12), fill=guide, width=1)
        else:
            # 道や川のような帯を対角線に沿って置く
            draw.rectangle((left, top, right, bottom), fill=ground)
            draw.polygon(
                [(left, bottom - 30), (left, bottom), (left + 40, bottom), (right, top + 25), (right, top),
                 (right - 30, top)],
                fill=sky,
            )
            draw.line((left, bottom, right, top), fill=guide, width=1)
            for t, r in ((0.25, 16), (0.5, 12), (0.75, 8)):
                cx = left + panel_w * t
                cy = bottom - panel_h * t
                draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=subject)
        draw.rectangle((left, top, right, bottom), outline="black", width=2)
    img.save(OUT_DIR / "composition.png")


# 分野ごとの目安. (名前, 始めるのに必要な費用, 1 回の活動時間). 値は 0: 低い・短い, 1: 中程度, 2: 高い・長い
GENRE_ESTIMATES: list[tuple[str, int, int]] = [
    ("美術鑑賞", 0, 1),
    ("コンサート鑑賞", 0, 1),
    ("舞台鑑賞", 1, 2),
    ("スケッチ・水彩画", 0, 0),
    ("油彩画", 1, 2),
    ("デジタルイラスト", 2, 1),
    ("書道", 0, 0),
    ("写真（スマートフォン）", 0, 0),
    ("写真（カメラ）", 2, 1),
    ("陶芸", 1, 1),
    ("編み物・刺繍", 0, 0),
    ("ピアノ", 2, 0),
    ("ギター・ウクレレ", 1, 0),
    ("合唱", 0, 1),
    ("ダンス", 0, 1),
    ("俳句・短歌", 0, 0),
    ("華道・茶道", 1, 1),
]


def fig_cost_time() -> None:
    """分野ごとの、始めるのに必要な費用と 1 回の活動時間の目安を 3 × 3 のマスに分類する."""
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    for cost in range(3):
        for hours in range(3):
            # 費用が低く時間が短いマスほど薄い色にする
            shade = 0.95 - 0.08 * (cost + hours)
            ax.add_patch(Rectangle((cost, hours), 1, 1, facecolor=(shade, shade, 1.0), edgecolor="white",
                                   linewidth=3))
            names = [name for name, c, h in GENRE_ESTIMATES if c == cost and h == hours]
            ax.text(cost + 0.5, hours + 0.5, "\n".join(names), ha="center", va="center", fontsize=10,
                    linespacing=1.5)
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.set_xticks([0.5, 1.5, 2.5])
    ax.set_xticklabels(["低い", "中程度", "高い"])
    ax.set_yticks([0.5, 1.5, 2.5])
    ax.set_yticklabels(["短い", "中程度", "長い"])
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xlabel("始めるのに必要な費用")
    ax.set_ylabel("1 回の活動時間")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "cost_time.png", dpi=110)
    plt.close(fig)


def main() -> None:
    """すべての図を生成する."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig_color_wheel()
    fig_composition()
    fig_cost_time()


if __name__ == "__main__":
    main()
