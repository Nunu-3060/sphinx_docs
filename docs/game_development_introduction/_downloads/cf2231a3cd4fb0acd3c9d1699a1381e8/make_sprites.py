"""Pillow を使い、ブロック崩し用のドット絵のスプライトシートを生成する。

実行方法:
    py make_sprites.py                      # sprites.png を出力する
    py make_sprites.py out.png --scale 4    # 4 倍に拡大した確認用の画像を出力する

スプライトシートには、左から 5 色のブロック、パドル、ボールの順に並べる。
各スプライトの位置は SPRITE_RECTS に（x, y, 幅, 高さ）で記録している。
"""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw

Color = tuple[int, int, int]

BLOCK_SIZE = (28, 10)  # ブロック 1 つの大きさ（ピクセル）
PADDLE_SIZE = (48, 6)
BALL_SIZE = 6
BLOCK_COLORS: list[Color] = [(239, 83, 80), (255, 167, 38), (255, 238, 88), (102, 187, 106), (66, 165, 245)]
PADDLE_COLOR: Color = (200, 210, 255)
BALL_COLOR: Color = (255, 255, 255)


def shade(color: Color, factor: float) -> Color:
    """色の明るさを factor 倍にする（1 より大きいと明るく、小さいと暗くなる）。"""
    r, g, b = (min(255, int(c * factor)) for c in color)
    return (r, g, b)


def make_bevel(size: tuple[int, int], color: Color) -> Image.Image:
    """左上を明るく、右下を暗くした、立体的に見える長方形を描く。"""
    width, height = size
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width - 1, height - 1), fill=color)
    draw.line((0, 0, width - 1, 0), fill=shade(color, 1.4))  # 上辺
    draw.line((0, 0, 0, height - 1), fill=shade(color, 1.4))  # 左辺
    draw.line((0, height - 1, width - 1, height - 1), fill=shade(color, 0.6))  # 下辺
    draw.line((width - 1, 0, width - 1, height - 1), fill=shade(color, 0.6))  # 右辺
    return image


def make_ball() -> Image.Image:
    image = Image.new("RGBA", (BALL_SIZE, BALL_SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(image).ellipse((0, 0, BALL_SIZE - 1, BALL_SIZE - 1), fill=BALL_COLOR)
    return image


def make_sheet() -> tuple[Image.Image, dict[str, tuple[int, int, int, int]]]:
    """スプライトを横 1 列に並べたシートと、各スプライトの位置を返す。"""
    sprites: dict[str, Image.Image] = {}
    for index, color in enumerate(BLOCK_COLORS):
        sprites[f"block{index}"] = make_bevel(BLOCK_SIZE, color)
    sprites["paddle"] = make_bevel(PADDLE_SIZE, PADDLE_COLOR)
    sprites["ball"] = make_ball()

    gap = 2  # スプライト同士の間隔。拡大縮小時に隣の絵がにじむのを防ぐ
    width = sum(image.width for image in sprites.values()) + gap * (len(sprites) + 1)
    height = max(image.height for image in sprites.values()) + gap * 2
    sheet = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    rects: dict[str, tuple[int, int, int, int]] = {}
    x = gap
    for name, image in sprites.items():
        sheet.paste(image, (x, gap))
        rects[name] = (x, gap, image.width, image.height)
        x += image.width + gap
    return sheet, rects


def main() -> None:
    parser = argparse.ArgumentParser(description="ブロック崩し用のスプライトシートを生成する。")
    parser.add_argument("output", nargs="?", default="sprites.png", type=Path, help="出力する PNG ファイル")
    parser.add_argument("--scale", type=int, default=1, help="拡大率（ドット絵がぼやけないよう最近傍法で拡大する）")
    args = parser.parse_args()

    sheet, rects = make_sheet()
    if args.scale > 1:
        sheet = sheet.resize((sheet.width * args.scale, sheet.height * args.scale), Image.Resampling.NEAREST)
    sheet.save(args.output)
    for name, rect in rects.items():
        print(f"{name}: {rect}")


if __name__ == "__main__":
    main()
