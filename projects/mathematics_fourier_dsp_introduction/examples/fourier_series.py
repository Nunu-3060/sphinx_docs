"""矩形波のフーリエ級数: 部分和の収束とギブス現象.

振幅 1、周期 T の矩形波（0 < t < T/2 で +1、T/2 < t < T で -1）は、
奇数次の正弦波だけを含み、次のように展開できる。

    x(t) = (4 / pi) * (sin(w0 t) + sin(3 w0 t) / 3 + sin(5 w0 t) / 5 + ...)

ここで w0 = 2 pi / T である。このサンプルでは、フーリエ係数を数値積分で
求めて理論値と比べ、部分和の最大値（行き過ぎ）を調べる。

使い方: python fourier_series.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import dsp_plot

PERIOD = 1.0  # 周期 T [s]


def square_wave(t: NDArray[np.float64]) -> NDArray[np.float64]:
    """振幅 1、周期 PERIOD の矩形波を返す."""
    phase = np.mod(t, PERIOD) / PERIOD
    result: NDArray[np.float64] = np.where(phase < 0.5, 1.0, -1.0)
    return result


def partial_sum(t: NDArray[np.float64], max_order: int) -> NDArray[np.float64]:
    """矩形波のフーリエ級数を max_order 次の高調波まで足した部分和を返す."""
    w0 = 2.0 * np.pi / PERIOD
    total = np.zeros_like(t)
    for k in range(1, max_order + 1, 2):  # 奇数次だけを足す
        total += 4.0 / (np.pi * k) * np.sin(k * w0 * t)
    return total


def sine_coefficients(max_order: int, num_points: int = 10000) -> NDArray[np.float64]:
    """正弦の係数 b_k = (2 / T) * integral of x(t) sin(k w0 t) dt を数値積分で求める.

    1 周期を num_points 個の点に分け、長方形の面積の和で積分を近似する。
    戻り値の k 番目の要素が b_k である（b_0 は使わないので 0 とする）。
    """
    dt = PERIOD / num_points
    t = np.linspace(dt / 2, PERIOD - dt / 2, num_points)  # 各区間の中点
    x = square_wave(t)
    w0 = 2.0 * np.pi / PERIOD
    b = np.zeros(max_order + 1)
    for k in range(1, max_order + 1):
        b[k] = 2.0 / PERIOD * np.sum(x * np.sin(k * w0 * t)) * dt
    return b


def report() -> None:
    """フーリエ係数と、部分和の最大値を表示する."""
    b = sine_coefficients(7)
    print("k   数値積分の b_k   理論値 4/(pi k)（k が奇数のとき）")
    for k in range(1, 8):
        theory = 4.0 / (np.pi * k) if k % 2 == 1 else 0.0
        print(f"{k}   {b[k]:10.6f}       {theory:10.6f}")
    print()
    t = np.linspace(0.0, PERIOD / 2, 200001)
    print("最高次数   部分和の最大値")
    for order in (5, 21, 101, 1001):
        print(f"{order:8d}   {partial_sum(t, order).max():.4f}")


def create_figure() -> Figure:
    """部分和が矩形波に近づく様子と、不連続点の付近の拡大図を描く."""
    t = np.linspace(-0.25, 1.25, 3001)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), width_ratios=(3, 2))
    ax = axes[0]
    ax.plot(t, square_wave(t), color="0.6", linewidth=2.5, label="矩形波")
    for i, order in enumerate((1, 3, 9, 49)):
        ax.plot(t, partial_sum(t, order), color=f"C{i}", linewidth=1.0, label=f"{order} 次まで")
    ax.set_xlabel("時間 t [s]")
    ax.set_title("部分和")
    ax.legend(loc="lower left", fontsize=8, ncols=5)
    ax.set_ylim(-1.6, 1.6)
    dsp_plot.style_axes(ax)

    ax = axes[1]
    t = np.linspace(-0.05, 0.05, 2001)
    ax.plot(t, square_wave(t), color="0.6", linewidth=2.5, label="矩形波")
    for i, order in enumerate((9, 49, 199)):
        ax.plot(t, partial_sum(t, order), color=f"C{i + 2}", linewidth=1.0, label=f"{order} 次まで")
    ax.axhline(1.179, color="k", linestyle=":", linewidth=0.8)
    ax.text(0.051, 1.179, "1.179", va="center", fontsize=9)
    ax.set_xlabel("時間 t [s]")
    ax.set_title("t = 0 の付近の拡大")
    ax.legend(loc="lower right", fontsize=8)
    ax.set_ylim(-1.4, 1.4)
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
