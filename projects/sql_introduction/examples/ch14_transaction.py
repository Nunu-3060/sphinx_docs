"""Python からトランザクションを制御する例（14 章）.

注文の追加、注文明細の追加、在庫数の更新を 1 つのトランザクションで行います。
在庫が足りない場合は例外を発生させ、すべての変更を取り消します。

shop.db の内容を変更しないよう、メモリ上に複製したデータベースを使います。

使い方::

    python ch14_transaction.py
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "shop.db"


class OutOfStockError(Exception):
    """在庫が足りないことを表す例外です."""


def open_copy(db_path: Path) -> sqlite3.Connection:
    """データベースをメモリ上に複製して開きます.

    PRAGMA foreign_keys はトランザクションの中では効果がないため、
    autocommit=True で接続して設定した後で autocommit を False にします。
    autocommit を False にすると、常にトランザクションの中にある状態になり、
    commit() または rollback() を呼ぶまで変更は確定しません。
    """
    conn = sqlite3.connect(":memory:", autocommit=True)
    source = sqlite3.connect(db_path)
    try:
        source.backup(conn)
    finally:
        source.close()
    conn.execute("PRAGMA foreign_keys = ON")
    conn.autocommit = False
    return conn


def place_order(
    conn: sqlite3.Connection,
    order_id: int,
    customer_id: int,
    ordered_on: str,
    items: list[tuple[int, int]],
) -> None:
    """注文を登録します. items は (商品番号, 数量) のリストです.

    with conn: のブロックを正常に抜けると commit() が、
    例外が発生すると rollback() が自動的に呼ばれます。
    """
    with conn:
        conn.execute(
            "INSERT INTO orders (order_id, customer_id, ordered_on, status)"
            " VALUES (?, ?, ?, '受付済')",
            (order_id, customer_id, ordered_on),
        )
        for product_id, quantity in items:
            row = conn.execute(
                "SELECT price, stock FROM products WHERE product_id = ?",
                (product_id,),
            ).fetchone()
            if row is None:
                raise ValueError(f"商品番号 {product_id} の商品はありません")
            price, stock = row
            if stock < quantity:
                raise OutOfStockError(
                    f"商品番号 {product_id} の在庫が足りません"
                    f"（在庫 {stock}、注文 {quantity}）"
                )
            conn.execute(
                "INSERT INTO order_items"
                " (order_id, product_id, quantity, unit_price)"
                " VALUES (?, ?, ?, ?)",
                (order_id, product_id, quantity, price),
            )
            conn.execute(
                "UPDATE products SET stock = stock - ? WHERE product_id = ?",
                (quantity, product_id),
            )


def show_state(conn: sqlite3.Connection) -> None:
    """注文の件数と、商品番号 1 と 5 の在庫数を表示します."""
    (order_count,) = conn.execute("SELECT COUNT(*) FROM orders").fetchone()
    stocks = conn.execute(
        "SELECT product_id, stock FROM products WHERE product_id IN (1, 5)"
    ).fetchall()
    print(f"  注文の件数: {order_count}、在庫数（商品番号, 在庫数）: {stocks}")


def main() -> None:
    """成功する注文と、在庫不足で失敗する注文を登録します."""
    conn = open_copy(DB_PATH)
    try:
        print("初期状態:")
        show_state(conn)

        print("注文 13（商品番号 1 を 3 個）を登録します。")
        place_order(conn, 13, 2, "2025-07-01", [(1, 3)])
        show_state(conn)

        print("注文 14（商品番号 1 を 2 個、商品番号 5 を 1 個）を登録します。")
        try:
            place_order(conn, 14, 3, "2025-07-02", [(1, 2), (5, 1)])
        except OutOfStockError as error:
            print(f"  エラー: {error}")
            print("  注文 14 の変更はすべて取り消されました。")
        show_state(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
