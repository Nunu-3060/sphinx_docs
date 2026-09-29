"""乱数を用いてランダムなメロディを生成し、MIDI ファイルへ出力するサンプル。"""

from __future__ import annotations

import random
from pathlib import Path

import pretty_midi

SCALE = [60, 62, 64, 65, 67, 69, 71, 72]
DURATIONS = [0.5, 0.25]
OUTPUT_PATH = Path(__file__).with_name("random_melody.mid")


def generate_melody(note_count: int) -> list[tuple[int, float]]:
    """音階とリズムの候補からランダムに選んで旋律を生成する。"""
    melody: list[tuple[int, float]] = []
    for _ in range(note_count):
        pitch = random.choice(SCALE)
        duration = random.choice(DURATIONS)
        melody.append((pitch, duration))
    return melody


def melody_to_midi(melody: list[tuple[int, float]], output_path: Path) -> None:
    """旋律のリストを MIDI ファイルへ書き出す。"""
    midi_data = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)

    start_time = 0.0
    for pitch, duration in melody:
        note = pretty_midi.Note(
            velocity=100,
            pitch=pitch,
            start=start_time,
            end=start_time + duration,
        )
        instrument.notes.append(note)
        start_time += duration

    midi_data.instruments.append(instrument)
    midi_data.write(str(output_path))


def main() -> None:
    melody = generate_melody(note_count=32)
    melody_to_midi(melody, OUTPUT_PATH)
    print(f"{OUTPUT_PATH.name} を出力しました。")


if __name__ == "__main__":
    main()
