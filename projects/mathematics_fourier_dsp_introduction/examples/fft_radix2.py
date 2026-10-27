"""基数 2 の FFT（Cooley-Tukey 法、時間間引き）を再帰で実装する.

長さ N（2 のべき乗）の DFT を、偶数番目と奇数番目の標本の DFT（長さ N/2）
に分け、次のバタフライ演算で組み合わせる。

    X[k]       = E[k] + W^k O[k]
    X[k + N/2] = E[k] - W^k O[k]      (W = exp(-j 2 pi / N), k = 0, ..., N/2 - 1)

このサンプルでは、np.fft.fft との一致を確かめ、複素乗算の回数と
計算時間を DFT（行列の積）と比べる。

使い方: python fft_radix2.py
"""

import math
import time
from collections.abc import Callable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import dsp_plot

Transform = Callable[[NDArray[np.complex128]], NDArray[np.complex128]]


def fft_radix2(x: NDArray[np.complex128]) -> NDArray[np.complex128]:
    """基数 2 の FFT を再帰で計算する. x の長さは 2 のべき乗でなければならない."""
    n_points = len(x)
    if n_points == 1:
        return x.copy()
    if n_points % 2 != 0:
        raise ValueError("長さは 2 のべき乗にする")
    even = fft_radix2(x[0::2])  # 偶数番目の標本の DFT
    odd = fft_radix2(x[1::2])  # 奇数番目の標本の DFT
    twiddle = np.exp(-2j * np.pi * np.arange(n_points // 2) / n_points)  # 回転因子 W^k
    t = twiddle * odd
    return np.concatenate([even + t, even - t])


def dft_by_matrix(x: NDArray[np.complex128]) -> NDArray[np.complex128]:
    """DFT を行列とベクトルの積で計算する（比較用）."""
    n_points = len(x)
    k = np.arange(n_points).reshape(-1, 1)
    w = np.exp(-2j * np.pi * k * np.arange(n_points) / n_points)
    result: NDArray[np.complex128] = w @ x
    return result


def elapsed(transform: Transform, x: NDArray[np.complex128], repeat: int = 3) -> float:
    """transform(x) の計算時間 [s] を repeat 回測り、最小値を返す."""
    best = math.inf
    for _ in range(repeat):
        start = time.perf_counter()
        transform(x)
        best = min(best, time.perf_counter() - start)
    return best


def random_signal(n_points: int) -> NDArray[np.complex128]:
    """長さ n_points の複素数の乱数の信号を返す."""
    rng = np.random.default_rng(0)
    result: NDArray[np.complex128] = rng.standard_normal(n_points) + 1j * rng.standard_normal(n_points)
    return result


def report() -> None:
    """np.fft.fft との一致と、複素乗算の回数を表示する."""
    for n_points in (8, 64, 1024):
        x = random_signal(n_points)
        print(f"N = {n_points:4d}: np.fft.fft と一致する: {np.allclose(fft_radix2(x), np.fft.fft(x))}")
    print()
    print("     N    DFT の乗算回数 N^2   FFT の乗算回数 (N/2) log2 N      比")
    for exponent in (3, 6, 10, 16, 20):
        n_points = 2**exponent
        dft_count = n_points**2
        fft_count = n_points // 2 * exponent
        print(f"{n_points:7d}   {dft_count:16,d}   {fft_count:22,d}   {dft_count / fft_count:9.1f}")


def create_figure() -> Figure:
    """DFT（行列の積）、自作の FFT、np.fft.fft の計算時間を両対数グラフで描く.

    計算時間は実行する計算機によって変わる。
    """
    sizes = [2**e for e in range(3, 12)]
    times: dict[str, list[float]] = {"DFT（行列の積）": [], "自作の FFT（再帰）": [], "np.fft.fft": []}
    for n_points in sizes:
        x = random_signal(n_points)
        times["DFT（行列の積）"].append(elapsed(dft_by_matrix, x))
        times["自作の FFT（再帰）"].append(elapsed(fft_radix2, x))
        times["np.fft.fft"].append(elapsed(np.fft.fft, x))
    fig, ax = plt.subplots(figsize=(7, 4))
    for i, (label, values) in enumerate(times.items()):
        ax.loglog(sizes, values, "o-", color=f"C{i}", label=label)
    ax.set_xscale("log", base=2)
    ax.set_xlabel("データの長さ N")
    ax.set_ylabel("計算時間 [s]")
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
