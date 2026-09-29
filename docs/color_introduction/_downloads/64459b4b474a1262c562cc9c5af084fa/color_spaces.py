"""「色空間」の章で使う図と数値を作る。

1. sRGB の値で等間隔な階調と、光の強さで等間隔な階調の比較
2. HSV と OKLCH で色相だけを回したときの、明るさの変化の比較
3. OKLab の a-b 平面の断面 (sRGB で表せる範囲)
4. RGB の距離が等しい色の組と、その色差 ΔE*ab の比較
"""

import numpy as np
from PIL import Image, ImageDraw

from color_utils import (FloatArray, delta_e_76, font, hex_to_rgb,
                         hsv_to_rgb, in_srgb_gamut, labeled_rows,
                         linear_to_srgb, oklab_to_srgb, oklch_to_srgb_in_gamut,
                         save_image, srgb_to_lab, swatches, to_grayscale,
                         to_uint8)

STRIP_WIDTH = 720
STRIP_HEIGHT = 48


def strip(row: FloatArray) -> FloatArray:
    """1 行分の色 (幅, 3) を縦に伸ばして帯状の画像にする。"""
    return np.repeat(row[np.newaxis, :, :], STRIP_HEIGHT, axis=0)


def stepped(values: FloatArray, steps: int) -> FloatArray:
    """0.0-1.0 の値を ``steps`` 段の階段状に丸める (段の違いを見やすくする)。"""
    return np.floor(values * steps) / (steps - 1)


def gamma_ramps() -> Image.Image:
    """sRGB の値で等間隔な階調と、線形な値 (光の強さ) で等間隔な階調。"""
    ramp = stepped(np.linspace(0.0, 1.0, STRIP_WIDTH, endpoint=False), 11)
    encoded = np.stack([ramp] * 3, axis=-1)
    linear = linear_to_srgb(encoded)
    return labeled_rows([
        ("sRGB value", strip(encoded)),
        ("Linear light", strip(linear)),
    ])


def hue_rotation() -> Image.Image:
    """HSV と OKLCH で色相を 1 周させた帯と、その明るさだけを残した帯。"""
    hue = np.linspace(0.0, 1.0, STRIP_WIDTH, endpoint=False)
    hsv = hsv_to_rgb(hue, 1.0, 1.0)
    oklch = oklch_to_srgb_in_gamut(0.75, 0.12, hue * 360.0)
    return labeled_rows([
        ("HSV", strip(hsv)),
        ("  lightness", strip(to_grayscale(hsv))),
        ("OKLCH", strip(oklch)),
        ("  lightness", strip(to_grayscale(oklch))),
    ], label_width=130)


def oklab_slice(lightness: float, size: int = 300,
                extent: float = 0.3) -> FloatArray:
    """明るさ L を固定した OKLab の a-b 平面。sRGB の色域外は灰色で塗る。"""
    axis = np.linspace(-extent, extent, size)
    a, b = np.meshgrid(axis, -axis)
    lab = np.stack([np.full_like(a, lightness), a, b], axis=-1)
    image = oklab_to_srgb(lab)
    image[~in_srgb_gamut(lab)] = 0.85
    # 原点 (無彩色の位置) に印を付ける。
    center = size // 2
    image[center - 1:center + 2, center - 8:center + 9] = 0.0
    image[center - 8:center + 9, center - 1:center + 2] = 0.0
    return image


def oklab_slices() -> Image.Image:
    """明るさ L を変えた OKLab の a-b 平面の断面を横に並べる。"""
    levels = [0.4, 0.6, 0.8, 0.95]
    size = 300
    gap = 16
    header = 32
    canvas = Image.new(
        "RGB", (len(levels) * (size + gap) + gap, size + header + gap),
        "white")
    draw = ImageDraw.Draw(canvas)
    label_font = font(18)
    for i, lightness in enumerate(levels):
        left = gap + i * (size + gap)
        canvas.paste(Image.fromarray(to_uint8(oklab_slice(lightness, size))),
                     (left, header))
        draw.text((left + size // 2, header // 2), f"L = {lightness:.2f}",
                  fill="black", font=label_font, anchor="mm")
    return canvas


# RGB のいずれか 1 成分だけを 51 (0x33) 変えた色の組。
# どの組も RGB 空間でのユークリッド距離は同じ 51 である。
DISTANCE_PAIRS = [
    ("#000000", "#003300"),
    ("#808080", "#80b380"),
    ("#0000ff", "#0033ff"),
    ("#ffff00", "#ffff33"),
    ("#00ff00", "#33ff00"),
]


def pair_delta_e(code1: str, code2: str) -> float:
    """2 つのカラーコードの色差 ΔE*ab を求める。"""
    lab1 = srgb_to_lab(hex_to_rgb(code1))
    lab2 = srgb_to_lab(hex_to_rgb(code2))
    return float(delta_e_76(lab1, lab2))


def distance_pairs() -> Image.Image:
    """RGB の距離が等しい色の組を並べ、色差 ΔE*ab をラベルに添える。"""
    rows = []
    for code1, code2 in DISTANCE_PAIRS:
        image = swatches([hex_to_rgb(code1), hex_to_rgb(code2)],
                         width=120, height=48)
        rows.append((f"dE = {pair_delta_e(code1, code2):4.1f}", image))
    return labeled_rows(rows, label_width=130)


def compare_distances() -> None:
    """RGB の距離と色差 ΔE*ab を表にして標準出力に表示する。"""
    print("色 1     色 2     RGB 距離  ΔE*ab")
    for code1, code2 in DISTANCE_PAIRS:
        rgb_distance = float(
            np.linalg.norm((hex_to_rgb(code1) - hex_to_rgb(code2)) * 255.0))
        print(f"{code1}  {code2}  {rgb_distance:8.1f}  "
              f"{pair_delta_e(code1, code2):5.1f}")


def main() -> None:
    """本章の図を作って保存し、色差の比較を表示する。"""
    save_image(gamma_ramps(), "gamma_ramps.png")
    save_image(hue_rotation(), "hue_rotation.png")
    save_image(oklab_slices(), "oklab_slices.png")
    save_image(distance_pairs(), "distance_pairs.png")
    compare_distances()


if __name__ == "__main__":
    main()
