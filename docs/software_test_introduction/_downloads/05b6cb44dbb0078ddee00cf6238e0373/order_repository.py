"""注文を SQLite のデータベースに保存する."""

import sqlite3


class OrderRepository:
    """注文の保存と集計を担当するクラス."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def create_table(self) -> None:
        """注文のテーブルを作る."""
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS orders ("
            " id INTEGER PRIMARY KEY,"
            " customer TEXT NOT NULL,"
            " amount INTEGER NOT NULL CHECK (amount >= 0))")

    def add(self, order_id: int, customer: str, amount: int) -> None:
        """注文を 1 件保存する.

        Raises:
            sqlite3.IntegrityError: 注文番号の重複や負の金額の場合。
        """
        with self._conn:  # 成功すればコミット、例外ならロールバック
            self._conn.execute(
                "INSERT INTO orders (id, customer, amount) VALUES (?, ?, ?)",
                (order_id, customer, amount))

    def total_by_customer(self) -> dict[str, int]:
        """顧客ごとの注文金額の合計を返す."""
        rows = self._conn.execute(
            "SELECT customer, SUM(amount) FROM orders GROUP BY customer")
        return {customer: total for customer, total in rows}
