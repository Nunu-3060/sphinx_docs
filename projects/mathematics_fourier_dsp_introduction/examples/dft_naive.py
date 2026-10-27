"""離散フーリエ変換（DFT）を定義どおりに計算し、numpy.fft.fft と比べる.

長さ N の信号 x[n] の DFT は次の式で定義される。

    X[k] = sum_{n=0}^{N-1} x[n] exp(-j 2 pi k n / N)    (k = 0, 1, ..., N - 1)

このサンプルでは、二重ループによる実装と行列による実装を作り、
np.fft.fft との一致、逆変換、パーセバルの定理、実信号の対称性を確かめる。

使い方: python dft_naive.py
"""

import numpy as np
from numpy.typing import NDArray


def dft_loop(x: NDArray[np.complex128]) -> NDArray[np.complex128]:
    """DFT を二重ループで計算する（計算量は N^2 に比例する）."""
    n_points = len(x)
    result = np.zeros(n_points, dtype=np.complex128)
    for k in range(n_points):
        for n in range(n_points):
            result[k] += x[n] * np.exp(-2j * np.pi * k * n / n_points)
    return result


def dft_matrix(n_points: int) -> NDArray[np.complex128]:
    """DFT 行列 W（W[k, n] = exp(-j 2 pi k n / N)）を返す."""
    k = np.arange(n_points).reshape(-1, 1)
    n = np.arange(n_points).reshape(1, -1)
    result: NDArray[np.complex128] = np.exp(-2j * np.pi * k * n / n_points)
    return result


def idft(spectrum: NDArray[np.complex128]) -> NDArray[np.complex128]:
    """逆 DFT を行列で計算する（x = W^H X / N）."""
    w = dft_matrix(len(spectrum))
    result: NDArray[np.complex128] = w.conj().T @ spectrum / len(spectrum)
    return result


def report() -> None:
    """DFT の計算結果と、各種の性質の確認結果を表示する."""
    n_points = 8
    n = np.arange(n_points)
    # 直流 0.5、k = 1 の余弦波（振幅 1）、k = 2 の正弦波（振幅 0.5）を足した信号
    x = (0.5 + np.cos(2 * np.pi * n / n_points) + 0.5 * np.sin(2 * np.pi * 2 * n / n_points)).astype(np.complex128)
    spectrum = dft_loop(x)
    with np.printoptions(precision=3, suppress=True):
        print("x    =", x.real)
        print("X[k] =", spectrum)
        print("|X[k]| =", np.abs(spectrum))
    print("ループと行列の結果が一致する:", np.allclose(spectrum, dft_matrix(n_points) @ x))
    print("np.fft.fft と一致する:", np.allclose(spectrum, np.fft.fft(x)))
    print("逆 DFT で元に戻る:", np.allclose(idft(spectrum), x))
    energy_time = np.sum(np.abs(x) ** 2)
    energy_freq = np.sum(np.abs(spectrum) ** 2) / n_points
    print(f"パーセバルの定理: sum |x|^2 = {energy_time:.4f}, sum |X|^2 / N = {energy_freq:.4f}")
    symmetric = np.allclose(spectrum[1:], np.conj(spectrum[1:][::-1]))
    print("実信号なので X[N - k] = conj(X[k]) が成り立つ:", symmetric)


def main() -> None:
    report()


if __name__ == "__main__":
    main()
