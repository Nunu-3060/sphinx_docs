"""サンプルスクリプトに共通する出力まわりの処理。

各スクリプトは、図や動画を次のフォルダーに保存する。

* コマンドライン引数で出力先 ROOT を与えた場合: ``ROOT/<スクリプト名>/``
* 引数が無い場合: ``examples/python/out/<スクリプト名>/``

本文のビルドでは、conf.py が ROOT に ``source/_generated`` を与えて実行する。
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray
from PIL import Image

FloatArray = NDArray[np.float64]
IntArray = NDArray[np.int64]
UIntArray = NDArray[np.uint32]
ByteArray = NDArray[np.uint8]


def output_dir(script_file: str) -> Path:
    """スクリプトごとの出力フォルダーを作って返す。script_file には __file__ を渡す。"""
    script = Path(script_file)
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else script.parent / "out"
    directory = root / script.stem
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def grid(width: int, height: int, scale: float = 1.0) -> tuple[FloatArray, FloatArray]:
    """画素の中心の座標 (x, y) を 2 次元配列で返す。

    x は 0〜scale、y は 0〜scale * height / width の範囲になる（縦横比を保つ）。
    """
    xs = (np.arange(width, dtype=np.float64) + 0.5) / width * scale
    ys = (np.arange(height, dtype=np.float64) + 0.5) / width * scale
    x, y = np.meshgrid(xs, ys)
    return x, y


def normalize(values: FloatArray) -> FloatArray:
    """最小値が 0、最大値が 1 になるように線形に変換する。"""
    low = float(values.min())
    high = float(values.max())
    if high - low < 1e-12:
        return np.zeros_like(values)
    return (values - low) / (high - low)


def to_bytes(image: FloatArray) -> ByteArray:
    """0〜1 の実数の画像を 0〜255 の 8 bit の画像に変換する。"""
    return (np.clip(image, 0.0, 1.0) * 255.0 + 0.5).astype(np.uint8)


def save_image(image: FloatArray | ByteArray, path: Path) -> None:
    """グレースケール (H, W) または RGB (H, W, 3) の画像を PNG で保存する。

    実数の配列は 0〜1 の範囲とみなす。
    """
    data = image if image.dtype == np.uint8 else to_bytes(image.astype(np.float64))
    Image.fromarray(data).save(path, optimize=True)


def tile_images(images: list[FloatArray], columns: int, gap: int = 4, background: float = 1.0) -> FloatArray:
    """同じ大きさの画像を、間隔を空けて格子状に並べた 1 枚の画像にする。"""
    rgb = [np.repeat(img[:, :, None], 3, axis=2) if img.ndim == 2 else img for img in images]
    height, width = rgb[0].shape[:2]
    rows = (len(rgb) + columns - 1) // columns
    canvas = np.full((rows * height + (rows - 1) * gap, columns * width + (columns - 1) * gap, 3), background)
    for index, img in enumerate(rgb):
        row, column = divmod(index, columns)
        top = row * (height + gap)
        left = column * (width + gap)
        canvas[top:top + height, left:left + width] = img
    return canvas


def setup_matplotlib() -> None:
    """matplotlib で日本語を表示できるようにし、図の体裁をそろえる。"""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    # 日本語を表示できるフォントのうち、インストールされているものだけを指定する
    # （無いフォントを指定すると、描画のたびに警告が出る）。
    installed = {font.name for font in font_manager.fontManager.ttflist}
    candidates = ["Yu Gothic", "Meiryo", "Noto Sans CJK JP", "IPAexGothic", "Hiragino Sans"]
    plt.rcParams["font.family"] = [name for name in candidates if name in installed] + ["DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["savefig.dpi"] = 100


def save_figure(figure: Any, path: Path) -> None:
    """matplotlib の図を PNG で保存して閉じる。"""
    import matplotlib.pyplot as plt

    figure.savefig(path, bbox_inches="tight")
    plt.close(figure)
