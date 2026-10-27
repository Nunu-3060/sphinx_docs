"""窓関数を使ったスペクトル解析: スペクトル漏れと振幅の推定.

標本化周波数 1000 Hz で 200 点（0.2 秒）を取り出すと、DFT の周波数の
間隔（周波数分解能）は 5 Hz になる。周波数が 5 Hz の整数倍でない正弦波は、
DFT の 1 つのビンに収まらず、周囲のビンに漏れる（スペクトル漏れ）。

このサンプルでは、矩形窓、ハン窓、ブラックマン窓で、
(1) 振幅の推定値、(2) 大きな正弦波の近くにある小さな正弦波の見え方を比べる。

使い方: python spectrum_analysis.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray
from scipy import signal

import dsp_plot

FS = 1000.0  # 標本化周波数 [Hz]
N_POINTS = 200  # 取り出す標本の数
WINDOWS = {"矩形窓": "boxcar", "ハン窓": "hann", "ブラックマン窓": "blackman"}


def amplitude_spectrum(x: NDArray[np.float64], window: str) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """窓関数を掛けて片側の振幅スペクトルを求め、(周波数, 振幅) を返す.

    振幅 A の正弦波の周波数が DFT のビンに一致するとき、その周波数の値が A
    になるように、窓関数の和で割って 2 倍する（直流成分は 2 倍しない）。
    """
    w = signal.get_window(window, len(x), fftbins=True)
    spectrum = np.fft.rfft(x * w)
    amplitude = 2.0 * np.abs(spectrum) / np.sum(w)
    amplitude[0] /= 2.0
    freqs = np.fft.rfftfreq(len(x), d=1.0 / FS)
    return freqs, amplitude


def tone(freq: float, amplitude: float = 1.0) -> NDArray[np.float64]:
    """周波数 freq [Hz]、振幅 amplitude の正弦波を N_POINTS 点返す."""
    t = np.arange(N_POINTS) / FS
    result: NDArray[np.float64] = amplitude * np.sin(2 * np.pi * freq * t)
    return result


def report() -> None:
    """周波数がビンに一致する場合としない場合の、振幅の推定値を表示する."""
    print(f"周波数分解能 = {FS / N_POINTS} Hz")
    print("振幅の推定値: 100 Hz（ビンに一致）、102.5 Hz（ビンの中間）")
    for name, window in WINDOWS.items():
        peaks = [amplitude_spectrum(tone(f), window)[1].max() for f in (100.0, 102.5)]
        print(f"  {peaks[0]:.3f}  {peaks[1]:.3f} ({20 * np.log10(peaks[1]):5.2f} dB)  {name}")
    print()
    x = tone(102.5) + tone(177.5, 0.001)
    print("102.5 Hz（振幅 1）と 177.5 Hz（振幅 0.001、-60 dB）を含む信号の 177.5 Hz 付近の値")
    for name, window in WINDOWS.items():
        freqs, amplitude = amplitude_spectrum(x, window)
        k = int(np.argmin(np.abs(freqs - 177.5)))
        print(f"  {20 * np.log10(amplitude[k]):6.1f} dB  {name}")


def create_figure() -> Figure:
    """1 つの正弦波のスペクトル（左）と、大小 2 つの正弦波のスペクトル（右）を描く."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)
    signals = [(tone(102.5), "102.5 Hz の正弦波"),
               (tone(102.5) + tone(177.5, 0.001), "102.5 Hz と 177.5 Hz（-60 dB）")]
    for ax, (x, title) in zip(axes, signals):
        for i, (name, window) in enumerate(WINDOWS.items()):
            freqs, amplitude = amplitude_spectrum(x, window)
            ax.plot(freqs, dsp_plot.to_db(amplitude), ".-", color=f"C{i}", linewidth=0.8, markersize=3,
                    label=name)
        ax.set_title(title)
        ax.set_xlabel("周波数 [Hz]")
        ax.set_xlim(0, 300)
        ax.set_ylim(-120, 5)
        dsp_plot.style_axes(ax)
    axes[1].axvline(177.5, color="0.4", linestyle=":", linewidth=1.0)
    axes[0].set_ylabel("振幅 [dB]")
    axes[0].legend(loc="upper right")
    fig.tight_layout()
    return fig


def main() -> None:
    report()
    dsp_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
