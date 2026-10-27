"""チャープ信号の短時間フーリエ変換（STFT）とスペクトログラム.

周波数が時間とともに 200 Hz から 3000 Hz まで直線的に上がる正弦波
（線形チャープ）を作り、scipy.signal.spectrogram でスペクトログラムを求める。
各時刻で振幅が最大になる周波数が、理論上の瞬時周波数と一致することを確かめる。

使い方: python spectrogram.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray
from scipy import signal

import dsp_plot

FS = 8000.0  # 標本化周波数 [Hz]
DURATION = 2.0  # 信号の長さ [s]
F_START = 200.0  # 開始時の周波数 [Hz]
F_END = 3000.0  # 終了時の周波数 [Hz]
SEGMENT = 256  # STFT の 1 区間の標本数
OVERLAP = 192  # 隣り合う区間の重なり


def chirp_signal() -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """線形チャープ信号の (時刻, 信号) を返す."""
    t = np.arange(int(FS * DURATION)) / FS
    x = signal.chirp(t, f0=F_START, t1=DURATION, f1=F_END, method="linear")
    return t, np.asarray(x, dtype=np.float64)


def instantaneous_frequency(t: float) -> float:
    """時刻 t [s] における理論上の瞬時周波数 [Hz]."""
    return F_START + (F_END - F_START) * t / DURATION


def compute_spectrogram() -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """ハン窓の STFT でスペクトログラムを求め、(周波数, 時刻, パワー) を返す."""
    _, x = chirp_signal()
    freqs, times, power = signal.spectrogram(x, fs=FS, window="hann", nperseg=SEGMENT, noverlap=OVERLAP)
    return freqs, times, power


def report() -> None:
    """いくつかの時刻で、パワーが最大の周波数と理論値を表示する."""
    freqs, times, power = compute_spectrogram()
    print(f"区間の長さ = {SEGMENT / FS * 1000:.0f} ms、周波数分解能 = {FS / SEGMENT:.2f} Hz、"
          f"時間の刻み = {(SEGMENT - OVERLAP) / FS * 1000:.0f} ms")
    print("時刻 [s]   最大の周波数 [Hz]   理論値 [Hz]")
    for target in (0.25, 0.5, 1.0, 1.5):
        i = int(np.argmin(np.abs(times - target)))
        peak = freqs[np.argmax(power[:, i])]
        print(f"{times[i]:7.3f}   {peak:12.1f}       {instantaneous_frequency(times[i]):9.1f}")


def create_figure() -> Figure:
    """チャープ信号の波形の一部と、スペクトログラムを描く."""
    t, x = chirp_signal()
    freqs, times, power = compute_spectrogram()
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), height_ratios=(1, 2))
    ax = axes[0]
    ax.plot(t, x, linewidth=0.6)
    ax.set_xlim(0, 0.05)
    ax.set_xlabel("時間 [s]")
    ax.set_title("波形（最初の 50 ms）")
    dsp_plot.style_axes(ax)
    ax = axes[1]
    level = 10 * np.log10(np.maximum(power, 1e-12) / power.max())
    mesh = ax.pcolormesh(times, freqs, level, shading="auto", vmin=-80, vmax=0, cmap="viridis", rasterized=True)
    ax.plot(times, [instantaneous_frequency(ti) for ti in times], "w--", linewidth=1.0, label="理論上の瞬時周波数")
    ax.set_xlabel("時間 [s]")
    ax.set_ylabel("周波数 [Hz]")
    ax.set_ylim(0, 4000)
    ax.set_title("スペクトログラム")
    ax.legend(loc="upper left")
    fig.colorbar(mesh, ax=ax, label="パワー [dB]")
    fig.tight_layout()
    return fig


def main() -> None:
    report()
    dsp_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
