"""本文で使う図をすべて生成する。conf.py からビルド時に呼び出される。

単体でも実行できる::

    python make_figures.py
"""

import sys
import zipfile
from pathlib import Path

FIGURES_DIR = Path(__file__).resolve().parent
SOURCE_DIR = FIGURES_DIR.parent
EXAMPLES_DIR = SOURCE_DIR.parent / "examples"
OUTPUT_DIR = SOURCE_DIR / "_generated"

# 図の生成にはサンプルコード（examples）の関数も使う
for path in (FIGURES_DIR, EXAMPLES_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import fig_animation  # noqa: E402
import fig_basics  # noqa: E402
import fig_character  # noqa: E402
import fig_color  # noqa: E402
import fig_lines  # noqa: E402
import fig_tiles  # noqa: E402


def make_examples_zip(out_dir: Path) -> None:
    """examples フォルダの配布用ファイルを zip にまとめる。"""
    with zipfile.ZipFile(out_dir / "examples.zip", "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(EXAMPLES_DIR.iterdir()):
            if path.is_file() and path.suffix in (".py", ".cfg"):
                archive.write(path, f"examples/{path.name}")


def generate_all(out_dir: Path = OUTPUT_DIR) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for module in (fig_basics, fig_lines, fig_color, fig_character, fig_tiles, fig_animation):
        module.generate(out_dir)
    make_examples_zip(out_dir)


if __name__ == "__main__":
    generate_all()
    print(f"図を {OUTPUT_DIR} に出力した")
