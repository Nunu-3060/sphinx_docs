"""第 5 章「規則から生まれる模様」: 左右対称化とマスクによるドット絵スプライトの生成。

* sprite_steps.png: マスク → ランダムに埋める → 左右対称にする → 輪郭を付ける → 色を付ける
* sprites_creatures.png: 生き物のマスクから作った多数のスプライト
* sprites_ships.png: 宇宙船のマスクから作った多数のスプライト
"""

from __future__ import annotations

import math

import numpy as np
from numpy.typing import NDArray

from color import oklch_to_srgb
from common import FloatArray, output_dir, save_image, setup_matplotlib
from texture import show_panels

IntGrid = NDArray[np.int64]

# マスク（左半分）。0: 常に空、1: ランダムに体か空、2: 常に体、3: 目（常に置く）
# 右端の列が体の中心線になる。
CREATURE_MASK = [
    "000000",
    "000011",
    "000111",
    "001132",
    "001122",
    "011122",
    "011112",
    "111112",
    "011112",
    "001112",
    "001101",
    "011001",
]
SHIP_MASK = [
    "000001",
    "000011",
    "000011",
    "000112",
    "000112",
    "001112",
    "001132",
    "011112",
    "111112",
    "111112",
    "011110",
    "001000",
]

EMPTY, BODY, ACCENT, EYE, OUTLINE = 0, 1, 2, 3, 4


def parse_mask(rows: list[str]) -> IntGrid:
    return np.array([[int(c) for c in row] for row in rows], dtype=np.int64)


def fill_half(mask: IntGrid, rng: np.random.Generator, density: float = 0.55, accent: float = 0.25) -> IntGrid:
    """マスクの左半分を乱数で埋める。値 1 のセルは確率 density で体になり、体の一部は差し色になる。"""
    half = np.zeros_like(mask)
    random = rng.random(mask.shape)
    half[(mask == 1) & (random < density)] = BODY
    half[mask == 2] = BODY
    half[(half == BODY) & (rng.random(mask.shape) < accent)] = ACCENT
    half[mask == 3] = EYE
    return half


def mirror(half: IntGrid) -> IntGrid:
    """左半分を左右反転して右側に付け、左右対称にする。"""
    return np.concatenate([half, half[:, ::-1]], axis=1)


def add_outline(sprite: IntGrid) -> IntGrid:
    """空のセルのうち、上下左右のどれかが体に接しているものを輪郭にする。周りに 1 セルの余白を足す。"""
    padded = np.pad(sprite, 1)
    filled = padded != EMPTY
    neighbor = np.zeros_like(filled)
    neighbor[1:, :] |= filled[:-1, :]
    neighbor[:-1, :] |= filled[1:, :]
    neighbor[:, 1:] |= filled[:, :-1]
    neighbor[:, :-1] |= filled[:, 1:]
    result = padded.copy()
    result[(padded == EMPTY) & neighbor] = OUTLINE
    return result


def colorize(sprite: IntGrid, hue: float, background: FloatArray) -> FloatArray:
    """セルの種類を色にする。体は上ほど明るくし、差し色は色相をずらす（OKLCH で明るさをそろえる）。"""
    height, width = sprite.shape
    rows = np.repeat(np.linspace(0.0, 1.0, height)[:, None], width, axis=1)
    hues = np.full(sprite.shape, hue)
    body = oklch_to_srgb(0.78 - 0.2 * rows, np.full(sprite.shape, 0.13), hues)
    accent = oklch_to_srgb(0.7 - 0.15 * rows, np.full(sprite.shape, 0.15), hues + 2.2)
    outline = oklch_to_srgb(np.full(sprite.shape, 0.25), np.full(sprite.shape, 0.05), hues)
    image = np.broadcast_to(background, (height, width, 3)).copy()
    image[sprite == BODY] = body[sprite == BODY]
    image[sprite == ACCENT] = accent[sprite == ACCENT]
    image[sprite == OUTLINE] = outline[sprite == OUTLINE]
    image[sprite == EYE] = (1.0, 1.0, 1.0)
    return image


def make_sprite(mask: IntGrid, seed: int, background: FloatArray) -> FloatArray:
    """マスクとシードから、色の付いたスプライトを 1 体作る。"""
    rng = np.random.default_rng(seed)
    sprite = add_outline(mirror(fill_half(mask, rng)))
    return colorize(sprite, hue=rng.random() * 2.0 * math.pi, background=background)


def sprite_sheet(mask: IntGrid, columns: int, rows: int, scale: int, seed: int) -> FloatArray:
    """スプライトを格子状に並べ、1 セルを scale × scale 画素に拡大した画像。"""
    background = np.array([0.93, 0.93, 0.95])
    sprites = [make_sprite(mask, seed + index, background) for index in range(columns * rows)]
    height, width = sprites[0].shape[:2]
    gap = 1
    sheet = np.ones((rows * (height + gap) + gap, columns * (width + gap) + gap, 3))
    for index, sprite in enumerate(sprites):
        row, column = divmod(index, columns)
        top = gap + row * (height + gap)
        left = gap + column * (width + gap)
        sheet[top:top + height, left:left + width] = sprite
    return np.repeat(np.repeat(sheet, scale, axis=0), scale, axis=1)


def labels_to_gray(sprite: IntGrid) -> FloatArray:
    """途中段階の表示用: 空を白、体を灰、差し色を薄い灰、目と輪郭を黒にする。"""
    levels = np.array([1.0, 0.45, 0.7, 0.0, 0.1])
    result: FloatArray = levels[sprite]
    return result


def draw_steps(file_name: str) -> None:
    mask = parse_mask(CREATURE_MASK)
    rng = np.random.default_rng(7)
    half = fill_half(mask, rng)
    full = mirror(half)
    outlined = add_outline(full)
    colored = colorize(outlined, hue=rng.random() * 2.0 * math.pi, background=np.array([0.93, 0.93, 0.95]))
    mask_view = np.array([1.0, 0.7, 0.35, 0.0])[mask]

    def pad(image: FloatArray) -> FloatArray:
        """大きさをそろえるため、左右対称にする前の半分の画像の右側と、周りを余白で埋める。"""
        target_h, target_w = outlined.shape
        top = (target_h - image.shape[0]) // 2
        left = (target_w - image.shape[1]) // 2
        canvas = np.ones((target_h, target_w) + image.shape[2:])
        canvas[top:top + image.shape[0], left:left + image.shape[1]] = image
        return canvas

    images = [pad(mask_view), pad(labels_to_gray(half)), pad(labels_to_gray(full)), labels_to_gray(outlined),
              colored]
    titles = ["マスク（左半分）", "乱数で埋める", "左右対称にする", "輪郭を付ける", "色を付ける"]
    show_panels(images, titles, output_dir(__file__) / file_name, size=2.4, interpolation="nearest")


def main() -> None:
    setup_matplotlib()
    draw_steps("sprite_steps.png")
    directory = output_dir(__file__)
    save_image(sprite_sheet(parse_mask(CREATURE_MASK), 12, 5, scale=5, seed=100), directory / "sprites_creatures.png")
    save_image(sprite_sheet(parse_mask(SHIP_MASK), 12, 5, scale=5, seed=500), directory / "sprites_ships.png")


if __name__ == "__main__":
    main()
