"""ゲームでよく使う効果音の作例.

どの効果音も「波形」「音程の変化」「音量の変化」の 3 つの組み合わせで作っている。
"""

from pathlib import Path

import numpy as np

from envelope import arpeggio, exponential_sweep, nes_decay, quantize_volume, vibrato
from waveforms import (CPU_CLOCK, NOISE_PERIODS, fade_edges, noise_from_rate, noise_wave, note_frequency,
                       note_number, phase_from_frequency, pulse_wave, triangle_wave)
from wav_io import SAMPLE_RATE, Signal, normalize, seconds_to_samples, write_wav


def jump() -> Signal:
    """ジャンプ: 音程が素早く上がる矩形波."""
    freq = exponential_sweep(180.0, 700.0, 0.18)
    volume = nes_decay(0.18, 2)
    return pulse_wave(phase_from_frequency(freq, freq.size), 0.25) * volume


def coin() -> Signal:
    """アイテム取得: 短い音の直後に 5 度上の音を伸ばす."""
    first = pulse_wave(phase_from_frequency(note_frequency(note_number("A5")), seconds_to_samples(0.07)), 0.5)
    second_length = 0.4
    second = pulse_wave(phase_from_frequency(note_frequency(note_number("E6")), seconds_to_samples(second_length)), 0.5)
    return np.concatenate([first, second * nes_decay(second_length, 3)])


def select() -> Signal:
    """決定: 細いパルス波で上昇する 2 音."""
    parts = [
        pulse_wave(phase_from_frequency(note_frequency(note_number(name)), seconds_to_samples(length)), 0.125)
        * nes_decay(length, 1)
        for name, length in (("C6", 0.05), ("G6", 0.1))
    ]
    return np.concatenate(parts)


def cancel() -> Signal:
    """キャンセル: 下降する 2 音. 決定と対になるよう音程の動きを逆にしている."""
    parts = [
        pulse_wave(phase_from_frequency(note_frequency(note_number(name)), seconds_to_samples(length)), 0.5)
        * nes_decay(length, 1)
        for name, length in (("G5", 0.05), ("C5", 0.1))
    ]
    return np.concatenate(parts)


def damage() -> Signal:
    """被ダメージ: 急降下する矩形波に短いノイズを重ねる."""
    seconds = 0.3
    freq = exponential_sweep(900.0, 80.0, seconds)
    tone = pulse_wave(phase_from_frequency(freq, freq.size), 0.5) * nes_decay(seconds, 3)
    noise = noise_wave(seconds, 5) * nes_decay(seconds, 0)
    return 0.7 * tone + 0.5 * noise


def explosion() -> Signal:
    """爆発: ノイズの周期を徐々に長く（音を低く）しながら、ゆっくり減衰させる."""
    seconds = 1.0
    num_samples = seconds_to_samples(seconds)
    # 周期インデックスを 6 から 15 へ時間とともに大きくする
    t = np.arange(num_samples) / SAMPLE_RATE
    index = np.minimum(6 + np.floor(t / 0.08), 15).astype(np.int64)
    rate = CPU_CLOCK / np.array(NOISE_PERIODS, dtype=np.float64)[index]
    volume = quantize_volume(np.exp(-3.5 * t))
    return noise_from_rate(rate, num_samples) * volume


def laser() -> Signal:
    """レーザー: 細いパルス波で高い音から一気に下げる."""
    seconds = 0.25
    freq = exponential_sweep(2400.0, 300.0, seconds)
    return pulse_wave(phase_from_frequency(freq, freq.size), 0.125) * nes_decay(seconds, 3)


def power_up() -> Signal:
    """パワーアップ: 長三和音のアルペジオで音程を段階的に上げていく."""
    seconds = 0.8
    parts = []
    for root in ("C5", "D5", "E5", "F5"):
        freq = arpeggio(note_number(root), [0, 4, 7, 12], seconds / 4, step=1.0 / 60.0)
        parts.append(pulse_wave(phase_from_frequency(freq, freq.size), 0.5))
    body = np.concatenate(parts)
    return body * quantize_volume(np.linspace(1.0, 0.3, body.size))


def heal() -> Signal:
    """回復: ビブラートをかけた三角波でやわらかく上昇させる."""
    parts = []
    for name in ("C5", "E5", "G5", "C6"):
        freq = vibrato(note_frequency(note_number(name)), 0.15, depth=0.2, rate=12.0)
        parts.append(triangle_wave(phase_from_frequency(freq, freq.size)))
    return np.concatenate(parts)


def random_effect(rng: np.random.Generator) -> Signal:
    """パラメータを乱数で決めて効果音を作る（sfxr と同じ考え方）."""
    seconds = float(rng.uniform(0.1, 0.5))
    start = float(rng.uniform(150.0, 2000.0))
    end = start * float(2.0 ** rng.uniform(-3.0, 2.0))
    duty = float(rng.choice([0.125, 0.25, 0.5]))
    decay_period = int(rng.integers(1, 6))
    freq = exponential_sweep(start, end, seconds)
    return pulse_wave(phase_from_frequency(freq, freq.size), duty) * nes_decay(seconds, decay_period)


def generate(out_dir: Path) -> list[Path]:
    """すべての効果音を書き出す."""
    sounds: dict[str, Signal] = {
        "se_jump": jump(),
        "se_coin": coin(),
        "se_select": select(),
        "se_cancel": cancel(),
        "se_damage": damage(),
        "se_explosion": explosion(),
        "se_laser": laser(),
        "se_power_up": power_up(),
        "se_heal": heal(),
    }
    rng = np.random.default_rng(seed=8)
    for n in range(1, 4):
        sounds[f"se_random_{n}"] = random_effect(rng)

    paths: list[Path] = []
    for name, signal in sounds.items():
        path = out_dir / f"{name}.wav"
        write_wav(path, normalize(fade_edges(signal), peak=0.5))
        paths.append(path)
    return paths


if __name__ == "__main__":
    for written in generate(Path("output")):
        print(written)
