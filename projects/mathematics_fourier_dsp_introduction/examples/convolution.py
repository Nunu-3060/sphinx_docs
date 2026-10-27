"""畳み込み和: 定義どおりの実装と numpy.convolve の比較.

LTI システムの出力 y[n] は、入力 x[n] とインパルス応答 h[n] の畳み込み和

    y[n] = sum over k of h[k] x[n - k]

で求められる。このサンプルでは、二重ループの素直な実装と np.convolve の
結果が一致することを確かめ、3 点の移動平均を例に出力を表示する。

使い方: python convolution.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import dsp_plot


def convolve(x: NDArray[np.float64], h: NDArray[np.float64]) -> NDArray[np.float64]:
    """有限長の x と h の畳み込み和を定義どおりに計算する.

    x の長さを N、h の長さを M とすると、結果の長さは N + M - 1 である。
    """
    n_out = len(x) + len(h) - 1
    y = np.zeros(n_out)
    for n in range(n_out):
        for k in range(len(h)):
            if 0 <= n - k < len(x):
                y[n] += h[k] * x[n - k]
    return y


def test_signals() -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """例に使う入力（ステップの後に減衰する信号）と、3 点の移動平均のインパルス応答を返す."""
    x = np.array([0.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.25, 0.0, 0.0, 0.0])
    h = np.full(3, 1.0 / 3.0)
    return x, h


def report() -> None:
    """自作の畳み込みと np.convolve の結果を表示する."""
    x, h = test_signals()
    y = convolve(x, h)
    with np.printoptions(precision=4, suppress=True):
        print("x =", x)
        print("h =", h)
        print("y =", y)
        print("np.convolve と一致する:", np.allclose(y, np.convolve(x, h)))
    # 長い信号でも一致することを、乱数の信号で確かめる
    rng = np.random.default_rng(0)
    x_long = rng.standard_normal(500)
    h_long = rng.standard_normal(40)
    print("乱数の信号でも一致する:", np.allclose(convolve(x_long, h_long), np.convolve(x_long, h_long)))


def create_figure() -> Figure:
    """入力、インパルス応答、出力を棒グラフで描く."""
    x, h = test_signals()
    y = convolve(x, h)
    fig, axes = plt.subplots(1, 3, figsize=(10, 2.8), sharey=True)
    for ax, signal, title, color in zip(axes, (x, h, y), ("入力 x[n]", "インパルス応答 h[n]", "出力 y[n]"),
                                        ("C0", "C2", "C1")):
        dsp_plot.stem(ax, np.arange(len(signal)), signal, color=color)
        ax.set_title(title)
        ax.set_xlabel("n")
        ax.set_xlim(-0.8, 12.8)
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
