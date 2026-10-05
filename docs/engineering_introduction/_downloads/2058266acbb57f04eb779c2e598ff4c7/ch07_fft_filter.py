"""第 7 章: 周波数スペクトルを求め、移動平均フィルターの効果を確かめる。

センサーの出力に、商用電源 (50 Hz) から混入した雑音と白色雑音が
乗っている、という想定の模擬信号を作ります。

* 離散フーリエ変換 (numpy.fft.rfft) で振幅スペクトルを求める
* 20 点の移動平均フィルターをかけ、50 Hz の成分が除かれることを
  確かめる (サンプリング周波数 1000 Hz では 20 点 = 50 Hz の 1 周期)

図は ch07_fft_filter.png として保存します。

実行例::

    python ch07_fft_filter.py --outdir output
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
import numpy as np
from matplotlib import font_manager
from matplotlib.figure import Figure
from numpy.typing import NDArray

JAPANESE_FONTS = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP"]

FS = 1000.0  # サンプリング周波数 [Hz]
DURATION = 1.0  # 信号の長さ [s]
WINDOW = 20  # 移動平均の点数

Array = NDArray[np.float64]


def setup_font() -> None:
    """図の文字に、見つかった日本語フォントを使う。"""
    names = {font.name for font in font_manager.fontManager.ttflist}
    for name in JAPANESE_FONTS:
        if name in names:
            matplotlib.rcParams["font.family"] = name
            break
    matplotlib.rcParams["axes.unicode_minus"] = False


def make_signal(seed: int) -> tuple[Array, Array]:
    """5 Hz の信号に 50 Hz の雑音と白色雑音を加えた模擬信号を作る。"""
    rng = np.random.default_rng(seed)
    t = np.arange(int(FS * DURATION), dtype=np.float64) / FS
    signal = np.sin(2 * np.pi * 5 * t)
    hum = 0.5 * np.sin(2 * np.pi * 50 * t)
    noise = rng.normal(0.0, 0.2, size=t.size)
    return t, signal + hum + noise


def moving_average(x: Array, window: int) -> Array:
    """過去 window 点の平均を出力する (因果的な) 移動平均フィルター。

    最初の window - 1 点は、そろっているデータだけで平均します。
    """
    cumsum = np.cumsum(np.insert(x, 0, 0.0))
    out = np.empty_like(x)
    for i in range(x.size):
        start = max(0, i + 1 - window)
        out[i] = (cumsum[i + 1] - cumsum[start]) / (i + 1 - start)
    return out


def amplitude_spectrum(x: Array) -> tuple[Array, Array]:
    """片側振幅スペクトルを返す (正弦波の振幅がそのまま読める尺度)。"""
    spectrum = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(x.size, d=1 / FS)
    amplitude = 2 * np.abs(spectrum) / x.size
    amplitude[0] /= 2  # 直流成分は 2 倍しない
    return freqs, amplitude


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path,
                        default=Path(__file__).resolve().parent / "output",
                        help="画像の保存先フォルダー")
    parser.add_argument("--seed", type=int, default=0,
                        help="雑音を作る乱数のシード")
    args = parser.parse_args()
    outdir: Path = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    t, raw = make_signal(args.seed)
    filtered = moving_average(raw, WINDOW)
    freqs, amp_raw = amplitude_spectrum(raw)
    _, amp_filtered = amplitude_spectrum(filtered)

    for f in (5, 50):
        index = int(np.argmin(np.abs(freqs - f)))
        print(f"{f:3d} Hz の振幅: フィルター前 {amp_raw[index]:.3f}, "
              f"フィルター後 {amp_filtered[index]:.3f}")
    delay_ms = (WINDOW - 1) / 2 / FS * 1000
    print(f"移動平均による遅れ: 約 {delay_ms:.1f} ms")

    setup_font()
    fig = Figure(figsize=(8, 6), layout="constrained")
    ax_time, ax_freq = fig.subplots(2, 1)

    shown = t < 0.4
    ax_time.plot(t[shown], raw[shown], color="lightgray", label="元の信号")
    ax_time.plot(t[shown], filtered[shown], label=f"{WINDOW} 点移動平均")
    ax_time.set_xlabel("時刻 [s]")
    ax_time.set_ylabel("振幅")
    ax_time.set_title("時間領域")
    ax_time.grid(alpha=0.3)
    ax_time.legend(loc="upper right")

    ax_freq.plot(freqs, amp_raw, color="gray", label="元の信号")
    ax_freq.plot(freqs, amp_filtered, label=f"{WINDOW} 点移動平均")
    ax_freq.set_xlim(0, 150)
    ax_freq.set_xlabel("周波数 [Hz]")
    ax_freq.set_ylabel("振幅")
    ax_freq.set_title("周波数領域 (5 Hz は残り、50 Hz は除かれる)")
    ax_freq.grid(alpha=0.3)
    ax_freq.legend(loc="upper right")
    fig.savefig(outdir / "ch07_fft_filter.png", dpi=120)
    print(f"図を {outdir} に保存しました。")


if __name__ == "__main__":
    main()
