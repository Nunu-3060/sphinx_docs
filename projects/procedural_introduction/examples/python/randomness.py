"""第 2 章「基礎の道具箱」: 乱数とハッシュ関数の図を作る。

* hash_compare.png: 掛け算と剰余だけの式、GLSL でよく見る fract(sin(...))、PCG ハッシュの比較
* distributions.png: ハッシュから作った一様分布・正規分布・重み付き選択のヒストグラム
"""

from __future__ import annotations

import math

import numpy as np

from common import FloatArray, output_dir, save_figure, setup_matplotlib
from prng import random2


def sin_hash(ix: FloatArray, iy: FloatArray) -> FloatArray:
    """GLSL の作例でよく使われる fract(sin(dot(p, k)) * 43758.5453) を、GPU と同じ 32 bit 浮動小数点数で計算する。"""
    x = ix.astype(np.float32)
    y = iy.astype(np.float32)
    s = np.sin(x * np.float32(12.9898) + y * np.float32(78.233)) * np.float32(43758.5453)
    return (s - np.floor(s)).astype(np.float64)


def linear_hash(ix: FloatArray, iy: FloatArray) -> FloatArray:
    """掛け算と剰余だけで作った、悪いハッシュの例。値は座標の 1 次式なので縞模様が現れる。"""
    return ((ix * 37 + iy * 91) % 256) / 256.0


def box_muller(u1: FloatArray, u2: FloatArray) -> FloatArray:
    """0〜1 の一様乱数 2 個から、平均 0・標準偏差 1 の正規乱数を作る（ボックス＝ミュラー法）。"""
    return np.sqrt(-2.0 * np.log(1.0 - u1)) * np.cos(2.0 * math.pi * u2)


def weighted_choice(u: FloatArray, weights: list[float]) -> FloatArray:
    """0〜1 の一様乱数 u を、重みに比例する確率で 0, 1, 2, ... の番号に変換する。"""
    cumulative = np.cumsum(weights) / np.sum(weights)
    return np.searchsorted(cumulative, u, side="right").astype(np.float64)


def draw_hash_compare(file_name: str) -> None:
    import matplotlib.pyplot as plt

    size = 128
    ix, iy = np.meshgrid(np.arange(size, dtype=np.float64), np.arange(size, dtype=np.float64))
    panels = [
        ("掛け算と剰余だけの式", linear_hash(ix, iy)),
        ("sin ハッシュ", sin_hash(ix, iy)),
        ("PCG ハッシュ（シード 0）", random2(ix.astype(np.int64), iy.astype(np.int64), seed=0)),
        ("PCG ハッシュ（シード 1）", random2(ix.astype(np.int64), iy.astype(np.int64), seed=1)),
    ]
    figure, axes = plt.subplots(1, 4, figsize=(12, 3.4))
    for ax, (title, image) in zip(axes, panels):
        ax.imshow(image, cmap="gray", vmin=0.0, vmax=1.0, interpolation="nearest")
        ax.set_title(title, fontsize=10)
        ax.set_axis_off()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_distributions(file_name: str) -> None:
    import matplotlib.pyplot as plt

    count = 20000
    index = np.arange(count)
    u1 = random2(index, 0, seed=1)
    u2 = random2(index, 0, seed=2)
    u3 = random2(index, 0, seed=3)
    weights = [5.0, 3.0, 1.0, 1.0]

    figure, axes = plt.subplots(1, 4, figsize=(12, 2.8))
    axes[0].hist(u1, bins=40, color="#4c72b0")
    axes[0].set_title("一様分布")
    axes[1].hist((u1 + u2 + u3) / 3.0, bins=40, color="#4c72b0")
    axes[1].set_title("一様乱数 3 個の平均")
    axes[2].hist(box_muller(u1, u2), bins=40, color="#4c72b0")
    axes[2].set_title("正規分布（ボックス＝ミュラー法）")
    choices = weighted_choice(u1, weights)
    axes[3].bar(range(len(weights)), [np.count_nonzero(choices == k) for k in range(len(weights))], color="#dd8452")
    axes[3].set_xticks(range(len(weights)), [f"重み {w:g}" for w in weights])
    axes[3].set_title("重み付き選択")
    for ax in axes[:3]:
        ax.set_yticks([])
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_hash_compare("hash_compare.png")
    draw_distributions("distributions.png")


if __name__ == "__main__":
    main()
