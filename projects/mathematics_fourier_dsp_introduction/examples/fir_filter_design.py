"""窓関数法による FIR ローパスフィルタの設計.

理想ローパスフィルタのインパルス応答（sinc 関数）を有限の長さで打ち切り、
窓関数を掛けて FIR フィルタを作る。自作の設計関数と scipy.signal.firwin の
結果が一致することを確かめ、窓関数による周波数特性の違いを比べる。

使い方: python fir_filter_design.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray
from scipy import signal

import dsp_plot

FS = 1000.0  # 標本化周波数 [Hz]
CUTOFF = 100.0  # カットオフ周波数 [Hz]
NUM_TAPS = 51  # タップ数（フィルタ係数の個数）
WINDOWS = {"矩形窓": "boxcar", "ハミング窓": "hamming", "ブラックマン窓": "blackman"}


def design_lowpass(num_taps: int, cutoff: float, fs: float, window: str) -> NDArray[np.float64]:
    """窓関数法で FIR ローパスフィルタの係数を求める.

    1. 理想ローパスフィルタのインパルス応答 h[n] = 2 fc sinc(2 fc (n - M)) を求める
       （fc = cutoff / fs は正規化したカットオフ周波数、M = (num_taps - 1) / 2）。
    2. 窓関数を掛けて、長さ num_taps に打ち切る。
    3. 直流での利得（係数の和）が 1 になるように正規化する。
    """
    fc = cutoff / fs
    n = np.arange(num_taps) - (num_taps - 1) / 2
    ideal = 2 * fc * np.sinc(2 * fc * n)
    h = ideal * signal.get_window(window, num_taps, fftbins=False)
    result: NDArray[np.float64] = h / np.sum(h)
    return result


def gain_db(h: NDArray[np.float64], num_freqs: int = 4096) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """FIR フィルタの (周波数 [Hz], 振幅特性 [dB]) を返す."""
    freqs, response = signal.freqz(h, worN=num_freqs, fs=FS)
    return np.asarray(freqs, dtype=np.float64), dsp_plot.to_db(response)


def report() -> None:
    """自作の設計と firwin の比較、および通過域と阻止域の特性を表示する."""
    for name, window in WINDOWS.items():
        same = np.allclose(design_lowpass(NUM_TAPS, CUTOFF, FS, window),
                           signal.firwin(NUM_TAPS, CUTOFF, window=window, fs=FS))
        print(f"{name}: firwin と一致する: {same}")
    print()
    print("通過域（0 - 50 Hz）の最大偏差、150 Hz 以上と 200 Hz 以上での最大利得")
    for name, window in WINDOWS.items():
        freqs, db = gain_db(design_lowpass(NUM_TAPS, CUTOFF, FS, window))
        passband = np.max(np.abs(db[freqs <= 50.0]))
        stop150 = np.max(db[freqs >= 150.0])
        stop200 = np.max(db[freqs >= 200.0])
        print(f"  {passband:6.3f} dB  {stop150:6.1f} dB  {stop200:6.1f} dB  {name}")
    delay = (NUM_TAPS - 1) / 2
    print()
    print(f"群遅延 = {delay:.0f} 標本 = {delay / FS * 1000:.0f} ms（すべての周波数で一定）")


def create_figure() -> Figure:
    """ハミング窓のインパルス応答（左）と、3 つの窓関数の振幅特性（右）を描く."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), width_ratios=(2, 3))
    ax = axes[0]
    h = design_lowpass(NUM_TAPS, CUTOFF, FS, "hamming")
    dsp_plot.stem(ax, np.arange(NUM_TAPS), h)
    ax.set_xlabel("n")
    ax.set_title("インパルス応答（ハミング窓）")
    dsp_plot.style_axes(ax)
    ax = axes[1]
    for i, (name, window) in enumerate(WINDOWS.items()):
        freqs, db = gain_db(design_lowpass(NUM_TAPS, CUTOFF, FS, window))
        ax.plot(freqs, db, color=f"C{i}", linewidth=1.0, label=name)
    ax.axvline(CUTOFF, color="0.4", linestyle=":", linewidth=1.0)
    ax.set_xlabel("周波数 [Hz]")
    ax.set_ylabel("利得 [dB]")
    ax.set_ylim(-110, 10)
    ax.set_xlim(0, FS / 2)
    ax.set_title("振幅特性")
    ax.legend(loc="upper right")
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
