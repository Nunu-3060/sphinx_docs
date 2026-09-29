"""sqlite3 モジュールの基本的な使い方（14 章）.

接続、SQL の実行、結果の取り出し、プレースホルダーの使い方を示します。
このスクリプトはデータを読み込むだけで、shop.db の内容は変更しません。

使い方::

    python ch14_basics.py
"""

import sqlite3
from contextlib import closing
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "shop.db"


def show_fetch_methods(conn: sqlite3.Connection) -> None:
    """結果を取り出す 3 つの方法を示します."""
    print("--- fetchone(): 1 行ずつ取り出す")
    cursor = conn.execute("SELECT COUNT(*) FROM products")
    row = cursor.fetchone()
    print(row)  # 行はタプルとして返されます

    print("--- fetchall(): すべての行をリストとして取り出す")
    cursor = conn.execute(
        "SELECT name, price FROM products WHERE category_id = 8"
    )
    print(cursor.fetchall())

    print("--- for 文: カーソルから 1 行ずつ取り出す")
    cursor = conn.execute(
        "SELECT name, price FROM products WHERE category_id = 6"
    )
    for name, price in cursor:
        print(name, price)


def show_placeholders(conn: sqlite3.Connection) -> None:
    """プレースホルダーを使って値を渡す方法を示します."""
    print("--- ? を使うプレースホルダー")
    min_price = 500
    cursor = conn.execute(
        "SELECT name, price FROM products WHERE price >= ? ORDER BY price",
        (min_price,),  # 値が 1 つでもタプルで渡します
    )
    print(cursor.fetchall())

    print("--- 名前付きのプレースホルダー")
    cursor = conn.execute(
        "SELECT name FROM customers"
        " WHERE prefecture = :pref AND registered_on >= :since",
        {"pref": "東京都", "since": "2024-02-01"},
    )
    print(cursor.fetchall())

    print("--- IN の値の個数が変わる場合")
    customer_ids = [1, 3, 5]
    marks = ", ".join("?" for _ in customer_ids)  # "?, ?, ?" を作ります
    cursor = conn.execute(
        f"SELECT name FROM customers WHERE customer_id IN ({marks})",
        customer_ids,
    )
    print(cursor.fetchall())


def show_row_factory(conn: sqlite3.Connection) -> None:
    """sqlite3.Row を使って列名で値を参照する方法を示します."""
    print("--- sqlite3.Row: 列名で値を参照する")
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(
        "SELECT customer_id, name, email FROM customers WHERE customer_id = ?",
        (3,),
    )
    row = cursor.fetchone()
    print(row["name"], row["email"])  # NULL は None になります
    print(dict(row))
    conn.row_factory = None  # 元の設定（タプルで返す）に戻します


def main() -> None:
    """各機能の例を順に実行します."""
    # closing() を使うと、with 文を抜けるときに接続が閉じられます。
    with closing(sqlite3.connect(DB_PATH)) as conn:
        show_fetch_methods(conn)
        show_placeholders(conn)
        show_row_factory(conn)


if __name__ == "__main__":
    main()
