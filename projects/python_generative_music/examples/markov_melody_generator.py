"""マルコフ連鎖を用いて旋律を生成し、MIDI ファイルへ出力するサンプル。"""

from __future__ import annotations

import random
from pathlib import Path

import pretty_midi

TransitionTable = dict[int, list[int]]

TRANSITION_TABLE: TransitionTable = {
    60: [62, 64],
    62: [60, 64, 65],
    64: [62, 65, 67],
    65: [64, 67],
    67: [65, 69, 72],
    69: [67, 72],
    72: [69, 67],
}

NOTE_DURATION = 0.4
OUTPUT_PATH = Path(__file__).with_name("markov_melody.mid")


def generate_melody(
    transition_table: TransitionTable,
    start_note: int,
    note_count: int,
) -> list[int]:
    """遷移確率表に従って、次に続く音をランダムに選びながら旋律を生成する。"""
    current_note = start_note
    melody = [current_note]
    for _ in range(note_count - 1):
        current_note = random.choice(transition_table[current_note])
        melody.append(current_note)
    return melody


def melody_to_midi(melody: list[int], output_path: Path) -> None:
    """旋律のリストを MIDI ファイルへ書き出す。"""
    midi_data = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)

    start_time = 0.0
    for pitch in melody:
        note = pretty_midi.Note(
            velocity=100,
            pitch=pitch,
            start=start_time,
            end=start_time + NOTE_DURATION,
        )
        instrument.notes.append(note)
        start_time += NOTE_DURATION

    midi_data.instruments.append(instrument)
    midi_data.write(str(output_path))


def main() -> None:
    melody = generate_melody(TRANSITION_TABLE, start_note=60, note_count=32)
    melody_to_midi(melody, OUTPUT_PATH)
    print(f"{OUTPUT_PATH.name} を出力しました。")


if __name__ == "__main__":
    main()
