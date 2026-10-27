"""画像の 2 次元 DFT: 振幅スペクトルと、低い周波数・高い周波数だけを残した画像.

テスト画像は Pillow で図形を描き、NumPy で斜めの縞模様を加えて作る。
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray
from PIL import Image, ImageDraw

SIZE = 128
RADIUS = 12  # 低域として残す半径（周波数の格子の単位）


def test_image() -> NDArray[np.float64]:
    """長方形、円、斜めの縞模様を含む、値が 0 から 1 のグレースケール画像を返す."""
    image = Image.new("L", (SIZE, SIZE), 0)
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 20, 56, 100), fill=200)
    draw.ellipse((70, 14, 116, 60), fill=255)
    pixels = np.asarray(image, dtype=np.float64) / 255.0
    yy, xx = np.mgrid[0:SIZE, 0:SIZE]
    stripes = 0.25 * (1 + np.sin(2 * np.pi * (xx + yy) / 8))  # 斜め 45 度、周期 8 画素（対角方向）の縞
    pixels[72:120, 68:120] = stripes[72:120, 68:120]
    return pixels


def create_figure() -> Figure:
    pixels = test_image()
    spectrum = np.fft.fftshift(np.fft.fft2(pixels))
    ky, kx = np.mgrid[-SIZE // 2:SIZE // 2, -SIZE // 2:SIZE // 2]
    low_mask = kx**2 + ky**2 <= RADIUS**2
    low = np.real(np.fft.ifft2(np.fft.ifftshift(spectrum * low_mask)))
    high = np.real(np.fft.ifft2(np.fft.ifftshift(spectrum * ~low_mask)))
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.4))
    axes[0].imshow(pixels, cmap="gray", vmin=0, vmax=1)
    axes[0].set_title("元の画像")
    axes[1].imshow(np.log10(1 + np.abs(spectrum)), cmap="magma",
                   extent=(-SIZE / 2 - 0.5, SIZE / 2 - 0.5, SIZE / 2 - 0.5, -SIZE / 2 - 0.5))
    axes[1].set_title("振幅スペクトル（対数）")
    axes[2].imshow(low, cmap="gray", vmin=0, vmax=1)
    axes[2].set_title(f"低域だけ（半径 {RADIUS}）")
    axes[3].imshow(high, cmap="gray")
    axes[3].set_title("高域だけ")
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    return fig
