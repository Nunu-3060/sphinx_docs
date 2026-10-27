"""バタワース IIR ローパスフィルタの設計（双一次変換）.

アナログのバタワースフィルタを双一次変換でデジタルフィルタに変換する。
1 次のフィルタを手計算の式で作って scipy.signal.butter の結果と比べ、
次数による振幅特性の違いと、プリワーピングを考慮した理論値との一致を確かめる。

使い方: python iir_filter_design.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray
from scipy import signal

import dsp_plot

FS = 1000.0  # 標本化周波数 [Hz]
CUTOFF = 100.0  # カットオフ周波数 [Hz]
ORDERS = (2, 4, 8)  # 比べる次数


def prewarp(f: float) -> float:
    """デジタルの周波数 f [Hz] に対応するアナログの角周波数 [rad/s] を返す（プリワーピング）."""
    return float(2 * FS * np.tan(np.pi * f / FS))


def first_order_lowpass() -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """1 次のアナログ LPF H(s) = wc / (s + wc) を双一次変換し、(b, a) を返す.

    s = 2 fs (1 - z^-1) / (1 + z^-1) を代入して整理すると
    H(z) = wc (1 + z^-1) / ((2 fs + wc) + (wc - 2 fs) z^-1) になる。
    """
    wc = prewarp(CUTOFF)
    b = np.array([wc, wc]) / (2 * FS + wc)
    a = np.array([1.0, (wc - 2 * FS) / (2 * FS + wc)])
    return b, a


def butterworth_gain(f: float, order: int) -> float:
    """デジタルのバタワースフィルタの、周波数 f [Hz] における利得の理論値."""
    ratio = prewarp(f) / prewarp(CUTOFF)
    return float(1.0 / np.sqrt(1.0 + ratio ** (2 * order)))


def report() -> None:
    """手計算の 1 次フィルタと butter の比較、および各次数の利得を表示する."""
    b, a = first_order_lowpass()
    b_ref, a_ref = signal.butter(1, CUTOFF, fs=FS)
    with np.printoptions(precision=6):
        print("手計算の b =", b, " a =", a)
        print("butter の b =", b_ref, " a =", a_ref)
    print("一致する:", np.allclose(b, b_ref) and np.allclose(a, a_ref))
    print()
    print("次数   100 Hz の利得   200 Hz の利得   200 Hz の理論値")
    for order in ORDERS:
        sos = signal.butter(order, CUTOFF, fs=FS, output="sos")
        _, response = signal.sosfreqz(sos, worN=[CUTOFF, 200.0], fs=FS)
        db = dsp_plot.to_db(response)
        theory = 20 * np.log10(butterworth_gain(200.0, order))
        print(f"{order:4d}   {db[0]:10.2f} dB   {db[1]:10.2f} dB   {theory:10.2f} dB")


def create_figure() -> Figure:
    """次数 2、4、8 のバタワースフィルタの振幅特性と位相特性を描く."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for i, order in enumerate(ORDERS):
        sos = signal.butter(order, CUTOFF, fs=FS, output="sos")
        freqs, response = signal.sosfreqz(sos, worN=4096, fs=FS)
        axes[0].plot(freqs, dsp_plot.to_db(response), color=f"C{i}", label=f"{order} 次")
        axes[1].plot(freqs, np.degrees(np.unwrap(np.angle(response))), color=f"C{i}", label=f"{order} 次")
    ax = axes[0]
    ax.axhline(-3.01, color="0.4", linestyle=":", linewidth=1.0)
    ax.axvline(CUTOFF, color="0.4", linestyle=":", linewidth=1.0)
    ax.set_ylim(-100, 5)
    ax.set_ylabel("利得 [dB]")
    ax.set_title("振幅特性")
    ax = axes[1]
    ax.axvline(CUTOFF, color="0.4", linestyle=":", linewidth=1.0)
    ax.set_ylabel("位相 [度]")
    ax.set_title("位相特性")
    for ax in axes:
        ax.set_xlim(0, FS / 2)
        ax.set_xlabel("周波数 [Hz]")
        ax.legend()
        dsp_plot.style_axes(ax)
    fig.tight_layout()
    return fig


def main() -> None:
    report()
    dsp_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
