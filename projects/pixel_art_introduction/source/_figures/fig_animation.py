"""第 9 章・第 10 章の図。"""

from pathlib import Path

from PIL import ImageDraw

from common import flatten, hstack, on_checker, save, scale
from reduce_colors import make_sample_image, reduce_colors
from sprite_data import hero_walk_images
from sprite_sheet import make_sheet, save_gif


def walk_frames(out_dir: Path) -> None:
    """歩行アニメーションの 4 フレーム。"""
    save(hstack([scale(flatten(frame), 8) for frame in hero_walk_images()], gap=16), out_dir, "walk_frames.png")


def walk_sheet(out_dir: Path) -> None:
    """4 フレームを横に並べたスプライトシート（区切り線付き）。"""
    factor = 6
    sheet = on_checker(make_sheet(hero_walk_images(), columns=4), factor)
    draw = ImageDraw.Draw(sheet)
    cell = 16 * factor
    for i in range(5):
        x = min(i * cell, sheet.width - 1)
        draw.line((x, 0, x, sheet.height - 1), fill=(220, 60, 60, 255), width=1)
    draw.line((0, 0, sheet.width - 1, 0), fill=(220, 60, 60, 255))
    draw.line((0, sheet.height - 1, sheet.width - 1, sheet.height - 1), fill=(220, 60, 60, 255))
    save(sheet, out_dir, "walk_sheet.png")


def walk_gifs(out_dir: Path) -> None:
    """表示時間を変えた歩行アニメーションの GIF。"""
    frames = hero_walk_images()
    for name, duration in (("walk_fast.gif", 80), ("walk.gif", 150), ("walk_slow.gif", 300)):
        save_gif(frames, out_dir / name, duration, 6)


def reduce_example(out_dir: Path) -> None:
    """元の画像、減色のみ、ディザリング付きの減色。"""
    original = make_sample_image()
    plain = scale(reduce_colors(original, 64, 8, dither=False), 4)
    dithered = scale(reduce_colors(original, 64, 8, dither=True), 4)
    save(hstack([original, plain, dithered], gap=16), out_dir, "reduce.png")


def generate(out_dir: Path) -> None:
    walk_frames(out_dir)
    walk_sheet(out_dir)
    walk_gifs(out_dir)
    reduce_example(out_dir)
