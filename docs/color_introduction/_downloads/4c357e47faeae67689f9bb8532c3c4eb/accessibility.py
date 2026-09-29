"""「アクセシビリティ」の章で使う図と数値を作る。

1. 文字色と背景色のコントラスト比と、WCAG の達成基準の判定
2. 色覚の多様性のシミュレーション (Machado らの方法)
3. 色だけに頼らない表現 (線の種類、印、直接のラベル)
"""

import numpy as np
from PIL import Image, ImageDraw

from color_utils import (FloatArray, contrast_ratio, font, hex_to_rgb,
                         labeled_rows, linear_to_srgb, save_image,
                         srgb_to_linear, swatches)

# Machado, Oliveira, Fernandes (2009) による、2 色覚 (重症度 1.0) の
# シミュレーション行列。線形 sRGB の値に掛けて使う。
CVD_MATRICES: dict[str, FloatArray] = {
    "Protan": np.array([
        [0.152286, 1.052583, -0.204868],
        [0.114503, 0.786281, 0.099216],
        [-0.003882, -0.048116, 1.051998],
    ]),
    "Deutan": np.array([
        [0.367322, 0.860646, -0.227968],
        [0.280085, 0.672501, 0.047413],
        [-0.011820, 0.042940, 0.968881],
    ]),
    "Tritan": np.array([
        [1.255528, -0.076749, -0.178779],
        [-0.078411, 0.930809, 0.147602],
        [0.004733, 0.691367, 0.303900],
    ]),
}

# 文字色と背景色の組。
CONTRAST_PAIRS = [
    ("#222222", "#ffffff"),
    ("#767676", "#ffffff"),
    ("#999999", "#ffffff"),
    ("#ffffff", "#f39800"),
    ("#ffffff", "#0068b7"),
    ("#e60012", "#1d2088"),
]


def simulate_cvd(rgb: FloatArray, kind: str) -> FloatArray:
    """sRGB の画像を、指定した種類の 2 色覚での見え方に近い色に変換する。"""
    linear = srgb_to_linear(rgb) @ CVD_MATRICES[kind].T
    return linear_to_srgb(linear)


def wcag_level(ratio: float) -> str:
    """通常の大きさの文字について、コントラスト比が満たす WCAG の水準。"""
    if ratio >= 7.0:
        return "AAA"
    if ratio >= 4.5:
        return "AA"
    return "fail"


def contrast_samples() -> Image.Image:
    """文字色と背景色の組ごとに見本の文字を描き、コントラスト比を添える。"""
    row_height, box_width, gap = 56, 300, 12
    width = box_width + 260
    height = gap + len(CONTRAST_PAIRS) * (row_height + gap)
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    sample_font = font(22)
    label_font = font(18)
    for i, (text_code, background_code) in enumerate(CONTRAST_PAIRS):
        top = gap + i * (row_height + gap)
        draw.rectangle((gap, top, gap + box_width, top + row_height),
                       fill=background_code, outline=(160, 160, 160))
        draw.text((gap + 16, top + row_height // 2), "Sample Text 123",
                  fill=text_code, font=sample_font, anchor="lm")
        ratio = contrast_ratio(hex_to_rgb(text_code),
                               hex_to_rgb(background_code))
        draw.text((gap + box_width + 16, top + row_height // 2),
                  f"{ratio:5.2f} : 1  {wcag_level(ratio)}", fill="black",
                  font=label_font, anchor="lm")
    return canvas


def cvd_palettes() -> Image.Image:
    """2 種類の配色を、2 色覚のシミュレーションとともに並べる。"""
    # 赤と緑を中心にした配色と、Okabe-Ito の配色から選んだ 4 色。
    red_green = [hex_to_rgb(c) for c in
                 ("#e60012", "#2ca02c", "#f39800", "#8fc31f")]
    okabe_ito = [hex_to_rgb(c) for c in
                 ("#d55e00", "#009e73", "#e69f00", "#0072b2")]
    chips = np.concatenate([
        swatches(red_green, width=72, height=48),
        np.ones((48, 32, 3)),
        swatches(okabe_ito, width=72, height=48),
    ], axis=1)
    rows = [("Original", chips)]
    for kind in CVD_MATRICES:
        rows.append((kind, simulate_cvd(chips, kind)))
    return labeled_rows(rows, label_width=120)


def draw_dashed_line(draw: ImageDraw.ImageDraw,
                     points: list[tuple[float, float]], color: str,
                     width: int) -> None:
    """点の列を結ぶ破線を描く。各区間を 5 つに分け、それぞれの前半だけを描く。"""
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        for start in np.arange(0.0, 1.0, 0.2):
            end = start + 0.12
            draw.line((x0 + (x1 - x0) * start, y0 + (y1 - y0) * start,
                       x0 + (x1 - x0) * end, y0 + (y1 - y0) * end),
                      fill=color, width=width)


def line_chart(redundant: bool, width: int = 360,
               height: int = 220) -> FloatArray:
    """2 本の折れ線のグラフを描く。

    ``redundant`` が偽のときは、赤と緑の色だけで系列を区別する。
    真のときは、色を朱色と青に変え、さらに線の種類 (実線と破線)、
    点の形 (丸と四角)、線の端の直接のラベルでも系列を区別する。
    """
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    left, right, top, bottom = 30, width - 70, 20, height - 30
    draw.line((left, top, left, bottom, right, bottom), fill="black",
              width=2)

    series = [
        ("A", [0.2, 0.35, 0.3, 0.55, 0.7]),
        ("B", [0.4, 0.3, 0.5, 0.45, 0.6]),
    ]
    colors = ["#d55e00", "#0072b2"] if redundant else ["#e60012", "#2ca02c"]
    label_font = font(18)
    for index, ((name, values), color) in enumerate(zip(series, colors)):
        xs = np.linspace(left + 20, right - 10, len(values))
        ys = bottom - (bottom - top) * np.array(values)
        points = list(zip(xs.tolist(), ys.tolist()))
        if not redundant:
            draw.line(points, fill=color, width=4)
            continue

        # 1 本目は実線と丸、2 本目は破線と四角で描く。
        if index == 0:
            draw.line(points, fill=color, width=4)
        else:
            draw_dashed_line(draw, points, color, width=4)
        for x, y in points:
            box = (x - 6, y - 6, x + 6, y + 6)
            if index == 0:
                draw.ellipse(box, fill=color)
            else:
                draw.rectangle(box, fill=color)
        draw.text((points[-1][0] + 12, points[-1][1]), name, fill=color,
                  font=label_font, anchor="lm")
    return np.asarray(canvas, dtype=float) / 255.0


def color_only_comparison() -> Image.Image:
    """色だけで区別したグラフと、ほかの手がかりを加えたグラフを比べる。"""
    gap = np.ones((220, 24, 3))
    rows = []
    for redundant, name in ((False, "Color only"), (True, "Redundant")):
        chart = line_chart(redundant)
        rows.append((name, np.concatenate(
            [chart, gap, simulate_cvd(chart, "Deutan")], axis=1)))
    return labeled_rows(rows, label_width=140)


def print_contrast_table() -> None:
    """コントラスト比の表を標準出力に表示する。"""
    print("文字色   背景色   コントラスト比  水準")
    for text_code, background_code in CONTRAST_PAIRS:
        ratio = contrast_ratio(hex_to_rgb(text_code),
                               hex_to_rgb(background_code))
        print(f"{text_code}  {background_code}  {ratio:6.2f}"
              f"          {wcag_level(ratio)}")


def main() -> None:
    """本章の図を作って保存し、コントラスト比の表を表示する。"""
    save_image(contrast_samples(), "contrast_samples.png")
    save_image(cvd_palettes(), "cvd_palettes.png")
    save_image(color_only_comparison(), "color_only.png")
    print_contrast_table()


if __name__ == "__main__":
    main()
