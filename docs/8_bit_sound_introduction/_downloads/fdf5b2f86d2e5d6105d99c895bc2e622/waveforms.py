"""ファミコン（NES）の音源 APU を手本にした基本波形の生成.

矩形波（パルス波）、三角波、ノイズの 3 種類を作る。
実機の完全な再現ではなく、音色を決める本質的な特徴だけを取り入れている。
"""

from pathlib import Path

import numpy as np
import numpy.typing as npt

from wav_io import SAMPLE_RATE, Signal, normalize, seconds_to_samples, write_wav

# NTSC 版ファミコンの CPU クロック周波数 [Hz]
CPU_CLOCK = 1_789_773.0

# 三角波チャンネルが 1 周期の間に出力する 32 段階の値（4 bit: 0 から 15）
TRIANGLE_SEQUENCE = np.array(list(range(15, -1, -1)) + list(range(16)), dtype=np.float64)

# ノイズチャンネルのタイマー周期（CPU クロック数）。インデックス 0 が最も高い音
NOISE_PERIODS = (4, 8, 16, 32, 64, 96, 128, 160, 202, 254, 380, 508, 762, 1016, 2034, 4068)

NOTE_OFFSETS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def note_number(name: str) -> int:
    """音名（例: "A4"、"C#5"、"Bb3"）を MIDI ノート番号に変換する.

    C4（中央のド）が 60、A4 が 69 になる。
    """
    letter = name[0].upper()
    rest = name[1:]
    accidental = 0
    while rest and rest[0] in "#b":
        accidental += 1 if rest[0] == "#" else -1
        rest = rest[1:]
    octave = int(rest)
    return 12 * (octave + 1) + NOTE_OFFSETS[letter] + accidental


def note_frequency(note: int) -> float:
    """MIDI ノート番号を周波数 [Hz] に変換する（12 平均律、A4 = 440 Hz）."""
    return float(440.0 * 2.0 ** ((note - 69) / 12.0))


def pulse_timer_frequency(frequency: float) -> float:
    """矩形波チャンネルが実際に出せる周波数のうち、最も近いものを返す.

    実機は 11 bit のタイマー値 t を使い、f = CPU_CLOCK / (16 * (t + 1)) の
    周波数しか出せない。t が 8 未満の場合は消音されるため、範囲を制限している。
    """
    timer = int(round(CPU_CLOCK / (16.0 * frequency) - 1.0))
    timer = min(max(timer, 8), 2047)
    return CPU_CLOCK / (16.0 * (timer + 1))


def phase_from_frequency(frequency: float | Signal, num_samples: int) -> Signal:
    """周波数（定数または時間変化する配列）から 0 以上 1 未満の位相を作る.

    位相はサンプルごとに frequency / SAMPLE_RATE ずつ進む。
    周波数を配列で与えれば、音程が滑らかに変化する音を作れる。
    """
    freq = np.broadcast_to(np.asarray(frequency, dtype=np.float64), (num_samples,))
    increments = freq / SAMPLE_RATE
    phase = np.cumsum(increments) - increments  # 最初のサンプルの位相を 0 にする
    return np.mod(phase, 1.0)


def pulse_wave(phase: Signal, duty: float | Signal = 0.5) -> Signal:
    """矩形波（パルス波）を作る. duty は 1 周期のうち高い値になっている割合.

    実機と同じく 1 と 0 の 2 値を作り、平均値 duty を引いて直流成分を取り除く。
    """
    return np.where(phase < duty, 1.0, 0.0) - duty


def triangle_wave(phase: Signal) -> Signal:
    """4 bit（16 段階）の階段状の三角波を作る."""
    step = np.floor(phase * 32.0).astype(np.int64)
    return TRIANGLE_SEQUENCE[step] / 7.5 - 1.0


def sine_wave(phase: Signal) -> Signal:
    """比較用の正弦波を作る."""
    return np.sin(2.0 * np.pi * phase)


def lfsr_sequence(short_mode: bool = False) -> npt.NDArray[np.int64]:
    """15 bit の線形帰還シフトレジスタ（LFSR）が出力するビット列を 1 周期分返す.

    通常モードでは bit 0 と bit 1、短周期モードでは bit 0 と bit 6 の
    排他的論理和を最上位（bit 14）に戻しながら右シフトする。
    """
    tap = 6 if short_mode else 1
    register = 1
    initial = register
    bits: list[int] = []
    while True:
        bits.append(register & 1)
        feedback = (register & 1) ^ ((register >> tap) & 1)
        register = (register >> 1) | (feedback << 14)
        if register == initial:
            break
    return np.array(bits, dtype=np.int64)


def noise_from_rate(clock_rate: float | Signal, num_samples: int, short_mode: bool = False) -> Signal:
    """LFSR を毎秒 clock_rate 回進めたときのノイズを作る.

    bit 0 が 0 のとき +1、1 のとき -1 を出力する。
    """
    rate = np.broadcast_to(np.asarray(clock_rate, dtype=np.float64), (num_samples,))
    sequence = lfsr_sequence(short_mode)
    position = np.floor(np.cumsum(rate / SAMPLE_RATE) - rate / SAMPLE_RATE).astype(np.int64)
    bits = sequence[position % sequence.size]
    return np.where(bits == 0, 1.0, -1.0)


def noise_wave(seconds: float, period_index: int, short_mode: bool = False) -> Signal:
    """ノイズチャンネルの周期インデックス（0 から 15）を指定してノイズを作る."""
    clock_rate = CPU_CLOCK / NOISE_PERIODS[period_index]
    return noise_from_rate(clock_rate, seconds_to_samples(seconds), short_mode)


def fade_edges(signal: Signal, seconds: float = 0.005) -> Signal:
    """音の始まりと終わりを短く滑らかにし、プチッというクリック音を防ぐ."""
    length = min(seconds_to_samples(seconds), signal.size // 2)
    if length == 0:
        return signal
    ramp = np.linspace(0.0, 1.0, length)
    result = signal.copy()
    result[:length] *= ramp
    result[-length:] *= ramp[::-1]
    return result


def tone(frequency: float, seconds: float, wave: str = "pulse", duty: float = 0.5) -> Signal:
    """一定の音程の音を作る. wave には "pulse"、"triangle"、"sine" を指定する."""
    phase = phase_from_frequency(frequency, seconds_to_samples(seconds))
    if wave == "pulse":
        return pulse_wave(phase, duty)
    if wave == "triangle":
        return triangle_wave(phase)
    if wave == "sine":
        return sine_wave(phase)
    raise ValueError(f"unknown wave: {wave}")


def generate(out_dir: Path) -> list[Path]:
    """本文で使う波形のサンプル音を書き出す."""
    a4 = note_frequency(note_number("A4"))
    sounds: dict[str, Signal] = {
        "sine_a4": tone(a4, 1.0, "sine"),
        "pulse_12_5_a4": tone(a4, 1.0, "pulse", 0.125),
        "pulse_25_a4": tone(a4, 1.0, "pulse", 0.25),
        "pulse_50_a4": tone(a4, 1.0, "pulse", 0.5),
        "triangle_a4": tone(a4, 1.0, "triangle"),
        "noise_long": noise_wave(1.0, 8),
        "noise_short": noise_wave(1.0, 8, short_mode=True),
    }
    # ノイズの周期インデックスを 0 から 15 まで順に変えて鳴らす
    sweep = [noise_wave(0.25, index) for index in range(len(NOISE_PERIODS))]
    sounds["noise_periods"] = np.concatenate([fade_edges(part) for part in sweep])

    paths: list[Path] = []
    for name, signal in sounds.items():
        path = out_dir / f"{name}.wav"
        write_wav(path, normalize(fade_edges(signal), peak=0.4))
        paths.append(path)
    return paths


if __name__ == "__main__":
    for written in generate(Path("output")):
        print(written)
