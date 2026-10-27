"""第 8 章の図。"""

import random
from pathlib import Path

from PIL import Image

from common import RGB, hstack, mix, save, scale
from sprite_data import GRASS_PALETTE, GRASS_TILE, make_image, slime_image, hero_image
from tile_preview import tile_image

TILE = 16
SAND: RGB = (222, 196, 140)
SAND_DARK: RGB = (190, 160, 110)
SAND_LIGHT: RGB = (238, 220, 172)

# 草地と道の境界の高さ（列ごと）。左右の端の値をそろえ、隣のタイルとつながるようにする。
EDGE_OFFSETS = [0, 0, 1, 1, 1, 0, 0, -1, -1, -1, 0, 0, 1, 0, 0, 0]


def grass() -> Image.Image:
    return make_image(GRASS_TILE, GRASS_PALETTE)


def sand() -> Image.Image:
    """小石を散らした道のタイル。小石の位置は 16 で割った余りを使い、端をまたいでもつながるようにする。"""
    image = Image.new("RGBA", (TILE, TILE), (*SAND, 255))
    for x, y in [(2, 3), (9, 1), (13, 6), (5, 10), (11, 12), (15, 9), (7, 14)]:
        image.putpixel((x % TILE, y % TILE), (*SAND_DARK, 255))
        image.putpixel(((x - 1) % TILE, (y - 1) % TILE), (*SAND_LIGHT, 255))
    return image


def edge(top_is_grass: bool) -> Image.Image:
    """草地と道の境界のタイル。"""
    image = sand()
    grass_tile = grass()
    dark = GRASS_PALETTE["d"]
    for x in range(TILE):
        boundary = 9 + EDGE_OFFSETS[x] if top_is_grass else 6 - EDGE_OFFSETS[x]
        for y in range(TILE):
            if top_is_grass and y < boundary or not top_is_grass and y > boundary:
                pixel = grass_tile.getpixel((x, y))
                assert isinstance(pixel, tuple)
                image.putpixel((x, y), pixel)
            elif y == boundary:
                image.putpixel((x, y), (*(dark if top_is_grass else mix(SAND, dark, 0.35)), 255))
    return image


def flower() -> Image.Image:
    image = grass()
    for x, y, color in [(7, 6, (250, 250, 240)), (6, 7, (250, 250, 240)), (8, 7, (250, 250, 240)),
                        (7, 8, (250, 250, 240)), (7, 7, (240, 200, 60))]:
        image.putpixel((x, y), (*color, 255))
    return image


def bad_grass() -> Image.Image:
    """右端と下端に濃い線があり、左上から右下へ暗くなるタイル（継ぎ目が目立つ例）。"""
    image = grass()
    for y in range(TILE):
        for x in range(TILE):
            pixel = image.getpixel((x, y))
            assert isinstance(pixel, tuple)
            color: RGB = (int(pixel[0]), int(pixel[1]), int(pixel[2]))
            color = mix(color, (30, 70, 40), (x + y) / 60)
            if x == TILE - 1 or y == TILE - 1:
                color = mix(color, (20, 50, 30), 0.5)
            image.putpixel((x, y), (*color, 255))
    return image


def tile_seams(out_dir: Path) -> None:
    """継ぎ目が目立つタイルと、継ぎ目が目立たないタイルを 3×3 枚並べたもの。"""
    save(hstack([scale(tile_image(bad_grass(), 3, 3), 4), scale(tile_image(grass(), 3, 3), 4)]), out_dir,
         "tile_seams.png")


def tile_set(out_dir: Path) -> None:
    """マップに使うタイルの一覧。"""
    tiles = [grass(), flower(), edge(True), sand(), edge(False)]
    save(hstack([scale(tile, 6) for tile in tiles], gap=12), out_dir, "tile_set.png")


def tile_map(out_dir: Path) -> None:
    """タイルを並べたマップにキャラクターを置いたもの。"""
    layout = [
        "gggfggggggg",
        "gggggggfggg",
        "fgggggggggg",
        "ttttttttttt",
        "sssssssssss",
        "bbbbbbbbbbb",
        "ggggfgggggg",
    ]
    tiles = {"g": grass(), "f": flower(), "t": edge(True), "s": sand(), "b": edge(False)}
    image = Image.new("RGBA", (len(layout[0]) * TILE, len(layout) * TILE))
    for row, line in enumerate(layout):
        for column, key in enumerate(line):
            image.paste(tiles[key], (column * TILE, row * TILE))
    image.alpha_composite(hero_image(), (4 * TILE, 4 * TILE - 6))
    image.alpha_composite(slime_image(), (7 * TILE, 1 * TILE))
    save(scale(image, 3), out_dir, "tile_map.png")


def busy_grass() -> Image.Image:
    """明暗差が大きく、細かい模様の草地（キャラクターが埋もれやすい例）。"""
    rng = random.Random(7)
    colors: list[RGB] = [(40, 120, 50), (120, 200, 60), (30, 70, 120), (210, 220, 90)]
    image = Image.new("RGBA", (TILE, TILE))
    for y in range(TILE):
        for x in range(TILE):
            image.putpixel((x, y), (*rng.choice(colors), 255))
    return image


def contrast(out_dir: Path) -> None:
    """模様の強い背景と落ち着いた背景に、同じキャラクターを置いたもの。"""
    scenes: list[Image.Image] = []
    for background in (busy_grass(), grass()):
        scene = tile_image(background, 3, 2)
        scene.alpha_composite(hero_image(), (16, 8))
        scene.alpha_composite(slime_image(), (30, 14))
        scenes.append(scale(scene, 5))
    save(hstack(scenes), out_dir, "contrast.png")


def generate(out_dir: Path) -> None:
    tile_seams(out_dir)
    tile_set(out_dir)
    tile_map(out_dir)
    contrast(out_dir)
