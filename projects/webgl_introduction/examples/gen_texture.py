"""WebGL のサンプルで使うテクスチャ画像を生成する。

使い方:
    python gen_texture.py                  # assets/ に 2 枚の PNG を出力
    python gen_texture.py --output-dir out

生成する画像:
    checker.png : 256 x 256 の市松模様。フィルタリングやラッピングの確認用
    uvgrid.png  : 512 x 512 の UV グリッド。各マスに列 (A-H) と行 (1-8) の
                  ラベルを描くので、テクスチャ座標の向きや上下反転を確認できる

Pillow (PIL) が必要。
"""

from __future__ import annotations

import argparse
import colorsys
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RGB = tuple[int, int, int]


def make_checker(
    size: int, cells: int, color1: RGB, color2: RGB
) -> Image.Image:
    """cells x cells マスの市松模様を作る。"""
    image = Image.new("RGB", (size, size), color1)
    draw = ImageDraw.Draw(image)
    cell = size // cells
    for row in range(cells):
        for col in range(cells):
            if (row + col) % 2 == 1:
                x, y = col * cell, row * cell
                draw.rectangle((x, y, x + cell - 1, y + cell - 1), fill=color2)
    return image


def make_uv_grid(size: int, cells: int) -> Image.Image:
    """ラベル付きの UV グリッドを作る。

    画像の左下が UV 座標 (0, 0)、右上が (1, 1) に対応するものとして、
    左下のマスを A1、右上のマスを H8 とする。
    """
    image = Image.new("RGB", (size, size))
    draw = ImageDraw.Draw(image)
    cell = size // cells
    font = ImageFont.load_default(size=cell // 3)
    for row in range(cells):
        for col in range(cells):
            # 横方向に色相、縦方向に明るさを変える
            hue = col / cells
            value = 0.55 + 0.4 * (cells - 1 - row) / (cells - 1)
            r, g, b = colorsys.hsv_to_rgb(hue, 0.55, value)
            color = (int(r * 255), int(g * 255), int(b * 255))
            x, y = col * cell, row * cell
            draw.rectangle(
                (x, y, x + cell - 1, y + cell - 1),
                fill=color,
                outline=(40, 40, 40),
            )
            # 画像の上端の行が UV の v = 1 側なので、行番号は下から数える
            label = f"{chr(ord('A') + col)}{cells - row}"
            draw.text(
                (x + cell / 2, y + cell / 2),
                label,
                fill=(20, 20, 20),
                font=font,
                anchor="mm",
            )
    # 上方向を示す矢印（画像の上端中央）
    cx = size // 2
    draw.polygon(
        [(cx, 4), (cx - cell // 4, cell // 4), (cx + cell // 4, cell // 4)],
        fill=(255, 255, 255),
        outline=(0, 0, 0),
    )
    return image


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="テクスチャ画像を生成します。")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "assets",
        help="出力先のフォルダー（既定: このスクリプトのフォルダーの assets）",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    output_dir: Path = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    images = {
        "checker.png": make_checker(256, 8, (235, 235, 235), (60, 60, 60)),
        "uvgrid.png": make_uv_grid(512, 8),
    }
    for name, image in images.items():
        path = output_dir / name
        image.save(path, optimize=True)
        print(f"{path} を出力しました。")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
