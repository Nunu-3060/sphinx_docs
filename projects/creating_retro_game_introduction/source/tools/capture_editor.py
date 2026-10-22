"""Pyxel Editor の画面を PNG で保存する。

Pyxel Editor も Pyxel で作られたアプリケーションなので、pyxel.init() をヘッドレスモードに、
pyxel.run() を「数フレーム進めて画面を保存する関数」に差し替えて起動する。
Pyxel は 1 つのプロセスで 1 回しか初期化できないため、エディタごとにプロセスを分けて実行する。

使い方:
    python capture_editor.py RESOURCE_FILE OUTPUT_DIR
"""

import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

EDITORS = ["image", "tilemap", "sound", "music"]


def capture(resource: str, out_file: str, editor: str) -> None:
    import pyxel
    import pyxel.cli

    original_init = pyxel.init

    def fake_init(*args: Any, **kwargs: Any) -> None:
        kwargs["headless"] = True
        original_init(*args, **kwargs)

    def fake_run(update: Callable[[], None], draw: Callable[[], None]) -> None:
        for _ in range(5):
            update()
            draw()
            pyxel.flip()
        pyxel.screen.save(out_file, 2)

    pyxel.init = fake_init
    pyxel.run = fake_run
    pyxel.cli.edit_pyxel_resource(resource, editor)


def main() -> None:
    if len(sys.argv) == 5 and sys.argv[1] == "--one":
        capture(sys.argv[2], sys.argv[3], sys.argv[4])
        return
    resource = str(Path(sys.argv[1]).resolve())
    out_dir = Path(sys.argv[2]).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    for editor in EDITORS:
        out_file = str(out_dir / f"editor_{editor}")
        subprocess.run([sys.executable, __file__, "--one", resource, out_file, editor], check=True)
        print(f"saved: {out_file}.png")


if __name__ == "__main__":
    main()
