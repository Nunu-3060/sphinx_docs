"""エイリアシング: 標本化すると、異なる周波数の正弦波が区別できなくなる.

標本化周波数 fs = 10 Hz で、3 Hz、7 Hz、13 Hz の余弦波を標本化すると、
すべて同じ標本値になる。ナイキスト周波数 fs / 2 = 5 Hz を超える成分は、
0 から fs / 2 の範囲の別の周波数（エイリアス）として現れる。

使い方: python aliasing.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import dsp_plot

FS = 10.0  # 標本化周波数 [Hz]


def apparent_frequency(f: float, fs: float) -> float:
    """周波数 f の正弦波を fs で標本化したとき、見かけの周波数（0 から fs / 2）を返す.

    f を fs の整数倍だけずらし、さらに負の周波数を正に折り返す。
    """
    shifted = f - fs * round(f / fs)  # -fs/2 から fs/2 の範囲に移す
    return abs(shifted)


def report() -> None:
    """いくつかの周波数の見かけの周波数と、標本値の一致を表示する."""
    print(f"標本化周波数 fs = {FS} Hz、ナイキスト周波数 = {FS / 2} Hz")
    print("周波数 [Hz]   見かけの周波数 [Hz]")
    for f in (1.0, 3.0, 4.0, 6.0, 7.0, 9.0, 10.0, 13.0, 27.0):
        print(f"{f:10.1f}   {apparent_frequency(f, FS):10.1f}")
    n = np.arange(10)
    x3 = np.cos(2 * np.pi * 3.0 * n / FS)
    x7 = np.cos(2 * np.pi * 7.0 * n / FS)
    x13 = np.cos(2 * np.pi * 13.0 * n / FS)
    print()
    print("3 Hz と 7 Hz の標本値が一致する:", np.allclose(x3, x7))
    print("3 Hz と 13 Hz の標本値が一致する:", np.allclose(x3, x13))


def create_figure() -> Figure:
    """7 Hz の余弦波の標本値が、3 Hz の余弦波の上にも乗ることを描く."""
    t = np.linspace(0.0, 1.0, 2001)
    n = np.arange(int(FS) + 1)
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.plot(t, np.cos(2 * np.pi * 7.0 * t), color="C0", linewidth=1.0, label="7 Hz の余弦波（元の信号）")
    ax.plot(t, np.cos(2 * np.pi * 3.0 * t), color="C1", linewidth=1.5, linestyle="--",
            label="3 Hz の余弦波（エイリアス）")
    ax.plot(n / FS, np.cos(2 * np.pi * 7.0 * n / FS), "o", color="k", label="標本値（fs = 10 Hz）")
    ax.set_xlabel("時間 t [s]")
    ax.set_ylim(-1.3, 1.6)
    ax.legend(loc="upper right", ncols=3, fontsize=9)
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
