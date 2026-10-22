"""テキストで書いた楽譜から複数チャンネルの曲を合成する簡易シーケンサ.

楽譜はトラッカーと同じく「1 ステップ = 1 行」の考え方で書く。
空白で区切った 1 つのトークンが 1 ステップ（既定では 16 分音符）に対応する。

* 音名（例: C4、F#3、Bb4）: その音を鳴らし始める
* ``-``: 直前の音を伸ばす
* ``.``: 休符（音を止める）
* ノイズチャンネルでは、DRUMS に登録した 1 文字（K、S、H）で打楽器を鳴らす
* ``|`` は小節の区切りで、読みやすくするためだけに使う（無視される）
"""

from dataclasses import dataclass, field
from typing import Literal

import numpy as np

from envelope import quantize_volume, vibrato
from waveforms import (CPU_CLOCK, NOISE_PERIODS, fade_edges, noise_from_rate, note_frequency, note_number,
                       phase_from_frequency, pulse_wave, triangle_wave)
from wav_io import SAMPLE_RATE, Signal, normalize, seconds_to_samples

WaveType = Literal["pulse", "triangle", "noise"]


@dataclass(frozen=True)
class Instrument:
    """音色の設定."""

    wave: WaveType
    duty: float = 0.5  # 矩形波のデューティ比
    volume: float = 1.0  # 最大音量（0.0 から 1.0）
    attack: float = 0.0  # 音量が最大になるまでの時間 [秒]
    decay: float = 0.0  # 持続音量まで下がる時間 [秒]
    sustain: float = 1.0  # 持続音量（最大音量に対する割合）
    release: float = 0.0  # 音を止めた後の余韻の長さ [秒]
    vibrato_depth: float = 0.0  # ビブラートの幅 [半音]
    vibrato_rate: float = 6.0  # ビブラートの速さ [回/秒]
    vibrato_delay: float = 0.2  # ビブラートがかかり始めるまでの時間 [秒]


@dataclass(frozen=True)
class Drum:
    """ノイズチャンネルで鳴らす打楽器の設定."""

    period_index: int  # ノイズの周期インデックス（0 から 15）
    length: float  # 鳴っている長さ [秒]
    volume: float = 1.0
    short_mode: bool = False


DRUMS: dict[str, Drum] = {
    "K": Drum(period_index=12, length=0.10),  # キック（バスドラム）
    "S": Drum(period_index=6, length=0.15, volume=0.8),  # スネア
    "H": Drum(period_index=0, length=0.04, volume=0.4),  # ハイハット
}


@dataclass
class Track:
    """1 チャンネル分の楽譜と音色."""

    name: str
    instrument: Instrument
    score: str
    gain: float = 1.0  # ミキシング時の音量


@dataclass
class Song:
    """曲全体の設定."""

    bpm: float
    tracks: list[Track] = field(default_factory=list)
    steps_per_beat: int = 4  # 1 拍を何ステップに分けるか（4 なら 16 分音符）

    @property
    def step_seconds(self) -> float:
        """1 ステップの長さ [秒]."""
        return 60.0 / self.bpm / self.steps_per_beat


@dataclass(frozen=True)
class Event:
    """楽譜から取り出した 1 つの音."""

    start: int  # 開始ステップ
    length: int  # 鳴らすステップ数
    value: str  # 音名または打楽器の文字


def tokenize(score: str) -> list[str]:
    """楽譜の文字列をステップごとのトークンに分割する."""
    return [token for token in score.replace("|", " ").split() if token]


def parse(score: str) -> tuple[list[Event], int]:
    """楽譜からイベントの一覧と全体のステップ数を取り出す."""
    tokens = tokenize(score)
    events: list[Event] = []
    current: tuple[int, str] | None = None  # 鳴っている音の (開始ステップ, 値)
    for step, token in enumerate(tokens + ["."]):  # 末尾に休符を足して最後の音を閉じる
        if token == "-":
            if current is None:
                raise ValueError(f"step {step}: '-' には伸ばす音が必要である")
            continue
        if current is not None:
            events.append(Event(current[0], step - current[0], current[1]))
            current = None
        if token != ".":
            current = (step, token)
    return events, len(tokens)


def envelope_for(instrument: Instrument, gate: float) -> Signal:
    """gate 秒だけ鍵盤を押したときの音量変化（リリース込み）を作る."""
    times = [0.0, instrument.attack, instrument.attack + instrument.decay]
    levels = [0.0 if instrument.attack > 0.0 else 1.0, 1.0, instrument.sustain]
    t = np.arange(seconds_to_samples(gate + instrument.release)) / SAMPLE_RATE
    held = np.interp(np.minimum(t, gate), times, levels)
    if instrument.release > 0.0:
        fade = np.clip(1.0 - (t - gate) / instrument.release, 0.0, 1.0)
        held = held * np.where(t > gate, fade, 1.0)
    return held


def render_note(instrument: Instrument, note: str, gate: float) -> Signal:
    """音名 note を gate 秒鳴らした音を作る."""
    envelope = envelope_for(instrument, gate)
    frequency = note_frequency(note_number(note))
    if instrument.vibrato_depth > 0.0:
        seconds = envelope.size / SAMPLE_RATE
        freq: float | Signal = vibrato(frequency, seconds, instrument.vibrato_depth,
                                       instrument.vibrato_rate, instrument.vibrato_delay)
    else:
        freq = frequency
    phase = phase_from_frequency(freq, envelope.size)
    if instrument.wave == "pulse":
        # 矩形波は音量が 16 段階なので、エンベロープを丸める
        return pulse_wave(phase, instrument.duty) * quantize_volume(envelope) * instrument.volume
    if instrument.wave == "triangle":
        # 三角波は音量を変えられないため、エンベロープは使わず鳴らすか止めるかだけにする。
        # ただし、音の切れ目でクリック音が出ないように、両端に 3 ミリ秒のフェードを入れる
        return fade_edges(triangle_wave(phase), 0.003) * instrument.volume
    raise ValueError(f"音名を鳴らせない波形である: {instrument.wave}")


def render_drum(drum: Drum) -> Signal:
    """打楽器 1 打分の音を作る."""
    num_samples = seconds_to_samples(drum.length)
    rate = CPU_CLOCK / NOISE_PERIODS[drum.period_index]
    t = np.arange(num_samples) / SAMPLE_RATE
    volume = quantize_volume(np.clip(1.0 - t / drum.length, 0.0, 1.0))
    return noise_from_rate(rate, num_samples, drum.short_mode) * volume * drum.volume


def render_track(track: Track, step_seconds: float, loop: bool) -> Signal:
    """1 チャンネル分を合成する.

    1 つのチャンネルは同時に 1 音しか出せないため、次の音が始まったら前の音の余韻は切る。
    loop が True のときは、曲の終わりからはみ出した余韻を曲の先頭に重ねる。
    """
    events, total_steps = parse(track.score)
    total = seconds_to_samples(total_steps * step_seconds)
    buffer = np.zeros(total * 2)  # はみ出した余韻を受け止めるため長めに確保する
    starts = [event.start for event in events]
    for i, event in enumerate(events):
        gate = event.length * step_seconds
        if track.instrument.wave == "noise":
            sound = render_drum(DRUMS[event.value])
        else:
            sound = render_note(track.instrument, event.value, gate)
        begin = seconds_to_samples(event.start * step_seconds)
        if i + 1 < len(starts):
            # 次の音の開始位置で打ち切る
            limit = seconds_to_samples(starts[i + 1] * step_seconds) - begin
        elif loop and starts:
            # 最後の音は、次の周回の最初の音の開始位置で打ち切る
            limit = total + seconds_to_samples(starts[0] * step_seconds) - begin
        else:
            limit = sound.size
        sound = sound[:limit]
        buffer[begin:begin + sound.size] += sound
    if loop:
        result: Signal = buffer[:total].copy()
        result += buffer[total:total * 2]  # 余韻を先頭へ折り返す
        return result
    used = int(np.max(np.nonzero(buffer)[0])) + 1 if np.any(buffer) else total
    return buffer[:max(total, used)]


def render_song(song: Song, loop: bool = True) -> Signal:
    """全チャンネルを合成してミキシングする."""
    tracks = [render_track(track, song.step_seconds, loop) * track.gain for track in song.tracks]
    length = max(track.size for track in tracks)
    mixed = np.zeros(length)
    for track in tracks:
        mixed[:track.size] += track
    return normalize(mixed, peak=0.8)
