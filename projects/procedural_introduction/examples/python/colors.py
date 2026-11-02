"""第 2 章「基礎の道具箱」: 色の生成の図を作る。

* color_interpolation.png: 2 色の間を sRGB・HSV・OKLab で補間したグラデーションの比較
* hue_lightness.png: HSV と OKLCH で色相だけを変えたときの見た目の明るさの比較
* cosine_palettes.png: コサインパレットの例
"""

from __future__ import annotations

import numpy as np

from color import (cosine_palette, hex_to_rgb, hsv_to_rgb, linear_to_srgb, oklab_to_srgb, oklch_to_srgb,
                   srgb_to_linear, srgb_to_oklab)
from common import FloatArray, output_dir, save_figure, setup_matplotlib


def rgb_to_hsv(rgb: FloatArray) -> FloatArray:
    """RGB を HSV（各成分 0〜1）に変換する。"""
    import matplotlib.colors

    result: FloatArray = matplotlib.colors.rgb_to_hsv(rgb)
    return result


def luminance_gray(rgb: FloatArray) -> FloatArray:
    """sRGB の色と相対輝度が等しい灰色を返す。色の見た目の明るさを比べるために使う。"""
    luminance = srgb_to_linear(rgb) @ np.array([0.2126, 0.7152, 0.0722])
    gray = linear_to_srgb(luminance)
    return np.repeat(gray[:, None], 3, axis=1)


def strip(colors: FloatArray, height: int = 40) -> FloatArray:
    """横に並んだ色 (N, 3) を、高さ height の帯の画像にする。"""
    return np.repeat(colors[None, :, :], height, axis=0)


def draw_interpolation(file_name: str) -> None:
    import matplotlib.pyplot as plt

    start = np.array(hex_to_rgb("#1f4fff"))
    end = np.array(hex_to_rgb("#ffd21f"))
    t = np.linspace(0.0, 1.0, 256)[:, None]

    srgb = start + (end - start) * t
    hsv_start = rgb_to_hsv(start)
    hsv_end = rgb_to_hsv(end)
    hsv = hsv_start + (hsv_end - hsv_start) * t
    hsv_colors = hsv_to_rgb(hsv[:, 0], hsv[:, 1], hsv[:, 2])
    lab_start = srgb_to_oklab(start)
    lab_end = srgb_to_oklab(end)
    oklab = oklab_to_srgb(lab_start + (lab_end - lab_start) * t)

    figure, axes = plt.subplots(3, 1, figsize=(8, 3.2))
    for ax, title, colors in zip(axes, ["sRGB で補間", "HSV で補間", "OKLab で補間"], [srgb, hsv_colors, oklab]):
        ax.imshow(strip(colors), aspect="auto")
        ax.set_ylabel(title, rotation=0, ha="right", va="center", fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_hue_lightness(file_name: str) -> None:
    import matplotlib.pyplot as plt

    hue = np.linspace(0.0, 1.0, 360, endpoint=False)
    hsv_colors = hsv_to_rgb(hue, np.full_like(hue, 0.8), np.full_like(hue, 0.95))
    oklch_colors = oklch_to_srgb(np.full_like(hue, 0.72), np.full_like(hue, 0.12), hue * 2.0 * np.pi)

    figure, axes = plt.subplots(4, 1, figsize=(8, 3.6))
    rows = [
        ("HSV", hsv_colors),
        ("HSV の明るさ", luminance_gray(hsv_colors)),
        ("OKLCH", oklch_colors),
        ("OKLCH の明るさ", luminance_gray(oklch_colors)),
    ]
    for ax, (title, colors) in zip(axes, rows):
        ax.imshow(strip(np.clip(colors, 0.0, 1.0), 30), aspect="auto")
        ax.set_ylabel(title, rotation=0, ha="right", va="center", fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


PALETTES: list[tuple[str, tuple[float, float, float], tuple[float, float, float],
                     tuple[float, float, float], tuple[float, float, float]]] = [
    ("虹", (0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (1.0, 1.0, 1.0), (0.0, 0.33, 0.67)),
    ("夕焼け", (0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (1.0, 1.0, 1.0), (0.0, 0.10, 0.20)),
    ("海", (0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (1.0, 1.0, 0.5), (0.80, 0.90, 0.30)),
    ("砂漠", (0.8, 0.5, 0.4), (0.2, 0.4, 0.2), (2.0, 1.0, 1.0), (0.0, 0.25, 0.25)),
]


def draw_cosine_palettes(file_name: str) -> None:
    import matplotlib.pyplot as plt

    t = np.linspace(0.0, 1.0, 256)
    figure, axes = plt.subplots(len(PALETTES), 1, figsize=(8, 0.75 * len(PALETTES) + 0.4))
    for ax, (name, a, b, c, d) in zip(axes, PALETTES):
        ax.imshow(strip(cosine_palette(t, a, b, c, d)), aspect="auto")
        ax.set_ylabel(name, rotation=0, ha="right", va="center", fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_interpolation("color_interpolation.png")
    draw_hue_lightness("hue_lightness.png")
    draw_cosine_palettes("cosine_palettes.png")


if __name__ == "__main__":
    main()
