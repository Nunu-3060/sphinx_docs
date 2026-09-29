"""第 3 章: ジャンプ率と行送りの違いを比較する画像を生成する。

* ch03_jump_ratio.png: 見出しと本文の文字の大きさの比 (ジャンプ率) の比較
* ch03_line_height.png: 行送り (行の基準線どうしの間隔) の比較

実行例::

    python ch03_typography.py --outdir output
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FontType = ImageFont.FreeTypeFont | ImageFont.ImageFont

REGULAR_FONTS = [
    "C:/Windows/Fonts/YuGothM.ttc",
    "C:/Windows/Fonts/meiryo.ttc",
    "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
]
BOLD_FONTS = [
    "C:/Windows/Fonts/YuGothB.ttc",
    "C:/Windows/Fonts/meiryob.ttc",
    "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
]

HEADING = "測定結果の概要"
BODY = ("今回の測定では、試料 A の応答時間が前回より 12 % 短くなりました。"
        "一方、試料 B は温度が高い条件でばらつきが大きく、"
        "追加の測定が必要です。詳細は次の節で説明します。")

# 行の先頭に置かない文字 (簡易的な禁則処理)
NO_LINE_START = "、。，．）」』!?！？%"

PANEL_W, PANEL_H = 420, 300
MARGIN = 24
TEXT_COLOR = "#222222"


def load_font(size: int, bold: bool = False) -> FontType:
    """日本語フォントを読み込む。見つからなければ既定のフォントを返す。"""
    for path in BOLD_FONTS if bold else REGULAR_FONTS:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def wrap_text(text: str, font: FontType, max_width: float) -> list[str]:
    """文字列を max_width に収まるように折り返す。

    日本語は 1 文字単位で、英数字は単語単位で折り返す。
    行頭禁則文字は前の行の末尾に残す。
    """
    tokens = re.findall(r"[0-9A-Za-z.]+|.", text)
    lines: list[str] = []
    current = ""
    for token in tokens:
        too_wide = font.getlength(current + token) > max_width
        if too_wide and current and token not in NO_LINE_START:
            lines.append(current.rstrip())
            current = token.lstrip()
        else:
            current += token
    if current:
        lines.append(current.rstrip())
    return lines


def draw_paragraph(draw: ImageDraw.ImageDraw, top: int, font: FontType,
                   size: int, line_height: float) -> None:
    """本文を折り返して描画する。line_height は行送りの、文字の大きさに対する倍率。"""
    lines = wrap_text(BODY, font, PANEL_W - MARGIN * 2)
    for i, line in enumerate(lines):
        y = top + i * size * line_height
        draw.text((MARGIN, y), line, font=font, fill=TEXT_COLOR)


def draw_label(draw: ImageDraw.ImageDraw, text: str) -> None:
    """パネル下部に説明ラベルを描画する。"""
    draw.text((MARGIN, PANEL_H - 36), text, font=load_font(15),
              fill="#1f5fbf")


def make_panel(heading_size: int, body_size: int, line_height: float,
               label: str) -> Image.Image:
    """見出しと本文から成る 1 枚のパネルを描画する。"""
    image = Image.new("RGB", (PANEL_W, PANEL_H), "white")
    draw = ImageDraw.Draw(image)
    draw.text((MARGIN, MARGIN), HEADING,
              font=load_font(heading_size, bold=True), fill=TEXT_COLOR)
    body_top = MARGIN + round(heading_size * 1.8)
    draw_paragraph(draw, body_top, load_font(body_size), body_size,
                   line_height)
    draw_label(draw, label)
    return image


def join_side_by_side(left: Image.Image, right: Image.Image) -> Image.Image:
    """2 枚の画像を、間に区切り線を入れて横に並べる。"""
    gap = 2
    joined = Image.new("RGB", (left.width + right.width + gap,
                               max(left.height, right.height)), "#cccccc")
    joined.paste(left, (0, 0))
    joined.paste(right, (left.width + gap, 0))
    return joined


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    # ジャンプ率: 見出し 18 px / 本文 16 px (約 1.1 倍) と 30 / 16 (約 1.9 倍)
    low = make_panel(18, 16, 1.7, "ジャンプ率 約 1.1 倍")
    high = make_panel(30, 16, 1.7, "ジャンプ率 約 1.9 倍")
    join_side_by_side(low, high).save(outdir / "ch03_jump_ratio.png")

    # 行送り: 文字の大きさの 1.2 倍と 1.7 倍
    tight = make_panel(24, 16, 1.2, "行送り 1.2 倍")
    loose = make_panel(24, 16, 1.7, "行送り 1.7 倍")
    join_side_by_side(tight, loose).save(outdir / "ch03_line_height.png")
    print(f"画像を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
