"""本文で使う図をすべて生成する。conf.py からビルド時に呼び出される。

単独で実行する場合は、examples のモジュールを読み込めるように examples をパスに加える。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "examples"))

import activity_figures  # noqa: E402
import body_figures  # noqa: E402
import sleep_figures  # noqa: E402


def main() -> list[Path]:
    """図を生成し、保存先のパスの一覧を返す。"""
    return body_figures.main() + sleep_figures.main() + activity_figures.main()


if __name__ == "__main__":
    for path in main():
        print(path)
