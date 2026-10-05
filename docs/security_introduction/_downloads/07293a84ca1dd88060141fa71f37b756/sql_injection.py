"""SQL インジェクションとプレースホルダーによる対策のサンプル.

メモリ上の SQLite データベースを使うため、外部への影響はありません。

実行方法:
    python sql_injection.py

必要なライブラリ:
    なし（標準ライブラリのみ）
"""

import sqlite3


def create_database() -> sqlite3.Connection:
    """サンプル用のユーザー表を作成する."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (name TEXT, password_hash TEXT)")
    conn.executemany(
        "INSERT INTO users VALUES (?, ?)",
        [("alice", "hash-a"), ("bob", "hash-b"), ("admin", "hash-x")],
    )
    return conn


def find_user_unsafe(conn: sqlite3.Connection, name: str) -> list[str]:
    """入力を文字列連結で SQL 文に埋め込む（悪い例）."""
    sql = f"SELECT name FROM users WHERE name = '{name}'"
    print(f"  実行される SQL: {sql}")
    return [row[0] for row in conn.execute(sql)]


def find_user_safe(conn: sqlite3.Connection, name: str) -> list[str]:
    """プレースホルダーを使い、入力を値として渡す（良い例）."""
    sql = "SELECT name FROM users WHERE name = ?"
    return [row[0] for row in conn.execute(sql, (name,))]


def main() -> None:
    conn = create_database()
    attack = "' OR '1'='1"

    print("[文字列連結（悪い例）]")
    print(f"  通常の入力: {find_user_unsafe(conn, 'alice')}")
    print(f"  攻撃の入力: {find_user_unsafe(conn, attack)}")

    print("[プレースホルダー（良い例）]")
    print(f"  通常の入力: {find_user_safe(conn, 'alice')}")
    print(f"  攻撃の入力: {find_user_safe(conn, attack)}")

    conn.close()


if __name__ == "__main__":
    main()
