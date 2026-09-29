"""第 1 章: デザインの 4 原則を適用する前後のカードを描画する。

同じ内容のイベント告知カードを 2 種類描画し、PNG 画像として保存します。

* ch01_before.png: 原則を意識せずに配置した例
* ch01_after.png: 近接・整列・反復・コントラストを適用した例

実行例::

    python ch01_principles.py --outdir output
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FontType = ImageFont.FreeTypeFont | ImageFont.ImageFont

WIDTH, HEIGHT = 640, 400

# 日本語を表示できるフォントの候補 (見つかった最初のものを使う)
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

TITLE = "Python デザイン勉強会"
DATE = "日時: 2026 年 10 月 20 日 (火) 19:00〜20:30"
PLACE = "会場: 本社 3F 会議室 A"
DESCRIPTION = "グラフと UI の見た目を改善するコツを紹介します。"
BUTTON = "参加登録はこちら"


def load_font(size: int, bold: bool = False) -> FontType:
    """日本語フォントを読み込む。見つからなければ既定のフォントを返す。"""
    for path in BOLD_FONTS if bold else REGULAR_FONTS:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def text_width(draw: ImageDraw.ImageDraw, text: str, font: FontType) -> float:
    """描画したときの文字列の幅 (ピクセル) を返す。"""
    return draw.textlength(text, font=font)


def draw_before() -> Image.Image:
    """原則を意識せずに要素を配置したカードを描画する。"""
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)
    font = load_font(20)  # すべて同じ大きさ (コントラストがない)
    gray = "#9a9a9a"  # 背景との明度差が小さく読みにくい

    # 中央揃えと左揃えが混在し、要素が等間隔に散らばっている
    title_x = (WIDTH - text_width(draw, TITLE, font)) / 2
    draw.text((title_x, 40), TITLE, font=font, fill=gray)
    draw.text((30, 110), DATE, font=font, fill=gray)
    draw.text((180, 180), PLACE, font=font, fill=gray)
    desc_x = (WIDTH - text_width(draw, DESCRIPTION, font)) / 2
    draw.text((desc_x, 250), DESCRIPTION, font=font, fill="#e07b39")

    # ボタンらしさが弱く、色もほかの要素と関係がない
    draw.rectangle((420, 320, 610, 365), outline="#6aa84f", width=1)
    draw.text((435, 330), BUTTON, font=font, fill="#6aa84f")
    return image


def draw_after() -> Image.Image:
    """4 原則を適用したカードを描画する。"""
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(image)

    accent = "#1f5fbf"  # アクセントカラー (反復して使う)
    text_main = "#222222"
    text_sub = "#555555"
    left = 56  # すべての要素をこの x 座標に揃える (整列)

    # アクセントカラーの帯で、カードの始まりを示す
    draw.rectangle((0, 0, 8, HEIGHT), fill=accent)

    # タイトルは大きく太く (コントラスト)
    draw.text((left, 40), TITLE, font=load_font(34, bold=True),
              fill=text_main)

    # 日時と会場は関係が深いので近づける (近接)
    info_font = load_font(18)
    draw.text((left, 112), DATE, font=info_font, fill=text_sub)
    draw.text((left, 142), PLACE, font=info_font, fill=text_sub)

    # 説明文はグループ間の余白を大きく取って区別する
    draw.text((left, 212), DESCRIPTION, font=load_font(18), fill=text_main)

    # ボタンはアクセントカラーで塗り、押せる要素であることを示す
    button_font = load_font(18, bold=True)
    button_w = text_width(draw, BUTTON, button_font) + 48
    draw.rounded_rectangle((left, 300, left + button_w, 348), radius=8,
                           fill=accent)
    # anchor="lm" で、文字列の左端・上下中央を指定座標に合わせる
    draw.text((left + 24, 324), BUTTON, font=button_font, fill="white",
              anchor="lm")
    return image


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    draw_before().save(outdir / "ch01_before.png")
    draw_after().save(outdir / "ch01_after.png")
    print(f"画像を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
