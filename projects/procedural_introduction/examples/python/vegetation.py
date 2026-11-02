"""第 10 章「配置と散布」: 地形の高さ・傾斜と密度マップに従って、木と岩を配置する。

* vegetation_maps.png: ハイトマップ、傾斜、木の密度、配置した点
* vegetation_scene.png: 配置した木と岩を、大きさ・向き・色をばらつかせて上から見た図
* instance_variation.png: インスタンスごとの変化（変化なし、大きさと向き、さらに色）
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import numpy as np

from color import gradient_map, hex_to_rgb, oklch_to_srgb, srgb_to_oklab
from common import FloatArray, output_dir, save_figure, setup_matplotlib
from noise import fbm, perlin2
from poisson_disk import bridson_variable
from prng import random2

SIZE_M = 400.0  # 地形の 1 辺の長さ（m）
RESOLUTION = 256  # ハイトマップの 1 辺の画素数
CELL_M = SIZE_M / RESOLUTION
MAX_HEIGHT_M = 40.0
WATER = 0.3  # 正規化した高さで、これより低い所は水


def smoothstep(edge0: float, edge1: float, x: FloatArray) -> FloatArray:
    """edge0〜edge1 の間で 0 から 1 へなめらかに変わる関数。"""
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    result: FloatArray = t * t * (3.0 - 2.0 * t)
    return result


def make_terrain() -> tuple[FloatArray, FloatArray]:
    """正規化した高さ（0〜1）と傾斜（度）の地図を作る。"""
    xs = np.linspace(0.0, 2.5, RESOLUTION)
    x, y = np.meshgrid(xs, xs)
    height = fbm(perlin2, x, y, octaves=5, seed=21) * 0.5 + 0.5
    height = np.clip((height - 0.2) / 0.6, 0.0, 1.0)
    slope = terrain_slope(height * MAX_HEIGHT_M, CELL_M)
    return height, slope


def terrain_slope(height_m: FloatArray, cell_m: float) -> FloatArray:
    """高さ（m）の地図から、各画素の傾斜の角度（度）を求める。勾配の大きさが tan(傾斜) に等しい。"""
    dz_dy, dz_dx = np.gradient(height_m, cell_m)
    result: FloatArray = np.degrees(np.arctan(np.hypot(dz_dx, dz_dy)))
    return result


def tree_density(height: FloatArray, slope: FloatArray, patches: FloatArray) -> FloatArray:
    """木の密度（0〜1）。標高・傾斜・森のまとまりを表すノイズの 3 つの条件を掛け合わせる。"""
    above_shore = smoothstep(WATER + 0.03, WATER + 0.08, height)  # 水辺と砂浜には生えない
    below_treeline = 1.0 - smoothstep(0.72, 0.85, height)  # 森林限界より上には生えない
    not_steep = 1.0 - smoothstep(18.0, 30.0, slope)  # 急な斜面には生えない
    return above_shore * below_treeline * not_steep * patches


def rock_density(height: FloatArray, slope: FloatArray) -> FloatArray:
    """岩の密度（0〜1）。急な斜面と高い所に多い。"""
    steep = smoothstep(15.0, 28.0, slope)
    high = 0.6 * smoothstep(0.7, 0.85, height)
    return np.clip(steep + high, 0.0, 1.0) * smoothstep(WATER, WATER + 0.02, height)


def lookup(image: FloatArray, x: float, y: float) -> float:
    """地図 image の、位置 (x, y)（m）の値を最も近い画素から読む。"""
    i = min(int(x / CELL_M), RESOLUTION - 1)
    j = min(int(y / CELL_M), RESOLUTION - 1)
    return float(image[j, i])


def scatter(density: FloatArray, min_radius: float, max_radius: float, seed: int) -> FloatArray:
    """密度の地図に従って点を置く。

    1. 密度が高いほど半径を小さくして、ポアソンディスク・サンプリングで点を作る（間隔の制御）。
    2. 各点を、その場所の密度の確率で残す（密度 0 の所には置かない）。
    """
    rng = np.random.default_rng(seed)

    def radius_at(x: float, y: float) -> float:
        d = lookup(density, x, y)
        return max_radius + (min_radius - max_radius) * d

    points = bridson_variable(SIZE_M, SIZE_M, radius_at, min_radius, max_radius, rng)
    keep = np.array([lookup(density, x, y) for x, y in points]) > rng.random(len(points))
    return points[keep]


@dataclass
class Instance:
    """配置した物体 1 個の情報。"""

    x: float
    y: float
    kind: str  # "broadleaf"（広葉樹）、"conifer"（針葉樹）、"rock"（岩）
    scale: float  # 大きさの倍率
    angle: float  # 向き（ラジアン）
    color: FloatArray  # 基本の色（sRGB）


BASE_COLORS = {"broadleaf": "#4f8a3c", "conifer": "#2f6b4a", "rock": "#8d8a84"}


def vary(index: int, kind: str, x: float, y: float, height: float, seed: int = 0) -> Instance:
    """インスタンスの番号から決まる乱数で、大きさ・向き・色をばらつかせる。

    番号ごとにハッシュで乱数を作るので、配置をやり直したり一部を消したりしても、
    ほかのインスタンスの見た目は変わらない。
    """
    u = [float(random2(index, k, seed)) for k in range(4)]
    scale = 0.75 + 0.5 * u[0]
    if kind != "rock":
        scale *= 1.0 - 0.3 * height  # 高い所ほど木を小さくする
    angle = 2.0 * math.pi * u[1]
    # 色は OKLCH で、色相と明るさを少しだけずらす（明るさの印象をそろえたまま変化を付ける）
    lab = srgb_to_oklab(np.array(hex_to_rgb(BASE_COLORS[kind])))
    lightness = lab[0] + 0.06 * (u[2] - 0.5)
    chroma = math.hypot(lab[1], lab[2]) * (0.8 + 0.4 * u[3])
    hue = math.atan2(lab[2], lab[1]) + (0.25 if kind != "rock" else 0.05) * (u[3] - 0.5)
    color = oklch_to_srgb(np.array(lightness), np.array(chroma), np.array(hue))
    return Instance(x, y, kind, scale, angle, color)


def outline(kind: str, index: int) -> FloatArray:
    """アイコンの輪郭（半径 1 程度の多角形、(K, 2)）。岩は番号ごとに形を変える。"""
    theta = np.linspace(0.0, 2.0 * math.pi, 64, endpoint=False)
    if kind == "broadleaf":
        r = 1.0 + 0.1 * np.sin(7.0 * theta) + 0.05 * np.sin(3.0 * theta + 1.0)  # 丸い樹冠の凹凸
    elif kind == "conifer":
        theta = np.linspace(0.0, 2.0 * math.pi, 18, endpoint=False)
        r = np.where(np.arange(18) % 2 == 0, 1.0, 0.62)  # 星形（針葉樹を上から見た形）
    else:
        theta = np.sort(2.0 * math.pi * random2(index, np.arange(7), 99))
        r = 0.7 + 0.3 * random2(index, np.arange(7), 98)
    return np.stack([r * np.cos(theta), r * np.sin(theta)], axis=-1)


def draw_instance(ax: Any, instance: Instance, size: float, index: int) -> None:
    """インスタンス 1 個を、影・本体・光の当たる面の 3 枚の多角形で描く。

    光は左上から来るものとし、影と明るい面のずれる向きは回転させない（向きを変えるのは形だけ）。
    """
    from matplotlib.patches import Polygon

    c, s = math.cos(instance.angle), math.sin(instance.angle)
    shape = outline(instance.kind, index) @ np.array([[c, s], [-s, c]]) * size * instance.scale
    center = np.array([instance.x, instance.y])
    light = np.array([-0.35, -0.35]) * size  # 画面の y は下向きなので、左上は (−x, −y) * instance.scale
    color = np.clip(instance.color, 0.0, 1.0)
    ax.add_patch(Polygon(center + shape - light * 0.9, closed=True, color="black", alpha=0.25, linewidth=0))
    ax.add_patch(Polygon(center + shape, closed=True, facecolor=color * 0.8, edgecolor=color * 0.55,
                         linewidth=0.4))
    ax.add_patch(Polygon(center + shape * 0.55 + light * 0.45, closed=True, facecolor=np.clip(color * 1.15, 0, 1),
                         linewidth=0))


def hillshade(height_m: FloatArray) -> FloatArray:
    """左上から光を当てたときの斜面の明るさ（0〜1）。"""
    dz_dy, dz_dx = np.gradient(height_m, CELL_M)
    normal = np.stack([-dz_dx, -dz_dy, np.ones_like(height_m)], axis=-1)
    normal /= np.linalg.norm(normal, axis=-1, keepdims=True)
    light = np.array([-0.5, -0.5, 0.7])  # 画像の y は下向きなので、左上は (−x, −y)
    light /= np.linalg.norm(light)
    result: FloatArray = np.clip(normal @ light, 0.0, 1.0)
    return result


def terrain_colors(height: FloatArray) -> FloatArray:
    """高さを地図の色にし、陰影を掛ける。"""
    stops = [(0.0, (0.20, 0.40, 0.62)), (WATER, (0.36, 0.58, 0.76)), (WATER + 0.01, (0.82, 0.78, 0.60)),
             (WATER + 0.05, (0.62, 0.70, 0.45)), (0.7, (0.55, 0.60, 0.42)), (0.85, (0.62, 0.58, 0.54)),
             (1.0, (0.95, 0.95, 0.95))]
    base = gradient_map(height, stops)
    shade = 0.55 + 0.6 * hillshade(height * MAX_HEIGHT_M)
    water = height < WATER
    shade = np.where(water, 1.0, shade)
    result: FloatArray = np.clip(base * shade[..., None], 0.0, 1.0)
    return result


def build_scene() -> tuple[FloatArray, FloatArray, FloatArray, list[Instance], FloatArray]:
    """地形と、配置したインスタンスの一覧を作る。"""
    height, slope = make_terrain()
    xs = np.linspace(0.0, 4.0, RESOLUTION)
    x, y = np.meshgrid(xs, xs)
    patches = smoothstep(-0.15, 0.25, fbm(perlin2, x, y, octaves=3, seed=5))  # 森と草地のまとまり
    trees = tree_density(height, slope, patches)
    rocks = rock_density(height, slope)

    instances: list[Instance] = []
    tree_points = scatter(trees, 5.0, 16.0, seed=1)
    for index, (px, py) in enumerate(tree_points):
        h = lookup(height, px, py)
        # 標高が高いほど針葉樹の割合を増やす
        kind = "conifer" if float(random2(index, 7, 3)) < smoothstep(0.45, 0.7, np.array(h)) else "broadleaf"
        instances.append(vary(index, kind, px, py, h))
    for index, (px, py) in enumerate(scatter(rocks, 6.0, 20.0, seed=2)):
        instances.append(vary(index + 100000, "rock", px, py, lookup(height, px, py)))
    return height, slope, trees, instances, tree_points


def draw_maps(file_name: str, height: FloatArray, slope: FloatArray, trees: FloatArray,
              instances: list[Instance]) -> None:
    import matplotlib.pyplot as plt

    extent = (0.0, SIZE_M, SIZE_M, 0.0)
    figure, axes = plt.subplots(1, 4, figsize=(14, 3.9))
    panels = [("高さ（m）", height * MAX_HEIGHT_M, "terrain"), ("傾斜（度）", slope, "magma"),
              ("木の密度", trees, "Greens")]
    for ax, (title, image, cmap) in zip(axes, panels):
        shown = ax.imshow(image, cmap=cmap, extent=extent)
        figure.colorbar(shown, ax=ax, fraction=0.045, pad=0.03)
        ax.set_title(title, fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
    ax = axes[3]
    ax.imshow(terrain_colors(height), extent=extent)
    for kind, color, label in [("broadleaf", "#2d6a1e", "広葉樹"), ("conifer", "#0f3d2a", "針葉樹"),
                               ("rock", "#555555", "岩")]:
        points = np.array([(i.x, i.y) for i in instances if i.kind == kind])
        ax.scatter(points[:, 0], points[:, 1], s=2, color=color, label=f"{label}（{len(points)}）")
    ax.set_xlim(0.0, SIZE_M)
    ax.set_ylim(SIZE_M, 0.0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(loc="lower left", fontsize=7, markerscale=4, framealpha=0.9)
    ax.set_title("配置した点", fontsize=10)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_scene(file_name: str, height: FloatArray, instances: list[Instance]) -> None:
    import matplotlib.pyplot as plt

    # 全体だと木が小さすぎるので、地図の一部（200 m 四方）を拡大して描く
    left, top, span = 40.0, 170.0, 200.0
    figure, ax = plt.subplots(figsize=(8.0, 8.0))
    ax.imshow(terrain_colors(height), extent=(0.0, SIZE_M, SIZE_M, 0.0), interpolation="bicubic")
    order = sorted(range(len(instances)), key=lambda k: instances[k].y)  # 手前（下）のものを後から描く
    for k in order:
        instance = instances[k]
        if left - 10 <= instance.x <= left + span + 10 and top - 10 <= instance.y <= top + span + 10:
            size = 2.6 if instance.kind != "rock" else 2.2
            draw_instance(ax, instance, size, k)
    ax.set_xlim(left, left + span)
    ax.set_ylim(top + span, top)
    ax.set_axis_off()
    figure.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
    save_figure(figure, output_dir(__file__) / file_name)


def draw_variation(file_name: str) -> None:
    import matplotlib.pyplot as plt

    rows = [("変化なし", False, False), ("大きさと向き", True, False), ("大きさ・向き・色", True, True)]
    figure, ax = plt.subplots(figsize=(10, 4.2))
    for row, (title, transform, colored) in enumerate(rows):
        for column in range(10):
            kind = "rock" if column >= 8 else ("conifer" if column >= 5 else "broadleaf")
            index = column + 10
            instance = vary(index, kind, column * 3.0, row * 3.2, 0.3)
            if not transform:
                instance.scale, instance.angle = 1.0, 0.0
            if not colored:
                instance.color = np.array(hex_to_rgb(BASE_COLORS[kind]))
            draw_instance(ax, instance, 1.1, index if transform else 0)  # 岩の形も番号で変わる
        ax.text(-2.2, row * 3.2, title, ha="right", va="center", fontsize=10)
    ax.set_xlim(-9.0, 29.0)
    ax.set_ylim(8.6, -1.8)
    ax.set_aspect("equal")
    ax.set_axis_off()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    height, slope, trees, instances, _ = build_scene()
    draw_maps("vegetation_maps.png", height, slope, trees, instances)
    draw_scene("vegetation_scene.png", height, instances)
    draw_variation("instance_variation.png")


if __name__ == "__main__":
    main()
