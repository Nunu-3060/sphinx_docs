"""FFT による高速な畳み込み: オーバーラップ加算法.

長い入力 x と、長さ M のインパルス応答 h の畳み込みを、次の手順で計算する。

1. x を長さ L のブロックに分ける
2. 各ブロックと h を長さ L + M - 1 以上にゼロ詰めし、FFT の積で畳み込む
3. 各ブロックの結果（長さ L + M - 1）を、ずらしながら足し合わせる

結果が np.convolve と一致することを確かめ、計算時間を比べる。

使い方: python fast_convolution.py
"""

import math
import time
from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray
from scipy import signal


def overlap_add(x: NDArray[np.float64], h: NDArray[np.float64], block: int = 1024) -> NDArray[np.float64]:
    """オーバーラップ加算法で x と h の畳み込み（長さ len(x) + len(h) - 1）を求める."""
    m = len(h)
    n_fft = 1 << (block + m - 2).bit_length()  # block + m - 1 以上の 2 のべき乗
    h_spectrum = np.fft.rfft(h, n=n_fft)
    y = np.zeros(len(x) + m - 1)
    for start in range(0, len(x), block):
        segment = x[start:start + block]
        piece = np.fft.irfft(np.fft.rfft(segment, n=n_fft) * h_spectrum, n=n_fft)
        length = len(segment) + m - 1
        y[start:start + length] += piece[:length]
    return y


def elapsed(func: Callable[[], object], repeat: int = 3) -> float:
    """func() の計算時間 [s] を repeat 回測り、最小値を返す."""
    best = math.inf
    for _ in range(repeat):
        start = time.perf_counter()
        func()
        best = min(best, time.perf_counter() - start)
    return best


def report() -> None:
    """結果の一致と、計算時間を表示する（計算時間は計算機によって変わる）."""
    rng = np.random.default_rng(3)
    x = rng.standard_normal(200_000)
    h = rng.standard_normal(1000)
    y = overlap_add(x, h)
    print("np.convolve と一致する:", np.allclose(y, np.convolve(x, h)))
    print("scipy.signal.oaconvolve と一致する:", np.allclose(y, signal.oaconvolve(x, h)))
    print()
    print(f"入力の長さ {len(x):,}、インパルス応答の長さ {len(h):,} のときの計算時間")
    print(f"  np.convolve（直接計算）      {elapsed(lambda: np.convolve(x, h)) * 1000:8.1f} ms")
    print(f"  overlap_add（自作）          {elapsed(lambda: overlap_add(x, h)) * 1000:8.1f} ms")
    print(f"  scipy.signal.oaconvolve      {elapsed(lambda: signal.oaconvolve(x, h)) * 1000:8.1f} ms")


def main() -> None:
    report()


if __name__ == "__main__":
    main()
