"""ユークリッドリズムのアルゴリズムでリズムパターンを生成し、MIDI ファイルへ出力するサンプル。"""

from __future__ import annotations

from pathlib import Path

import pretty_midi

STEP_DURATION = 0.2
BAR_REPEAT_COUNT = 4
KICK_NOTE_NUMBER = 36
OUTPUT_PATH = Path(__file__).with_name("euclidean_rhythm.mid")


def euclidean_rhythm(pulses: int, steps: int) -> list[bool]:
    """Bjorklund のアルゴリズムにより、pulses 個の拍を steps 個のステップへ均等に配置する。"""
    if pulses <= 0:
        return [False] * steps
    if pulses >= steps:
        return [True] * steps

    groups: list[list[bool]] = [[True] for _ in range(pulses)]
    remainders: list[list[bool]] = [[False] for _ in range(steps - pulses)]

    while len(remainders) > 1:
        pair_count = min(len(groups), len(remainders))
        merged = [groups[i] + remainders[i] for i in range(pair_count)]
        leftover_groups = groups[pair_count:]
        leftover_remainders = remainders[pair_count:]
        groups = merged
        remainders = (
            leftover_groups if leftover_groups else leftover_remainders
        )

    result: list[bool] = []
    for group in groups + remainders:
        result.extend(group)
    return result


def pattern_to_midi(
    pattern: list[bool], repeat_count: int, output_path: Path
) -> None:
    """リズムパターンを繰り返しながら、ドラム用の MIDI ファイルへ書き出す。"""
    midi_data = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0, is_drum=True)

    start_time = 0.0
    for _ in range(repeat_count):
        for hit in pattern:
            if hit:
                note = pretty_midi.Note(
                    velocity=100,
                    pitch=KICK_NOTE_NUMBER,
                    start=start_time,
                    end=start_time + STEP_DURATION,
                )
                instrument.notes.append(note)
            start_time += STEP_DURATION

    midi_data.instruments.append(instrument)
    midi_data.write(str(output_path))


def main() -> None:
    pattern = euclidean_rhythm(pulses=5, steps=8)
    pattern_to_midi(pattern, BAR_REPEAT_COUNT, OUTPUT_PATH)
    print(f"{OUTPUT_PATH.name} を出力しました。")


if __name__ == "__main__":
    main()
