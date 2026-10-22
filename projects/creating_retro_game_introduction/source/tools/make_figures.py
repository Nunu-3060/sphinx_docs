"""本文で使う図 (PIL / matplotlib) をまとめて生成する。

使い方:
    python make_figures.py

出力先:
    source/images/figures/
"""

import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pyxel
from matplotlib.patches import Rectangle
from PIL import Image, ImageDraw, ImageFont

matplotlib.use("Agg")

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "source" / "images" / "figures"
RESOURCE = ROOT / "examples" / "assets" / "cosmo_rush.pyxres"
sys.path.insert(0, str(ROOT / "examples" / "assets"))

import make_assets  # noqa: E402

FONT_PATH = "C:/Windows/Fonts/BIZ-UDGothicR.ttc"
plt.rcParams["font.family"] = "BIZ UDGothic"
plt.rcParams["font.size"] = 11

PALETTE = [
    0x000000, 0x2B335F, 0x7E2072, 0x19959C, 0x8B4852, 0x395C98, 0xA9C1FF, 0xEEEEEE,
    0xD4186C, 0xD38441, 0xE9C35B, 0x70C6A9, 0x7696DE, 0xA3A3A3, 0xFF9798, 0xEDC7B0,
]
COLOR_NAMES = [
    "BLACK", "NAVY", "PURPLE", "GREEN", "BROWN", "DARK_BLUE", "LIGHT_BLUE", "WHITE",
    "RED", "ORANGE", "YELLOW", "LIME", "CYAN", "GRAY", "PINK", "PEACH",
]
BG = (238, 238, 238)


def rgb(col: int) -> tuple[int, int, int]:
    c = PALETTE[col]
    return (c >> 16) & 0xFF, (c >> 8) & 0xFF, c & 0xFF


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size)


def rows_to_image(rows: list[str], scale: int, bg: tuple[int, int, int] = BG, grid: bool = False) -> Image.Image:
    """ドット絵の文字列のリストを拡大した画像にする。"." と "0" は背景色で塗る。"""
    h = len(rows)
    w = len(rows[0])
    img = Image.new("RGB", (w * scale, h * scale), bg)
    draw = ImageDraw.Draw(img)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in ".0":
                continue
            col = int(ch, 16)
            draw.rectangle([x * scale, y * scale, (x + 1) * scale - 1, (y + 1) * scale - 1], fill=rgb(col))
    if grid:
        for i in range(w + 1):
            draw.line([i * scale, 0, i * scale, h * scale], fill=(200, 200, 200))
        for i in range(h + 1):
            draw.line([0, i * scale, w * scale, i * scale], fill=(200, 200, 200))
    return img


def bank_rows(bank: int, x: int, y: int, w: int, h: int) -> list[str]:
    """イメージバンクの矩形領域を、ドット絵の文字列のリストとして読み出す。"""
    img = pyxel.images[bank]
    return ["".join(f"{img.pget(x + i, y + j):x}" for i in range(w)) for j in range(h)]


def save(img: Image.Image, name: str) -> None:
    path = OUT / name
    img.save(path)
    print(f"saved: {path}")


def save_plot(fig: plt.Figure, name: str) -> None:
    path = OUT / name
    fig.savefig(path, dpi=110, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"saved: {path}")


# ---------------------------------------------------------------------------


def make_palette() -> None:
    cell_w, cell_h = 150, 54
    img = Image.new("RGB", (cell_w * 4 + 20, cell_h * 4 + 20), "white")
    draw = ImageDraw.Draw(img)
    f = font(14)
    for col in range(16):
        x = 10 + col % 4 * cell_w
        y = 10 + col // 4 * cell_h
        draw.rectangle([x, y, x + 40, y + 40], fill=rgb(col), outline=(120, 120, 120))
        draw.text((x + 48, y + 2), f"{col}  ({col:X})", fill=(0, 0, 0), font=f)
        draw.text((x + 48, y + 20), COLOR_NAMES[col], fill=(80, 80, 80), font=font(13))
    save(img, "palette.png")


def make_coords() -> None:
    fig, ax = plt.subplots(figsize=(5.2, 4.4))
    ax.set_xlim(-12, 172)
    ax.set_ylim(132, -14)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 160, 120, fill=False, lw=1.5, ec="#333"))
    ax.annotate("", xy=(172, 0), xytext=(0, 0), arrowprops={"arrowstyle": "->", "lw": 1.5})
    ax.annotate("", xy=(0, 132), xytext=(0, 0), arrowprops={"arrowstyle": "->", "lw": 1.5})
    ax.text(166, -4, "x", fontsize=13)
    ax.text(-8, 130, "y", fontsize=13)
    ax.text(-10, -5, "(0, 0)", fontsize=10)
    ax.text(140, 128, "(159, 119)", fontsize=10)
    ax.add_patch(Rectangle((60, 40), 32, 24, fc="#a9c1ff", ec="#395c98", lw=1.5))
    ax.plot([60], [40], "o", color="#d4186c")
    ax.text(48, 36, "(x, y)", fontsize=11, color="#d4186c")
    ax.annotate("", xy=(92, 70), xytext=(60, 70), arrowprops={"arrowstyle": "<->"})
    ax.text(72, 78, "w", fontsize=11)
    ax.annotate("", xy=(98, 64), xytext=(98, 40), arrowprops={"arrowstyle": "<->"})
    ax.text(101, 54, "h", fontsize=11)
    ax.text(20, 100, "画面サイズ 160 × 120 の場合", fontsize=11)
    save_plot(fig, "coords.png")


def make_aabb() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.8))
    cases = [
        ("重なっている", (10, 10, 40, 30), (35, 25, 40, 30)),
        ("重なっていない (b.x ≧ a.x + a.w)", (10, 10, 40, 30), (60, 25, 30, 30)),
    ]
    for ax, (title, a, b) in zip(axes, cases):
        ax.set_xlim(0, 100)
        ax.set_ylim(70, 0)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title, fontsize=12)
        ax.add_patch(Rectangle(a[:2], a[2], a[3], fc="#a9c1ff", ec="#395c98", alpha=0.8, lw=1.5))
        ax.add_patch(Rectangle(b[:2], b[2], b[3], fc="#ff9798", ec="#d4186c", alpha=0.7, lw=1.5))
        ax.text(a[0] + 2, a[1] + 6, "a", fontsize=13)
        ax.text(b[0] + b[2] - 6, b[1] + b[3] - 3, "b", fontsize=13)
        for x in (a[0], a[0] + a[2]):
            ax.axvline(x, color="#395c98", ls=":", lw=1)
        for x in (b[0], b[0] + b[2]):
            ax.axvline(x, color="#d4186c", ls=":", lw=1)
    fig.text(
        0.5, -0.04,
        "a.x < b.x + b.w  かつ  b.x < a.x + a.w  かつ  a.y < b.y + b.h  かつ  b.y < a.y + a.h  のとき重なる",
        ha="center", fontsize=11,
    )
    save_plot(fig, "aabb.png")


def make_hitbox() -> None:
    scale = 16
    rows = bank_rows(0, 16, 0, 16, 16)
    img = rows_to_image(rows, scale, grid=True)
    pad = 10
    canvas = Image.new("RGB", (img.width + pad * 2 + 230, img.height + pad * 2), "white")
    canvas.paste(img, (pad, pad))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([pad, pad, pad + 16 * scale, pad + 16 * scale], outline=(57, 92, 152), width=3)
    m = 5
    draw.rectangle(
        [pad + m * scale, pad + m * scale, pad + (16 - m) * scale, pad + (16 - m) * scale],
        outline=(212, 24, 108), width=4,
    )
    f = font(16)
    tx = pad + 16 * scale + 20
    draw.rectangle([tx, 40, tx + 20, 60], outline=(57, 92, 152), width=3)
    draw.text((tx + 30, 40), "画像の範囲 (16 × 16)", fill=(0, 0, 0), font=f)
    draw.rectangle([tx, 90, tx + 20, 110], outline=(212, 24, 108), width=4)
    draw.text((tx + 30, 90), "当たり判定 (6 × 6)", fill=(0, 0, 0), font=f)
    draw.text((tx, 140), "margin = 5", fill=(0, 0, 0), font=f)
    save(canvas, "hitbox.png")


def make_waveforms() -> None:
    t = np.linspace(0, 2, 800, endpoint=False)
    phase = t % 1.0
    triangle = np.where(phase < 0.5, 4 * phase - 1, 3 - 4 * phase)
    square = np.where(phase < 0.5, 1.0, -1.0)
    pulse = np.where(phase < 0.25, 1.0, -1.0)
    rng = np.random.default_rng(3)
    noise = np.repeat(rng.choice([-1.0, 1.0], size=80), 10)
    waves = [
        ("T: トライアングル (三角波)", triangle),
        ("S: スクエア (矩形波)", square),
        ("P: パルス (幅の狭い矩形波)", pulse),
        ("N: ノイズ", noise),
    ]
    fig, axes = plt.subplots(4, 1, figsize=(7, 5.6), sharex=True)
    for ax, (label, wave) in zip(axes, waves):
        ax.plot(t, wave, color="#395c98", lw=1.6)
        ax.set_ylim(-1.4, 1.4)
        ax.set_yticks([])
        ax.set_title(label, loc="left", fontsize=11)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
    axes[-1].set_xticks([0, 1, 2])
    axes[-1].set_xticklabels(["0", "1 周期", "2 周期"])
    fig.tight_layout()
    save_plot(fig, "waveforms.png")


def make_pixelart_steps() -> None:
    body = make_assets.PLAYER_BODY
    silhouette = [row.translate(str.maketrans("567cd", "ddddd")) for row in body]
    base = [row.translate(str.maketrans("57", "66")) for row in body]
    final = body + make_assets.PLAYER_FLAMES[0]
    steps = [
        ("1. シルエット", make_assets.mirror(silhouette) + ["." * 16] * 2),
        ("2. 基本色", make_assets.mirror(base) + ["." * 16] * 2),
        ("3. 陰影とハイライト", make_assets.mirror(body) + ["." * 16] * 2),
        ("4. 噴射の炎を追加", make_assets.mirror(final)),
    ]
    scale = 10
    w = 16 * scale
    canvas = Image.new("RGB", (len(steps) * (w + 24) + 4, w + 40), "white")
    draw = ImageDraw.Draw(canvas)
    for i, (label, rows) in enumerate(steps):
        img = rows_to_image(rows, scale, grid=True)
        x = 12 + i * (w + 24)
        canvas.paste(img, (x, 4))
        draw.text((x, w + 12), label, fill=(0, 0, 0), font=font(15))
    save(canvas, "pixelart_steps.png")


def make_animation_frames() -> None:
    scale = 6
    items = [
        ("自機 (2 コマ)", [(16, 0), (32, 0)]),
        ("敵 A (2 コマ)", [(0, 16), (16, 16)]),
        ("爆発 (4 コマ)", [(0, 64), (16, 64), (32, 64), (48, 64)]),
    ]
    cell = 16 * scale
    canvas = Image.new("RGB", (6 + 4 * (cell + 8), len(items) * (cell + 34) + 4), "white")
    draw = ImageDraw.Draw(canvas)
    for r, (label, frames) in enumerate(items):
        y = 4 + r * (cell + 34)
        draw.text((6, y), label, fill=(0, 0, 0), font=font(15))
        for c, (u, v) in enumerate(frames):
            img = rows_to_image(bank_rows(0, u, v, 16, 16), scale, bg=(43, 51, 95))
            canvas.paste(img, (6 + c * (cell + 8), y + 24))
    save(canvas, "animation_frames.png")


def make_bank_layout() -> None:
    scale = 3
    rows = bank_rows(0, 0, 0, 128, 176)
    img = rows_to_image(rows, scale, bg=(43, 51, 95))
    draw = ImageDraw.Draw(img)
    for i in range(0, 128 * scale + 1, 8 * scale):
        draw.line([i, 0, i, 176 * scale], fill=(57, 92, 152))
    for i in range(0, 176 * scale + 1, 8 * scale):
        draw.line([0, i, 128 * scale, i], fill=(57, 92, 152))
    labels = [
        (0, "y = 0: 自機 (2 コマ)、自機の弾、敵の弾"),
        (16, "y = 16: 敵 A、敵 B、敵 C (各 2 コマ)"),
        (32, "y = 32: ボス (32 × 32, 2 コマ)"),
        (64, "y = 64: 爆発 (4 コマ)"),
        (128, "y = 128: 背景用のタイル (星、星雲)"),
        (136, "y = 136: 背景用のタイル (惑星、小惑星)"),
    ]
    canvas = Image.new("RGB", (img.width + 320, img.height + 2), "white")
    canvas.paste(img, (0, 0))
    d2 = ImageDraw.Draw(canvas)
    for y, text in labels:
        py = y * scale + 10
        d2.line([img.width, py, img.width + 16, py], fill=(212, 24, 108), width=2)
        d2.text((img.width + 22, py - 9), text, fill=(0, 0, 0), font=font(15))
    save(canvas, "bank_layout.png")


def make_scroll() -> None:
    """2 枚のタイルマップを縦に並べてスクロールさせる仕組みの図 (縮尺 1/2)。"""
    k = 0.5
    offset = 100
    canvas = Image.new("RGB", (640, 600), "white")
    draw = ImageDraw.Draw(canvas)
    f = font(15)
    left = 220
    screen_top = 260

    def y_of(v: float) -> int:
        return int(screen_top + v * k)

    blue = (169, 193, 255)
    pink = (255, 151, 152)
    draw.rectangle([left, y_of(offset - 512), left + 128 * k, y_of(offset)], fill=blue, outline=(57, 92, 152), width=2)
    draw.rectangle([left, y_of(offset), left + 128 * k, y_of(offset + 512)], fill=pink, outline=(212, 24, 108), width=2)
    draw.text((left - 214, y_of(offset - 512) - 8), "1 枚目: y = offset - 512", fill=(0, 0, 0), font=f)
    draw.text((left - 214, y_of(offset) - 8), "2 枚目: y = offset", fill=(0, 0, 0), font=f)
    draw.line([left - 20, y_of(offset - 512), left, y_of(offset - 512)], fill=(0, 0, 0), width=2)
    draw.line([left - 20, y_of(offset), left, y_of(offset)], fill=(0, 0, 0), width=2)
    draw.rectangle([left - 4, y_of(0), left + 128 * k + 4, y_of(160)], outline=(0, 0, 0), width=4)
    rx = left + 128 * k + 16
    draw.text((rx, y_of(0) + 4), "画面 (128 × 160)", fill=(0, 0, 0), font=f)
    draw.text((rx, y_of(0) + 26), "上の部分は 1 枚目の下端、", fill=(0, 0, 0), font=f)
    draw.text((rx, y_of(0) + 48), "下の部分は 2 枚目の上端が見える", fill=(0, 0, 0), font=f)
    draw.text((rx, y_of(-300)), "どちらも高さ MAP_HEIGHT (512)", fill=(0, 0, 0), font=f)
    draw.text((rx, y_of(-260)), "offset が増えると 2 枚とも下へ動く。", fill=(0, 0, 0), font=f)
    draw.text((rx, y_of(-220)), "offset が 512 に達したら 0 に戻すと、", fill=(0, 0, 0), font=f)
    draw.text((rx, y_of(-180)), "同じ見た目のまま無限に続く。", fill=(0, 0, 0), font=f)
    save(canvas, "scroll.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pyxel.init(128, 160, headless=True)
    pyxel.load(str(RESOURCE))
    make_palette()
    make_coords()
    make_aabb()
    make_hitbox()
    make_waveforms()
    make_pixelart_steps()
    make_animation_frames()
    make_bank_layout()
    make_scroll()


if __name__ == "__main__":
    main()
