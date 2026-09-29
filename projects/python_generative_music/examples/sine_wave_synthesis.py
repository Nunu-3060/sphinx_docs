"""numpy でサイン波を合成し、ADSR エンベロープを適用して WAV ファイルへ出力するサンプル。"""

from __future__ import annotations

import wave
from pathlib import Path

import numpy as np

SAMPLE_RATE = 44100
FREQUENCY = 440.0
DURATION = 2.0
OUTPUT_PATH = Path(__file__).with_name("sine_wave.wav")


def generate_sine_wave(
    frequency: float,
    duration: float,
    sample_rate: int,
) -> np.ndarray:
    """指定した周波数のサイン波を、指定した長さ分だけ生成する。"""
    sample_count = int(sample_rate * duration)
    times = np.linspace(0, duration, sample_count, endpoint=False)
    return np.sin(2 * np.pi * frequency * times)


def apply_adsr_envelope(
    samples: np.ndarray,
    sample_rate: int,
    attack: float,
    decay: float,
    sustain_level: float,
    release: float,
) -> np.ndarray:
    """アタック・ディケイ・サステイン・リリースからなる音量変化を適用する。"""
    total_count = len(samples)
    attack_count = int(sample_rate * attack)
    decay_count = int(sample_rate * decay)
    release_count = int(sample_rate * release)
    sustain_count = total_count - attack_count - decay_count - release_count
    sustain_count = max(sustain_count, 0)

    envelope = np.concatenate(
        [
            np.linspace(0.0, 1.0, attack_count, endpoint=False),
            np.linspace(1.0, sustain_level, decay_count, endpoint=False),
            np.full(sustain_count, sustain_level),
            np.linspace(sustain_level, 0.0, release_count),
        ]
    )
    envelope = envelope[:total_count]
    return samples[: len(envelope)] * envelope


def write_wav(
    samples: np.ndarray, sample_rate: int, output_path: Path
) -> None:
    """浮動小数点の波形データを 16 ビット PCM の WAV ファイルへ書き出す。"""
    normalized = np.clip(samples, -1.0, 1.0)
    pcm_data = (normalized * 32767).astype(np.int16)

    with wave.open(str(output_path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm_data.tobytes())


def main() -> None:
    samples = generate_sine_wave(FREQUENCY, DURATION, SAMPLE_RATE)
    samples = apply_adsr_envelope(
        samples,
        SAMPLE_RATE,
        attack=0.05,
        decay=0.1,
        sustain_level=0.6,
        release=0.3,
    )
    write_wav(samples, SAMPLE_RATE, OUTPUT_PATH)
    print(f"{OUTPUT_PATH.name} を出力しました。")


if __name__ == "__main__":
    main()
