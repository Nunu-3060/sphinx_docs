"""サイクロマティック複雑度の簡易計算（第 10 章）.

関数ごとに「分岐の数 + 1」を数え、サイクロマティック複雑度の近似値を求める。
分岐として ``if``・``for``・``while``・``except``・条件式・
``and`` / ``or`` などを数える。実用には radon などの専用ツールを使うとよい。

実行方法: ``python ch10_cyclomatic.py 対象ファイル.py``
"""

import ast
import sys
from pathlib import Path

BRANCH_NODES = (
    ast.If,
    ast.For,
    ast.AsyncFor,
    ast.While,
    ast.ExceptHandler,
    ast.IfExp,
    ast.comprehension,
    ast.Assert,
    ast.match_case,
)


def complexity(function: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    """関数のサイクロマティック複雑度（近似値）を返す."""
    count = 1
    for node in ast.walk(function):
        if isinstance(node, BRANCH_NODES):
            count += 1
        elif isinstance(node, ast.BoolOp):
            # a and b and c は 2 つの分岐として数える
            count += len(node.values) - 1
    return count


def analyze(source: str) -> list[tuple[str, int]]:
    """ソースコード中の各関数の名前と複雑度の一覧を返す."""
    tree = ast.parse(source)
    return [
        (node.name, complexity(node))
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]


def main(argv: list[str]) -> int:
    """コマンドライン引数で指定したファイルを解析して結果を表示する."""
    if len(argv) != 2:
        print("使い方: python ch10_cyclomatic.py 対象ファイル.py")
        return 1
    source = Path(argv[1]).read_text(encoding="utf-8")
    for name, value in analyze(source):
        print(f"{name}: {value}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
