"""知覚的に均等な色空間 OKLab による明るさの比較と色の補間。

HSV(HSB)の明度 V は RGB の最大成分をそのまま表しているだけで、
人間が感じる明るさとは一致しない。V を固定して色相だけを回すと、
黄色は明るく、青は暗く見える。Björn Ottosson (2020) の **OKLab** は、
座標の差が見た目の色の差にほぼ比例するよう設計された色空間で、
明るさ L と、2つの色度軸 a(緑-赤)・b(青-黄)から成る。
ここでは sRGB と OKLab の相互変換を NumPy で自前実装し、次の2つを
確かめる。

1. HSV と OKLCH(OKLab の極座標表示)で色相を回したときの、
   知覚的な明るさの変化の違い
2. sRGB の値のまま補間したグラデーションと、OKLab で補間した
   グラデーションの違い
"""

import numpy as np
from PIL import Image

from palette import hsv_to_rgb

# 線形 sRGB -> LMS(錐体応答に近い3成分)への変換行列。
_RGB_TO_LMS: np.ndarray = np.array([
    [0.4122214708, 0.5363325363, 0.0514459929],
    [0.2119034982, 0.6806995451, 0.1073969566],
    [0.0883024619, 0.2817188376, 0.6299787005]])

# 立方根を取った LMS -> OKLab (L, a, b) への変換行列。
_LMS_TO_LAB: np.ndarray = np.array([
    [0.2104542553, 0.7936177850, -0.0040720468],
    [1.9779984951, -2.4285922050, 0.4505937099],
    [0.0259040371, 0.7827717662, -0.8086757660]])


def srgb_to_linear(rgb: np.ndarray) -> np.ndarray:
    """ガンマ補正された sRGB 値(0.0-1.0)を、光の強さに比例する線形値に戻す。"""
    rgb = np.asarray(rgb, dtype=float)
    return np.where(
        rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4
    )


def linear_to_srgb(linear: np.ndarray) -> np.ndarray:
    """線形値(0.0-1.0)を、画像として保存する sRGB 値にガンマ補正する。"""
    linear = np.clip(np.asarray(linear, dtype=float), 0.0, 1.0)
    return np.where(
        linear <= 0.0031308,
        linear * 12.92,
        1.055 * linear ** (1.0 / 2.4) - 0.055,
    )


def srgb_to_oklab(rgb: np.ndarray) -> np.ndarray:
    """sRGB 値(末尾の軸が RGB、0.0-1.0)を OKLab (L, a, b) に変換する。"""
    lms: np.ndarray = srgb_to_linear(rgb) @ _RGB_TO_LMS.T
    return np.cbrt(lms) @ _LMS_TO_LAB.T


def oklab_to_srgb(lab: np.ndarray) -> np.ndarray:
    """OKLab (L, a, b) を sRGB 値(0.0-1.0)に戻す。

    sRGB で表せない色(色域外)は、各成分を 0.0-1.0 に切り詰める。
    """
    lms_cbrt: np.ndarray = np.asarray(lab, dtype=float) @ np.linalg.inv(
        _LMS_TO_LAB
    ).T
    linear: np.ndarray = lms_cbrt**3 @ np.linalg.inv(_RGB_TO_LMS).T
    return linear_to_srgb(linear)


def oklch_to_srgb(
    lightness: np.ndarray | float,
    chroma: np.ndarray | float,
    hue: np.ndarray | float,
) -> np.ndarray:
    """OKLCH (明るさ L、彩度 C、色相 h) を sRGB 値(0.0-1.0)に変換する。

    OKLCH は OKLab の (a, b) 平面を極座標で表したもので、色相 ``hue``
    は HSV と同じく 1 周 = 1.0 の環状の値として扱う。
    """
    angle: np.ndarray = 2.0 * np.pi * np.asarray(hue, dtype=float)
    lab: np.ndarray = np.stack(
        np.broadcast_arrays(
            np.asarray(lightness, dtype=float),
            chroma * np.cos(angle),
            chroma * np.sin(angle),
        ),
        axis=-1,
    )
    return oklab_to_srgb(lab)


def mix_srgb(
    start: np.ndarray, end: np.ndarray, t: np.ndarray
) -> np.ndarray:
    """2色を sRGB の値のまま線形補間する。t は形状 (steps,) の配列。"""
    return start + (end - start) * t[:, np.newaxis]


def mix_oklab(
    start: np.ndarray, end: np.ndarray, t: np.ndarray
) -> np.ndarray:
    """2色を OKLab 空間で線形補間し、sRGB 値に戻す。"""
    lab_start: np.ndarray = srgb_to_oklab(start)
    lab_end: np.ndarray = srgb_to_oklab(end)
    return oklab_to_srgb(lab_start + (lab_end - lab_start) * t[:, np.newaxis])


def lightness_as_gray(rgb: np.ndarray) -> np.ndarray:
    """各色の OKLab の明るさ L を、同じ明るさに見えるグレーに置き換える。"""
    lightness: np.ndarray = srgb_to_oklab(rgb)[..., 0]
    gray_lab: np.ndarray = np.stack(
        [lightness, np.zeros_like(lightness), np.zeros_like(lightness)],
        axis=-1,
    )
    return oklab_to_srgb(gray_lab)


def _band(colors: np.ndarray, height: int) -> np.ndarray:
    """(steps, 3) の色配列(0.0-1.0)を、高さ height の帯状の画素配列にする。"""
    row: np.ndarray = (np.clip(colors, 0.0, 1.0) * 255).round()
    return np.tile(row.astype(np.uint8)[np.newaxis], (height, 1, 1))


def render_bands(
    rows: list[np.ndarray], height: int = 60, gap: int = 6
) -> Image.Image:
    """複数の (steps, 3) の色配列を、白い隙間を挟んで縦に並べた画像にする。"""
    width: int = rows[0].shape[0]
    total: int = height * len(rows) + gap * (len(rows) - 1)
    pixels: np.ndarray = np.full((total, width, 3), 255, dtype=np.uint8)
    for i, colors in enumerate(rows):
        top: int = i * (height + gap)
        pixels[top:top + height] = _band(colors, height)
    return Image.fromarray(pixels)


def main() -> None:
    steps: int = 480
    hues: np.ndarray = np.linspace(0.0, 1.0, steps, endpoint=False)

    # 上2段: HSV で S=V=1 のまま色相を回した帯と、その明るさ。
    # 下2段: OKLCH で L・C を固定して色相を回した帯と、その明るさ。
    hsv_band: np.ndarray = hsv_to_rgb(hues, 1.0, 1.0)
    oklch_band: np.ndarray = oklch_to_srgb(0.75, 0.12, hues)
    render_bands(
        [
            hsv_band,
            lightness_as_gray(hsv_band),
            oklch_band,
            lightness_as_gray(oklch_band),
        ]
    ).save("oklab_hue_lightness.png")

    # 同じ2色の間を、sRGB の値のまま補間した場合(上)と
    # OKLab で補間した場合(下)を比べる。
    t: np.ndarray = np.linspace(0.0, 1.0, steps)
    pairs: list[tuple[np.ndarray, np.ndarray]] = [
        (np.array([0.0, 0.2, 1.0]), np.array([1.0, 0.85, 0.0])),
        (np.array([1.0, 0.0, 0.3]), np.array([0.0, 0.8, 0.4])),
    ]
    rows: list[np.ndarray] = []
    for start, end in pairs:
        rows.append(mix_srgb(start, end, t))
        rows.append(mix_oklab(start, end, t))
    render_bands(rows).save("oklab_gradient.png")


if __name__ == "__main__":
    main()
