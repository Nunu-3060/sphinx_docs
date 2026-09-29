"""「印刷物の配色」の章で使う図を作る。

1. 簡易的な式で RGB の画像を CMYK の 4 つの版に分けた図
2. 網点の面積率と印刷の濃さの関係 (ドットゲインと用紙の影響) の簡易モデル

どちらも考え方を示すための単純化したモデルである。実際の印刷用の変換には、
印刷条件に合わせた ICC プロファイルを使う。
"""

import numpy as np
from PIL import Image, ImageDraw

from color_utils import (FloatArray, font, gray, hex_to_rgb, labeled_rows,
                         linear_to_srgb, save_image, srgb_to_linear, to_uint8)
from palette import sunset_scene

# 各インキの色 (sRGB 値)。版を表示するときに使う。
INK_COLORS: dict[str, FloatArray] = {
    "C": hex_to_rgb("#00a0e9"),
    "M": hex_to_rgb("#e4007f"),
    "Y": hex_to_rgb("#fff100"),
    "K": hex_to_rgb("#231815"),
}


def naive_rgb_to_cmyk(rgb: FloatArray) -> FloatArray:
    """RGB を CMYK の網点の面積率 (0.0-1.0) に変換する簡易的な式。

    K (黒) を R、G、B の最大値から決め、残りを C、M、Y に割り振る。
    インキや用紙の特性を考慮していないので、実際の印刷の色は再現できない。
    """
    rgb = np.asarray(rgb, dtype=float)
    k = 1.0 - rgb.max(axis=-1)
    # K = 1 (黒) の画素では C、M、Y を 0 にする (0 除算を避ける)。
    scale = np.where(k < 1.0, 1.0 - k, 1.0)[..., np.newaxis]
    cmy = (1.0 - rgb - k[..., np.newaxis]) / scale
    return np.concatenate([cmy, k[..., np.newaxis]], axis=-1)


def plate_image(coverage: FloatArray, ink: FloatArray) -> FloatArray:
    """1 つの版の面積率を、白い紙にそのインキだけを刷った色で表す。"""
    return 1.0 - coverage[..., np.newaxis] * (1.0 - ink)


def cmyk_plates() -> Image.Image:
    """元の画像と、そこから分けた C、M、Y、K の 4 つの版を並べる。"""
    scene = sunset_scene(width=240, height=160)
    cmyk = naive_rgb_to_cmyk(scene)
    tiles = [("RGB", scene)]
    for i, name in enumerate(INK_COLORS):
        tiles.append((name, plate_image(cmyk[..., i], INK_COLORS[name])))

    gap, header = 12, 28
    width = len(tiles) * (240 + gap) + gap
    canvas = Image.new("RGB", (width, 160 + header + gap), "white")
    label_font = font(18)
    draw = ImageDraw.Draw(canvas)
    for i, (name, tile) in enumerate(tiles):
        left = gap + i * (240 + gap)
        canvas.paste(Image.fromarray(to_uint8(tile)), (left, header))
        draw.rectangle((left - 1, header - 1, left + 240, header + 160),
                       outline=(160, 160, 160))
        draw.text((left + 120, header // 2), name, fill="black",
                  font=label_font, anchor="mm")
    return canvas


def dot_gain(coverage: FloatArray, gain_at_half: float) -> FloatArray:
    """網点が太ることによる、実際の面積率の増え方を放物線で近似する。

    面積率 50% のときに ``gain_at_half`` だけ増え、0% と 100% では増えない。
    """
    gained = coverage + gain_at_half * 4.0 * coverage * (1.0 - coverage)
    return np.clip(gained, 0.0, 1.0)


def printed_tone(coverage: FloatArray, paper: FloatArray,
                 ink: FloatArray) -> FloatArray:
    """黒インキの網点の面積率から、印刷物の見た目の色を求める。

    Murray-Davies の式にならい、光の反射率 (線形な値) を、インキの部分と
    紙の部分の面積で重み付けして平均する。
    """
    reflectance = (coverage[..., np.newaxis] * srgb_to_linear(ink)
                   + (1.0 - coverage[..., np.newaxis]) * srgb_to_linear(paper))
    return linear_to_srgb(reflectance)


def tone_steps() -> Image.Image:
    """面積率 0% から 100% までの階調を、印刷の条件ごとに並べる。"""
    coverage = np.repeat(np.linspace(0.0, 1.0, 11), 60)
    white_paper, black_ink = gray(1.0), gray(0.08)
    uncoated_paper, uncoated_ink = hex_to_rgb("#f1ede3"), gray(0.18)

    rows = [
        ("Nominal", printed_tone(coverage, white_paper, black_ink)),
        ("Dot gain 15%",
         printed_tone(dot_gain(coverage, 0.15), white_paper, black_ink)),
        ("Uncoated",
         printed_tone(dot_gain(coverage, 0.22), uncoated_paper,
                      uncoated_ink)),
    ]
    return labeled_rows(
        [(name, np.repeat(row[np.newaxis, :, :], 48, axis=0))
         for name, row in rows],
        label_width=150)


def main() -> None:
    """本章の図を作り、保存する。"""
    save_image(cmyk_plates(), "cmyk_plates.png")
    save_image(tone_steps(), "print_tones.png")


if __name__ == "__main__":
    main()
