"""第 7 章の図。"""

from pathlib import Path

from PIL import Image

from common import INK, flatten, hstack, mix, save, scale, vstack
from sprite_data import HERO, HERO_PALETTE, GRASS_TILE, GRASS_PALETTE, make_image

# 陰の色を基本色に置き換える対応表（基本色だけの段階を作るため）
FLAT = {"H": "h", "S": "s", "B": "b", "P": "p"}


def silhouette() -> Image.Image:
    rows = ["".join("K" if c != "." else "." for c in row) for row in HERO]
    return make_image(rows, HERO_PALETTE)


def flat() -> Image.Image:
    rows = ["".join(FLAT.get(c, c) for c in row) for row in HERO]
    return make_image(rows, HERO_PALETTE)


def colored_outline(selective: bool) -> Image.Image:
    """輪郭を隣接する色の暗い色に置き換える。

    selective=True のときは、光の当たる側（上と左）の輪郭を明るめにする（セルアウト）。
    """
    height, width = len(HERO), len(HERO[0])
    image = make_image(HERO, HERO_PALETTE)
    for y in range(height):
        for x in range(width):
            if HERO[y][x] != "K":
                continue
            # 下・右・上・左の順に、輪郭でも透明でもない隣のピクセルを探す
            for dx, dy, lit in ((0, 1, True), (1, 0, True), (0, -1, False), (-1, 0, False)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and HERO[ny][nx] not in ".Ke":
                    neighbor = HERO_PALETTE[HERO[ny][nx]]
                    amount = 0.45 if selective and lit else 0.7
                    color = mix(neighbor, INK, amount)
                    image.putpixel((x, y), (*color, 255))
                    break
    return image


def no_outline() -> Image.Image:
    rows = [row.replace("K", ".") for row in HERO]
    return make_image(rows, HERO_PALETTE)


def character_steps(out_dir: Path) -> None:
    """シルエット → 基本色 → 陰影 → 輪郭の調整。"""
    images = [silhouette(), flat(), make_image(HERO, HERO_PALETTE), colored_outline(True)]
    save(hstack([scale(flatten(image), 8) for image in images], gap=16), out_dir, "character_steps.png")


def outline_styles(out_dir: Path) -> None:
    """黒っぽい輪郭、色付きの輪郭、セルアウト、輪郭なし。"""
    images = [make_image(HERO, HERO_PALETTE), colored_outline(False), colored_outline(True), no_outline()]
    save(hstack([scale(flatten(image), 8) for image in images], gap=16), out_dir, "outline_styles.png")


def visibility(out_dir: Path) -> None:
    """明るい背景・草地・暗い背景の上に置いて見え方を確認する（上段は 4 倍、下段は等倍）。"""
    hero = make_image(HERO, HERO_PALETTE)
    grass = make_image(GRASS_TILE, GRASS_PALETTE)
    light = Image.new("RGBA", (32, 32), (236, 236, 228, 255))
    field = Image.new("RGBA", (32, 32))
    for y in (0, 16):
        for x in (0, 16):
            field.paste(grass, (x, y))
    dark = Image.new("RGBA", (32, 32), (30, 30, 46, 255))
    scenes: list[Image.Image] = []
    for background in (light, field, dark):
        scene = background.copy()
        scene.alpha_composite(hero, (8, 8))
        scenes.append(scene)
    top = hstack([scale(scene, 4) for scene in scenes], gap=16)
    bottom = hstack(scenes, gap=16 + 96)
    save(vstack([top, bottom], gap=16), out_dir, "visibility.png")


def generate(out_dir: Path) -> None:
    character_steps(out_dir)
    outline_styles(out_dir)
    visibility(out_dir)
