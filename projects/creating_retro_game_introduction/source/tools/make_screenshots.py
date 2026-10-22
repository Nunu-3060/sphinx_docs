"""本文で使うゲーム画面のスクリーンショットをまとめて生成する。

capture.py を並列に実行し、source/images/screens/ に PNG を保存する。
ヘッドレスモードでも実時間 (30 fps) で進むため、完了まで数分かかる。

使い方:
    python make_screenshots.py
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "examples"
OUT = ROOT / "source" / "images" / "screens"
CAPTURE = Path(__file__).resolve().parent / "capture.py"

# (スクリプト、出力名、フレーム、追加オプション)
JOBS: list[tuple[str, str, int, list[str]]] = [
    ("ch01_hello/main.py", "ch01_hello", 60, []),
    ("ch03_basics/draw_demo.py", "ch03_draw", 10, []),
    ("ch03_basics/input_demo.py", "ch03_input", 100, []),
    ("ch03_basics/motion_demo.py", "ch03_motion", 150, []),
    ("ch03_basics/collision_demo.py", "ch03_collision", 92, []),
    ("ch03_basics/random_demo.py", "ch03_random", 120, []),
    ("ch06_step1", "step1", 60, []),
    ("ch06_step2", "step2", 60, []),
    ("ch06_step3", "step3", 200, []),
    ("ch06_step4", "step4", 300, []),
    ("ch07_step5", "step5_title", 20, ["--idle"]),
    ("ch07_step6", "step6", 300, []),
    ("ch07_step7", "step7", 300, []),
    ("ch07_step9", "step9", 307, []),
    ("ch07_step9", "step9_gameover", 1500, ["--mortal", "--passive"]),
    ("cosmo_rush", "game_title", 60, ["--idle"]),
    ("cosmo_rush", "game_play", 700, []),
    ("cosmo_rush", "game_boss", 1560, []),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    procs = []
    for script, name, frame, options in JOBS:
        cmd = [sys.executable, str(CAPTURE), str(EXAMPLES / script), str(OUT / name), str(frame), *options]
        procs.append((name, frame, subprocess.Popen(cmd, stdout=subprocess.DEVNULL)))
    for name, frame, proc in procs:
        proc.wait()
        src = OUT / f"{name}_{frame}.png"
        dst = OUT / f"{name}.png"
        src.replace(dst)
        print(f"saved: {dst}")


if __name__ == "__main__":
    main()
