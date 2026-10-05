"""第 7 章: A/D 変換の量子化雑音を確かめる。

フルスケールの正弦波を N ビットで量子化したときの信号対量子化雑音比
(SQNR) を計算し、理論式 SQNR ≈ 6.02 N + 1.76 [dB] と比べます。

実行例::

    python ch07_quantization.py
"""

from __future__ import annotations

import math

import numpy as np
from numpy.typing import NDArray

Array = NDArray[np.float64]


def quantize(x: Array, bits: int) -> Array:
    """範囲 [-1, 1) の信号を bits ビットで量子化する (中央値に丸める)。"""
    levels = 2 ** bits
    step = 2.0 / levels  # 量子化ステップ (1 LSB の大きさ)
    codes = np.clip(np.floor((x + 1.0) / step), 0, levels - 1)
    result: Array = -1.0 + (codes + 0.5) * step
    return result


def sqnr_db(bits: int, samples: int = 100_000) -> float:
    """フルスケールの正弦波を量子化したときの SQNR [dB] を返す。"""
    n = np.arange(samples, dtype=np.float64)
    # 周期がサンプル数と公約数を持たないように、無理数比の周波数にする
    x = np.sin(2 * np.pi * n / (100 * math.sqrt(2)))
    error = quantize(x, bits) - x
    signal_power = float(np.mean(x ** 2))
    noise_power = float(np.mean(error ** 2))
    return 10 * math.log10(signal_power / noise_power)


def main() -> None:
    print("ビット数  シミュレーション[dB]  理論値[dB]")
    for bits in (4, 8, 10, 12, 16):
        theory = 6.02 * bits + 1.76
        print(f"{bits:8d}  {sqnr_db(bits):20.2f}  {theory:10.2f}")


if __name__ == "__main__":
    main()
