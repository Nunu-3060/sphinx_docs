"""テクスチャを作るための小さな道具（第 3〜5 章で使う）。

* smoothstep・mix など GLSL と同名の関数
* ハイトマップから法線を求め、法線マップの色に符号化する関数
* 法線と光の向きから明るさを計算する簡単な陰影付け
* 複数の画像に題名を付けて横に並べた図を保存する関数
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import numpy as np

from common import FloatArray, save_figure


def smoothstep(edge0: float | FloatArray, edge1: float | FloatArray, x: FloatArray) -> FloatArray:
    """GLSL の smoothstep と同じ。edge0〜edge1 の間で 0 から 1 へ滑らかに変わる。edge0 > edge1 でもよい。"""
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def mix(a: FloatArray | Sequence[float], b: FloatArray | Sequence[float], t: FloatArray) -> FloatArray:
    """GLSL の mix と同じ線形補間。a, b が色 (3 成分) で t が (H, W) なら (H, W, 3) を返す。"""
    a_array = np.asarray(a, dtype=np.float64)
    b_array = np.asarray(b, dtype=np.float64)
    t_array = np.asarray(t, dtype=np.float64)
    # a または b が色（最後の軸が 3 成分）で、t が色の軸を持たないなら、t に色の軸を足す。
    is_color = any(c.shape[-1:] == (3,) and c.ndim != t_array.ndim for c in (a_array, b_array))
    weight = t_array[..., None] if is_color else t_array
    result: FloatArray = a_array + (b_array - a_array) * weight
    return result


def height_to_normal(height: FloatArray, strength: float = 1.0, wrap: bool = False) -> FloatArray:
    """ハイトマップ (H, W) から単位法線 (H, W, 3) を求める。

    隣の画素との差（中心差分）で x, y 方向の傾きを求め、面の法線 (-∂h/∂x, -∂h/∂y, 1) を正規化する。
    strength は凹凸の強さ（高さの倍率）。画像の行は下向きに増えるが、法線の y は上向きを正とする
    （OpenGL 方式）。wrap を True にすると、端では反対側の画素を隣とみなす（シームレスな画像用）。
    """
    # 周囲に 1 画素ずつ足して、端の画素でも左右・上下の隣を参照できるようにする。
    padded = np.pad(height, 1, mode="wrap" if wrap else "edge")
    dx = (padded[1:-1, 2:] - padded[1:-1, :-2]) * 0.5  # 右の画素 - 左の画素
    d_row = (padded[2:, 1:-1] - padded[:-2, 1:-1]) * 0.5  # 下の画素 - 上の画素
    dy = -d_row  # 画像の下向きの差分を、上向きの傾きに直す
    normal = np.stack([-strength * dx, -strength * dy, np.ones_like(height)], axis=-1)
    result: FloatArray = normal / np.linalg.norm(normal, axis=-1, keepdims=True)
    return result


def encode_normal(normal: FloatArray) -> FloatArray:
    """-1〜1 の法線の各成分を 0〜1 に写し、RGB の画像にする（法線マップ）。"""
    return normal * 0.5 + 0.5


def shade(
    normal: FloatArray,
    albedo: FloatArray,
    light: Sequence[float] = (-0.5, 0.6, 0.65),
    ambient: float = 0.25,
) -> FloatArray:
    """拡散反射（ランバート）による簡単な陰影。albedo は (H, W, 3) の色、light は光の来る向き。"""
    direction = np.asarray(light, dtype=np.float64)
    direction = direction / np.linalg.norm(direction)
    diffuse = np.clip(normal @ direction, 0.0, 1.0)
    result: FloatArray = albedo * (ambient + (1.0 - ambient) * diffuse)[..., None]
    return np.clip(result, 0.0, 1.0)


def show_panels(
    images: Sequence[FloatArray],
    titles: Sequence[str],
    path: Path,
    columns: int | None = None,
    size: float = 3.0,
    cmap: str = "gray",
    interpolation: str = "bilinear",
) -> None:
    """画像を題名付きで格子状に並べた図を保存する。グレースケールは 0〜1 の範囲で表示する。

    セル・オートマトンやドット絵のように画素の境目を見せたい画像には interpolation="nearest" を渡す。
    """
    import matplotlib.pyplot as plt

    columns = len(images) if columns is None else columns
    rows = (len(images) + columns - 1) // columns
    aspect = images[0].shape[0] / images[0].shape[1]  # 縦 / 横。図の高さを画像の縦横比に合わせる
    figure, axes = plt.subplots(rows, columns, figsize=(size * columns, (size * aspect + 0.35) * rows), squeeze=False)
    for ax in axes.flat:
        ax.set_axis_off()
    for ax, image, title in zip(axes.flat, images, titles):
        ax.imshow(np.clip(image, 0.0, 1.0), cmap=cmap, vmin=0.0, vmax=1.0, interpolation=interpolation)
        ax.set_title(title, fontsize=10)
    figure.tight_layout()
    save_figure(figure, path)
