"""ドット絵の画像を検査し、よくある問題を報告する。

検査する項目:

* 使用色数が上限を超えていないか
* 半透明のピクセル（完全な透明でも不透明でもないピクセル）が無いか
* 画像の幅と高さが指定した値の倍数になっているか

問題が見つかった場合は終了コード 1 で終了する。

使い方::

    python check_sprite.py                          # サンプルのスライムを検査
    python check_sprite.py hero.png --max-colors 8  # 色数の上限を 8 にして検査
"""

import argparse
import sys
from collections import Counter

from PIL import Image

from sprite_data import slime_image

RGBA = tuple[int, int, int, int]


def count_colors(image: Image.Image) -> Counter[RGBA]:
    """完全な透明を除いた各色のピクセル数を数える。"""
    rgba = image.convert("RGBA")
    counter: Counter[RGBA] = Counter()
    for y in range(rgba.height):
        for x in range(rgba.width):
            pixel = rgba.getpixel((x, y))
            assert isinstance(pixel, tuple)
            r, g, b, a = (int(v) for v in pixel)
            if a != 0:
                counter[(r, g, b, a)] += 1
    return counter


def check(image: Image.Image, max_colors: int, grid: int) -> list[str]:
    """問題点の一覧を返す。問題が無ければ空のリストを返す。"""
    problems: list[str] = []
    colors = count_colors(image)

    if len(colors) > max_colors:
        problems.append(f"色数が {len(colors)} 色あり、上限の {max_colors} 色を超えている")

    translucent = sum(n for (_, _, _, a), n in colors.items() if a != 255)
    if translucent:
        problems.append(f"半透明のピクセルが {translucent} 個ある")

    if image.width % grid or image.height % grid:
        problems.append(f"大きさ {image.width}x{image.height} が {grid} の倍数になっていない")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="ドット絵の画像を検査する")
    parser.add_argument("input", nargs="?", help="入力画像（省略時はサンプルのスライム）")
    parser.add_argument("--max-colors", type=int, default=16, help="色数の上限（既定値: 16）")
    parser.add_argument("--grid", type=int, default=8, help="幅と高さが倍数になるべき値（既定値: 8）")
    args = parser.parse_args()

    image = Image.open(args.input) if args.input else slime_image()
    colors = count_colors(image)

    print(f"大きさ: {image.width}x{image.height}")
    print(f"色数: {len(colors)}")
    for (r, g, b, a), n in colors.most_common():
        print(f"  #{r:02x}{g:02x}{b:02x} (alpha={a:3d}): {n} ピクセル")

    problems = check(image, args.max_colors, args.grid)
    for problem in problems:
        print(f"問題: {problem}")
    if not problems:
        print("問題は見つからなかった")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
