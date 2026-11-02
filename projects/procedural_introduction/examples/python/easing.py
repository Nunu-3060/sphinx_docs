"""第 2 章「基礎の道具箱」: 補間・イージング・範囲変換の図を作る。

* easing_curves.png: 線形補間、smoothstep、smootherstep、各種イージング関数のグラフ
* shaping.png: ノイズに範囲変換・しきい値・smoothstep・グラデーションマップを順に適用した結果
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

from color import gradient_map, hex_to_rgb
from common import FloatArray, grid, output_dir, save_figure, setup_matplotlib, tile_images
from noise import fbm, perlin2


def smoothstep(edge0: float, edge1: float, x: FloatArray) -> FloatArray:
    """GLSL の smoothstep と同じ。edge0〜edge1 の間を 3 次式 3t^2 - 2t^3 で滑らかに 0 から 1 へ変える。"""
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def smootherstep(t: FloatArray) -> FloatArray:
    """5 次式 6t^5 - 15t^4 + 10t^3。両端で 2 階微分も 0 になる。"""
    t = np.clip(t, 0.0, 1.0)
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)


def remap(x: FloatArray, in_low: float, in_high: float, out_low: float, out_high: float) -> FloatArray:
    """値の範囲を in_low〜in_high から out_low〜out_high へ線形に写す。"""
    return out_low + (x - in_low) * (out_high - out_low) / (in_high - in_low)


EASINGS: dict[str, Callable[[FloatArray], FloatArray]] = {
    "線形": lambda t: t,
    "smoothstep": lambda t: smoothstep(0.0, 1.0, t),
    "smootherstep": smootherstep,
    "ease-in（2 乗）": lambda t: t * t,
    "ease-out（3 次）": lambda t: 1.0 - (1.0 - t) ** 3,
    "ease-in-out（sin）": lambda t: 0.5 - 0.5 * np.cos(np.pi * t),
}


def draw_easing_curves(file_name: str) -> None:
    import matplotlib.pyplot as plt

    t = np.linspace(0.0, 1.0, 200)
    figure, axes = plt.subplots(1, 2, figsize=(10, 4))
    for name in ["線形", "smoothstep", "smootherstep"]:
        axes[0].plot(t, EASINGS[name](t), label=name)
    axes[0].set_title("補間の重み")
    for name in ["線形", "ease-in（2 乗）", "ease-out（3 次）", "ease-in-out（sin）"]:
        axes[1].plot(t, EASINGS[name](t), label=name)
    axes[1].set_title("イージング関数")
    for ax in axes:
        ax.set_xlabel("t（入力）")
        ax.set_ylabel("出力")
        ax.set_aspect("equal")
        ax.grid(alpha=0.3)
        ax.legend(fontsize=9)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_shaping(file_name: str) -> None:
    import matplotlib.pyplot as plt

    x, y = grid(256, 256, scale=4.0)
    raw = fbm(perlin2, x, y, octaves=5, seed=7)  # おおむね -1〜1（第 3 章で詳しく扱う）
    unit = np.clip(remap(raw, -0.6, 0.6, 0.0, 1.0), 0.0, 1.0)
    threshold = (unit > 0.5).astype(np.float64)
    soft = smoothstep(0.45, 0.55, unit)
    colored = gradient_map(unit, [
        (0.0, hex_to_rgb("#1d3557")), (0.45, hex_to_rgb("#457b9d")), (0.5, hex_to_rgb("#e9d8a6")),
        (0.6, hex_to_rgb("#6a994e")), (0.85, hex_to_rgb("#386641")), (1.0, hex_to_rgb("#f1faee")),
    ])
    titles = ["remap で 0〜1 に", "しきい値 0.5", "smoothstep(0.45, 0.55)", "グラデーションマップ"]
    images = [unit, threshold, soft, colored]
    figure, axes = plt.subplots(1, 4, figsize=(12, 3.3))
    for ax, title, image in zip(axes, titles, images):
        rgb = tile_images([image], columns=1)
        ax.imshow(rgb)
        ax.set_title(title, fontsize=10)
        ax.set_axis_off()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_easing_curves("easing_curves.png")
    draw_shaping("shaping.png")


if __name__ == "__main__":
    main()
