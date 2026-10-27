"""本文で使う図を生成する.

Sphinx のビルド開始時に conf.py から main() が呼び出される。
単独で実行しても図を生成できる。
"""

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


def fig_ph_cleaners() -> None:
    """汚れの性質と洗剤の液性 (pH) の対応."""
    fig, ax = plt.subplots(figsize=(10, 4.6))

    # 家庭用品品質表示法による液性の区分
    bands = [
        (0.0, 3.0, "酸性", "#f4a6a6"),
        (3.0, 6.0, "弱酸性", "#f9d3b4"),
        (6.0, 8.0, "中性", "#d9ecc4"),
        (8.0, 11.0, "弱アルカリ性", "#b9d8f0"),
        (11.0, 14.0, "アルカリ性", "#a9b8ec"),
    ]
    for start, end, label, color in bands:
        ax.add_patch(Rectangle((start, 0.0), end - start, 1.0, facecolor=color, edgecolor="white", linewidth=2))
        ax.text((start + end) / 2, 0.5, label, ha="center", va="center", fontsize=12)

    # 洗剤・掃除用品の例 (おおよその pH)
    products = [
        (2.2, "クエン酸水"),
        (7.0, "台所用中性洗剤"),
        (8.2, "重曹水"),
        (9.8, "セスキ炭酸ソーダ水"),
        (12.5, "塩素系漂白剤"),
    ]
    for ph, label in products:
        ax.plot([ph, ph], [-0.05, -0.35], color="#444444", linewidth=1)
        ax.plot(ph, -0.05, marker="v", color="#444444")
        ax.text(ph, -0.45, label, ha="center", va="top", fontsize=10)

    # 汚れの種類と、落とすのに向く洗剤
    ax.annotate(
        "水あか・石けんかす\n(アルカリ性の汚れ)\n→ 酸性の洗剤で落とす",
        xy=(2.0, 1.02), xytext=(2.0, 1.75), ha="center", va="center", fontsize=10,
        arrowprops={"arrowstyle": "->", "color": "#b03030"},
    )
    ax.annotate(
        "油汚れ・皮脂・手あか\n(酸性の汚れ)\n→ アルカリ性の洗剤で落とす",
        xy=(10.5, 1.02), xytext=(10.5, 1.75), ha="center", va="center", fontsize=10,
        arrowprops={"arrowstyle": "->", "color": "#3050b0"},
    )
    ax.text(7.0, 1.55, "軽い汚れは\n中性洗剤で十分", ha="center", va="center", fontsize=10)

    ax.set_xlim(0, 14)
    ax.set_ylim(-1.0, 2.2)
    ax.set_xticks(range(0, 15))
    ax.set_yticks([])
    ax.text(14.3, 0.0, "pH", ha="left", va="center", fontsize=11)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_position(("data", 0.0))
    ax.set_title("汚れの性質と洗剤の液性")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "ph_cleaners.png", dpi=120)
    plt.close(fig)


def fig_bacteria_temperature() -> None:
    """食中毒の原因となる細菌と温度の関係."""
    fig, ax = plt.subplots(figsize=(10, 4.2))

    zones = [
        (-45.0, -15.0, "冷凍 (-15 ℃ 以下)\n増殖がほぼ止まる\n(死滅はしない)", "#a9c8f0"),
        (-15.0, 10.0, "冷蔵 (10 ℃ 以下)\n増殖が\nゆっくりになる", "#cfe3f5"),
        (10.0, 60.0, "危険温度帯 (10〜60 ℃)\n細菌が増えやすい", "#f6c0b0"),
        (60.0, 75.0, "増えにくい", "#f9e0b8"),
        (75.0, 100.0, "加熱の目安\n中心部 75 ℃ で 1 分以上", "#f4a6a6"),
    ]
    for start, end, label, color in zones:
        ax.add_patch(Rectangle((start, 0.0), end - start, 1.0, facecolor=color, edgecolor="white", linewidth=2))
        ax.text((start + end) / 2, 0.5, label, ha="center", va="center", fontsize=9.5)

    # 特に増えやすい温度帯
    ax.add_patch(Rectangle((30.0, 1.08), 10.0, 0.12, facecolor="#c03020"))
    ax.text(35.0, 1.32, "30〜40 ℃ で特に増えやすい", ha="center", va="bottom", fontsize=10, color="#c03020")

    ax.set_xlim(-45, 100)
    ax.set_ylim(-0.1, 1.6)
    ax.set_xticks([-15, 0, 10, 20, 30, 40, 50, 60, 75, 100])
    ax.set_yticks([])
    ax.set_xlabel("温度 [℃]")
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    ax.set_title("細菌が増えやすい温度帯")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "bacteria_temperature.png", dpi=120)
    plt.close(fig)


def fig_refrigerator() -> None:
    """冷蔵庫の温度帯と、それぞれに入れる食品の例."""
    width, height = 760, 650
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    title_font = load_font(22)
    head_font = load_font(18)
    body_font = load_font(15)

    draw.text((width // 2, 18), "冷蔵庫の温度帯と入れる食品の例", fill="black", font=title_font, anchor="mt")

    # 本体 (左) とドアポケット (右)
    left, right, door_right = 40, 520, 720
    top = 60
    rooms = [
        ("冷蔵室  約 3〜6 ℃", "総菜・作り置き・乳製品・卵・\n開封後の調味料", 200, "#dceefa"),
        ("チルド室  約 0〜2 ℃", "肉・魚・加工肉・発酵食品", 70, "#c4e0f5"),
        ("野菜室  約 3〜8 ℃", "野菜・果物", 120, "#d9ecc4"),
        ("冷凍室  約 -18 ℃", "冷凍食品・小分けして冷凍した\n肉・魚・ご飯", 140, "#c7cdf0"),
    ]
    y = top
    for head, body, h, color in rooms:
        draw.rectangle((left, y, right, y + h), fill=color, outline="#555555", width=2)
        draw.text((left + 16, y + 12), head, fill="black", font=head_font)
        draw.multiline_text((left + 16, y + 42), body, fill="#333333", font=body_font, spacing=6)
        y += h

    # ドアポケットは冷蔵室の扉にある
    draw.rectangle((right + 10, top, door_right, top + 270), fill="#fbf1d6", outline="#555555", width=2)
    draw.text((right + 22, top + 12), "ドアポケット", fill="black", font=head_font)
    draw.text((right + 22, top + 40), "約 6〜9 ℃", fill="black", font=head_font)
    draw.multiline_text(
        (right + 22, top + 74), "飲み物・調味料\n\n扉の開け閉めで\n温度が上がりやすい\n傷みやすい食品\nは入れない",
        fill="#333333", font=body_font, spacing=6,
    )

    draw.text(
        (width // 2, height - 26), "温度と部屋の配置は機種によって異なる。取扱説明書で確認する。",
        fill="#555555", font=body_font, anchor="mm",
    )
    img.save(OUT_DIR / "refrigerator.png")


def main() -> None:
    """すべての図を生成する."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig_ph_cleaners()
    fig_bacteria_temperature()
    fig_refrigerator()


if __name__ == "__main__":
    main()
