"""第 2 章・第 3 章の図。"""

import io
from pathlib import Path

from PIL import Image

from common import PANEL, flatten, hstack, on_checker, save, scale, with_grid
from sprite_data import slime_image


def pixel_grid(out_dir: Path) -> None:
    """等倍・4 倍・16 倍（格子付き）のスライム。"""
    slime = slime_image()
    images = [on_checker(slime, 1), on_checker(slime, 4), with_grid(on_checker(slime, 1), 16)]
    save(hstack(images), out_dir, "pixel_grid.png")


def scaling(out_dir: Path) -> None:
    """最近傍補間とバイリニア補間による 8 倍拡大の比較。"""
    slime = flatten(slime_image())
    size = (slime.width * 8, slime.height * 8)
    nearest = slime.resize(size, Image.Resampling.NEAREST)
    bilinear = slime.resize(size, Image.Resampling.BILINEAR)
    save(hstack([nearest, bilinear]), out_dir, "scaling.png")


def non_integer(out_dir: Path) -> None:
    """整数倍（3 倍）と非整数倍（2.5 倍）の拡大の比較。見やすいようにさらに 4 倍にしてある。"""
    slime = flatten(slime_image())
    three = slime.resize((48, 48), Image.Resampling.NEAREST)
    two_and_half = slime.resize((40, 40), Image.Resampling.NEAREST)
    save(hstack([scale(three, 4), scale(two_and_half, 4)]), out_dir, "non_integer.png")


def png_jpeg(out_dir: Path) -> list[int]:
    """PNG と JPEG で保存した画像の比較。各画像の色数を返す。"""
    slime = flatten(slime_image(), PANEL).convert("RGB")
    buffer = io.BytesIO()
    slime.save(buffer, format="JPEG", quality=75)
    jpeg = Image.open(io.BytesIO(buffer.getvalue())).convert("RGB")
    save(hstack([scale(slime, 8), scale(jpeg, 8)]), out_dir, "png_jpeg.png")
    return [len(image.getcolors(65536) or []) for image in (slime, jpeg)]


def generate(out_dir: Path) -> None:
    pixel_grid(out_dir)
    scaling(out_dir)
    non_integer(out_dir)
    png_jpeg(out_dir)
