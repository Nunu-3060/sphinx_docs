"""色の生成と変換。

* sRGB と線形 RGB、OKLab の相互変換
* コサインパレット（Inigo Quilez による）
* グラデーションマップ（0〜1 の値を色に対応付ける）

色はすべて 0〜1 の実数で扱い、最後の軸を RGB（または L, a, b）の 3 成分とする。
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from common import FloatArray


def srgb_to_linear(srgb: FloatArray) -> FloatArray:
    """sRGB の値を、光の強さに比例する線形 RGB に変換する。"""
    return np.where(srgb <= 0.04045, srgb / 12.92, ((srgb + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(linear: FloatArray) -> FloatArray:
    """線形 RGB を sRGB に変換する。"""
    linear = np.clip(linear, 0.0, 1.0)
    return np.where(linear <= 0.0031308, linear * 12.92, 1.055 * linear ** (1.0 / 2.4) - 0.055)


_LMS_FROM_LINEAR = np.array(
    [[0.4122214708, 0.5363325363, 0.0514459929],
     [0.2119034982, 0.6806995451, 0.1073969566],
     [0.0883024619, 0.2817188376, 0.6299787005]]
)
_LAB_FROM_LMS = np.array(
    [[0.2104542553, 0.7936177850, -0.0040720468],
     [1.9779984951, -2.4285922050, 0.4505937099],
     [0.0259040371, 0.7827717662, -0.8086757660]]
)


def srgb_to_oklab(srgb: FloatArray) -> FloatArray:
    """sRGB を OKLab（L: 明るさ、a: 緑〜赤、b: 青〜黄）に変換する。"""
    lms = srgb_to_linear(srgb) @ _LMS_FROM_LINEAR.T
    result: FloatArray = np.cbrt(lms) @ _LAB_FROM_LMS.T
    return result


def oklab_to_srgb(lab: FloatArray) -> FloatArray:
    """OKLab を sRGB に変換する。sRGB の範囲外の色は 0〜1 に切り詰める。"""
    lms = (lab @ np.linalg.inv(_LAB_FROM_LMS).T) ** 3
    return linear_to_srgb(lms @ np.linalg.inv(_LMS_FROM_LINEAR).T)


def oklch_to_srgb(lightness: FloatArray, chroma: FloatArray, hue: FloatArray) -> FloatArray:
    """OKLCH（明るさ、彩度、色相 [ラジアン]）を sRGB に変換する。"""
    lab = np.stack([lightness, chroma * np.cos(hue), chroma * np.sin(hue)], axis=-1)
    return oklab_to_srgb(lab)


def hsv_to_rgb(hue: FloatArray, saturation: FloatArray, value: FloatArray) -> FloatArray:
    """HSV（色相 0〜1、彩度、明度）を RGB に変換する。"""
    h6 = (hue % 1.0) * 6.0
    k = np.stack([(5.0 + h6) % 6.0, (3.0 + h6) % 6.0, (1.0 + h6) % 6.0], axis=-1)
    weight = np.clip(np.minimum(k, 4.0 - k), 0.0, 1.0)
    result: FloatArray = value[..., None] * (1.0 - saturation[..., None] * weight)
    return result


def cosine_palette(
    t: FloatArray,
    a: Sequence[float] = (0.5, 0.5, 0.5),
    b: Sequence[float] = (0.5, 0.5, 0.5),
    c: Sequence[float] = (1.0, 1.0, 1.0),
    d: Sequence[float] = (0.0, 0.33, 0.67),
) -> FloatArray:
    """コサインパレット color(t) = a + b cos(2π(c t + d))。4 つの 3 次元ベクトルで色の変化を決める。"""
    t3 = np.asarray(t, dtype=np.float64)[..., None]
    result: FloatArray = np.asarray(a) + np.asarray(b) * np.cos(2.0 * np.pi * (np.asarray(c) * t3 + np.asarray(d)))
    return np.clip(result, 0.0, 1.0)


def gradient_map(values: FloatArray, stops: Sequence[tuple[float, Sequence[float]]]) -> FloatArray:
    """0〜1 の値を、(位置, RGB) の組で決めたグラデーションの色に置き換える。

    stops は位置の小さい順に並べる。色は sRGB の値をそのまま線形補間する。
    """
    positions = np.array([position for position, _ in stops])
    colors = np.array([rgb for _, rgb in stops], dtype=np.float64)
    clipped = np.clip(values, 0.0, 1.0)
    channels = [np.interp(clipped, positions, colors[:, channel]) for channel in range(3)]
    return np.stack(channels, axis=-1)


def hex_to_rgb(code: str) -> tuple[float, float, float]:
    """'#RRGGBB' 形式の色を 0〜1 の RGB にする。"""
    code = code.lstrip("#")
    return (int(code[0:2], 16) / 255.0, int(code[2:4], 16) / 255.0, int(code[4:6], 16) / 255.0)
