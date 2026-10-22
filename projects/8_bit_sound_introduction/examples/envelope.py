"""音量や音程の時間変化（エンベロープ、スイープ、ビブラート、アルペジオ）.

どの関数も「1 サンプルごとの値を並べた配列」を返す。
音量の配列は波形に掛け算し、周波数の配列は phase_from_frequency に渡して使う。
"""

from pathlib import Path

import numpy as np

from waveforms import fade_edges, note_frequency, note_number, phase_from_frequency, pulse_wave, triangle_wave
from wav_io import SAMPLE_RATE, Signal, normalize, seconds_to_samples, write_wav

# ファミコンのサウンドドライバが音量や音程を書き換える間隔（1 フレーム）[秒]
FRAME = 1.0 / 60.0


def adsr(attack: float, decay: float, sustain: float, hold: float, release: float) -> Signal:
    """ADSR エンベロープを作る.

    attack 秒で 0 から 1 へ上がり、decay 秒で sustain の音量まで下がる。
    その音量を hold 秒保った後、release 秒で 0 に戻る。
    """
    times = np.cumsum([0.0, attack, decay, hold, release])
    levels = [0.0, 1.0, sustain, sustain, 0.0]
    t = np.arange(seconds_to_samples(float(times[-1]))) / SAMPLE_RATE
    return np.interp(t, times, levels)


def nes_decay(seconds: float, period: int) -> Signal:
    """ファミコンの矩形波・ノイズが持つ減衰エンベロープを再現する.

    音量は 15 から始まり、毎秒 240 回のクロックが (period + 1) 回来るたびに
    1 ずつ下がって 0 で止まる。period は 0 から 15 の整数である。
    """
    t = np.arange(seconds_to_samples(seconds)) / SAMPLE_RATE
    level = 15.0 - np.floor(t * 240.0 / (period + 1))
    return np.maximum(level, 0.0) / 15.0


def quantize_volume(envelope: Signal, levels: int = 16) -> Signal:
    """音量を 4 bit（16 段階）のような粗い段階に丸める."""
    return np.round(envelope * (levels - 1)) / (levels - 1)


def exponential_sweep(start: float, end: float, seconds: float) -> Signal:
    """周波数を start から end へ指数関数的に（音程として均等に）変化させる."""
    return np.geomspace(start, end, seconds_to_samples(seconds))


def vibrato(frequency: float, seconds: float, depth: float, rate: float, delay: float = 0.0) -> Signal:
    """ビブラート（音程の周期的な揺れ）をかけた周波数を返す.

    depth は揺れの幅 [半音]、rate は 1 秒あたりの揺れの回数である。
    delay 秒が経過するまでは揺らさない。
    """
    t = np.arange(seconds_to_samples(seconds)) / SAMPLE_RATE
    swing = depth * np.sin(2.0 * np.pi * rate * np.maximum(t - delay, 0.0))
    return frequency * 2.0 ** (swing / 12.0)


def arpeggio(root: int, offsets: list[int], seconds: float, step: float = FRAME) -> Signal:
    """root（MIDI ノート番号）から offsets 半音ずつ離れた音を step 秒ごとに切り替える.

    1 チャンネルで和音のように聞かせる「アルペジオ」の手法である。
    """
    t = np.arange(seconds_to_samples(seconds)) / SAMPLE_RATE
    index = np.floor(t / step).astype(np.int64) % len(offsets)
    notes = root + np.array(offsets)[index]
    return 440.0 * 2.0 ** ((notes - 69) / 12.0)


def pseudo_echo(signal: Signal, delay: float, gain: float, repeats: int = 2) -> Signal:
    """遅らせて小さくした同じ音を重ね、エコーのように聞かせる."""
    offset = seconds_to_samples(delay)
    result = np.concatenate([signal, np.zeros(offset * repeats)])
    for n in range(1, repeats + 1):
        result[offset * n:offset * n + signal.size] += signal * gain ** n
    return result


def generate(out_dir: Path) -> list[Path]:
    """本文で使う音の加工のサンプル音を書き出す."""
    c5 = note_frequency(note_number("C5"))
    sounds: dict[str, Signal] = {}

    # 音量エンベロープのない音と、ADSR をかけた音
    env = adsr(0.01, 0.15, 0.5, 0.4, 0.3)
    sounds["no_envelope"] = pulse_wave(phase_from_frequency(c5, env.size))
    sounds["adsr"] = sounds["no_envelope"] * env

    # 16 段階で減衰するファミコン風の音（減衰の速さを 2 通り）
    for period in (2, 8):
        decay = nes_decay(1.0, period)
        sounds[f"nes_decay_{period}"] = pulse_wave(phase_from_frequency(c5, decay.size), 0.25) * decay

    # ピッチスイープ（上昇と下降）
    up = exponential_sweep(200.0, 1600.0, 0.4)
    sounds["sweep_up"] = pulse_wave(phase_from_frequency(up, up.size)) * nes_decay(0.4, 4)
    down = exponential_sweep(1600.0, 200.0, 0.4)
    sounds["sweep_down"] = pulse_wave(phase_from_frequency(down, down.size)) * nes_decay(0.4, 4)

    # ビブラート
    wobble = vibrato(c5, 1.5, depth=0.3, rate=6.0, delay=0.3)
    sounds["vibrato"] = pulse_wave(phase_from_frequency(wobble, wobble.size), 0.5)

    # アルペジオ（長三和音と短三和音）
    for name, offsets in (("major", [0, 4, 7]), ("minor", [0, 3, 7])):
        freq = arpeggio(note_number("C5"), offsets, 1.0)
        sounds[f"arpeggio_{name}"] = pulse_wave(phase_from_frequency(freq, freq.size), 0.5)

    # 1 フレームごとにデューティ比を切り替える
    seconds = 1.0
    num_samples = seconds_to_samples(seconds)
    frame_index = np.floor(np.arange(num_samples) / SAMPLE_RATE / FRAME).astype(np.int64)
    duty = np.array([0.125, 0.25, 0.5, 0.25])[frame_index % 4]
    sounds["duty_switch"] = pulse_wave(phase_from_frequency(c5, num_samples), duty)

    # 疑似エコー
    phrase = np.concatenate([
        pulse_wave(phase_from_frequency(note_frequency(note_number(name)), seconds_to_samples(0.15)), 0.5)
        * nes_decay(0.15, 1)
        for name in ("C5", "E5", "G5", "C6")
    ])
    sounds["echo_off"] = np.concatenate([phrase, np.zeros(seconds_to_samples(0.4))])
    sounds["echo_on"] = pseudo_echo(phrase, delay=0.2, gain=0.4)

    # 三角波は音量を変えられないため、音を短く切って休符を挟むことで区切りを表す
    notes = []
    for name in ("A2", "A3", "F2", "F3", "G2", "G3", "E2", "E3"):
        tone = triangle_wave(phase_from_frequency(note_frequency(note_number(name)), seconds_to_samples(0.18)))
        notes.append(fade_edges(tone, 0.003))  # 音の切れ目でクリック音が出ないようにする
        notes.append(np.zeros(seconds_to_samples(0.07)))
    sounds["triangle_bass"] = np.concatenate(notes)

    paths: list[Path] = []
    for name, signal in sounds.items():
        path = out_dir / f"{name}.wav"
        write_wav(path, normalize(fade_edges(signal), peak=0.4))
        paths.append(path)
    return paths


if __name__ == "__main__":
    for written in generate(Path("output")):
        print(written)
