"""第 3 章「ノイズ」: ノイズの種類と仕組みの図を作る。

* noise_types.png: バリューノイズ・パーリンノイズ・シンプレックスノイズ・セルラーノイズの比較
* lattice.png: 各ノイズの格子（格子点の値、勾配ベクトル、三角形の格子）
* profile.png: バリューノイズとパーリンノイズの断面（1 次元のグラフ）
* worley.png: セルラーノイズの F1・F2・F2−F1・セルの番号
* worley_jitter.png: 特徴点のずらし量 jitter による違い
"""

from __future__ import annotations

import math

import numpy as np

from color import cosine_palette
from common import FloatArray, grid, output_dir, save_figure, setup_matplotlib
from noise import perlin2, simplex2, value2, worley2
from prng import random2
from texture import show_panels

SIZE = 256  # 1 枚の画像の画素数（縦横）
UNSKEW = (3.0 - math.sqrt(3.0)) / 6.0  # シンプレックスノイズの歪めた格子を元に戻す係数（noise.py と同じ）


def to_unit(values: FloatArray) -> FloatArray:
    """-1〜1 のノイズの値を、表示用に 0〜1 へ写す。"""
    return np.clip(values * 0.5 + 0.5, 0.0, 1.0)


def draw_noise_types(file_name: str) -> None:
    x, y = grid(SIZE, SIZE, scale=8.0)
    f1, _, _ = worley2(x, y, seed=1)
    images = [to_unit(value2(x, y, seed=1)), to_unit(perlin2(x, y, seed=1)), to_unit(simplex2(x, y, seed=1)), f1]
    titles = ["バリューノイズ", "パーリンノイズ", "シンプレックスノイズ", "セルラーノイズ（F1）"]
    show_panels(images, titles, output_dir(__file__) / file_name)


def draw_lattice(file_name: str) -> None:
    """格子の構造を、ノイズの画像に重ねて描く。"""
    import matplotlib.pyplot as plt

    cells = 4
    x, y = grid(SIZE, SIZE, scale=float(cells))
    extent = (0.0, float(cells), float(cells), 0.0)
    figure, axes = plt.subplots(1, 3, figsize=(12, 4.3))
    points = np.arange(cells + 1)
    px, py = np.meshgrid(points, points)

    # バリューノイズ: 格子点に置いた値を、点の色で示す。
    ax = axes[0]
    ax.imshow(to_unit(value2(x, y, seed=3)), cmap="gray", vmin=0, vmax=1, extent=extent)
    values = random2(px, py, seed=3)
    ax.scatter(px, py, c=values, cmap="gray", vmin=0, vmax=1, s=70, edgecolors="#dd8452", linewidths=2, zorder=3)
    ax.set_title("バリューノイズ: 格子点に値を置く", fontsize=10)

    # パーリンノイズ: 格子点に置いた単位勾配ベクトルを矢印で示す。
    ax = axes[1]
    ax.imshow(to_unit(perlin2(x, y, seed=3)), cmap="gray", vmin=0, vmax=1, extent=extent)
    angle = random2(px, py, seed=3) * 2.0 * math.pi
    # 画像の y 軸は下向きなので、矢印の y 成分はそのまま下向きの量として描く。
    ax.quiver(px, py, np.cos(angle), np.sin(angle), color="#dd8452", angles="xy", scale_units="xy", scale=2.2,
              width=0.012, zorder=3)
    ax.scatter(px, py, color="#dd8452", s=18, zorder=3)
    ax.set_title("パーリンノイズ: 格子点に勾配を置く", fontsize=10)

    # シンプレックスノイズ: 斜めに歪めた格子（正三角形に近い三角形）を描く。
    ax = axes[2]
    ax.imshow(to_unit(simplex2(x, y, seed=3)), cmap="gray", vmin=0, vmax=1, extent=extent)
    for i in range(-4, cells + 6):
        for j in range(-4, cells + 6):
            for di, dj in ((1, 0), (0, 1), (1, 1)):
                a = np.array([i, i + di], dtype=np.float64)
                b = np.array([j, j + dj], dtype=np.float64)
                t = (a + b) * UNSKEW  # 歪めた格子の座標を元の平面に戻す
                ax.plot(a - t, b - t, color="#dd8452", linewidth=1.0)
    ax.set_title("シンプレックスノイズ: 三角形の格子", fontsize=10)

    for ax in axes[:2]:
        for k in points:
            ax.axhline(k, color="#4c72b0", linewidth=0.8)
            ax.axvline(k, color="#4c72b0", linewidth=0.8)
    for ax in axes:
        ax.set_xlim(0, cells)
        ax.set_ylim(cells, 0)
        ax.set_xticks([])
        ax.set_yticks([])
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_profile(file_name: str) -> None:
    """y を整数に固定した断面。格子点（x が整数）での値の違いを見る。"""
    import matplotlib.pyplot as plt

    xs = np.linspace(0.0, 8.0, 801)
    ys = np.full_like(xs, 2.0)
    figure, ax = plt.subplots(figsize=(10, 3.2))
    ax.plot(xs, value2(xs, ys, seed=5), label="バリューノイズ", color="#4c72b0")
    ax.plot(xs, perlin2(xs, ys, seed=5), label="パーリンノイズ", color="#dd8452")
    lattice = np.arange(9, dtype=np.float64)
    ax.scatter(lattice, value2(lattice, np.full_like(lattice, 2.0), seed=5), color="#4c72b0", zorder=3)
    ax.scatter(lattice, perlin2(lattice, np.full_like(lattice, 2.0), seed=5), color="#dd8452", zorder=3)
    ax.set_xticks(lattice)
    ax.set_xlabel("x（整数の位置が格子点）")
    ax.set_ylabel("ノイズの値")
    ax.axhline(0.0, color="#999999", linewidth=0.8)
    ax.grid(alpha=0.3)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=9, frameon=False)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_worley(file_name: str) -> None:
    x, y = grid(SIZE, SIZE, scale=6.0)
    f1, f2, cell = worley2(x, y, seed=2)
    colors = cosine_palette(cell, d=(0.0, 0.1, 0.2))
    images = [np.clip(f1, 0, 1), np.clip(f2 * 0.8, 0, 1), np.clip((f2 - f1) * 1.5, 0, 1), colors]
    titles = ["F1（最も近い点までの距離）", "F2（2 番目に近い点）", "F2 − F1（境界からの距離）", "最も近い点の番号"]
    show_panels(images, titles, output_dir(__file__) / file_name)


def draw_worley_jitter(file_name: str) -> None:
    x, y = grid(SIZE, SIZE, scale=6.0)
    images = []
    titles = []
    for jitter in (0.0, 0.5, 1.0):
        f1, f2, _ = worley2(x, y, seed=2, jitter=jitter)
        images.append(np.clip((f2 - f1) * 1.5, 0, 1))
        titles.append(f"jitter = {jitter:g}")
    show_panels(images, titles, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_noise_types("noise_types.png")
    draw_lattice("lattice.png")
    draw_profile("profile.png")
    draw_worley("worley.png")
    draw_worley_jitter("worley_jitter.png")


if __name__ == "__main__":
    main()
