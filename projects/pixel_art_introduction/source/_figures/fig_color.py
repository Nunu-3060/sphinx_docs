"""第 5 章・第 6 章の図。"""

import colorsys
import math
import random
from pathlib import Path

import matplotlib
from PIL import Image, ImageDraw

from common import INK, PAPER, RGB, hstack, mix, save, scale, vstack
from make_palette import make_ramp

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# 球の陰影の段階（ランプの番号）
OUTLINE, SHADOW, REFLECT, BASE, LIGHT, HIGHLIGHT = range(6)
Levels = list[list[int | None]]

LIGHT_DIR = (-0.55, -0.6, 0.58)       # 光源の方向（左上手前）
REFLECT_DIR = (0.6, 0.7, -0.2)        # 反射光の方向（右下奥）


def _normalize(v: tuple[float, float, float]) -> tuple[float, float, float]:
    length = math.sqrt(sum(c * c for c in v))
    return (v[0] / length, v[1] / length, v[2] / length)


def sphere_levels(size: int, stage: int, pillow: bool = False) -> Levels:
    """球を塗り分けた段階の 2 次元配列を返す。None は球の外側。

    stage 1: 基本色のみ、2: 陰を追加、3: 明部を追加、4: ハイライトを追加、5: 反射光を追加
    pillow=True のときは光源を無視し、中心からの距離で塗り分ける（ピロー・シェーディング）。
    """
    radius = size / 2 - 1.5
    center = size / 2
    light = _normalize(LIGHT_DIR)
    reflect = _normalize(REFLECT_DIR)
    levels: Levels = [[None] * size for _ in range(size)]
    for py in range(size):
        for px in range(size):
            dx = (px + 0.5 - center) / radius
            dy = (py + 0.5 - center) / radius
            d2 = dx * dx + dy * dy
            if d2 > 1.0:
                continue
            nz = math.sqrt(1.0 - d2)
            if pillow:
                r = math.sqrt(d2)
                levels[py][px] = SHADOW if r > 0.75 else BASE if r > 0.45 else LIGHT if r > 0.15 else HIGHLIGHT
                continue
            intensity = dx * light[0] + dy * light[1] + nz * light[2]
            level = BASE
            if stage >= 2 and intensity < 0.2:
                level = SHADOW
                if stage >= 5 and dx * reflect[0] + dy * reflect[1] + nz * reflect[2] > 0.5:
                    level = REFLECT
            if stage >= 3 and intensity > 0.62:
                level = LIGHT
            if stage >= 4 and intensity > 0.93:
                level = HIGHLIGHT
            levels[py][px] = level
    # 輪郭：球の外側で、上下左右のいずれかが球の内側のピクセル
    for py in range(size):
        for px in range(size):
            if levels[py][px] is None:
                neighbors = [(px + 1, py), (px - 1, py), (px, py + 1), (px, py - 1)]
                if any(0 <= x < size and 0 <= y < size and levels[y][x] not in (None, OUTLINE)
                       for x, y in neighbors):
                    levels[py][px] = OUTLINE
    return levels


def levels_image(levels: Levels, ramp: list[RGB], background: RGB = PAPER) -> Image.Image:
    """段階の配列をランプの色で塗った画像を返す。"""
    size = len(levels)
    image = Image.new("RGBA", (size, size), (*background, 255))
    for y, row in enumerate(levels):
        for x, level in enumerate(row):
            if level is not None:
                color = INK if level == OUTLINE else ramp[level]
                image.putpixel((x, y), (*color, 255))
    return image


def ball_ramp(shift: float = 20.0) -> list[RGB]:
    """球の塗りに使う 6 色（先頭は輪郭用で、輪郭は INK で描くので使わない）。"""
    ramp = make_ramp(hue=350.0, steps=5, shift=shift, value_range=(0.3, 1.0), saturation_range=(0.25, 0.7))
    shadow, base, light, highlight = ramp[0], ramp[2], ramp[3], ramp[4]
    return [INK, shadow, mix(shadow, ramp[1], 0.6), base, light, highlight]


def ramps(out_dir: Path) -> None:
    """色相を固定したランプと、色相をずらしたランプ。"""
    rows: list[Image.Image] = []
    for shift in (0.0, 30.0):
        colors = make_ramp(hue=120.0, steps=6, shift=shift)
        row = Image.new("RGBA", (6, 1))
        for i, color in enumerate(colors):
            row.putpixel((i, 0), (*color, 255))
        rows.append(scale(row, 48))
    save(vstack(rows, gap=12), out_dir, "ramps.png")


def ramp_hsv(out_dir: Path) -> None:
    """2 つのランプの色相・彩度・明度の変化をグラフにする。"""
    fig, axes = plt.subplots(1, 3, figsize=(9, 2.8), dpi=100)
    for shift, style, label in ((0.0, "o--", "shift = 0"), (30.0, "s-", "shift = 30")):
        colors = make_ramp(hue=120.0, steps=6, shift=shift)
        hsv = [colorsys.rgb_to_hsv(r / 255, g / 255, b / 255) for r, g, b in colors]
        steps = list(range(1, len(colors) + 1))
        axes[0].plot(steps, [h * 360 for h, _, _ in hsv], style, label=label)
        axes[1].plot(steps, [s for _, s, _ in hsv], style, label=label)
        axes[2].plot(steps, [v for _, _, v in hsv], style, label=label)
    for ax, title in zip(axes, ("Hue [deg]", "Saturation", "Value")):
        ax.set_title(title)
        ax.set_xlabel("step (dark -> light)")
        ax.grid(alpha=0.3)
    axes[1].set_ylim(0, 1)
    axes[2].set_ylim(0, 1)
    axes[0].legend()
    fig.tight_layout()
    fig.savefig(out_dir / "ramp_hsv.png")
    plt.close(fig)


def ramp_spheres(out_dir: Path) -> None:
    """色相を固定したランプと、色相をずらしたランプで塗った球。"""
    images = [scale(levels_image(sphere_levels(24, 5), ball_ramp(shift)), 8) for shift in (0.0, 30.0)]
    save(hstack(images), out_dir, "ramp_spheres.png")


def shading_steps(out_dir: Path) -> None:
    """球に陰影を付けていく 5 段階。"""
    ramp = ball_ramp()
    images = [scale(levels_image(sphere_levels(24, stage), ramp), 6) for stage in range(1, 6)]
    save(hstack(images, gap=16), out_dir, "shading_steps.png")


def pillow_shading(out_dir: Path) -> None:
    """ピロー・シェーディングと、光源を意識した陰影。"""
    ramp = ball_ramp()
    images = [scale(levels_image(sphere_levels(24, 5, pillow=True), ramp), 8),
              scale(levels_image(sphere_levels(24, 5), ramp), 8)]
    save(hstack(images), out_dir, "pillow_shading.png")


def orphans(out_dir: Path) -> None:
    """孤立ドットが散らばった陰影と、整理した陰影。"""
    ramp = ball_ramp()
    clean = sphere_levels(24, 5)
    noisy = [row[:] for row in clean]
    rng = random.Random(3)
    order = [SHADOW, BASE, LIGHT]
    for y in range(2, 22):
        for x in range(2, 22):
            level = noisy[y][x]
            if level in order and rng.random() < 0.12:
                index = order.index(level) + rng.choice((-1, 1))
                noisy[y][x] = order[max(0, min(len(order) - 1, index))]
    images = [scale(levels_image(noisy, ramp), 8), scale(levels_image(clean, ramp), 8)]
    save(hstack(images), out_dir, "orphans.png")


BAYER_4 = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def dithering(out_dir: Path) -> None:
    """境界をそのまま接する場合、境界に市松模様を挟む場合、規則的ディザによるグラデーション。"""
    width, height = 64, 12
    dark: RGB = (59, 66, 128)
    light: RGB = (226, 160, 94)

    hard = Image.new("RGBA", (width, height))
    band = Image.new("RGBA", (width, height))
    bayer = Image.new("RGBA", (width, height))
    for y in range(height):
        for x in range(width):
            hard.putpixel((x, y), (*(dark if x < 32 else light), 255))
            in_band = 28 <= x < 36
            use_light = (x + y) % 2 == 0 if in_band else x >= 32
            band.putpixel((x, y), (*(light if use_light else dark), 255))
            threshold = (BAYER_4[y % 4][x % 4] + 0.5) / 16
            bayer.putpixel((x, y), (*(light if x / (width - 1) > threshold else dark), 255))
    rows = [scale(image, 8) for image in (hard, band, bayer)]
    save(vstack(rows, gap=12), out_dir, "dithering.png")


def antialias(out_dir: Path) -> None:
    """傾き 1:4 の境界線。アンチエイリアスなしと、中間色を 2 段階加えたもの。"""
    width, height = 32, 12
    tones = [PAPER, mix(PAPER, INK, 1 / 3), mix(PAPER, INK, 2 / 3), INK]
    sharp = Image.new("RGBA", (width, height), (*PAPER, 255))
    smooth = sharp.copy()
    sub = 6
    for y in range(height):
        for x in range(width):
            # ピクセルを細かく分割し、理想の境界線より下（塗る側）に入る割合（被覆率）を求める
            covered = sum(1 for sy in range(sub) for sx in range(sub)
                          if y + (sy + 0.5) / sub > 9.5 - (x + (sx + 0.5) / sub) / 4)
            coverage = covered / (sub * sub)
            if coverage >= 0.5:
                sharp.putpixel((x, y), (*INK, 255))
            level = 3 if coverage >= 0.8 else 2 if coverage >= 0.5 else 1 if coverage >= 0.2 else 0
            smooth.putpixel((x, y), (*tones[level], 255))
    columns = [vstack([scale(image, 8), scale(image, 2)], gap=16) for image in (sharp, smooth)]
    save(vstack(columns, gap=24), out_dir, "antialias.png")


def pyxel_palette(out_dir: Path) -> None:
    """Pyxel の既定のパレット（16 色）。"""
    import pyxel

    image = Image.new("RGBA", (8, 2))
    draw = ImageDraw.Draw(image)
    for i, value in enumerate(pyxel.DEFAULT_COLORS):
        color = ((value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF, 255)
        draw.point((i % 8, i // 8), fill=color)
    save(scale(image, 40), out_dir, "pyxel_palette.png")


def generate(out_dir: Path) -> None:
    ramps(out_dir)
    ramp_hsv(out_dir)
    ramp_spheres(out_dir)
    shading_steps(out_dir)
    pillow_shading(out_dir)
    orphans(out_dir)
    dithering(out_dir)
    antialias(out_dir)
    pyxel_palette(out_dir)
