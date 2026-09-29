"""10 章：graphviz パッケージを使わずに DOT を生成するサンプル.

タスクの依存関係を DOT の文字列として組み立て、subprocess で dot コマンドを
実行して SVG に出力する。Python の標準ライブラリだけで動作する。
出力先は、このファイルと同じフォルダーの output フォルダーである。
"""

import subprocess
import sys
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent / "output"

# タスクの名前と、そのタスクより先に終わらせる必要があるタスクの一覧。
# 名前には、DOT でエスケープが必要な二重引用符とバックスラッシュも含めている。
TASKS: dict[str, list[str]] = {
    "download": [],
    'read "config.ini"': [],
    "build": ["download", 'read "config.ini"'],
    "test": ["build"],
    r"copy to C:\release": ["test"],
}


def quote(text: str) -> str:
    """文字列を DOT の二重引用符で囲んだ ID に変換する.

    バックスラッシュと二重引用符の前にバックスラッシュを付けてエスケープする。
    バックスラッシュを先に処理しないと、二重引用符のエスケープに付けた
    バックスラッシュまで二重にエスケープされてしまう。
    """
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def build_dot() -> str:
    """タスクの依存関係を表す DOT の文字列を返す."""
    lines = [
        "digraph tasks {",
        "    rankdir=LR;",
        "    node [shape=box, style=rounded];",
    ]
    for task, requirements in TASKS.items():
        lines.append(f"    {quote(task)};")
        for requirement in requirements:
            lines.append(f"    {quote(requirement)} -> {quote(task)};")
    lines.append("}")
    return "\n".join(lines) + "\n"


def main() -> int:
    """DOT ファイルと SVG ファイルを出力し、終了コードを返す."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    dot_path = OUTPUT_DIR / "ch10_dot_from_string.gv"
    svg_path = OUTPUT_DIR / "ch10_dot_from_string.svg"
    dot_path.write_text(build_dot(), encoding="utf-8")

    try:
        subprocess.run(["dot", "-Tsvg", str(dot_path), "-o", str(svg_path)],
                       check=True)
    except FileNotFoundError:
        print("dot コマンドが見つかりません。Graphviz をインストールし、"
              "PATH を設定してください。", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as error:
        print(f"dot コマンドが失敗しました（終了コード {error.returncode}）。",
              file=sys.stderr)
        return 1

    print(f"{svg_path} を出力しました。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
