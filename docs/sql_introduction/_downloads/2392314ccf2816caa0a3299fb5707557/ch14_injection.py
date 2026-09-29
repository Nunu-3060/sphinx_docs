"""SQL インジェクションとその対策の例（14 章）.

利用者が入力した文字列を SQL 文に直接埋め込むと、
SQL 文の意味が書き換えられてしまうことを示します。
このスクリプトはデータを読み込むだけで、shop.db の内容は変更しません。

使い方::

    python ch14_injection.py
"""

import sqlite3
from contextlib import closing
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "shop.db"


def find_customers_unsafe(conn: sqlite3.Connection, name: str) -> list[str]:
    """【危険な例】入力された文字列を SQL 文に直接埋め込んで検索します."""
    sql = f"SELECT name FROM customers WHERE name = '{name}'"
    print(f"  実行される SQL: {sql}")
    return [row[0] for row in conn.execute(sql)]


def find_customers_safe(conn: sqlite3.Connection, name: str) -> list[str]:
    """【安全な例】プレースホルダーを使って値を渡して検索します."""
    sql = "SELECT name FROM customers WHERE name = ?"
    return [row[0] for row in conn.execute(sql, (name,))]


def main() -> None:
    """通常の入力と悪意のある入力で、2 つの関数の結果を比べます."""
    inputs = ["佐藤花子", "' OR '1'='1"]
    with closing(sqlite3.connect(DB_PATH)) as conn:
        for text in inputs:
            print(f"入力: {text}")
            print(f"  危険な例の結果: {find_customers_unsafe(conn, text)}")
            print(f"  安全な例の結果: {find_customers_safe(conn, text)}")


if __name__ == "__main__":
    main()
