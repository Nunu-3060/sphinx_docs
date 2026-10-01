"""SQL インジェクションの危険性と対策を比較するサンプルです。

利用者の入力を文字列連結で SQL 文に埋め込むと、入力に含まれる
記号が SQL の一部として解釈され、意図しないデータが取得されます。
プレースホルダーを使えば、入力は常に「値」として扱われます。

実行方法::

    python sql_injection.py
"""

import sqlite3


def create_database() -> sqlite3.Connection:
    """デモ用のテーブルを持つインメモリーデータベースを作成します。"""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (name TEXT, email TEXT)")
    conn.executemany(
        "INSERT INTO users VALUES (?, ?)",
        [
            ("alice", "alice@example.com"),
            ("bob", "bob@example.com"),
            ("carol", "carol@example.com"),
        ],
    )
    return conn


def find_user_unsafe(conn: sqlite3.Connection,
                     name: str) -> list[tuple[str, str]]:
    """【悪い例】入力を文字列連結で SQL 文に埋め込みます。"""
    sql = f"SELECT name, email FROM users WHERE name = '{name}'"
    return conn.execute(sql).fetchall()


def find_user_safe(conn: sqlite3.Connection,
                   name: str) -> list[tuple[str, str]]:
    """【良い例】プレースホルダーを使って入力を値として渡します。"""
    sql = "SELECT name, email FROM users WHERE name = ?"
    return conn.execute(sql, (name,)).fetchall()


def main() -> None:
    """通常の入力と攻撃的な入力で、2 つの関数の結果を比較します。"""
    conn = create_database()
    inputs = ["alice", "' OR '1'='1"]

    for name in inputs:
        print(f"入力: {name!r}")
        print("  悪い例:", find_user_unsafe(conn, name))
        print("  良い例:", find_user_safe(conn, name))

    conn.close()


if __name__ == "__main__":
    main()
