"""DTMF 信号（電話のプッシュ音）の生成と、ゲルツェル法による検出.

DTMF では、各キーを「低群の周波数」と「高群の周波数」の 2 つの正弦波の和で表す。

           1209 Hz  1336 Hz  1477 Hz  1633 Hz
    697 Hz    1        2        3        A
    770 Hz    4        5        6        B
    852 Hz    7        8        9        C
    941 Hz    *        0        #        D

検出には、特定の周波数の DFT の値だけを効率よく求めるゲルツェル法を使う。

使い方: python dtmf_detection.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import dsp_plot

FS = 8000.0  # 標本化周波数 [Hz]
TONE = 0.08  # 1 つのキーの音の長さ [s]
GAP = 0.04  # キーの間の無音の長さ [s]
LOW = (697.0, 770.0, 852.0, 941.0)
HIGH = (1209.0, 1336.0, 1477.0, 1633.0)
KEYS = ("123A", "456B", "789C", "*0#D")


def key_frequencies(key: str) -> tuple[float, float]:
    """キーに対応する (低群の周波数, 高群の周波数) を返す."""
    for row, keys in enumerate(KEYS):
        if key in keys:
            return LOW[row], HIGH[keys.index(key)]
    raise ValueError(f"DTMF のキーではない: {key}")


def generate(keys: str, noise_std: float = 0.3) -> NDArray[np.float64]:
    """キーの並びに対応する DTMF 信号を作り、白色雑音を加えて返す."""
    t = np.arange(int(FS * TONE)) / FS
    gap = np.zeros(int(FS * GAP))
    parts = []
    for key in keys:
        f_low, f_high = key_frequencies(key)
        parts.append(0.5 * np.sin(2 * np.pi * f_low * t) + 0.5 * np.sin(2 * np.pi * f_high * t))
        parts.append(gap)
    x = np.concatenate(parts)
    rng = np.random.default_rng(2)
    result: NDArray[np.float64] = x + noise_std * rng.standard_normal(len(x))
    return result


def goertzel_power(x: NDArray[np.float64], freq: float) -> float:
    """ゲルツェル法で、周波数 freq [Hz] における |X|^2 を求める.

    2 次の IIR フィルタ s[n] = x[n] + 2 cos(w) s[n-1] - s[n-2] を通し、
    最後の 2 つの値から |X|^2 = s1^2 + s2^2 - 2 cos(w) s1 s2 を計算する。
    """
    coeff = float(2.0 * np.cos(2.0 * np.pi * freq / FS))
    s1 = 0.0
    s2 = 0.0
    for sample in x:
        s1, s2 = float(sample) + coeff * s1 - s2, s1
    return s1 * s1 + s2 * s2 - coeff * s1 * s2


def detect(x: NDArray[np.float64]) -> str:
    """DTMF 信号をキーの長さごとに区切り、押されたキーを判定する.

    この例では、キーの音と無音の長さが分かっているものとして区切る。
    """
    tone_len = int(FS * TONE)
    step = tone_len + int(FS * GAP)
    result = ""
    for start in range(0, len(x) - tone_len + 1, step):
        block = x[start:start + tone_len]
        row = int(np.argmax([goertzel_power(block, f) for f in LOW]))
        col = int(np.argmax([goertzel_power(block, f) for f in HIGH]))
        result += KEYS[row][col]
    return result


def report() -> None:
    """DTMF 信号を作って検出し、結果を表示する."""
    keys = "0123456789*#"
    x = generate(keys)
    print(f"送ったキー: {keys}")
    print(f"検出したキー: {detect(x)}")
    block = x[:int(FS * TONE)]
    spectrum = np.fft.rfft(block)
    freqs = np.fft.rfftfreq(len(block), d=1.0 / FS)
    k = int(np.argmin(np.abs(freqs - 941.0)))
    print(f"{freqs[k]:.1f} Hz の |X|^2: ゲルツェル法 = {goertzel_power(block, freqs[k]):.1f}、"
          f"FFT = {abs(spectrum[k]) ** 2:.1f}")


def create_figure() -> Figure:
    """キー「5」の DTMF 信号の振幅スペクトルと、8 つの周波数の検出値を描く."""
    x = generate("5")[:int(FS * TONE)]
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), width_ratios=(3, 2))
    ax = axes[0]
    w = np.hanning(len(x))
    freqs = np.fft.rfftfreq(len(x), d=1.0 / FS)
    ax.plot(freqs, dsp_plot.to_db(2 * np.fft.rfft(x * w) / np.sum(w)), linewidth=0.8)
    for f in LOW + HIGH:
        ax.axvline(f, color="0.6", linestyle=":", linewidth=0.8)
    ax.set_xlim(500, 1800)
    ax.set_xlabel("周波数 [Hz]")
    ax.set_ylabel("振幅 [dB]")
    ax.set_title("キー「5」のスペクトル")
    dsp_plot.style_axes(ax)
    ax = axes[1]
    freqs_all = LOW + HIGH
    powers = [goertzel_power(x, f) for f in freqs_all]
    colors = ["C1" if f in key_frequencies("5") else "C0" for f in freqs_all]
    ax.bar([f"{f:.0f}" for f in freqs_all], powers, color=colors)
    ax.tick_params(axis="x", labelrotation=60)
    ax.set_xlabel("周波数 [Hz]")
    ax.set_title("ゲルツェル法の |X|²")
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
