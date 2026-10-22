"""ノイズをそのまま速度にした流れと、カールノイズで作った流れを比べる.

使い方: python ch18_curl_noise.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy.typing import NDArray

import vc_plot

Array = NDArray[np.float64]
N_WAVES = 12  # 重ね合わせる正弦波の数


class SmoothNoise:
    """ランダムな向きと位相の正弦波を重ね合わせた、滑らかなスカラー場."""

    def __init__(self, seed: int) -> None:
        rng = np.random.default_rng(seed)
        angle = rng.uniform(0.0, 2.0 * np.pi, N_WAVES)
        wavenumber = rng.uniform(1.5, 3.5, N_WAVES)
        self.kx = wavenumber * np.cos(angle)
        self.ky = wavenumber * np.sin(angle)
        self.phase = rng.uniform(0.0, 2.0 * np.pi, N_WAVES)
        self.amp = 1.0 / N_WAVES**0.5

    def value(self, x: Array, y: Array) -> Array:
        """場の値 psi(x, y)."""
        result = np.zeros_like(x)
        for kx, ky, ph in zip(self.kx, self.ky, self.phase):
            result += self.amp * np.sin(kx * x + ky * y + ph)
        return result

    def gradient(self, x: Array, y: Array) -> tuple[Array, Array]:
        """場の勾配 (d psi/dx, d psi/dy). 正弦波の微分なので厳密に計算できる."""
        gx = np.zeros_like(x)
        gy = np.zeros_like(x)
        for kx, ky, ph in zip(self.kx, self.ky, self.phase):
            c = self.amp * np.cos(kx * x + ky * y + ph)
            gx += kx * c
            gy += ky * c
        return gx, gy


def naive_velocity(x: Array, y: Array) -> tuple[Array, Array]:
    """2 つの独立なノイズを、そのまま速度の x 成分と y 成分にする."""
    return SmoothNoise(1).value(x, y), SmoothNoise(2).value(x, y)


def curl_noise_velocity(x: Array, y: Array) -> tuple[Array, Array]:
    """ノイズ psi を (0, 0, psi) の z 成分とみなし、その回転 (d psi/dy, -d psi/dx) を速度にする."""
    gx, gy = SmoothNoise(3).gradient(x, y)
    return gy, -gx


def draw(ax: Axes, vx: Array, vy: Array, xx: Array, yy: Array, title: str) -> object:
    """背景に発散の値を色で、その上に流線を描き、色の対応を返す."""
    h = xx[0, 1] - xx[0, 0]
    div = np.gradient(vx, h, axis=1) + np.gradient(vy, h, axis=0)
    image = ax.imshow(div, origin="lower", extent=(xx.min(), xx.max(), yy.min(), yy.max()),
                      cmap="coolwarm", vmin=-3.0, vmax=3.0)
    ax.streamplot(xx, yy, vx, vy, color="k", density=1.1, linewidth=0.7, arrowsize=0.8)
    ax.set_xlim(xx.min(), xx.max())
    ax.set_ylim(yy.min(), yy.max())
    ax.set_aspect("equal")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title(title)
    return image


def create_figure() -> Figure:
    """2 つの流れを左右に並べて描く."""
    xx, yy = vc_plot.mesh((0.0, 4.0), (0.0, 4.0), 120)
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 4.4))
    draw(axes[0], *naive_velocity(xx, yy), xx, yy, "ノイズをそのまま速度にした流れ")
    image = draw(axes[1], *curl_noise_velocity(xx, yy), xx, yy, "カールノイズの流れ")
    fig.colorbar(image, ax=axes, label="発散 $\\nabla \\cdot \\mathbf{v}$", shrink=0.8)  # type: ignore[arg-type]
    return fig


def report() -> None:
    """格子上で差分により発散を求め、その最大値を比べる."""
    xx, yy = vc_plot.mesh((0.0, 4.0), (0.0, 4.0), 401)
    h = xx[0, 1] - xx[0, 0]
    for name, (vx, vy) in (("ノイズをそのまま速度に", naive_velocity(xx, yy)),
                           ("カールノイズ", curl_noise_velocity(xx, yy))):
        div = np.gradient(vx, h, axis=1, edge_order=2) + np.gradient(vy, h, axis=0, edge_order=2)
        print(f"{name}: 発散の絶対値の最大 = {np.max(np.abs(div)):.2e}")


def main() -> None:
    vc_plot.setup_font()
    report()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
