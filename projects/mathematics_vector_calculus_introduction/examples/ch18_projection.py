"""ベクトル場から勾配の成分を取り除き、発散のない場を取り出す（圧力投影）.

周期境界の正方形 [0, 2 pi) x [0, 2 pi) で、ポアソン方程式を高速フーリエ変換（FFT）で解く。
使い方: python ch18_projection.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import vc_plot

Array = NDArray[np.float64]
N = 64  # 1 辺の格子点の数


def grid() -> tuple[Array, Array]:
    """周期境界の格子点の座標を返す（軸 0 が y、軸 1 が x）."""
    x = np.arange(N) * (2.0 * np.pi / N)
    xx, yy = np.meshgrid(x, x)
    return xx, yy


def test_field(xx: Array, yy: Array) -> tuple[Array, Array, Array, Array]:
    """発散のない成分 u と、勾配の成分 grad phi を足した場 w を作り、(w_x, w_y, u_x, u_y) を返す.

    u は psi = sin x sin y から u = (d psi/dy, -d psi/dx) として作る。
    phi = 0.8 cos x cos 2y とする。
    """
    ux = np.sin(xx) * np.cos(yy)
    uy = -np.cos(xx) * np.sin(yy)
    gx = -0.8 * np.sin(xx) * np.cos(2.0 * yy)
    gy = -1.6 * np.cos(xx) * np.sin(2.0 * yy)
    return ux + gx, uy + gy, ux, uy


def wavenumbers() -> tuple[Array, Array]:
    """FFT の各成分に対応する波数 (k_x, k_y) を返す."""
    k = np.fft.fftfreq(N, d=1.0 / N)
    kx, ky = np.meshgrid(k, k)
    return kx, ky


def spectral_divergence(vx: Array, vy: Array) -> Array:
    """FFT を使って発散を求める."""
    kx, ky = wavenumbers()
    div_hat = 1j * kx * np.fft.fft2(vx) + 1j * ky * np.fft.fft2(vy)
    result: Array = np.real(np.fft.ifft2(div_hat))
    return result


def project(wx: Array, wy: Array) -> tuple[Array, Array, Array, Array]:
    """ポアソン方程式 ∇²p = div w を解き、(u_x, u_y, (grad p)_x, (grad p)_y) を返す. u = w - grad p."""
    kx, ky = wavenumbers()
    k2 = kx**2 + ky**2
    k2[0, 0] = 1.0  # 定数成分（波数 0）は p に影響しないので、0 による割り算を避ける
    div_hat = 1j * kx * np.fft.fft2(wx) + 1j * ky * np.fft.fft2(wy)
    p_hat = -div_hat / k2  # ラプラシアンは波数空間では -|k|^2 を掛けることになる
    p_hat[0, 0] = 0.0
    px = np.real(np.fft.ifft2(1j * kx * p_hat))
    py = np.real(np.fft.ifft2(1j * ky * p_hat))
    return wx - px, wy - py, px, py


def create_figure() -> Figure:
    """元の場 w、取り除いた勾配の成分 grad p、残った発散のない場 u を並べて描く."""
    xx, yy = grid()
    wx, wy, _, _ = test_field(xx, yy)
    ux, uy, px, py = project(wx, wy)
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.8))
    step = 4
    s = (slice(None, None, step), slice(None, None, step))
    panels = [
        (wx, wy, "元の場 $\\mathbf{w}$", "C0"),
        (px, py, "勾配の成分 $\\nabla p$", "C3"),
        (ux, uy, "発散のない場 $\\mathbf{u} = \\mathbf{w} - \\nabla p$", "C2"),
    ]
    for ax, (vx, vy, title, color) in zip(axes, panels):
        ax.quiver(xx[s], yy[s], vx[s], vy[s], color=color, scale=22.0, width=0.007)
        ax.set_aspect("equal")
        ax.set_xlim(0.0, 2.0 * np.pi)
        ax.set_ylim(0.0, 2.0 * np.pi)
        ax.set_xticks([0.0, np.pi, 2.0 * np.pi], ["0", "$\\pi$", "$2\\pi$"])
        ax.set_yticks([0.0, np.pi, 2.0 * np.pi], ["0", "$\\pi$", "$2\\pi$"])
        ax.set_title(title, fontsize=11)
    fig.tight_layout()
    return fig


def report() -> None:
    """投影の前後の発散と、取り出した場が正しい u と一致するかを表示する."""
    xx, yy = grid()
    wx, wy, ux_true, uy_true = test_field(xx, yy)
    ux, uy, _, _ = project(wx, wy)
    print(f"投影前の発散の最大: {np.max(np.abs(spectral_divergence(wx, wy))):.3e}")
    print(f"投影後の発散の最大: {np.max(np.abs(spectral_divergence(ux, uy))):.3e}")
    error = max(np.max(np.abs(ux - ux_true)), np.max(np.abs(uy - uy_true)))
    print(f"正しい u との差の最大: {error:.3e}")


def main() -> None:
    vc_plot.setup_font()
    report()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
