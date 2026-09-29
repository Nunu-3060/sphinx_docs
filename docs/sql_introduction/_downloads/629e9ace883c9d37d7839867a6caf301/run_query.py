"""SQL ファイル（または SQL 文）を実行し、結果を表形式で表示するスクリプト.

SQL 文を 1 文ずつ実行し、文ごとに結果を表示します。
途中の文でエラーが発生しても、エラー内容を表示して次の文へ進みます。

既定では shop.db をメモリ上に複製してから実行するため、
UPDATE や DELETE を実行しても shop.db の内容は変わりません。
変更を shop.db に保存したい場合は --save を指定します。

使い方::

    python run_query.py sql/ch04_select.sql
    python run_query.py -e "SELECT * FROM products LIMIT 3;"
    python run_query.py --save my_changes.sql
"""

import argparse
import sqlite3
import sys
import unicodedata
from collections.abc import Sequence
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
DEFAULT_DB = HERE / "shop.db"


def split_statements(sql: str) -> list[str]:
    """SQL の文字列を 1 文ずつのリストに分割します.

    sqlite3.complete_statement() は、文字列がセミコロンで終わる
    完全な SQL 文かどうかを判定する関数です。
    文字列リテラルやコメントの中のセミコロンは文の終わりとみなしません。
    セミコロンが現れるたびに判定し、完全な文になった時点で区切ります。
    """
    statements: list[str] = []
    start = 0
    for i, ch in enumerate(sql):
        if ch == ";" and sqlite3.complete_statement(sql[start:i + 1]):
            statements.append(sql[start:i + 1].strip())
            start = i + 1
    # 末尾に残ったコメントや空白は無視します。
    rest = sql[start:]
    code_lines = [
        line for line in rest.splitlines()
        if line.strip() and not line.strip().startswith("--")
    ]
    if code_lines:
        statements.append(rest.strip())
    return statements


def display_width(text: str) -> int:
    """端末に表示したときの幅を返します（全角文字は 2 として数えます）."""
    return sum(
        2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
        for ch in text
    )


def pad(text: str, width: int) -> str:
    """表示幅が width になるように右側を空白で埋めます."""
    return text + " " * (width - display_width(text))


def to_text(value: Any) -> str:
    """セルの値を表示用の文字列に変換します（None は NULL と表示します）."""
    return "NULL" if value is None else str(value)


def format_table(columns: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
    """列名と行のリストから、罫線付きの表の文字列を作ります."""
    cells = [[to_text(v) for v in row] for row in rows]
    widths = [display_width(c) for c in columns]
    for row in cells:
        widths = [max(w, display_width(c)) for w, c in zip(widths, row)]

    lines = [" | ".join(pad(c, w) for c, w in zip(columns, widths))]
    lines.append("-+-".join("-" * w for w in widths))
    for row in cells:
        lines.append(" | ".join(pad(c, w) for c, w in zip(row, widths)))
    lines.append(f"({len(rows)} 行)")
    return "\n".join(lines)


def run_statement(conn: sqlite3.Connection, statement: str) -> str:
    """1 文を実行し、結果を表示用の文字列で返します."""
    try:
        cursor = conn.execute(statement)
        rows = cursor.fetchall()
    except sqlite3.Error as error:
        return f"エラー: {type(error).__name__}: {error}"

    if cursor.description is not None:
        columns = [d[0] for d in cursor.description]
        return format_table(columns, rows)
    if cursor.rowcount >= 0:
        return f"({cursor.rowcount} 行を変更しました)"
    return "(実行しました)"


def open_database(db_path: Path, save: bool) -> sqlite3.Connection:
    """データベースを開きます.

    save が False のときは、メモリ上に複製したデータベースを返します。
    autocommit=True を指定すると、Python 側で暗黙にトランザクションを
    開始しなくなり、BEGIN や COMMIT を SQL として書いたとおりに実行できます。
    """
    if save:
        conn = sqlite3.connect(db_path, autocommit=True)
    else:
        source = sqlite3.connect(db_path)
        conn = sqlite3.connect(":memory:", autocommit=True)
        try:
            source.backup(conn)
        finally:
            source.close()
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def main() -> int:
    """コマンドライン引数を解釈して SQL を実行します."""
    parser = argparse.ArgumentParser(description="SQL を実行して結果を表示します。")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("sql_file", nargs="?", type=Path, help="SQL ファイル")
    group.add_argument("-e", "--execute", help="実行する SQL 文")
    parser.add_argument(
        "--db", type=Path, default=DEFAULT_DB, help="データベースファイル"
    )
    parser.add_argument(
        "--save", action="store_true", help="変更をデータベースファイルに保存する"
    )
    args = parser.parse_args()

    if not args.db.exists():
        print(f"{args.db} がありません。先に create_shop_db.py を実行してください。")
        return 1

    if args.execute is not None:
        sql: str = args.execute
    else:
        sql = args.sql_file.read_text(encoding="utf-8")

    conn = open_database(args.db, args.save)
    try:
        for statement in split_statements(sql):
            print(f">>> {statement}")
            print(run_statement(conn, statement))
            print()
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
