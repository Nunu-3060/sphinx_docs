"""第 8 章：各点収束と一様収束の違いを数値で確かめる。

次の 3 つの実験を行い、結果を表形式で表示する。

1. f_n(x) = x^n の、区間 [0, 0.9] と [0, 1) における sup|f_n(x) - 0| の変化
2. g_n(x) = n x e^{-n x^2} の、区間 [0, 1] における積分値と最大値の変化
3. 矩形波のフーリエ級数の部分和の最大値（ギブズ現象）

sup や最大値は、区間内に細かくとった格子点上の最大値で近似する。
表の見出しは、桁をそろえるために英字で表示する。

実行方法:
    python ch08_uniform_convergence.py
"""

import math

import numpy as np
import numpy.typing as npt

FloatArray = npt.NDArray[np.float64]


def sup_on_grid(values: FloatArray) -> float:
    """格子点上の値の絶対値の最大値を返す（sup の近似）。"""
    return float(np.max(np.abs(values)))


def experiment_power() -> None:
    """実験 1：x^n は [0, 0.9] では一様収束するが、[0, 1) では一様収束しない。"""
    print("Experiment 1: sup|x^n|")
    x_closed = np.linspace(0.0, 0.9, 10001)
    # [0, 1) を近似するため、右端の 1 を除いた格子点を使う
    x_open = np.linspace(0.0, 1.0, 100001)[:-1]
    print(f"{'n':>6} {'sup on [0, 0.9]':>16} {'sup on [0, 1)':>16}")
    for n in [1, 10, 100, 1000]:
        print(f"{n:>6} {sup_on_grid(x_closed**n):>16.3e} {sup_on_grid(x_open**n):>16.3e}")
    print()


def spike(n: int, x: FloatArray) -> FloatArray:
    """g_n(x) = n x e^{-n x^2}。"""
    return n * x * np.exp(-n * x**2)


def experiment_spike() -> None:
    """実験 2：各点収束の極限は 0 だが、積分値は 1/2 に近づく。"""
    print("Experiment 2: g_n(x) = n x exp(-n x^2) on [0, 1]")
    x = np.linspace(0.0, 1.0, 200001)
    print(f"{'n':>6} {'integral':>12} {'exact':>12} {'max':>10}")
    for n in [1, 10, 100, 1000, 10000]:
        y = spike(n, x)
        numerical = float(np.trapezoid(y, x))
        exact = (1.0 - math.exp(-n)) / 2.0
        print(f"{n:>6} {numerical:>12.6f} {exact:>12.6f} {sup_on_grid(y):>10.3f}")
    print()


def square_wave_partial_sum(num_terms: int, x: FloatArray) -> FloatArray:
    """矩形波のフーリエ級数 (4/π) Σ sin((2k-1)x)/(2k-1) の、最初の num_terms 項の部分和。"""
    total = np.zeros_like(x)
    for k in range(1, num_terms + 1):
        m = 2 * k - 1
        total += np.sin(m * x) / m
    return 4.0 / math.pi * total


def experiment_gibbs() -> None:
    """実験 3：部分和の最大値は 1 に近づかず、約 1.179 に近づく。"""
    print("Experiment 3: maximum of Fourier partial sums of the square wave")
    # 部分和は x = π/2 に関して対称なので、(0, π/2] で最大値を探せば十分である
    x = np.linspace(0.0, math.pi / 2, 200001)[1:]
    print(f"{'terms':>6} {'max':>10} {'argmax x':>10}")
    for num_terms in [5, 10, 50, 100, 500]:
        y = square_wave_partial_sum(num_terms, x)
        i = int(np.argmax(y))
        print(f"{num_terms:>6} {float(y[i]):>10.5f} {float(x[i]):>10.5f}")
    print("limit (theory): (2/pi) Si(pi) = 1.17898...")


def main() -> None:
    """3 つの実験を順に実行する。"""
    experiment_power()
    experiment_spike()
    experiment_gibbs()


if __name__ == "__main__":
    main()
