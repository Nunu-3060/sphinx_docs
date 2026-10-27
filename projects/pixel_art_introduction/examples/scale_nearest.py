"""ドット絵を整数倍に拡大する（最近傍補間）。

使い方::

    python scale_nearest.py                  # サンプルのスライムを 8 倍に拡大
    python scale_nearest.py input.png -s 4   # input.png を 4 倍に拡大
"""

import argparse
from pathlib import Path

from PIL import Image

from sprite_data import slime_image


def scale_nearest(image: Image.Image, factor: int) -> Image.Image:
    """画像を factor 倍に拡大する。

    最近傍補間を使うため、1 ピクセルがそのまま factor×factor の正方形になる。
    """
    if factor < 1:
        raise ValueError("倍率は 1 以上の整数で指定する")
    size = (image.width * factor, image.height * factor)
    return image.resize(size, Image.Resampling.NEAREST)


def main() -> None:
    parser = argparse.ArgumentParser(description="ドット絵を整数倍に拡大する")
    parser.add_argument("input", nargs="?", help="入力画像（省略時はサンプルのスライム）")
    parser.add_argument("-s", "--scale", type=int, default=8, help="倍率（既定値: 8）")
    parser.add_argument("-o", "--output", default="output/scaled.png", help="出力先")
    args = parser.parse_args()

    image = Image.open(args.input) if args.input else slime_image()
    scaled = scale_nearest(image, args.scale)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    scaled.save(output)
    print(f"{image.width}x{image.height} -> {scaled.width}x{scaled.height}: {output}")


if __name__ == "__main__":
    main()
