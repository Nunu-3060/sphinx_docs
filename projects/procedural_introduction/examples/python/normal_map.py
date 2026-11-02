"""第 4 章「パターンとマテリアル」: ハイトマップから法線マップを作る図を作る。

* normal_map.png: ハイトマップ → 法線マップ → 光の向きを変えて陰影を付けた結果
* normal_strength.png: 凹凸の強さ（strength）を変えた陰影
"""

from __future__ import annotations

import numpy as np

from common import FloatArray, grid, output_dir, setup_matplotlib
from noise import fbm, perlin2, worley2
from texture import encode_normal, height_to_normal, shade, show_panels, smoothstep

SIZE = 320
ALBEDO = (0.72, 0.70, 0.66)  # 石の色（陰影の違いを見やすくするため一様にする）


def stone_height(x: FloatArray, y: FloatArray, seed: int = 0) -> FloatArray:
    """丸みのある石を並べたハイトマップ（0〜1）。境界からの距離 F2−F1 で盛り上げ、細かな凹凸を足す。"""
    f1, f2, _ = worley2(x, y, seed=seed, jitter=0.8)
    dome = smoothstep(0.02, 0.4, f2 - f1)
    detail = fbm(perlin2, x * 6.0, y * 6.0, octaves=4, seed=seed + 1)
    return np.clip(0.8 * dome + 0.06 * detail + 0.1, 0.0, 1.0)


def draw_normal_map(file_name: str) -> None:
    x, y = grid(SIZE, SIZE, scale=4.0)
    height = stone_height(x, y, seed=5)
    normal = height_to_normal(height, strength=25.0)
    albedo = np.broadcast_to(np.array(ALBEDO), (SIZE, SIZE, 3))
    images = [height, encode_normal(normal), shade(normal, albedo, light=(-0.6, 0.6, 0.5)),
              shade(normal, albedo, light=(0.8, -0.2, 0.5))]
    titles = ["ハイトマップ", "法線マップ（RGB = xyz）", "陰影（左上から光）", "陰影（右から光）"]
    show_panels(images, titles, output_dir(__file__) / file_name)


def draw_strength(file_name: str) -> None:
    x, y = grid(SIZE, SIZE, scale=4.0)
    height = stone_height(x, y, seed=5)
    albedo = np.broadcast_to(np.array(ALBEDO), (SIZE, SIZE, 3))
    strengths = (6.0, 25.0, 100.0)
    images = [shade(height_to_normal(height, strength=s), albedo) for s in strengths]
    show_panels(images, [f"strength = {s:g}" for s in strengths], output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_normal_map("normal_map.png")
    draw_strength("normal_strength.png")


if __name__ == "__main__":
    main()
