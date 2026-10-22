"""4 チャンネル構成のループ BGM の作例.

イ短調（A マイナー）、コード進行は Am - F - G - C - Am - F - G - E の 8 小節である。
1 小節は 16 ステップ（16 分音符 16 個）で、各チャンネルの楽譜は 1 小節ずつ並べている。
"""

from pathlib import Path

import numpy as np

from sequencer import Instrument, Song, Track, render_song
from wav_io import write_wav

MELODY = " | ".join([
    "A4 - - - C5 - E5 - D5 - C5 - B4 - C5 -",  # Am
    "A4 - - - - - F4 - A4 - C5 - F5 - E5 -",  # F
    "D5 - - - B4 - G4 - B4 - D5 - G5 - F5 -",  # G
    "E5 - - - - - - - C5 - D5 - E5 - G5 -",  # C
    "A5 - - - G5 - E5 - . . E5 - G5 - A5 -",  # Am
    "F5 - - - E5 - C5 - . . A4 - C5 - F5 -",  # F
    "G5 - - - F5 - D5 - B4 - D5 - F5 - E5 -",  # G
    "E5 - - - - - - - G#4 - - - B4 - - -",  # E
])

HARMONY = " | ".join([
    "A3 - C4 - E4 - C4 - A3 - C4 - E4 - C4 -",  # Am
    "A3 - C4 - F4 - C4 - A3 - C4 - F4 - C4 -",  # F
    "B3 - D4 - G4 - D4 - B3 - D4 - G4 - D4 -",  # G
    "C4 - E4 - G4 - E4 - C4 - E4 - G4 - E4 -",  # C
    "A3 - C4 - E4 - C4 - A3 - C4 - E4 - C4 -",  # Am
    "A3 - C4 - F4 - C4 - A3 - C4 - F4 - C4 -",  # F
    "B3 - D4 - G4 - D4 - B3 - D4 - G4 - D4 -",  # G
    "B3 - E4 - G#4 - E4 - B3 - E4 - G#4 - E4 -",  # E
])

BASS = " | ".join([
    "A2 - A3 - A2 - A3 - A2 - A3 - A2 - A3 -",  # Am
    "F2 - F3 - F2 - F3 - F2 - F3 - F2 - F3 -",  # F
    "G2 - G3 - G2 - G3 - G2 - G3 - G2 - G3 -",  # G
    "C3 - C4 - C3 - C4 - C3 - C4 - C3 - C4 -",  # C
    "A2 - A3 - A2 - A3 - A2 - A3 - A2 - A3 -",  # Am
    "F2 - F3 - F2 - F3 - F2 - F3 - F2 - F3 -",  # F
    "G2 - G3 - G2 - G3 - G2 - G3 - G2 - G3 -",  # G
    "E2 - E3 - E2 - E3 - E2 - E3 - E2 - E3 -",  # E
])

DRUM_BAR = "K . H . S . H . K . K . S . H H"
DRUM_FILL = "K . H . S . H . S . S . S S S S"
DRUMS = " | ".join([DRUM_BAR] * 7 + [DRUM_FILL])


def build_song() -> Song:
    """曲データを組み立てる."""
    lead = Instrument("pulse", duty=0.5, decay=0.3, sustain=0.6, release=0.05,
                      vibrato_depth=0.15, vibrato_rate=6.0, vibrato_delay=0.25)
    chord = Instrument("pulse", duty=0.25, decay=0.12, sustain=0.2, release=0.02)
    bass = Instrument("triangle")
    noise = Instrument("noise")
    return Song(bpm=140.0, tracks=[
        Track("pulse1", lead, MELODY, gain=0.9),
        Track("pulse2", chord, HARMONY, gain=0.5),
        Track("triangle", bass, BASS, gain=0.5),
        Track("noise", noise, DRUMS, gain=0.4),
    ])


def generate(out_dir: Path) -> list[Path]:
    """ループ 1 回分と、ループのつなぎ目を確認するための 2 回分を書き出す."""
    song = build_song()
    loop = render_song(song, loop=True)
    loop_path = out_dir / "bgm_loop.wav"
    preview_path = out_dir / "bgm_loop_twice.wav"
    write_wav(loop_path, loop)
    write_wav(preview_path, np.tile(loop, 2))

    # 楽器ごとの音を確認するため、各チャンネルを単独で書き出す
    paths = [loop_path, preview_path]
    for track in song.tracks:
        solo = Song(bpm=song.bpm, tracks=[Track(track.name, track.instrument, track.score)])
        path = out_dir / f"bgm_solo_{track.name}.wav"
        write_wav(path, render_song(solo, loop=True) * 0.6)
        paths.append(path)
    return paths


if __name__ == "__main__":
    for written in generate(Path("output")):
        print(written)
