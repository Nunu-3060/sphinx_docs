"""ファイルへの書き込みと読み込みの基本を示すサンプルです。"""

import tempfile
from pathlib import Path


def write_lines(path: Path, lines: list[str]) -> None:
    """指定したパスのファイルに、複数行のテキストを書き込みます。"""
    with path.open(mode="w", encoding="utf-8") as file:
        for line in lines:
            file.write(line + "\n")


def read_lines(path: Path) -> list[str]:
    """指定したパスのファイルを読み込み、行のリストとして返します。"""
    lines: list[str] = []
    with path.open(mode="r", encoding="utf-8") as file:
        for line in file:
            lines.append(line.rstrip("\n"))
    return lines


def main() -> None:
    """一時ファイルへの書き込みと読み込みの結果を表示します。"""
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path: Path = Path(temp_dir) / "memo.txt"

        write_lines(file_path, ["1 行目です。", "2 行目です。", "3 行目です。"])
        print("ファイルに書き込みました:", file_path)

        lines: list[str] = read_lines(file_path)
        print("読み込んだ内容:")
        for line in lines:
            print(line)


if __name__ == "__main__":
    main()
