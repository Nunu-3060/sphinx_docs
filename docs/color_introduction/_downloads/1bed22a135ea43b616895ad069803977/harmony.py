"""「配色の基本」の章で使う図を作る。

1. 12 色の色相環
2. 色相環の上での位置関係にもとづく配色 (補色、類似色など)
3. トーンにもとづく配色 (トーンオントーン、トーンイントーン)
4. 配色の面積比 (70:25:5) の比較
"""

import numpy as np
from PIL import Image, ImageDraw

from color_utils import (FloatArray, hex_to_rgb, hsv_to_rgb, labeled_rows,
                         oklch_to_srgb_in_gamut, save_image, save_rgb,
                         swatches, to_uint8)

# 配色の例の基準にする色相 (度)。HSV で青に近い色。
BASE_HUE = 210.0

# 色相環上での位置関係にもとづく配色。基準の色相からの角度で表す。
HUE_SCHEMES: list[tuple[str, list[float]]] = [
    ("Complementary", [0.0, 180.0]),
    ("Analogous", [-30.0, 0.0, 30.0]),
    ("Triadic", [0.0, 120.0, 240.0]),
    ("Split compl.", [0.0, 150.0, 210.0]),
    ("Tetradic", [0.0, 90.0, 180.0, 270.0]),
]


def hsv_color(hue_deg: float, saturation: float = 0.75,
              value: float = 0.9) -> FloatArray:
    """色相を度で指定して、HSV から sRGB 値を求める。"""
    return hsv_to_rgb(hue_deg / 360.0, saturation, value)


def rgb_tuple(rgb: FloatArray) -> tuple[int, int, int]:
    """sRGB 値を、PIL の描画関数に渡す 0-255 の整数の組にする。"""
    r, g, b = (int(v) for v in to_uint8(rgb))
    return (r, g, b)


def draw_wheel(draw: ImageDraw.ImageDraw, center: tuple[float, float],
               radius: float, segments: int,
               saturation: float = 0.75, value: float = 0.9) -> None:
    """HSV の色相環を ``segments`` 個の扇形に分けて描く。赤を真上に置く。"""
    cx, cy = center
    box = (cx - radius, cy - radius, cx + radius, cy + radius)
    step = 360.0 / segments
    for i in range(segments):
        hue = i * step
        # PIL の角度は 3 時の方向から時計回り。赤 (0 度) を 12 時に置く。
        start = hue - 90.0 - step / 2.0
        draw.pieslice(box, start, start + step,
                      fill=rgb_tuple(hsv_color(hue, saturation, value)))
    inner = radius * 0.55
    draw.ellipse((cx - inner, cy - inner, cx + inner, cy + inner),
                 fill="white")


def wheel_point(center: tuple[float, float], radius: float,
                hue_deg: float) -> tuple[float, float]:
    """色相環の上で色相 ``hue_deg`` にあたる点の座標を返す。"""
    angle = np.deg2rad(hue_deg - 90.0)
    return (center[0] + radius * float(np.cos(angle)),
            center[1] + radius * float(np.sin(angle)))


def color_wheel(size: int = 360) -> Image.Image:
    """12 色の色相環。"""
    canvas = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(canvas)
    draw_wheel(draw, (size / 2, size / 2), size * 0.45, 12)
    return canvas


def scheme_wheel(offsets: list[float], size: int = 160) -> FloatArray:
    """色相環の上に、配色に使う色相の位置を結んだ多角形を描く。"""
    canvas = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(canvas)
    center = (size / 2, size / 2)
    radius = size * 0.45
    draw_wheel(draw, center, radius, 36)

    points = [wheel_point(center, radius * 0.775, BASE_HUE + offset)
              for offset in offsets]
    if len(points) > 1:
        draw.line(points + [points[0]], fill="black", width=2)
    for x, y in points:
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill="white",
                     outline="black", width=2)
    return np.asarray(canvas, dtype=float) / 255.0


def hue_schemes() -> Image.Image:
    """色相にもとづく配色を、色相環上の位置と色見本で並べる。"""
    rows = []
    gap = np.ones((160, 24, 3))
    for name, offsets in HUE_SCHEMES:
        colors = [hsv_color(BASE_HUE + offset) for offset in offsets]
        chips = swatches(colors, width=96, height=96)
        chips = np.pad(chips, ((32, 32), (0, 0), (0, 0)), constant_values=1.0)
        rows.append((name, np.concatenate(
            [scheme_wheel(offsets), gap, chips], axis=1)))
    return labeled_rows(rows, label_width=160)


def tone_schemes() -> Image.Image:
    """OKLCH を使ったトーンオントーンとトーンイントーンの色見本。"""
    # トーンオントーン: 色相をそろえ、明るさを大きく変える。
    tone_on_tone = [oklch_to_srgb_in_gamut(lightness, 0.12, 250.0)
                    for lightness in np.linspace(0.35, 0.92, 6)]
    # トーンイントーン: 明るさと彩度 (トーン) をそろえ、色相を変える。
    tone_in_tone = [oklch_to_srgb_in_gamut(0.75, 0.09, hue)
                    for hue in np.linspace(20.0, 220.0, 6)]
    # 比較用: 色相も明るさもばらばらな 6 色。
    random_colors = [hex_to_rgb(code) for code in (
        "#e41a1c", "#ffff33", "#377eb8", "#f781bf", "#4daf4a", "#a65628")]
    return labeled_rows([
        ("Tone on tone", swatches(tone_on_tone, width=96, height=72)),
        ("Tone in tone", swatches(tone_in_tone, width=96, height=72)),
        ("Unordered", swatches(random_colors, width=96, height=72)),
    ], label_width=160)


def proportion_panels() -> FloatArray:
    """同じ 3 色を、等しい面積と 70:25:5 の面積で使った図を並べる。"""
    width, height = 360, 240
    base = hex_to_rgb("#f2eee6")
    main = hex_to_rgb("#2f5d8a")
    accent = hex_to_rgb("#e07a2f")

    # 3 色を 1/3 ずつの面積で塗る。
    equal = np.empty((height, width, 3))
    equal[:, :120] = base
    equal[:, 120:240] = main
    equal[:, 240:] = accent

    # ベース 70%、メイン 25%、アクセント 5% で塗る。
    # 上部の帯 (360 x 60) が 25%、ボタン (108 x 40) が 5% にあたる。
    ratio = np.tile(base, (height, width, 1))
    ratio[:60] = main
    ratio[150:190, 126:234] = accent

    # 明るいベース色が紙面に溶け込まないよう、灰色の枠を付ける。
    framed = [np.pad(panel, ((1, 1), (1, 1), (0, 0)), constant_values=0.6)
              for panel in (equal, ratio)]
    gap = np.ones((height + 2, 24, 3))
    return np.concatenate([framed[0], gap, framed[1]], axis=1)


def main() -> None:
    """本章の図を作り、保存する。"""
    save_image(color_wheel(), "color_wheel.png")
    save_image(hue_schemes(), "hue_schemes.png")
    save_image(tone_schemes(), "tone_schemes.png")
    save_rgb(proportion_panels(), "proportion.png")


if __name__ == "__main__":
    main()
