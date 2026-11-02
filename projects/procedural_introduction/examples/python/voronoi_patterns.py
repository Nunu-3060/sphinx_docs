"""第 4 章「パターンとマテリアル」: ボロノイ図（セルラーノイズ）を使った模様の図を作る。

* voronoi_patterns.png: 石畳・ひび割れ・細胞
* voronoi_steps.png: 石畳を作る手順（F2−F1 → 目地のマスク → 石ごとの色 → 仕上げ）
"""

from __future__ import annotations

import numpy as np

from color import hex_to_rgb
from common import FloatArray, grid, output_dir, setup_matplotlib
from noise import fbm, perlin2, worley2
from texture import mix, show_panels, smoothstep

SIZE = 320


def cobblestone(x: FloatArray, y: FloatArray, seed: int = 0) -> tuple[FloatArray, FloatArray, FloatArray, FloatArray]:
    """石畳。(色, 石のマスク, 境界からの距離 F2−F1, 石ごとの乱数) を返す。"""
    # 座標を少し歪めて、石の輪郭を直線でなくする。
    wx = x + 0.15 * fbm(perlin2, x * 2.0, y * 2.0, octaves=3, seed=seed + 10)
    wy = y + 0.15 * fbm(perlin2, x * 2.0, y * 2.0, octaves=3, seed=seed + 20)
    f1, f2, cell = worley2(wx, wy, seed=seed, jitter=0.8)
    edge = f2 - f1
    stone = smoothstep(0.05, 0.12, edge)  # 目地（境界の近く）を 0、石を 1 にする
    bevel = smoothstep(0.05, 0.35, edge)  # 石の縁ほど暗くして、丸みを感じさせる
    detail = fbm(perlin2, x * 8.0, y * 8.0, octaves=4, seed=seed + 30)
    stone_color = mix(hex_to_rgb("#6b6862"), hex_to_rgb("#a59f94"), cell)
    stone_color = stone_color * (0.75 + 0.25 * bevel + 0.12 * detail)[..., None]
    mortar_color = mix(hex_to_rgb("#3a3128"), hex_to_rgb("#5a4d3e"), np.clip(detail * 0.5 + 0.5, 0.0, 1.0))
    return np.clip(mix(mortar_color, stone_color, stone), 0.0, 1.0), stone, edge, cell


def cracks(x: FloatArray, y: FloatArray, seed: int = 0) -> FloatArray:
    """乾いた泥のひび割れ。大小 2 段階の網目を重ねる。"""
    base = fbm(perlin2, x * 1.5, y * 1.5, octaves=5, seed=seed)
    ground = mix(hex_to_rgb("#9c7b55"), hex_to_rgb("#c9a978"), np.clip(base * 0.8 + 0.5, 0.0, 1.0))
    darkness = np.zeros_like(x)
    for scale, width, strength, offset in ((1.0, 0.035, 1.0, 0), (2.7, 0.025, 0.55, 1)):
        # ノイズで座標を歪め、境界線を曲がりくねらせる。
        wx = x * scale + 0.25 * fbm(perlin2, x * 3.0, y * 3.0, octaves=3, seed=seed + 10 + offset)
        wy = y * scale + 0.25 * fbm(perlin2, x * 3.0, y * 3.0, octaves=3, seed=seed + 20 + offset)
        f1, f2, _ = worley2(wx, wy, seed=seed + 40 + offset)
        darkness = np.maximum(darkness, strength * smoothstep(width, width * 0.3, f2 - f1))
    return ground * (1.0 - 0.8 * darkness)[..., None]


def cells(x: FloatArray, y: FloatArray, seed: int = 0) -> FloatArray:
    """顕微鏡で見た細胞。F1 で核、F2−F1 で細胞膜、セルの乱数で細胞ごとの色を作る。"""
    wx = x + 0.1 * fbm(perlin2, x * 2.0, y * 2.0, octaves=3, seed=seed + 10)
    wy = y + 0.1 * fbm(perlin2, x * 2.0, y * 2.0, octaves=3, seed=seed + 20)
    f1, f2, cell = worley2(wx, wy, seed=seed, jitter=0.7)
    body = mix(hex_to_rgb("#f2b5c8"), hex_to_rgb("#d98bb5"), cell)
    body = body * (1.0 - 0.25 * smoothstep(0.1, 0.6, f1))[..., None]  # 中心から離れるほど少し暗く
    nucleus = smoothstep(0.17, 0.13, f1)
    membrane = smoothstep(0.06, 0.02, f2 - f1)
    color = mix(body, hex_to_rgb("#5b2a6e"), nucleus)
    return mix(color, hex_to_rgb("#fbeef3"), membrane)


def draw_patterns(file_name: str) -> None:
    x, y = grid(SIZE, SIZE, scale=5.0)
    stones, _, _, _ = cobblestone(x, y, seed=1)
    images = [stones, cracks(x * 0.8, y * 0.8, seed=2), cells(x, y, seed=3)]
    show_panels(images, ["石畳", "ひび割れ", "細胞"], output_dir(__file__) / file_name, size=3.6)


def draw_steps(file_name: str) -> None:
    x, y = grid(SIZE, SIZE, scale=5.0)
    stones, mask, edge, cell = cobblestone(x, y, seed=1)
    colors = mix(hex_to_rgb("#6b6862"), hex_to_rgb("#a59f94"), cell)
    images = [np.clip(edge * 2.5, 0.0, 1.0), mask, colors, stones]
    titles = ["F2 − F1", "目地のマスク（smoothstep）", "石ごとの乱数で色を選ぶ", "縁の陰影と細部を加える"]
    show_panels(images, titles, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_patterns("voronoi_patterns.png")
    draw_steps("voronoi_steps.png")


if __name__ == "__main__":
    main()
