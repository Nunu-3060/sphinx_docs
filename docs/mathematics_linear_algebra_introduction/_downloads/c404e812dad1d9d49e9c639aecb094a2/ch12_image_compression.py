"""特異値分解による画像の低ランク近似.

Pillow で図形を描いたグレースケールの画像（128 × 128 画素）を行列とみなし、
大きい方から k 個の特異値だけを残した行列で近似する。

使い方: python ch12_image_compression.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray
from PIL import Image, ImageDraw

import la_plot

Matrix = NDArray[np.float64]
RANKS = [1, 5, 10, 20, 40]


def make_image() -> Matrix:
    """図形を描いた画像を作り、画素値が 0 から 1 の行列として返す."""
    size = 128
    image = Image.new("L", (size, size), color=230)
    draw = ImageDraw.Draw(image)
    draw.rectangle((10, 12, 60, 70), fill=60)
    draw.ellipse((55, 30, 118, 93), fill=140)
    draw.polygon([(20, 118), (64, 78), (108, 118)], fill=20)
    for x in range(0, size, 16):
        draw.line([(x, 0), (x + 40, 40)], fill=180, width=2)
    return np.asarray(image, dtype=float) / 255.0


def low_rank(a: Matrix, k: int) -> Matrix:
    """特異値の大きい方から k 個を使って a を近似した行列を返す."""
    u, s, vt = np.linalg.svd(a, full_matrices=False)
    return (u[:, :k] * s[:k]) @ vt[:k]


def report() -> None:
    """ランクごとの、データ量の比と相対誤差を表示する."""
    a = make_image()
    m, n = a.shape
    print(f"画像の大きさ {m} × {n}、ランク {np.linalg.matrix_rank(a)}")
    for k in RANKS:
        error = np.linalg.norm(a - low_rank(a, k)) / np.linalg.norm(a)
        ratio = k * (m + n + 1) / (m * n)
        print(f"k = {k:2d}: データ量の比 {ratio:6.1%}、相対誤差 {error:.4f}")


def create_figure() -> Figure:
    """元の画像、低ランク近似の画像、特異値のグラフを描く."""
    a = make_image()
    fig, axes = plt.subplots(2, 4, figsize=(12, 6.4))
    images = [("元の画像", a)] + [(f"k = {k}", low_rank(a, k)) for k in RANKS]
    for ax, (title, image) in zip(axes.flat, images):
        ax.imshow(np.clip(image, 0.0, 1.0), cmap="gray", vmin=0.0, vmax=1.0)
        ax.set_title(title)
        ax.axis("off")
    ax_sv = axes.flat[-2]
    s = np.linalg.svd(a, compute_uv=False)
    s = s[:np.linalg.matrix_rank(a)]  # 0 とみなせる（丸め誤差の）特異値は描かない
    ax_sv.semilogy(np.arange(1, s.size + 1), s, ".-", color="C0")
    ax_sv.set_title("特異値（対数目盛り）")
    ax_sv.set_xlabel("番号")
    ax_sv.grid(True, color="0.9")
    axes.flat[-1].axis("off")
    fig.tight_layout()
    return fig


def main() -> None:
    report()
    la_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
