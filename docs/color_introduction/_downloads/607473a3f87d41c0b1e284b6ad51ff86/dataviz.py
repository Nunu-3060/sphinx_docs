"""「データ可視化の配色」の章で使う図を作る。

1. カラーマップの 3 つの種類 (連続、発散、カテゴリ)
2. 虹色のカラーマップ (jet) と、明るさが単調に変わるカラーマップの比較
3. カラーマップに沿った明るさ L の変化のグラフ
4. カテゴリの配色の比較 (HSV で色相を等分した色と Okabe-Ito の配色)
"""

from typing import Callable

import numpy as np
from PIL import Image, ImageDraw

from color_utils import (FloatArray, font, hex_to_rgb, hsv_to_rgb,
                         labeled_rows, oklab_lightness,
                         oklch_to_srgb_in_gamut, save_image, swatches,
                         to_grayscale, to_uint8)

Colormap = Callable[[FloatArray], FloatArray]

# Okabe と Ito が提案した、色覚の多様性に配慮したカテゴリの配色。
OKABE_ITO = ["#000000", "#e69f00", "#56b4e9", "#009e73",
             "#f0e442", "#0072b2", "#d55e00", "#cc79a7"]


def jet(t: FloatArray) -> FloatArray:
    """MATLAB などで使われてきた虹色のカラーマップ jet を近似する。

    青から水色、緑、黄を経て赤に至る。RGB の各成分を折れ線で与える。
    """
    t = np.asarray(t, dtype=float)[..., np.newaxis]
    centers = np.array([0.75, 0.5, 0.25])  # R, G, B の山の位置
    return np.asarray(np.clip(1.5 - np.abs(4.0 * (t - centers)), 0.0, 1.0),
                      dtype=float)


def sequential(t: FloatArray) -> FloatArray:
    """暗い紫から青緑を経て明るい黄に至る、連続のカラーマップ。

    OKLCH の明るさ L を t に比例して増やすので、明るさは単調に変わる。
    彩度 C は、途中の青緑でも sRGB の色域に収まる大きさに抑えている。
    色域の境界で彩度が切り詰められると、色の変化に折れ目ができるためである。
    """
    t = np.asarray(t, dtype=float)
    lightness = 0.27 + 0.68 * t
    chroma = 0.085 + 0.065 * t ** 2
    hue = 300.0 - 195.0 * t
    return oklch_to_srgb_in_gamut(lightness, chroma, hue)


def diverging(t: FloatArray) -> FloatArray:
    """青から白に近い色を経て赤に至る、発散のカラーマップ。

    中央 (t = 0.5) で最も明るく、両端に向かって同じ割合で暗くなる。
    """
    t = np.asarray(t, dtype=float)
    distance = np.abs(t - 0.5) * 2.0  # 中央からの距離 (0.0-1.0)
    lightness = 0.97 - 0.50 * distance
    chroma = 0.15 * distance
    hue = np.where(t < 0.5, 255.0, 25.0)
    return oklch_to_srgb_in_gamut(lightness, chroma, hue)


def sample_field(width: int = 360, height: int = 240) -> FloatArray:
    """なだらかな山と谷を重ねた、0.0-1.0 の値を持つ 2 次元のデータ。"""
    y, x = np.mgrid[0:height, 0:width].astype(float)
    u, v = x / width, y / height
    field = (0.6 * u
             + 0.25 * np.exp(-((u - 0.3) ** 2 + (v - 0.4) ** 2) / 0.02)
             - 0.2 * np.exp(-((u - 0.7) ** 2 + (v - 0.6) ** 2) / 0.03)
             + 0.05 * np.sin(u * 20.0) * np.sin(v * 14.0))
    value_range = field.max() - field.min()
    normalized: FloatArray = (field - field.min()) / value_range
    return normalized


def colormap_strip(colormap: Colormap, width: int = 640,
                   height: int = 48) -> FloatArray:
    """カラーマップを左 (0.0) から右 (1.0) へ並べた帯。"""
    row = colormap(np.linspace(0.0, 1.0, width))
    return np.repeat(row[np.newaxis, :, :], height, axis=0)


def stepped_colormap(colors: list[str]) -> Colormap:
    """カテゴリの色を区切って並べるだけのカラーマップを作る。"""
    table = np.array([hex_to_rgb(code) for code in colors])

    def colormap(t: FloatArray) -> FloatArray:
        index = np.minimum((np.asarray(t) * len(table)).astype(int),
                           len(table) - 1)
        colors: FloatArray = table[index]
        return colors

    return colormap


def colormap_types() -> Image.Image:
    """連続、発散、カテゴリの 3 種類のカラーマップを並べる。"""
    return labeled_rows([
        ("Sequential", colormap_strip(sequential)),
        ("Diverging", colormap_strip(diverging)),
        ("Qualitative", colormap_strip(stepped_colormap(OKABE_ITO))),
    ], label_width=140)


def field_comparison() -> Image.Image:
    """同じデータを jet と連続のカラーマップで塗り、明るさだけも並べる。"""
    field = sample_field()
    gap = np.ones((field.shape[0], 16, 3))
    rows = []
    for name, colormap in (("jet", jet), ("Sequential", sequential)):
        colored = colormap(field)
        rows.append((name, np.concatenate(
            [colored, gap, to_grayscale(colored)], axis=1)))
    return labeled_rows(rows, label_width=140)


def lightness_plot(width: int = 640, height: int = 360) -> Image.Image:
    """カラーマップに沿った OKLab の明るさ L の変化を折れ線で描く。

    線そのものをカラーマップの色で塗り、どの色がどの明るさかを示す。
    """
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    label_font = font(16)
    left, right, top, bottom = 60, width - 130, 20, height - 50

    # 軸と目盛り。
    draw.line((left, top, left, bottom, right, bottom), fill="black",
              width=2)
    for value in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = bottom - (bottom - top) * value
        draw.line((left - 5, y, left, y), fill="black", width=2)
        draw.text((left - 10, y), f"{value:.2f}", fill="black",
                  font=label_font, anchor="rm")
        x = left + (right - left) * value
        draw.line((x, bottom, x, bottom + 5), fill="black", width=2)
        draw.text((x, bottom + 10), f"{value:.2f}", fill="black",
                  font=label_font, anchor="mt")
    draw.text(((left + right) / 2, height - 12), "position in colormap",
              fill="black", font=label_font, anchor="mm")

    t = np.linspace(0.0, 1.0, 400)
    for name, colormap in (("jet", jet), ("Sequential", sequential),
                           ("Diverging", diverging)):
        colors = colormap(t)
        lightness = oklab_lightness(colors)
        xs = left + (right - left) * t
        ys = bottom - (bottom - top) * lightness
        for i in range(len(t) - 1):
            r, g, b = (int(v) for v in to_uint8(colors[i]))
            draw.line((xs[i], ys[i], xs[i + 1], ys[i + 1]), fill=(r, g, b),
                      width=6)
        draw.text((right + 10, ys[-1]), name, fill="black", font=label_font,
                  anchor="lm")
    return canvas


def qualitative_comparison() -> Image.Image:
    """カテゴリの配色 2 種類を、明るさだけを残した色見本とともに並べる。"""
    hues = np.arange(8) / 8.0
    hsv_colors = [hsv_to_rgb(h, 0.9, 0.9) for h in hues]
    okabe_ito = [hex_to_rgb(code) for code in OKABE_ITO]
    hsv_chips = swatches(hsv_colors, width=64, height=48)
    okabe_chips = swatches(okabe_ito, width=64, height=48)
    return labeled_rows([
        ("HSV hues", hsv_chips),
        ("  lightness", to_grayscale(hsv_chips)),
        ("Okabe-Ito", okabe_chips),
        ("  lightness", to_grayscale(okabe_chips)),
    ], label_width=140)


def main() -> None:
    """本章の図を作り、保存する。"""
    save_image(colormap_types(), "colormap_types.png")
    save_image(field_comparison(), "colormap_field.png")
    save_image(lightness_plot(), "colormap_lightness.png")
    save_image(qualitative_comparison(), "qualitative.png")


if __name__ == "__main__":
    main()
