"""発展課題 10-A の解答例: 複雑度の上限を検査するスクリプト（第 10 章）.

指定したフォルダー内のすべての Python ファイルを解析し、
サイクロマティック複雑度が上限を超える関数を一覧表示する。
上限を超える関数があれば終了コード 1 を返すため、CI で利用できる。

実行方法: ``python adv10_complexity_gate.py 検査するフォルダー --max 10``
"""

import argparse
import sys
from pathlib import Path

from ch10_cyclomatic import analyze


def find_complex_functions(
    directory: Path, limit: int
) -> list[tuple[Path, str, int]]:
    """複雑度が ``limit`` を超える (ファイル, 関数名, 複雑度) の一覧を返す."""
    found = []
    for path in sorted(directory.rglob("*.py")):
        source = path.read_text(encoding="utf-8")
        for name, value in analyze(source):
            if value > limit:
                found.append((path, name, value))
    # 複雑度の大きい順に並べる
    return sorted(found, key=lambda item: item[2], reverse=True)


def main(argv: list[str]) -> int:
    """検査を実行し、上限を超える関数がなければ 0、あれば 1 を返す."""
    parser = argparse.ArgumentParser(description="複雑度の上限を検査する")
    parser.add_argument("directory", type=Path, help="検査するフォルダー")
    parser.add_argument("--max", type=int, default=10, dest="limit",
                        help="複雑度の上限（既定値: 10）")
    args = parser.parse_args(argv)

    found = find_complex_functions(args.directory, args.limit)
    for path, name, value in found:
        print(f"{path}: {name} の複雑度 {value} が上限 {args.limit} を超えている")
    print(f"上限を超える関数: {len(found)} 件")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
