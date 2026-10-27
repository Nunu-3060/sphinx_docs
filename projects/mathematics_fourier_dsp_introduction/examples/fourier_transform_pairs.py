"""代表的なフーリエ変換の対を数値積分で確かめる.

フーリエ変換 X(f) = integral of x(t) exp(-j 2 pi f t) dt を、細かい刻みの
長方形の和で近似し、理論式と比べる。扱う信号は次の 3 つである。

* 矩形パルス（幅 1、高さ 1）   ->  sinc(f) = sin(pi f) / (pi f)
* ガウス関数 exp(-pi t^2)     ->  exp(-pi f^2)
* 片側指数関数 exp(-a t) u(t)  ->  1 / (a + j 2 pi f)

使い方: python fourier_transform_pairs.py
"""

from collections.abc import Callable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import dsp_plot

Signal = Callable[[NDArray[np.float64]], NDArray[np.float64]]
Spectrum = Callable[[NDArray[np.float64]], NDArray[np.complex128]]

DECAY = 2.0  # 片側指数関数の減衰の速さ a [1/s]


def rect(t: NDArray[np.float64]) -> NDArray[np.float64]:
    """幅 1、高さ 1 の矩形パルス（|t| < 1/2 で 1）."""
    result: NDArray[np.float64] = np.where(np.abs(t) < 0.5, 1.0, 0.0)
    return result


def gauss(t: NDArray[np.float64]) -> NDArray[np.float64]:
    """ガウス関数 exp(-pi t^2)."""
    result: NDArray[np.float64] = np.exp(-np.pi * t**2)
    return result


def one_sided_exp(t: NDArray[np.float64]) -> NDArray[np.float64]:
    """片側指数関数 exp(-a t) u(t)（t < 0 では 0）."""
    result: NDArray[np.float64] = np.where(t >= 0.0, np.exp(-DECAY * np.maximum(t, 0.0)), 0.0)
    return result


def rect_spectrum(f: NDArray[np.float64]) -> NDArray[np.complex128]:
    """矩形パルスのフーリエ変換の理論値 sinc(f)."""
    return np.sinc(f).astype(np.complex128)  # np.sinc(f) は sin(pi f) / (pi f)


def gauss_spectrum(f: NDArray[np.float64]) -> NDArray[np.complex128]:
    """ガウス関数のフーリエ変換の理論値 exp(-pi f^2)."""
    return np.exp(-np.pi * f**2).astype(np.complex128)


def one_sided_exp_spectrum(f: NDArray[np.float64]) -> NDArray[np.complex128]:
    """片側指数関数のフーリエ変換の理論値 1 / (a + j 2 pi f)."""
    result: NDArray[np.complex128] = np.asarray(1.0 / (DECAY + 2j * np.pi * f), dtype=np.complex128)
    return result


PAIRS: list[tuple[str, Signal, Spectrum]] = [
    ("矩形パルス", rect, rect_spectrum),
    ("ガウス関数", gauss, gauss_spectrum),
    ("片側指数関数", one_sided_exp, one_sided_exp_spectrum),
]


def fourier_transform(x: Signal, f: NDArray[np.float64], t_max: float = 20.0,
                      dt: float = 1e-3) -> NDArray[np.complex128]:
    """x(t) のフーリエ変換を、-t_max から t_max までの長方形の和で近似する."""
    t = np.arange(-t_max, t_max, dt) + dt / 2  # 各区間の中点
    xt = x(t)
    result: NDArray[np.complex128] = np.array([np.sum(xt * np.exp(-2j * np.pi * fk * t)) * dt for fk in f])
    return result


def report() -> None:
    """数値積分と理論式の差の最大値を表示する."""
    f = np.linspace(-5.0, 5.0, 101)
    print("|数値積分 - 理論値| の最大値（-5 Hz <= f <= 5 Hz）")
    for name, x, spectrum in PAIRS:
        error = np.max(np.abs(fourier_transform(x, f) - spectrum(f)))
        print(f"  {error:.2e}  {name}")


def create_figure() -> Figure:
    """3 つの信号の波形（左）と振幅スペクトル（右）を描く."""
    t = np.linspace(-2.0, 3.0, 2001)
    f = np.linspace(-5.0, 5.0, 2001)
    fig, axes = plt.subplots(3, 2, figsize=(10, 7.5))
    for row, (name, x, spectrum) in enumerate(PAIRS):
        ax = axes[row, 0]
        ax.plot(t, x(t), color="C0")
        ax.set_ylabel(name)
        ax.set_ylim(-0.1, 1.2)
        dsp_plot.style_axes(ax)
        ax = axes[row, 1]
        values = spectrum(f)
        if np.allclose(values.imag, 0.0):
            ax.plot(f, values.real, color="C1", label="X(f)（実数）")
        else:
            ax.plot(f, np.abs(values), color="C1", label="|X(f)|")
        ax.axhline(0.0, color="0.5", linewidth=0.8)
        ax.legend(loc="upper right", fontsize=9)
        dsp_plot.style_axes(ax)
    axes[0, 0].set_title("時間領域 x(t)")
    axes[0, 1].set_title("周波数領域")
    axes[2, 0].set_xlabel("時間 t [s]")
    axes[2, 1].set_xlabel("周波数 f [Hz]")
    fig.tight_layout()
    return fig


def main() -> None:
    report()
    dsp_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
