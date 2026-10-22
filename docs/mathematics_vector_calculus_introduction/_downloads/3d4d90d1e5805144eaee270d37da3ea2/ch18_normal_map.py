"""高さの分布（ハイトマップ）の勾配から法線を求め、ノーマルマップと陰影を描く.

使い方: python ch18_normal_map.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import vc_plot

Array = NDArray[np.float64]
N = 128  # 画像の 1 辺の画素数
LIGHT = np.array([-1.0, 1.0, 1.5]) / np.linalg.norm([-1.0, 1.0, 1.5])  # 光が来る向き（単位ベクトル）


def height_map() -> tuple[Array, float]:
    """[-1, 1] x [-1, 1] の範囲の高さ H(x, y) と、画素の間隔を返す. 2 つの山と 1 本の溝を置く."""
    x = np.linspace(-1.0, 1.0, N)
    xx, yy = np.meshgrid(x, x)
    height = (0.25 * np.exp(-((xx + 0.4)**2 + (yy - 0.3)**2) / 0.06)
              + 0.15 * np.exp(-((xx - 0.45)**2 + (yy + 0.35)**2) / 0.03)
              - 0.05 * np.exp(-(xx - yy * 0.3 - 0.2)**2 / 0.004))
    return height, float(x[1] - x[0])


def normals(height: Array, spacing: float) -> Array:
    """曲面 z = H(x, y) の単位法線ベクトルを、(N, N, 3) の配列で返す.

    曲面は g(x, y, z) = z - H(x, y) = 0 の等値面なので、法線は grad g = (-H_x, -H_y, 1) の向きである。
    """
    dH_dy, dH_dx = np.gradient(height, spacing)
    n = np.stack([-dH_dx, -dH_dy, np.ones_like(height)], axis=-1)
    result: Array = n / np.linalg.norm(n, axis=-1, keepdims=True)
    return result


def create_figure() -> Figure:
    """ハイトマップ、ノーマルマップ、法線から計算した陰影を並べて描く."""
    height, spacing = height_map()
    n = normals(height, spacing)
    normal_map = (n + 1.0) / 2.0  # 各成分を [-1, 1] から [0, 1] に移して RGB として表示する
    shade = np.clip(n @ LIGHT, 0.0, 1.0)  # ランバート反射：法線と光の向きの内積

    fig, axes = plt.subplots(1, 3, figsize=(10.0, 3.6))
    extent = (-1.0, 1.0, -1.0, 1.0)
    axes[0].imshow(height, origin="lower", extent=extent, cmap="gray")
    axes[0].set_title("ハイトマップ（明るいほど高い）")
    axes[1].imshow(normal_map, origin="lower", extent=extent)
    axes[1].set_title("ノーマルマップ（RGB = 法線の xyz）")
    axes[2].imshow(shade, origin="lower", extent=extent, cmap="gray", vmin=0.0, vmax=1.0)
    axes[2].set_title("法線による陰影")
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    return fig


def main() -> None:
    vc_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
