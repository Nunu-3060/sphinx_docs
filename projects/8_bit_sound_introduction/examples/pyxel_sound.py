"""Pyxel の音源機能でジングル（短いフレーズ）を作る.

Pyxel はレトロゲーム向けの Python 製ゲームエンジンで、三角波・矩形波・パルス波・ノイズの
4 種類の波形を持つ 4 チャンネルの音源を内蔵している。

* python pyxel_sound.py: ウィンドウを開き、スペースキーでジングルを鳴らす
* make_all.py から generate() を呼ぶと、ウィンドウを開かずに WAV ファイルに書き出す
"""

import wave
from pathlib import Path

import numpy as np
import pyxel

from wav_io import normalize, write_wav

# Pyxel の音名は C0 から B4 までで、A2 が 440 Hz である（科学的音名表記より 2 オクターブ小さい）
JINGLE_NOTES = "c3 e3 g3 c4 c4 c4 r g3 c4 c4 c4 c4"
JINGLE_TONES = "s"  # t: 三角波、s: 矩形波、p: パルス波、n: ノイズ
JINGLE_VOLUMES = "6"  # 0 から 7 の 8 段階
JINGLE_EFFECTS = "nnnnnnnnnnnf"  # n: なし、s: スライド、v: ビブラート、f: フェードアウト
JINGLE_SPEED = 9  # 1 音の長さ（120 で 1 秒）


def build_jingle() -> pyxel.Sound:
    """ジングルの Sound を作る. 短い文字列は末尾まで繰り返して使われる."""
    sound = pyxel.Sound()
    sound.set(JINGLE_NOTES, JINGLE_TONES, JINGLE_VOLUMES, JINGLE_EFFECTS, JINGLE_SPEED)
    return sound


def generate(out_dir: Path) -> list[Path]:
    """ジングルを WAV ファイルに書き出す.

    Pyxel が書き出す WAV は音量が小さいため、読み込み直して音量を揃える。
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    sound = build_jingle()
    path = out_dir / "pyxel_jingle.wav"
    seconds = sound.total_sec() or 1.0
    sound.save(str(path), seconds + 0.2)
    with wave.open(str(path), "rb") as wav_file:
        sample_rate = wav_file.getframerate()
        frames = wav_file.readframes(wav_file.getnframes())
    signal = np.frombuffer(frames, dtype="<i2").astype(np.float64) / 32768.0
    write_wav(path, normalize(signal, peak=0.5), sample_rate)
    return [path]


class App:
    """スペースキーでジングルを鳴らすだけのアプリケーション."""

    def __init__(self) -> None:
        pyxel.init(160, 120, title="Pyxel Sound")
        self.jingle = build_jingle()
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        if pyxel.btnp(pyxel.KEY_SPACE):
            pyxel.play(0, self.jingle)
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self) -> None:
        pyxel.cls(1)
        pyxel.text(30, 50, "SPACE: PLAY JINGLE", 7)
        pyxel.text(30, 62, "Q: QUIT", 7)


if __name__ == "__main__":
    App()
