"""雑音の除去: 周波数領域での除去、バタワースフィルタ、移動平均の比較.

10 Hz と 25 Hz の正弦波を足した信号に白色雑音を加え、次の 3 つの方法で
雑音を減らす。元の信号との差から SNR（信号対雑音比）を求めて比べる。

1. FFT で周波数領域に変換し、40 Hz を超える成分を 0 にして逆変換する
2. カットオフ周波数 40 Hz の 4 次バタワース LPF を filtfilt で掛ける
3. 21 点の移動平均を掛ける

使い方: python noise_reduction.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray
from scipy import signal

import dsp_plot

FS = 1000.0  # 標本化周波数 [Hz]
DURATION = 1.0  # 信号の長さ [s]
CUTOFF = 40.0  # 除去の境目の周波数 [Hz]
NOISE_STD = 0.5  # 雑音の標準偏差


def make_signals() -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """(時刻, 元の信号, 雑音を加えた信号) を返す."""
    t = np.arange(int(FS * DURATION)) / FS
    clean = np.sin(2 * np.pi * 10 * t) + 0.5 * np.sin(2 * np.pi * 25 * t)
    rng = np.random.default_rng(1)
    noisy = clean + NOISE_STD * rng.standard_normal(len(t))
    return t, clean, noisy


def fft_mask(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """FFT で CUTOFF を超える周波数の成分を 0 にして、逆変換する."""
    spectrum = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(len(x), d=1.0 / FS)
    spectrum[freqs > CUTOFF] = 0.0
    return np.fft.irfft(spectrum, n=len(x))


def butterworth(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """4 次のバタワース LPF を順方向と逆方向に掛ける（位相のずれがない）."""
    sos = signal.butter(4, CUTOFF, fs=FS, output="sos")
    return np.asarray(signal.sosfiltfilt(sos, x), dtype=np.float64)


def moving_average(x: NDArray[np.float64], length: int = 21) -> NDArray[np.float64]:
    """length 点の移動平均（中心をそろえる）."""
    return np.convolve(x, np.full(length, 1.0 / length), mode="same")


METHODS = {"FFT による除去": fft_mask, "バタワース LPF": butterworth, "移動平均": moving_average}


def snr_db(clean: NDArray[np.float64], estimate: NDArray[np.float64]) -> float:
    """元の信号と推定値の差を雑音とみなした SNR [dB]."""
    return float(10 * np.log10(np.sum(clean**2) / np.sum((estimate - clean) ** 2)))


def report() -> None:
    """各方法で雑音を減らした後の SNR を表示する."""
    _, clean, noisy = make_signals()
    # 両端は、フィルタの過渡的な応答や周期の仮定の影響を受けるので、評価から除く
    inner = slice(100, -100)
    print(f"SNR = {snr_db(clean[inner], noisy[inner]):5.1f} dB  雑音を加えた信号")
    for name, method in METHODS.items():
        print(f"SNR = {snr_db(clean[inner], method(noisy)[inner]):5.1f} dB  {name}")


def create_figure() -> Figure:
    """雑音を加えた信号と除去の結果（上）、およびそれぞれの振幅スペクトル（下）を描く."""
    t, clean, noisy = make_signals()
    fig, axes = plt.subplots(2, 1, figsize=(10, 6.5))
    ax = axes[0]
    ax.plot(t, noisy, color="0.75", linewidth=0.8, label="雑音を加えた信号")
    ax.plot(t, clean, color="k", linewidth=1.5, label="元の信号")
    for i, (name, method) in enumerate(METHODS.items()):
        ax.plot(t, method(noisy), color=f"C{i}", linewidth=1.0, label=name)
    ax.set_xlim(0.3, 0.6)
    ax.set_xlabel("時間 [s]")
    ax.legend(loc="upper right", ncols=5, fontsize=8)
    ax.set_ylim(-3.0, 3.5)
    dsp_plot.style_axes(ax)
    ax = axes[1]
    freqs = np.fft.rfftfreq(len(t), d=1.0 / FS)
    scale = 2.0 / len(t)
    ax.plot(freqs, dsp_plot.to_db(scale * np.fft.rfft(noisy)), color="0.75", linewidth=0.8, label="雑音を加えた信号")
    for i, (name, method) in enumerate(METHODS.items()):
        if name == "FFT による除去":
            continue
        ax.plot(freqs, dsp_plot.to_db(scale * np.fft.rfft(method(noisy))), color=f"C{i}", linewidth=0.8, label=name)
    ax.axvline(CUTOFF, color="0.4", linestyle=":", linewidth=1.0)
    ax.set_xlim(0, 200)
    ax.set_ylim(-100, 5)
    ax.set_xlabel("周波数 [Hz]")
    ax.set_ylabel("振幅 [dB]")
    ax.legend(loc="upper right", fontsize=8)
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
