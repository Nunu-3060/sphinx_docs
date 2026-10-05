"""全ての章で使う共通の関数と型をまとめたモジュール。

本資料のサンプルコードでは、画像を NumPy 配列で表す。

* 画像は形状 (高さ, 幅, 3) の配列とし、末尾の軸を (R, G, B) とする。
* 色の値は 0.0 から 1.0 の実数で扱い、保存するときだけ 0 から 255 の
  整数に変換する。
* 照明の計算は光の強さに比例する線形な値で行い、保存する直前に
  sRGB の値に変換する。

主な内容は次のとおり。

* ベクトルの正規化
* sRGB のガンマ補正(線形な値と sRGB の値の相互変換)
* 画像の保存、拡大、横に並べた図の作成
* 図の保存先ディレクトリの取得
"""

import sys
from pathlib import Path
from typing import Sequence

import numpy as np
from numpy.typing import NDArray
from PIL import Image

FloatArray = NDArray[np.float64]
IntArray = NDArray[np.int64]
BoolArray = NDArray[np.bool_]

# 図の背景や、図を並べるときの余白の色(白)。
WHITE: FloatArray = np.array([1.0, 1.0, 1.0])


# ---------------------------------------------------------------------------
# ベクトル
# ---------------------------------------------------------------------------

def normalize(v: FloatArray) -> FloatArray:
    """末尾の軸をベクトルとみなし、長さを 1 にしたベクトルを返す。

    長さが 0 のベクトルは、0 除算を避けるためにそのまま返す。
    """
    length = np.linalg.norm(v, axis=-1, keepdims=True)
    return np.asarray(v / np.where(length > 0.0, length, 1.0),
                      dtype=np.float64)


# ---------------------------------------------------------------------------
# ガンマ補正
# ---------------------------------------------------------------------------

def srgb_to_linear(c: FloatArray) -> FloatArray:
    """sRGB の値(0.0 から 1.0)を、光の強さに比例する線形な値に変換する。"""
    c = np.asarray(c, dtype=np.float64)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(c: FloatArray) -> FloatArray:
    """線形な値を sRGB の値に変換する。範囲外の値は 0.0 から 1.0 に収める。"""
    c = np.clip(np.asarray(c, dtype=np.float64), 0.0, 1.0)
    return np.where(c <= 0.0031308, c * 12.92,
                    1.055 * c ** (1.0 / 2.4) - 0.055)


# ---------------------------------------------------------------------------
# 画像
# ---------------------------------------------------------------------------

def to_pil(image: FloatArray) -> Image.Image:
    """0.0 から 1.0 の値を持つ (高さ, 幅, 3) の配列を Pillow の画像にする。"""
    data = np.clip(image, 0.0, 1.0) * 255.0 + 0.5
    return Image.fromarray(data.astype(np.uint8))


def from_pil(image: Image.Image) -> FloatArray:
    """Pillow の画像を 0.0 から 1.0 の値を持つ (高さ, 幅, 3) の配列にする。"""
    return np.asarray(image.convert("RGB"), dtype=np.float64) / 255.0


def enlarge(image: FloatArray, scale: int) -> FloatArray:
    """画素を scale × scale の正方形に引き伸ばして画像を拡大する。

    画素の様子が見えるように、補間はせずに同じ値を繰り返す。
    """
    return np.repeat(np.repeat(image, scale, axis=0), scale, axis=1)


def hstack(images: Sequence[FloatArray], gap: int = 16) -> FloatArray:
    """高さの同じ画像を、白い余白を挟んで横に並べた画像を返す。"""
    height = images[0].shape[0]
    spacer = np.ones((height, gap, 3))
    parts: list[FloatArray] = []
    for i, image in enumerate(images):
        if i > 0:
            parts.append(spacer)
        parts.append(image)
    return np.concatenate(parts, axis=1)


def save_image(image: FloatArray, path: Path) -> None:
    """画像を PNG 形式で保存する。"""
    to_pil(image).save(path)
    print(f"saved: {path}")


def output_dir() -> Path:
    """図の保存先ディレクトリを返す。

    コマンドライン引数で指定されていればそのディレクトリを、なければ
    カレントディレクトリの下の ``figures`` を使う。
    """
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("figures")
    path.mkdir(parents=True, exist_ok=True)
    return path
