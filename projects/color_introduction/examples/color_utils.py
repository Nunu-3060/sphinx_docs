"""色の変換と画像の保存に使う共通の関数をまとめたモジュール。

本資料のサンプルコードは、全てこのモジュールの関数を使って色を扱う。
色は NumPy 配列で表し、末尾の軸を (R, G, B) などの 3 成分とする。
sRGB の値は 0.0 から 1.0 の実数で扱い、画像として保存するときだけ
0 から 255 の整数に変換する。

主な内容は次のとおり。

* 16 進数のカラーコードと sRGB 値の相互変換
* sRGB のガンマ補正(非線形な値と、光の強さに比例する線形な値の変換)
* HSV から sRGB への変換
* CIE XYZ、CIELAB への変換と色差 ΔE*ab
* OKLab、OKLCH と sRGB の相互変換、色域に収まるように彩度を下げる処理
* WCAG の相対輝度とコントラスト比
"""

import sys
from pathlib import Path
from typing import Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray
from PIL import Image, ImageDraw, ImageFont

FloatArray = NDArray[np.float64]

# 線形 sRGB から CIE XYZ (D65 白色点) への変換行列 (IEC 61966-2-1)。
RGB_TO_XYZ: FloatArray = np.array([
    [0.4124564, 0.3575761, 0.1804375],
    [0.2126729, 0.7151522, 0.0721750],
    [0.0193339, 0.1191920, 0.9503041],
])

# D65 白色点の XYZ 値 (Y = 1 に正規化したもの)。
WHITE_D65: FloatArray = np.array([0.95047, 1.0, 1.08883])

# 線形 sRGB から LMS (錐体の応答に近い 3 成分) への変換行列 (OKLab)。
_RGB_TO_LMS: FloatArray = np.array([
    [0.4122214708, 0.5363325363, 0.0514459929],
    [0.2119034982, 0.6806995451, 0.1073969566],
    [0.0883024619, 0.2817188376, 0.6299787005],
])

# 立方根を取った LMS から OKLab (L, a, b) への変換行列。
_LMS_TO_LAB: FloatArray = np.array([
    [0.2104542553, 0.7936177850, -0.0040720468],
    [1.9779984951, -2.4285922050, 0.4505937099],
    [0.0259040371, 0.7827717662, -0.8086757660],
])

_LMS_TO_RGB: FloatArray = np.linalg.inv(_RGB_TO_LMS)
_LAB_TO_LMS: FloatArray = np.linalg.inv(_LMS_TO_LAB)


# ---------------------------------------------------------------------------
# カラーコード
# ---------------------------------------------------------------------------

def hex_to_rgb(code: str) -> FloatArray:
    """``"#1f77b4"`` のようなカラーコードを sRGB 値 (0.0-1.0) に変換する。"""
    text = code.lstrip("#")
    if len(text) != 6:
        raise ValueError(f"6 桁のカラーコードではありません: {code}")
    values = [int(text[i:i + 2], 16) for i in range(0, 6, 2)]
    return np.array(values, dtype=float) / 255.0


def rgb_to_hex(rgb: ArrayLike) -> str:
    """sRGB 値 (0.0-1.0) を ``"#rrggbb"`` 形式のカラーコードに変換する。"""
    r, g, b = to_uint8(rgb)
    return f"#{r:02x}{g:02x}{b:02x}"


def to_uint8(rgb: ArrayLike) -> NDArray[np.uint8]:
    """sRGB 値 (0.0-1.0) を、画像に保存する 0-255 の整数に変換する。"""
    values = np.clip(np.asarray(rgb, dtype=float), 0.0, 1.0)
    return np.asarray(np.round(values * 255.0), dtype=np.uint8)


# ---------------------------------------------------------------------------
# sRGB のガンマ補正
# ---------------------------------------------------------------------------

def srgb_to_linear(rgb: ArrayLike) -> FloatArray:
    """ガンマ補正された sRGB 値を、光の強さに比例する線形な値に戻す。"""
    values = np.asarray(rgb, dtype=float)
    return np.where(
        values <= 0.04045,
        values / 12.92,
        ((values + 0.055) / 1.055) ** 2.4,
    )


def linear_to_srgb(linear: ArrayLike) -> FloatArray:
    """線形な値を、画像として保存する sRGB 値にガンマ補正する。

    0.0-1.0 の範囲外の値は、範囲内に切り詰めてから変換する。
    """
    values: FloatArray = np.clip(np.asarray(linear, dtype=float), 0.0, 1.0)
    return np.where(
        values <= 0.0031308,
        values * 12.92,
        1.055 * values ** (1.0 / 2.4) - 0.055,
    )


# ---------------------------------------------------------------------------
# HSV
# ---------------------------------------------------------------------------

def hsv_to_rgb(hue: ArrayLike, saturation: ArrayLike,
               value: ArrayLike) -> FloatArray:
    """HSV を sRGB 値に変換する。

    色相 ``hue`` は 1 周を 1.0 とする値 (0.0 が赤、1/3 が緑、2/3 が青)、
    彩度 ``saturation`` と明度 ``value`` は 0.0-1.0 の値で与える。
    引数は同じ形の配列でもよく、戻り値の末尾に RGB の軸が加わる。
    """
    h = np.mod(np.asarray(hue, dtype=float), 1.0) * 6.0
    s = np.asarray(saturation, dtype=float)
    v = np.asarray(value, dtype=float)
    h, s, v = np.broadcast_arrays(h, s, v)

    sector = np.floor(h).astype(int) % 6
    fraction = h - np.floor(h)
    p = v * (1.0 - s)
    q = v * (1.0 - s * fraction)
    t = v * (1.0 - s * (1.0 - fraction))

    # 色相環を 60 度ずつ 6 つに分け、区間ごとに RGB の並びを決める。
    r = np.choose(sector, [v, q, p, p, t, v])
    g = np.choose(sector, [t, v, v, q, p, p])
    b = np.choose(sector, [p, p, t, v, v, q])
    return np.stack([r, g, b], axis=-1)


# ---------------------------------------------------------------------------
# CIE XYZ と CIELAB
# ---------------------------------------------------------------------------

def srgb_to_xyz(rgb: ArrayLike) -> FloatArray:
    """sRGB 値を CIE XYZ (D65、白の Y = 1) に変換する。"""
    return srgb_to_linear(rgb) @ RGB_TO_XYZ.T


def xyz_to_lab(xyz: ArrayLike) -> FloatArray:
    """CIE XYZ を CIELAB (L*, a*, b*) に変換する。白色点は D65 とする。"""
    ratio = np.asarray(xyz, dtype=float) / WHITE_D65
    delta = 6.0 / 29.0
    f = np.where(
        ratio > delta ** 3,
        np.cbrt(ratio),
        ratio / (3.0 * delta ** 2) + 4.0 / 29.0,
    )
    lightness = 116.0 * f[..., 1] - 16.0
    a = 500.0 * (f[..., 0] - f[..., 1])
    b = 200.0 * (f[..., 1] - f[..., 2])
    return np.stack([lightness, a, b], axis=-1)


def srgb_to_lab(rgb: ArrayLike) -> FloatArray:
    """sRGB 値を CIELAB (L*, a*, b*) に変換する。"""
    return xyz_to_lab(srgb_to_xyz(rgb))


def delta_e_76(lab1: ArrayLike, lab2: ArrayLike) -> FloatArray:
    """CIELAB の 2 色の間のユークリッド距離 (色差 ΔE*ab) を求める。"""
    diff = np.asarray(lab1, dtype=float) - np.asarray(lab2, dtype=float)
    return np.sqrt(np.sum(diff ** 2, axis=-1))


# ---------------------------------------------------------------------------
# OKLab と OKLCH
# ---------------------------------------------------------------------------

def srgb_to_oklab(rgb: ArrayLike) -> FloatArray:
    """sRGB 値を OKLab (L, a, b) に変換する。"""
    lms = srgb_to_linear(rgb) @ _RGB_TO_LMS.T
    return np.cbrt(lms) @ _LMS_TO_LAB.T


def oklab_to_linear(lab: ArrayLike) -> FloatArray:
    """OKLab を線形 sRGB 値に変換する。色域外の値は切り詰めない。"""
    lms_cbrt = np.asarray(lab, dtype=float) @ _LAB_TO_LMS.T
    return (lms_cbrt ** 3) @ _LMS_TO_RGB.T


def oklab_to_srgb(lab: ArrayLike) -> FloatArray:
    """OKLab を sRGB 値に変換する。色域外の成分は 0.0-1.0 に切り詰める。"""
    return linear_to_srgb(oklab_to_linear(lab))


def oklch_to_oklab(lightness: ArrayLike, chroma: ArrayLike,
                   hue_deg: ArrayLike) -> FloatArray:
    """OKLCH (明るさ L、彩度 C、色相角 h [度]) を OKLab に変換する。"""
    angle = np.deg2rad(np.asarray(hue_deg, dtype=float))
    c = np.asarray(chroma, dtype=float)
    lightness_arr, a, b = np.broadcast_arrays(
        np.asarray(lightness, dtype=float), c * np.cos(angle),
        c * np.sin(angle))
    return np.stack([lightness_arr, a, b], axis=-1)


def oklab_to_oklch(lab: ArrayLike) -> FloatArray:
    """OKLab を OKLCH (L, C, h [度]) に変換する。h は 0 以上 360 未満。"""
    values = np.asarray(lab, dtype=float)
    chroma = np.hypot(values[..., 1], values[..., 2])
    hue = np.mod(np.rad2deg(np.arctan2(values[..., 2], values[..., 1])),
                 360.0)
    return np.stack([values[..., 0], chroma, hue], axis=-1)


def in_srgb_gamut(lab: ArrayLike, tolerance: float = 1e-6) -> NDArray[
        np.bool_]:
    """OKLab の色が sRGB の色域 (RGB が全て 0.0-1.0) に収まるかを返す。"""
    linear = oklab_to_linear(lab)
    inside = (linear >= -tolerance) & (linear <= 1.0 + tolerance)
    return np.all(inside, axis=-1)


def oklch_to_srgb_in_gamut(lightness: ArrayLike, chroma: ArrayLike,
                           hue_deg: ArrayLike) -> FloatArray:
    """OKLCH を sRGB 値に変換する。色域外の色は彩度だけを下げて収める。

    RGB の各成分を単純に切り詰めると、明るさや色相まで変わってしまう。
    ここでは明るさ L と色相 h を保ったまま、色域に収まる最大の彩度を
    二分探索で求める。
    """
    lightness_arr, chroma_arr, hue_arr = np.broadcast_arrays(
        np.asarray(lightness, dtype=float), np.asarray(chroma, dtype=float),
        np.asarray(hue_deg, dtype=float))
    # low は常に色域内、high は元の彩度から始まる探索範囲の上端。
    low = np.zeros_like(chroma_arr)
    high = chroma_arr.copy()
    for _ in range(30):
        middle = (low + high) / 2.0
        ok = in_srgb_gamut(oklch_to_oklab(lightness_arr, middle, hue_arr))
        low = np.where(ok, middle, low)
        high = np.where(ok, high, middle)
    return oklab_to_srgb(oklch_to_oklab(lightness_arr, low, hue_arr))


def oklab_lightness(rgb: ArrayLike) -> FloatArray:
    """sRGB 値の知覚的な明るさとして、OKLab の L (0.0-1.0) を返す。"""
    return srgb_to_oklab(rgb)[..., 0]


# ---------------------------------------------------------------------------
# WCAG のコントラスト比
# ---------------------------------------------------------------------------

def relative_luminance(rgb: ArrayLike) -> FloatArray:
    """WCAG で定義された相対輝度 (黒が 0.0、白が 1.0) を求める。"""
    linear = srgb_to_linear(rgb)
    weights = np.array([0.2126, 0.7152, 0.0722])
    return np.asarray(linear @ weights, dtype=float)


def contrast_ratio(rgb1: ArrayLike, rgb2: ArrayLike) -> float:
    """2 色のコントラスト比 (1.0 から 21.0) を求める。"""
    lum1 = float(relative_luminance(rgb1))
    lum2 = float(relative_luminance(rgb2))
    lighter, darker = max(lum1, lum2), min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)


# ---------------------------------------------------------------------------
# 画像の作成と保存
# ---------------------------------------------------------------------------

def output_dir() -> Path:
    """画像の保存先ディレクトリを返す。

    コマンドライン引数で指定されていればそのディレクトリを、なければ
    カレントディレクトリの ``output`` を使う。ディレクトリがなければ作る。
    """
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("output")
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_rgb(rgb: ArrayLike, name: str) -> None:
    """sRGB 値の配列 (高さ, 幅, 3) を PNG 画像として保存する。"""
    path = output_dir() / name
    Image.fromarray(to_uint8(rgb)).save(path)
    print(f"保存しました: {path}")


def save_image(image: Image.Image, name: str) -> None:
    """PIL の画像を PNG 画像として保存する。"""
    path = output_dir() / name
    image.save(path)
    print(f"保存しました: {path}")


def swatches(colors: Sequence[ArrayLike], width: int = 64,
             height: int = 64) -> FloatArray:
    """色の並びを、横に並べた色見本の画像 (高さ, 幅, 3) にする。"""
    row = np.array([np.asarray(c, dtype=float) for c in colors])
    tiles = np.repeat(row[np.newaxis, :, :], height, axis=0)
    return np.repeat(tiles, width, axis=1)


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """図中のラベルに使うフォントを返す。

    Pillow に同梱されたフォントを使うため、ラベルは英数字だけで書く。
    """
    return ImageFont.load_default(size=size)


def gray(value: float) -> FloatArray:
    """R = G = B = ``value`` の灰色の sRGB 値を返す。"""
    return np.array([value, value, value])


def to_grayscale(rgb: ArrayLike) -> FloatArray:
    """画像の各画素を、OKLab の明るさ L だけを残した灰色に変換する。

    色相と彩度を取り除くことで、明るさの分布だけを確かめられる。
    """
    lab = srgb_to_oklab(rgb)
    lab[..., 1:] = 0.0
    return oklab_to_srgb(lab)


def labeled_rows(rows: Sequence[tuple[str, ArrayLike]],
                 label_width: int = 180, gap: int = 12,
                 font_size: int = 18) -> Image.Image:
    """左端にラベルを付けた画像を、上から順に縦に並べた 1 枚の画像にする。

    ``rows`` は (ラベル, sRGB 値の画像配列) の組の並び。
    """
    arrays = [to_uint8(image) for _, image in rows]
    width = label_width + max(a.shape[1] for a in arrays) + gap
    height = sum(a.shape[0] for a in arrays) + gap * (len(arrays) + 1)
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    label_font = font(font_size)

    top = gap
    for (label, _), array in zip(rows, arrays):
        canvas.paste(Image.fromarray(array), (label_width, top))
        # 白に近い色が背景に溶け込まないよう、細い灰色の枠で囲む。
        draw.rectangle(
            (label_width - 1, top - 1, label_width + array.shape[1],
             top + array.shape[0]), outline=(160, 160, 160))
        draw.text((gap, top + array.shape[0] // 2), label, fill="black",
                  font=label_font, anchor="lm")
        top += array.shape[0] + gap
    return canvas
