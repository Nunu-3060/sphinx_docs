"""注文の集約を保存するリポジトリです.

リポジトリは、集約をまるごと保存し、まるごと取り出します。明細だけを
取り出したり、明細だけを更新したりするメソッドは用意しません。

リポジトリのインターフェース（OrderRepository）は model に定義しており、
このモジュールには、その実装だけを置きます。
"""

import copy
import sqlite3

from .model import Money, Order, OrderLine, OrderStatus


class InMemoryOrderRepository:
    """注文をメモリ上に保存します（テストや試作に使います）."""

    def __init__(self) -> None:
        self._orders: dict[str, Order] = {}

    def next_id(self) -> str:
        return f"O-{len(self._orders) + 1:04d}"

    def save(self, order: Order) -> None:
        # 保存後に呼び出し側がオブジェクトを変更しても影響しないようにする
        self._orders[order.order_id] = copy.deepcopy(order)

    def get(self, order_id: str) -> Order | None:
        order = self._orders.get(order_id)
        return copy.deepcopy(order) if order is not None else None


_SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS order_lines (
    order_id TEXT NOT NULL REFERENCES orders (order_id),
    line_no INTEGER NOT NULL,
    product_id TEXT NOT NULL,
    unit_price INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (order_id, line_no)
);
"""


class SqliteOrderRepository:
    """注文を SQLite のデータベースに保存します."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection
        self._connection.executescript(_SCHEMA)

    def next_id(self) -> str:
        (count,) = self._connection.execute(
            "SELECT COUNT(*) FROM orders").fetchone()
        return f"O-{count + 1:04d}"

    def save(self, order: Order) -> None:
        # 注文と明細を 1 つのトランザクションで保存する
        with self._connection:
            self._connection.execute(
                "INSERT OR REPLACE INTO orders VALUES (?, ?, ?)",
                (order.order_id, order.customer_id, order.status.value))
            self._connection.execute(
                "DELETE FROM order_lines WHERE order_id = ?",
                (order.order_id,))
            self._connection.executemany(
                "INSERT INTO order_lines VALUES (?, ?, ?, ?, ?)",
                [(order.order_id, line_no, line.product_id,
                  line.unit_price.amount, line.quantity)
                 for line_no, line in enumerate(order.lines, start=1)])

    def get(self, order_id: str) -> Order | None:
        row = self._connection.execute(
            "SELECT customer_id, status FROM orders WHERE order_id = ?",
            (order_id,)).fetchone()
        if row is None:
            return None
        customer_id, status = row
        cursor = self._connection.execute(
            "SELECT product_id, unit_price, quantity FROM order_lines"
            " WHERE order_id = ? ORDER BY line_no", (order_id,))
        lines = [OrderLine(product_id, Money(unit_price), quantity)
                 for product_id, unit_price, quantity in cursor]
        return Order.restore(order_id, customer_id, OrderStatus(status),
                             lines)
