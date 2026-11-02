"""ハイトマップ（高さの 2 次元配列）を作り、表示する関数（第 7 章）。

ハイトマップは heights[行 y, 列 x] の実数の配列で、格子の間隔を 1 とする。高さは
おおむね 0〜1 にそろえ、斜面の傾きを計算するときは height_scale を掛けて、格子の間隔と
同じ単位にする（256 × 256 の地図で height_scale = 48 なら、最高点の高さは幅の 3/16）。
"""

from __future__ import annotations

import numpy as np

from color import gradient_map, hex_to_rgb
from common import FloatArray, grid, normalize
from noise import fbm, perlin2

# 標高の色（0〜1 の値に対する色）。海面の高さを SEA_LEVEL とする。
SEA_LEVEL = 0.35
TERRAIN_STOPS = [
    (0.00, hex_to_rgb("#1d3f6e")),
    (SEA_LEVEL - 0.001, hex_to_rgb("#4a86b8")),
    (SEA_LEVEL, hex_to_rgb("#d8c99b")),
    (SEA_LEVEL + 0.04, hex_to_rgb("#7fae5a")),
    (0.60, hex_to_rgb("#4e7d3a")),
    (0.75, hex_to_rgb("#8a7a5c")),
    (0.90, hex_to_rgb("#b5aca0")),
    (1.00, hex_to_rgb("#ffffff")),
]


def fbm_heightmap(size: int, seed: int = 0, scale: float = 4.0, octaves: int = 6, gain: float = 0.5,
                  lacunarity: float = 2.0) -> FloatArray:
    """パーリンノイズの fBm によるハイトマップ（0〜1 に正規化）。scale は地図の幅に入る大きな山の数の目安。"""
    x, y = grid(size, size, scale)
    return normalize(fbm(perlin2, x, y, octaves=octaves, lacunarity=lacunarity, gain=gain, seed=seed))


def island_mask(size: int, power: float = 2.0) -> FloatArray:
    """中心で 1、四隅に向かって 0 に近づく重み。ハイトマップに掛けると島になる。"""
    x, y = grid(size, size, 2.0)
    distance = np.hypot(x - 1.0, y - 1.0) / np.sqrt(2.0)
    result: FloatArray = 1.0 - distance ** power
    return result


def diamond_square(levels: int, roughness: float = 0.5, seed: int = 0) -> FloatArray:
    """ダイアモンドスクエア法によるハイトマップ。大きさは (2^levels + 1) 四方。

    正方形の中心（ダイアモンド段階）と辺の中点（スクエア段階）の高さを、周りの点の平均に
    乱数を足して決め、格子の間隔を半分にしていく。乱数の振幅は 1 段ごとに roughness 倍にする。
    戻り値は 0〜1 に正規化する。
    """
    rng = np.random.default_rng(seed)
    size = 2 ** levels + 1
    h = np.zeros((size, size))
    h[::size - 1, ::size - 1] = rng.uniform(-1.0, 1.0, (2, 2))
    step = size - 1
    amplitude = 1.0
    while step > 1:
        half = step // 2
        # ダイアモンド段階: 正方形の 4 隅の平均 + 乱数を中心に置く。
        corners = h[:-1:step, :-1:step] + h[:-1:step, step::step] + h[step::step, :-1:step] + h[step::step, step::step]
        centers = h[half::step, half::step]
        h[half::step, half::step] = corners / 4.0 + amplitude * rng.uniform(-1.0, 1.0, centers.shape)
        # スクエア段階: 辺の中点に、上下左右 4 点（地図の端では 3 点）の平均 + 乱数を置く。
        padded = np.pad(h, half, constant_values=np.nan)
        for row_start, column_start in ((0, half), (half, 0)):
            rows = np.arange(row_start, size, step)
            columns = np.arange(column_start, size, step)
            r, c = np.meshgrid(rows + half, columns + half, indexing="ij")
            neighbors = np.stack([padded[r - half, c], padded[r + half, c], padded[r, c - half], padded[r, c + half]])
            mean = np.nanmean(neighbors, axis=0)
            h[row_start::step, column_start::step] = mean + amplitude * rng.uniform(-1.0, 1.0, mean.shape)
        step = half
        amplitude *= roughness
    return normalize(h)


def surface_normals(heights: FloatArray, height_scale: float = 48.0) -> FloatArray:
    """ハイトマップの各点の単位法線 (H, W, 3)。高さの勾配 (∂h/∂x, ∂h/∂y) から (-∂h/∂x, -∂h/∂y, 1) を正規化する。"""
    dh_dy, dh_dx = np.gradient(heights * height_scale)
    normals = np.stack([-dh_dx, -dh_dy, np.ones_like(heights)], axis=-1)
    result: FloatArray = normals / np.linalg.norm(normals, axis=-1, keepdims=True)
    return result


def hillshade(heights: FloatArray, height_scale: float = 48.0, azimuth: float = 315.0,
              altitude: float = 45.0) -> FloatArray:
    """陰影起伏（ヒルシェード）。光を方位 azimuth 度（画像の上が北）、高度 altitude 度から当てた明るさ (0〜1)。

    配列の行番号は画像の下向きに増えるので、北（画像の上）は y の負の向きになる。
    """
    a = np.deg2rad(azimuth)
    e = np.deg2rad(altitude)
    light = np.array([np.sin(a) * np.cos(e), -np.cos(a) * np.cos(e), np.sin(e)])
    result: FloatArray = np.clip(surface_normals(heights, height_scale) @ light, 0.0, 1.0)
    return result


def shaded_relief(heights: FloatArray, height_scale: float = 48.0, colors: FloatArray | None = None) -> FloatArray:
    """標高の色にヒルシェードを掛けた画像 (H, W, 3)。海面より下は平らな水面として陰影を付けない。"""
    base = gradient_map(heights, TERRAIN_STOPS) if colors is None else colors
    land = np.maximum(heights, SEA_LEVEL)
    shade = hillshade(land, height_scale)
    light = 0.45 + 0.75 * shade
    result: FloatArray = np.clip(base * light[..., None], 0.0, 1.0)
    return result


def base_terrain(size: int = 256, seed: int = 5) -> FloatArray:
    """第 7 章で侵食・川・バイオームの元にする地形（fBm を島の形にし、低地を平らにしたもの）。"""
    h = fbm_heightmap(size, seed=seed, scale=3.0, octaves=5)
    h = normalize(h * 0.75 + 0.55 * island_mask(size, 2.5))
    result: FloatArray = h ** 1.3  # 低い所を平らに、高い所を険しくする
    return normalize(result) * 0.95 + 0.02
