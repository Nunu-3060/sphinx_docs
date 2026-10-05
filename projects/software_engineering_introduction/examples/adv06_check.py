"""発展課題 6-A の解答例: 品質検査をまとめて実行するスクリプト（第 6 章）.

flake8、mypy、単体テストを順に実行し、結果をまとめて表示する。
1 つでも失敗した場合は終了コード 1 を返すため、
第 8 章の継続的インテグレーションのパイプラインからそのまま利用できる。

実行方法: ``python adv06_check.py 検査するフォルダー``
"""

import subprocess
import sys
from pathlib import Path

CHECKS: list[tuple[str, list[str]]] = [
    ("flake8", ["-m", "flake8", "."]),
    ("mypy", ["-m", "mypy", "--strict", "."]),
    ("unittest", ["-m", "unittest", "discover", "-p", "*_test_*.py"]),
]


def run_check(name: str, args: list[str], directory: Path) -> bool:
    """1 つの検査を実行し、成功したら True を返す."""
    result = subprocess.run(
        [sys.executable, *args],
        cwd=directory,
        capture_output=True,
        text=True,
    )
    passed = result.returncode == 0
    print(f"[{'OK' if passed else 'NG'}] {name}")
    if not passed:
        # 失敗した検査だけ詳細を表示する
        print(result.stdout + result.stderr)
    return passed


def main(argv: list[str]) -> int:
    """すべての検査を実行し、すべて成功なら 0、それ以外は 1 を返す."""
    directory = Path(argv[1]) if len(argv) > 1 else Path(".")
    results = [run_check(name, args, directory) for name, args in CHECKS]
    failed = results.count(False)
    print(f"{len(results)} 件中 {failed} 件の検査が失敗した")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
