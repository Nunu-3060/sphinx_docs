"""タイルを敷き詰めて、継ぎ目が目立たないかを確認する。

使い方::

    python tile_preview.py                 # サンプルの草地タイルを 3×3 枚並べる
    python tile_preview.py tile.png -n 4   # tile.png を 4×4 枚並べる
"""

import argparse
from pathlib import Path

from PIL import Image

from scale_nearest import scale_nearest
from sprite_data import grass_tile_image


def tile_image(tile: Image.Image, columns: int, rows: int) -> Image.Image:
    """タイルを columns×rows 枚並べた画像を返す。"""
    result = Image.new(tile.mode, (tile.width * columns, tile.height * rows))
    for row in range(rows):
        for column in range(columns):
            result.paste(tile, (column * tile.width, row * tile.height))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="タイルを敷き詰めて継ぎ目を確認する")
    parser.add_argument("input", nargs="?", help="タイル画像（省略時はサンプルの草地）")
    parser.add_argument("-n", "--count", type=int, default=3, help="縦横に並べる枚数（既定値: 3）")
    parser.add_argument("-s", "--scale", type=int, default=4, help="倍率（既定値: 4）")
    args = parser.parse_args()

    tile = Image.open(args.input) if args.input else grass_tile_image()
    preview = scale_nearest(tile_image(tile, args.count, args.count), args.scale)

    output = Path("output/tile_preview.png")
    output.parent.mkdir(parents=True, exist_ok=True)
    preview.save(output)
    print(f"保存した: {output}")


if __name__ == "__main__":
    main()
