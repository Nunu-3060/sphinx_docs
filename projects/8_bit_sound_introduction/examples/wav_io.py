"""WAV ファイルの書き出しを行う共通モジュール.

本書のサンプルコードはすべて、浮動小数点数の配列（値の範囲は -1.0 から 1.0）
として音を作り、最後にこのモジュールで 16 bit の WAV ファイルに変換する。
"""

import wave
from pathlib import Path

import numpy as np
import numpy.typing as npt

# 1 秒あたりのサンプル数（サンプリング周波数）
SAMPLE_RATE = 44100

# 浮動小数点数の音声データを表す型
Signal = npt.NDArray[np.float64]


def seconds_to_samples(seconds: float) -> int:
    """秒数をサンプル数に変換する."""
    return int(round(seconds * SAMPLE_RATE))


def silence(seconds: float) -> Signal:
    """指定した長さの無音を返す."""
    return np.zeros(seconds_to_samples(seconds), dtype=np.float64)


def normalize(signal: Signal, peak: float = 0.9) -> Signal:
    """最大振幅が peak になるように音量を揃える."""
    max_amplitude = float(np.max(np.abs(signal))) if signal.size > 0 else 0.0
    if max_amplitude == 0.0:
        return signal
    return signal * (peak / max_amplitude)


def write_wav(path: Path, signal: Signal, sample_rate: int = SAMPLE_RATE) -> None:
    """モノラル 16 bit の WAV ファイルとして書き出す.

    範囲外の値は -1.0 から 1.0 に切り詰める（クリッピング）。
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    clipped = np.clip(signal, -1.0, 1.0)
    pcm = (clipped * 32767.0).astype("<i2")  # リトルエンディアンの 16 bit 整数
    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(1)  # モノラル
        wav_file.setsampwidth(2)  # 1 サンプルあたり 2 バイト = 16 bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm.tobytes())


def main() -> None:
    """動作確認として 440 Hz の正弦波を 1 秒間書き出す."""
    t = np.arange(SAMPLE_RATE) / SAMPLE_RATE
    signal = 0.5 * np.sin(2.0 * np.pi * 440.0 * t)
    write_wav(Path("output") / "sine_440.wav", signal)


if __name__ == "__main__":
    main()
