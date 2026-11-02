"""第 3 章「ノイズ」: 3 次元ノイズの断面を時間とともに動かすアニメーションと、ループの考え方の図を作る。

* slices.png: 3 次元パーリンノイズを z = 一定の平面で切った断面
* noise_time.mp4: z を時刻とともに進めた断面の動画（4 秒）
* loop_concept.png: 円周に沿ってノイズを読むと、値の列が継ぎ目なく繰り返すことを示す図
"""

from __future__ import annotations

import math

import numpy as np
from PIL import Image

from color import gradient_map, hex_to_rgb
from common import FloatArray, grid, output_dir, save_figure, setup_matplotlib, to_bytes
from noise import fbm3, perlin2, perlin3
from texture import show_panels
from video import VideoWriter, find_ffmpeg

# 雲のような色の並び（暗い空 → 明るい雲）
CLOUD = [(0.0, hex_to_rgb("#0b2545")), (0.45, hex_to_rgb("#13315c")), (0.6, hex_to_rgb("#8da9c4")),
         (0.8, hex_to_rgb("#eef4ed")), (1.0, hex_to_rgb("#ffffff"))]


def frame_at(x: FloatArray, y: FloatArray, time: float, speed: float = 0.25) -> FloatArray:
    """時刻 time [秒] の断面。z = speed × time の平面で 3 次元の fBm を切る。"""
    z = np.full_like(x, speed * time)
    # 平面内でもゆっくり流す（x を時刻に比例してずらす）と、雲が風に流れるように見える。
    value = fbm3(x + 0.1 * time, y, z, octaves=3, seed=8)
    return gradient_map(np.clip(value * 0.9 + 0.5, 0.0, 1.0), CLOUD)


def draw_slices(file_name: str) -> None:
    x, y = grid(192, 192, scale=4.0)
    depths = (0.0, 0.25, 0.5, 1.0)
    images = [np.clip(perlin3(x, y, np.full_like(x, z), seed=8) * 0.8 + 0.5, 0, 1) for z in depths]
    titles = [f"z = {z:g}" for z in depths]
    show_panels(images, titles, output_dir(__file__) / file_name)


def write_video(file_name: str, seconds: float = 4.0, fps: int = 30) -> None:
    # 計算を軽くするため 320 × 180 で計算し、640 × 360 に拡大する（ノイズは滑らかなので拡大で劣化しにくい）。
    x, y = grid(320, 180, scale=4.0)
    with VideoWriter(output_dir(__file__) / file_name, 640, 360, fps=fps) as writer:
        for index in range(int(seconds * fps)):
            small = Image.fromarray(to_bytes(frame_at(x, y, index / fps)))
            writer.write(np.asarray(small.resize((640, 360), Image.Resampling.BILINEAR)))


def draw_loop_concept(file_name: str) -> None:
    """2 次元ノイズを円周に沿って読むと、角度について周期的な 1 次元の値の列が得られる。"""
    import matplotlib.pyplot as plt

    center = (2.0, 2.0)
    radius = 1.2
    figure, axes = plt.subplots(1, 2, figsize=(12, 4.2), gridspec_kw={"width_ratios": [1, 2.2]})

    x, y = grid(256, 256, scale=4.0)
    axes[0].imshow(np.clip(perlin2(x, y, seed=6) * 0.5 + 0.5, 0, 1), cmap="gray", vmin=0, vmax=1,
                   extent=(0.0, 4.0, 4.0, 0.0))
    angle = np.linspace(0.0, 2.0 * math.pi, 200)
    axes[0].plot(center[0] + radius * np.cos(angle), center[1] + radius * np.sin(angle), color="#dd8452", linewidth=2)
    axes[0].set_title("円周に沿ってノイズを読む", fontsize=10)
    axes[0].set_axis_off()

    t = np.linspace(0.0, 2.0, 801)  # ループ 2 周分（1 周 = 1）
    theta = 2.0 * math.pi * t
    on_circle = perlin2(center[0] + radius * np.cos(theta), center[1] + radius * np.sin(theta), seed=6)
    # 比較: 直線に沿って読んだ値を、長さ 1 ごとに先頭へ戻して繰り返す（継ぎ目で値が飛ぶ）。
    straight = perlin2(np.mod(t, 1.0) * 2.0 * math.pi * radius, np.full_like(t, 0.5), seed=6)
    axes[1].plot(t, straight, color="#999999", label="直線に沿って読み、先頭に戻す")
    axes[1].plot(t, on_circle, color="#dd8452", label="円周に沿って読む")
    axes[1].axvline(1.0, color="#4c72b0", linestyle="--", linewidth=1)
    axes[1].set_xlabel("時刻（1 でループの 1 周）")
    axes[1].set_ylabel("ノイズの値")
    axes[1].grid(alpha=0.3)
    axes[1].legend(fontsize=9, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_slices("slices.png")
    draw_loop_concept("loop_concept.png")
    if find_ffmpeg() is None:
        print("ffmpeg が見つからないので動画を作らない")
        return
    write_video("noise_time.mp4")


if __name__ == "__main__":
    main()
