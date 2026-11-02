"""第 7 章「地形」: 高さと湿度によるバイオームの割り当て。

* biomes.png: 湿度の地図、高さと湿度からバイオームを引く表、バイオームの地図
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from color import hex_to_rgb
from common import FloatArray, IntArray, grid, normalize, output_dir, save_figure, setup_matplotlib
from heightmap import SEA_LEVEL, hillshade
from noise import fbm, perlin2
from terrain_erosion import eroded_terrain
from terrain_rivers import flow_network, river_segments

BoolArray = NDArray[np.bool_]

# バイオームの名前と色。番号は BIOME_TABLE と biome_map の戻り値で使う。
BIOMES = [
    ("海", "#3f6fa3"), ("湖", "#5a8fc8"), ("浜", "#e0d3a5"),
    ("砂漠", "#d9c27e"), ("草原", "#a4c46a"), ("季節林", "#5f9e48"), ("熱帯雨林", "#2f7a3a"),
    ("低木地", "#b3a36f"), ("落葉樹林", "#6c9a52"), ("温帯雨林", "#3f7f5a"),
    ("針葉樹林", "#4f6f4f"), ("裸地", "#8f877c"), ("ツンドラ", "#b8b8a0"), ("雪", "#f4f6f8"),
]
BIOME_INDEX = {name: index for index, (name, _) in enumerate(BIOMES)}

# 行: 標高帯（低い順）、列: 湿度（乾燥 → 湿潤）
ELEVATION_BANDS = ["低地", "丘陵", "山地", "高山"]
MOISTURE_BANDS = ["乾燥", "やや乾燥", "やや湿潤", "湿潤"]
BIOME_TABLE = [
    ["砂漠", "草原", "季節林", "熱帯雨林"],
    ["低木地", "草原", "落葉樹林", "温帯雨林"],
    ["低木地", "低木地", "針葉樹林", "針葉樹林"],
    ["裸地", "ツンドラ", "雪", "雪"],
]


def moisture_map(heights: FloatArray, water: BoolArray, seed: int = 11) -> FloatArray:
    """湿度（0〜1）。水（海・湖・川）に近いほど湿り、そこに大きな広がりのノイズを重ねる。

    最後に陸の湿度を順位に置き換え、0〜1 に均等に分布させる（どの湿度帯も同じ面積になる）。
    """
    from scipy.ndimage import distance_transform_edt

    size = heights.shape[0]
    distance = distance_transform_edt(~water)  # 最も近い水までの距離（格子の数）
    near_water = np.exp(-distance / 25.0)
    x, y = grid(size, size, 2.0)
    regional = normalize(fbm(perlin2, x, y, octaves=4, seed=seed))
    raw = 0.5 * near_water + 0.5 * regional
    land = heights >= SEA_LEVEL
    result = np.ones_like(raw)
    order = np.argsort(np.argsort(raw[land]))
    result[land] = order / max(len(order) - 1, 1)
    return result


def biome_map(heights: FloatArray, moisture: FloatArray, lake: BoolArray, seed: int = 12) -> IntArray:
    """高さと湿度から、表 BIOME_TABLE を引いてバイオームの番号を決める。

    境界が直線的にならないように、表を引く前に高さと湿度へ細かいノイズを少し足す。
    """
    size = heights.shape[0]
    x, y = grid(size, size, 24.0)
    jitter = fbm(perlin2, x, y, octaves=3, seed=seed)
    elevation = (heights - SEA_LEVEL) / (1.0 - SEA_LEVEL) + 0.03 * jitter  # 海面からの相対的な高さ
    wet = moisture + 0.05 * jitter
    band = np.clip((elevation / 0.25).astype(np.int64), 0, 3)
    column = np.clip((wet / 0.25).astype(np.int64), 0, 3)
    table = np.array([[BIOME_INDEX[name] for name in row] for row in BIOME_TABLE])
    result = table[band, column]
    result = np.where(elevation < 0.02, BIOME_INDEX["浜"], result)
    result = np.where(lake, BIOME_INDEX["湖"], result)
    result = np.where(heights < SEA_LEVEL, BIOME_INDEX["海"], result)
    return result.astype(np.int64)


def biome_colors(biomes: IntArray) -> FloatArray:
    """バイオームの番号を色にする。"""
    palette = np.array([hex_to_rgb(code) for _, code in BIOMES])
    result: FloatArray = palette[biomes]
    return result


def terrain_layers() -> tuple[FloatArray, FloatArray, IntArray, IntArray, FloatArray]:
    """侵食した地形から、高さ・湿度・バイオーム・流向・集水量をまとめて作る。"""
    heights = eroded_terrain()
    lake_depth, receivers, accumulation = flow_network(heights)
    land = heights >= SEA_LEVEL
    lake = (lake_depth > 1e-3) & land
    river = (accumulation >= 60) & land
    moisture = moisture_map(heights, ~land | lake | river)
    receivers = np.where(lake.reshape(-1), -1, receivers)  # 湖の中には川を描かない
    return heights, moisture, biome_map(heights, moisture, lake), receivers, accumulation


def draw_biomes(file_name: str) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    from matplotlib.patches import Rectangle

    heights, moisture, biomes, receivers, accumulation = terrain_layers()
    land = heights >= SEA_LEVEL
    figure = plt.figure(figsize=(12, 4.3))
    grid_spec = figure.add_gridspec(1, 3, width_ratios=[1.0, 1.05, 1.0])

    ax = figure.add_subplot(grid_spec[0, 0])
    cmap = plt.get_cmap("YlGnBu").with_extremes(bad="#cccccc")
    ax.imshow(np.where(land, moisture, np.nan), cmap=cmap, vmin=0, vmax=1)
    ax.set_title("湿度（水の近くと大きなノイズ）", fontsize=10)
    ax.set_axis_off()

    ax = figure.add_subplot(grid_spec[0, 1])
    for row, names in enumerate(BIOME_TABLE):
        for column, name in enumerate(names):
            color = hex_to_rgb(dict(BIOMES)[name])
            ax.add_patch(Rectangle((column, row), 1, 1, facecolor=color, edgecolor="white", linewidth=1.5))
            text_color = "white" if name in ("熱帯雨林", "温帯雨林", "針葉樹林") else "black"
            ax.text(column + 0.5, row + 0.5, name, ha="center", va="center", fontsize=9, color=text_color)
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.set_xticks(np.arange(4) + 0.5, MOISTURE_BANDS, fontsize=8)
    ax.set_yticks(np.arange(4) + 0.5, ELEVATION_BANDS, fontsize=8)
    ax.set_xlabel("湿度 →")
    ax.set_ylabel("標高 →")
    ax.set_aspect("equal")
    ax.tick_params(length=0)
    for side in ax.spines.values():
        side.set_visible(False)
    ax.set_title("標高と湿度からバイオームを引く表", fontsize=10)

    ax = figure.add_subplot(grid_spec[0, 2])
    shade = hillshade(np.maximum(heights, SEA_LEVEL))
    image = biome_colors(biomes) * (0.55 + 0.6 * shade[..., None])
    ax.imshow(np.clip(image, 0, 1))
    segments, values = river_segments(receivers, accumulation, threshold=60)
    ax.add_collection(LineCollection(list(segments), linewidths=0.3 + 0.6 * np.log10(values / 60), colors="#2a62b0"))
    ax.set_title("バイオームの地図（陰影と川を重ねた）", fontsize=10)
    ax.set_axis_off()
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_biomes("biomes.png")


if __name__ == "__main__":
    main()
