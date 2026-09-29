"""第 2 章: 文字色と背景色のコントラスト比を計算する。

WCAG 2.2 の定義に従って相対輝度とコントラスト比を計算し、
結果を表示するとともに、見本画像 ch02_contrast.png を保存します。

実行例::

    python ch02_color_contrast.py --outdir output
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RGB = tuple[int, int, int]
FontType = ImageFont.FreeTypeFont | ImageFont.ImageFont

FONT_CANDIDATES = [
    "C:/Windows/Fonts/YuGothM.ttc",
    "C:/Windows/Fonts/meiryo.ttc",
    "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]

# (文字色, 背景色) の組み合わせ
COLOR_PAIRS: list[tuple[str, str]] = [
    ("#222222", "#ffffff"),
    ("#767676", "#ffffff"),
    ("#9a9a9a", "#ffffff"),
    ("#ffffff", "#1f5fbf"),
    ("#ffffff", "#f39c12"),
    ("#d62728", "#2ca02c"),
]


def load_font(size: int) -> FontType:
    """日本語フォントを読み込む。見つからなければ既定のフォントを返す。"""
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def hex_to_rgb(code: str) -> RGB:
    """'#rrggbb' 形式の文字列を (R, G, B) に変換する。"""
    code = code.lstrip("#")
    return (int(code[0:2], 16), int(code[2:4], 16), int(code[4:6], 16))


def srgb_to_linear(value: int) -> float:
    """sRGB の 0〜255 の値を、ガンマ補正を外した 0〜1 の値に変換する。"""
    c = value / 255
    if c <= 0.04045:
        return c / 12.92
    return float(((c + 0.055) / 1.055) ** 2.4)


def relative_luminance(rgb: RGB) -> float:
    """相対輝度 (黒 = 0, 白 = 1) を返す。"""
    r, g, b = (srgb_to_linear(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(color1: RGB, color2: RGB) -> float:
    """2 色のコントラスト比 (1〜21) を返す。引数の順序は問わない。"""
    l1 = relative_luminance(color1)
    l2 = relative_luminance(color2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def judge(ratio: float) -> str:
    """WCAG 2.2 の達成基準 (通常の大きさの文字) に対する判定を返す。"""
    if ratio >= 7.0:
        return "AAA"
    if ratio >= 4.5:
        return "AA"
    if ratio >= 3.0:
        return "大きな文字のみ AA"
    return "不適合"


def draw_samples(pairs: list[tuple[str, str]]) -> Image.Image:
    """色の組み合わせごとに、見本の文字とコントラスト比を描画する。"""
    row_h, width = 64, 720
    image = Image.new("RGB", (width, row_h * len(pairs)), "white")
    draw = ImageDraw.Draw(image)
    sample_font = load_font(22)
    info_font = load_font(18)

    for i, (fg, bg) in enumerate(pairs):
        top = i * row_h
        ratio = contrast_ratio(hex_to_rgb(fg), hex_to_rgb(bg))
        draw.rectangle((0, top, 360, top + row_h - 1), fill=bg)
        draw.text((20, top + row_h // 2), "読みやすさの見本 Aa",
                  font=sample_font, fill=fg, anchor="lm")
        info = f"{fg} / {bg}  {ratio:5.2f} : 1  {judge(ratio)}"
        draw.text((380, top + row_h // 2), info, font=info_font,
                  fill="#222222", anchor="lm")
    return image


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    for fg, bg in COLOR_PAIRS:
        ratio = contrast_ratio(hex_to_rgb(fg), hex_to_rgb(bg))
        print(f"{fg} on {bg}: {ratio:5.2f} : 1 ({judge(ratio)})")

    draw_samples(COLOR_PAIRS).save(outdir / "ch02_contrast.png")
    print(f"画像を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
