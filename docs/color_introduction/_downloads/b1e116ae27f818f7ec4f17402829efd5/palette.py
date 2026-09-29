"""「パレットの作り方」の章で使う図を作る。

1. 2 色の間の補間 (グラデーション) を、色空間ごとに比べる
2. 基準の色から濃淡の段階 (カラースケール) を作る
3. 画像から代表的な色を k-means 法で取り出す
"""

import numpy as np
from numpy.typing import NDArray
from PIL import Image, ImageDraw

from color_utils import (FloatArray, font, hex_to_rgb, labeled_rows,
                         linear_to_srgb, oklab_to_oklch, oklab_to_srgb,
                         oklch_to_srgb_in_gamut, rgb_to_hex, save_image,
                         srgb_to_linear, srgb_to_oklab, swatches,
                         to_grayscale, to_uint8)

STRIP_WIDTH = 640
STRIP_HEIGHT = 48


def strip(row: FloatArray) -> FloatArray:
    """1 行分の色 (幅, 3) を縦に伸ばして帯状の画像にする。"""
    return np.repeat(row[np.newaxis, :, :], STRIP_HEIGHT, axis=0)


# ---------------------------------------------------------------------------
# 補間
# ---------------------------------------------------------------------------

def lerp(start: FloatArray, end: FloatArray, t: FloatArray) -> FloatArray:
    """``start`` から ``end`` へ、割合 ``t`` (0.0-1.0) で線形補間する。"""
    return start + (end - start) * t[:, np.newaxis]


def interpolate_srgb(start: FloatArray, end: FloatArray,
                     t: FloatArray) -> FloatArray:
    """sRGB の値のまま補間する。"""
    return lerp(start, end, t)


def interpolate_linear(start: FloatArray, end: FloatArray,
                       t: FloatArray) -> FloatArray:
    """線形な値 (光の強さ) に戻してから補間する。"""
    mixed = lerp(srgb_to_linear(start), srgb_to_linear(end), t)
    return linear_to_srgb(mixed)


def interpolate_oklab(start: FloatArray, end: FloatArray,
                      t: FloatArray) -> FloatArray:
    """OKLab の直交座標 (L, a, b) で補間する。"""
    mixed = lerp(srgb_to_oklab(start), srgb_to_oklab(end), t)
    return oklab_to_srgb(mixed)


def interpolate_oklch(start: FloatArray, end: FloatArray,
                      t: FloatArray) -> FloatArray:
    """OKLCH の極座標 (L, C, h) で補間する。色相は近い向きに回す。"""
    lch1 = oklab_to_oklch(srgb_to_oklab(start))
    lch2 = oklab_to_oklch(srgb_to_oklab(end))
    # 色相の差を -180 度から 180 度の範囲にして、短い向きに回す。
    hue_diff = (lch2[2] - lch1[2] + 180.0) % 360.0 - 180.0
    lightness = lch1[0] + (lch2[0] - lch1[0]) * t
    chroma = lch1[1] + (lch2[1] - lch1[1]) * t
    hue = lch1[2] + hue_diff * t
    return oklch_to_srgb_in_gamut(lightness, chroma, hue)


def interpolation_comparison() -> Image.Image:
    """青から黄への補間を、4 つの方法で比べる。"""
    start, end = hex_to_rgb("#0000ff"), hex_to_rgb("#ffff00")
    t = np.linspace(0.0, 1.0, STRIP_WIDTH)
    return labeled_rows([
        ("sRGB", strip(interpolate_srgb(start, end, t))),
        ("Linear RGB", strip(interpolate_linear(start, end, t))),
        ("OKLab", strip(interpolate_oklab(start, end, t))),
        ("OKLCH", strip(interpolate_oklch(start, end, t))),
    ], label_width=130)


# ---------------------------------------------------------------------------
# カラースケール
# ---------------------------------------------------------------------------

def mix_scale(base: FloatArray, steps: int) -> list[FloatArray]:
    """基準の色に白または黒を sRGB の値で混ぜて、濃淡の段階を作る。

    明るい側の半分は白を、暗い側の半分は黒を混ぜる。
    """
    white, black = np.ones(3), np.zeros(3)
    half = steps // 2
    light = [base + (white - base) * (1.0 - i / half) for i in range(half)]
    dark = [base + (black - base) * (i / (steps - half))
            for i in range(steps - half)]
    return light + dark


def oklch_scale(base: FloatArray, steps: int, lightest: float = 0.96,
                darkest: float = 0.30) -> list[FloatArray]:
    """基準の色の色相を保ち、OKLab の明るさ L を等間隔に変えて段階を作る。

    明るさは ``lightest`` から ``darkest`` まで変える。明るさの両端では
    表せる彩度が小さくなるため、彩度は中央で最大になるように山形に変え、
    さらに色域に収まるように下げる。
    """
    _, base_chroma, hue = oklab_to_oklch(srgb_to_oklab(base))
    colors = []
    for lightness in np.linspace(lightest, darkest, steps):
        # 明るさ 0.62 付近で基準の彩度になり、両端に向かって小さくなる。
        weight = 1.0 - abs(lightness - 0.62) / 0.5
        chroma = base_chroma * max(weight, 0.15)
        colors.append(oklch_to_srgb_in_gamut(lightness, chroma, hue))
    return colors


def scale_comparison() -> Image.Image:
    """2 つの方法で作ったカラースケールと、その明るさを並べる。"""
    # 明度の高い橙を基準にすると、2 つの方法の違いが分かりやすい。
    base = hex_to_rgb("#e8a33d")
    steps = 10
    mixed = swatches(mix_scale(base, steps), width=64, height=56)
    perceptual = swatches(oklch_scale(base, steps), width=64, height=56)
    return labeled_rows([
        ("sRGB mix", mixed),
        ("  lightness", to_grayscale(mixed)),
        ("OKLCH", perceptual),
        ("  lightness", to_grayscale(perceptual)),
    ], label_width=130)


# ---------------------------------------------------------------------------
# 画像からの配色の抽出
# ---------------------------------------------------------------------------

def sunset_scene(width: int = 480, height: int = 320,
                 seed: int = 1) -> FloatArray:
    """夕焼けの海辺を模した画像を作る (抽出の題材にする)。"""
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:height, 0:width].astype(float)
    horizon = height * 0.62

    # 空: 上の紫から地平線の橙へのグラデーション。
    sky_t = np.clip(y / horizon, 0.0, 1.0)
    sky_top, sky_bottom = hex_to_rgb("#3b2c63"), hex_to_rgb("#f39a4a")
    image = oklab_to_srgb(
        srgb_to_oklab(sky_top) * (1.0 - sky_t[..., np.newaxis])
        + srgb_to_oklab(sky_bottom) * sky_t[..., np.newaxis])

    # 太陽: 地平線に半分沈んだ円。
    sun_x = width * 0.62
    sun = (x - sun_x) ** 2 + (y - horizon) ** 2 < (height * 0.1) ** 2
    image[sun] = hex_to_rgb("#ffd36b")

    # 山並み: 正弦波を重ねた稜線より下を暗い色で塗る。
    # 太陽を隠さないよう、太陽に近いほど山を低くする。
    envelope = np.clip((np.abs(x - sun_x) - 40.0) / 100.0, 0.0, 1.0)
    ridge = horizon - envelope * (
        40.0 + 18.0 * np.sin(x / 57.0) + 10.0 * np.sin(x / 23.0 + 1.0))
    image[(y > ridge) & (y < horizon)] = hex_to_rgb("#4a2f4f")

    # 海: 地平線より下。深いところほど暗い青にする。
    sea_t = np.clip((y - horizon) / (height - horizon), 0.0, 1.0)
    sea_top, sea_bottom = hex_to_rgb("#6b5a8e"), hex_to_rgb("#1d2b4f")
    sea = (sea_top * (1.0 - sea_t[..., np.newaxis])
           + sea_bottom * sea_t[..., np.newaxis])
    below = y >= horizon
    image[below] = sea[below]

    # 海面に映る太陽の光: 横縞状の明るい帯。
    glitter = (below & (np.abs(x - sun_x) < 36.0 - sea_t * 24.0)
               & (np.sin(y * 0.9 + np.sin(x * 0.2) * 2.0) > 0.3))
    image[glitter] = hex_to_rgb("#f7b267")

    noise = rng.normal(0.0, 0.015, image.shape)
    return np.clip(image + noise, 0.0, 1.0)


def kmeans(points: FloatArray, k: int, iterations: int = 30,
           seed: int = 0) -> tuple[FloatArray, NDArray[np.intp]]:
    """k-means 法で点の集まりを ``k`` 個のクラスタに分ける。

    戻り値は (各クラスタの中心, 各点が属するクラスタの番号)。
    """
    rng = np.random.default_rng(seed)
    centers = points[rng.choice(len(points), size=k, replace=False)]
    labels = np.zeros(len(points), dtype=np.intp)
    for _ in range(iterations):
        # 各点を、最も近い中心のクラスタに割り当てる。
        distances = np.linalg.norm(
            points[:, np.newaxis, :] - centers[np.newaxis, :, :], axis=-1)
        labels = np.argmin(distances, axis=1)
        # 各クラスタの中心を、属する点の平均に動かす。
        for i in range(k):
            members = points[labels == i]
            if len(members) > 0:
                centers[i] = members.mean(axis=0)
    return centers, labels


def extract_palette(image: FloatArray, k: int,
                    sample: int = 6000) -> list[tuple[FloatArray, float]]:
    """画像から ``k`` 色を取り出し、(色, 画像に占める割合) の並びを返す。

    距離を見た目の差に近づけるため、画素を OKLab に変換してから分類する。
    計算を軽くするため、画素の一部を無作為に選んで使う。
    """
    rng = np.random.default_rng(0)
    pixels = srgb_to_oklab(image.reshape(-1, 3))
    chosen = pixels[rng.choice(len(pixels), size=sample, replace=False)]
    centers, labels = kmeans(chosen, k)
    shares = np.bincount(labels, minlength=k) / len(labels)
    order = np.argsort(centers[:, 0])  # 暗い色から明るい色の順に並べる。
    return [(oklab_to_srgb(centers[i]), float(shares[i])) for i in order]


def palette_figure(image: FloatArray,
                   palette: list[tuple[FloatArray, float]]) -> Image.Image:
    """元の画像の下に、取り出した色と占める割合を並べた図を作る。"""
    height, width = image.shape[:2]
    chip = width // len(palette)
    canvas = Image.new("RGB", (width, height + chip + 32), "white")
    canvas.paste(Image.fromarray(to_uint8(image)), (0, 0))
    draw = ImageDraw.Draw(canvas)
    label_font = font(16)
    for i, (color, share) in enumerate(palette):
        left = i * chip
        r, g, b = (int(v) for v in to_uint8(color))
        draw.rectangle((left, height + 8, left + chip - 8, height + chip),
                       fill=(r, g, b))
        draw.text((left + (chip - 8) // 2, height + chip + 16),
                  f"{share * 100:.0f}%", fill="black", font=label_font,
                  anchor="mm")
    return canvas


def main() -> None:
    """本章の図を作って保存し、画像から取り出した色を表示する。"""
    save_image(interpolation_comparison(), "interpolation.png")
    save_image(scale_comparison(), "color_scale.png")

    scene = sunset_scene()
    palette = extract_palette(scene, k=6)
    save_image(palette_figure(scene, palette), "extracted_palette.png")
    print("取り出した色 (割合)")
    for color, share in palette:
        print(f"  {rgb_to_hex(color)}  {share * 100:5.1f}%")


if __name__ == "__main__":
    main()
