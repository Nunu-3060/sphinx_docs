"""カオスを生む「引き伸ばし」の仕組みを、テント写像とパイこね変換で見る.

* テント写像: 狭い区間に集めた点が、反復のたびに 2 倍に広がり、やがて区間全体に散らばる
* パイこね変換: 正方形を横に 2 倍に引き伸ばし、縦に半分に縮め、切って重ねる

使い方: python ch04_stretch_fold.py [--save DIR]
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import plot_util


def tent(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """テント写像 T(x) = 1 - |1 - 2x|（x < 1/2 なら 2x、そうでなければ 2 - 2x）."""
    return 1.0 - np.abs(1.0 - 2.0 * x)


def baker_image(image: NDArray[np.float64]) -> NDArray[np.float64]:
    """画像にパイこね変換 B(x, y) = (2x mod 1, (y + floor(2x)) / 2) を 1 回施す.

    出力の各画素について、逆写像で元の画像の位置を求めて色を取る（最近傍補間）。
    画像の行の番号は上から数えるので、y = 0 を画像の下端に対応させる。
    """
    h, w = image.shape[:2]
    xs = (np.arange(w) + 0.5) / w
    ys = 1.0 - (np.arange(h) + 0.5) / h
    x, y = np.meshgrid(xs, ys)
    lower = y < 0.5
    # 下半分は左半分から、上半分は右半分から来る
    src_x = np.where(lower, x / 2.0, (x + 1.0) / 2.0)
    src_y = np.where(lower, 2.0 * y, 2.0 * y - 1.0)
    col = np.clip((src_x * w).astype(int), 0, w - 1)
    row = np.clip(((1.0 - src_y) * h).astype(int), 0, h - 1)
    result: NDArray[np.float64] = image[row, col]
    return result


def initial_image(size: int = 256) -> NDArray[np.float64]:
    """左右で色の違う正方形に、円を 1 つ描いた RGB 画像を作る."""
    t = (np.arange(size) + 0.5) / size
    x, y = np.meshgrid(t, 1.0 - t)
    image = np.ones((size, size, 3))
    image[x < 0.5] = (0.65, 0.80, 0.95)
    image[x >= 0.5] = (0.98, 0.85, 0.60)
    circle = (x - 0.35) ** 2 + (y - 0.6) ** 2 < 0.2**2
    image[circle] = (0.80, 0.15, 0.15)
    return image


def create_figures() -> dict[str, Figure]:
    """テント写像で点が広がる様子（tent）と、パイこね変換の反復（baker）の図を作る."""
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.2), gridspec_kw={"width_ratios": [1, 2]})
    grid = np.linspace(0.0, 1.0, 201)
    ax1.plot(grid, tent(grid))
    ax1.plot([0.0, 1.0], [0.0, 1.0], color="0.5", linewidth=1.0)
    ax1.set_aspect("equal")
    ax1.set_xlabel("$x_n$")
    ax1.set_ylabel("$x_{n+1}$")
    ax1.set_title("テント写像")
    rng = np.random.default_rng(1)
    x = 0.3 + 0.001 * rng.random(300)
    for n in range(13):
        ax2.plot(np.full(x.shape, n), x, "_", color="C0", markersize=8, alpha=0.5)
        x = tent(x)
    ax2.set_xlabel("反復回数 $n$")
    ax2.set_ylabel("$x_n$")
    ax2.set_title("幅 0.001 の区間に集めた 300 個の点の行方")
    ax2.set_ylim(0.0, 1.0)
    fig1.tight_layout()

    image = initial_image()
    steps = (0, 1, 2, 3, 6)
    fig2, axes = plt.subplots(1, len(steps), figsize=(13.0, 2.9))
    n = 0
    for ax, target in zip(axes, steps):
        while n < target:
            image = baker_image(image)
            n += 1
        ax.imshow(image, extent=(0.0, 1.0, 0.0, 1.0))
        ax.set_title(f"{target} 回")
        ax.set_xticks([])
        ax.set_yticks([])
    fig2.tight_layout()
    return {"tent": fig1, "baker": fig2}


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures)


if __name__ == "__main__":
    main()
