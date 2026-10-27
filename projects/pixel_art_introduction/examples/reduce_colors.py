"""画像を縮小・減色して、ドット絵の下書きを作る。

写真やイラストから直接ドット絵を作ることはできないが、
配色や構図を検討するための下書きとしては役に立つ。

使い方::

    python reduce_colors.py                       # サンプル画像（グラデーション）を使う
    python reduce_colors.py photo.jpg -W 48 -c 8  # 幅 48 ピクセル、8 色に変換
"""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw

from scale_nearest import scale_nearest


def make_sample_image() -> Image.Image:
    """夕焼け空と太陽を描いたサンプル画像（なめらかなグラデーション）を作る。"""
    width, height = 256, 192
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)
    for y in range(height):
        t = y / (height - 1)
        color = (round(40 + 215 * t), round(30 + 120 * t), round(110 - 40 * t))
        draw.line((0, y, width - 1, y), fill=color)
    draw.ellipse((88, 96, 168, 176), fill=(255, 236, 160))
    draw.rectangle((0, 150, width - 1, height - 1), fill=(30, 24, 60))
    return image


def reduce_colors(image: Image.Image, width: int, colors: int, dither: bool) -> Image.Image:
    """幅 width ピクセルに縮小し、colors 色に減色した画像を返す。"""
    height = max(1, round(image.height * width / image.width))
    # 縮小時は周囲の色を平均する BOX を使い、細部のちらつきを抑える
    small = image.convert("RGB").resize((width, height), Image.Resampling.BOX)
    # まず色数を減らしたパレットを求め、そのパレットに合わせて各ピクセルの色を決め直す
    palette = small.quantize(colors=colors, dither=Image.Dither.NONE)
    method = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    return small.quantize(palette=palette, dither=method).convert("RGB")


def main() -> None:
    parser = argparse.ArgumentParser(description="画像を縮小・減色してドット絵の下書きを作る")
    parser.add_argument("input", nargs="?", help="入力画像（省略時はサンプル画像）")
    parser.add_argument("-W", "--width", type=int, default=64, help="縮小後の幅（既定値: 64）")
    parser.add_argument("-c", "--colors", type=int, default=8, help="色数（既定値: 8）")
    parser.add_argument("--dither", action="store_true", help="誤差拡散ディザリングを使う")
    parser.add_argument("-s", "--scale", type=int, default=4, help="保存時の倍率（既定値: 4）")
    args = parser.parse_args()

    image = Image.open(args.input) if args.input else make_sample_image()
    reduced = reduce_colors(image, args.width, args.colors, args.dither)

    output = Path("output/reduced.png")
    output.parent.mkdir(parents=True, exist_ok=True)
    scale_nearest(reduced, args.scale).save(output)
    print(f"保存した: {output}")


if __name__ == "__main__":
    main()
