"""本書で使うすべてのサンプル音を一括で生成する.

使い方: python make_all.py [出力フォルダ]（省略時は output）

本書の HTML をビルドするときは、Sphinx の conf.py から generate_all() が呼び出される。
"""

import sys
from pathlib import Path

import bgm_example
import envelope
import pyxel_sound
import sound_effects
import waveforms


def generate_all(out_dir: Path) -> list[Path]:
    """すべてのサンプル音を out_dir に書き出し、書き出したファイルの一覧を返す."""
    paths: list[Path] = []
    for module in (waveforms, envelope, sound_effects, bgm_example, pyxel_sound):
        paths.extend(module.generate(out_dir))
    return paths


def main() -> None:
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "output"
    paths = generate_all(out_dir)
    for path in paths:
        print(path)
    print(f"{len(paths)} files written to {out_dir}")


if __name__ == "__main__":
    main()
