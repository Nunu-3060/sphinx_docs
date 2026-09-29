"""pandas と SQL を組み合わせる例（14 章）.

SQL で集計した結果を DataFrame として読み込む方法と、
DataFrame をデータベースのテーブルとして書き込む方法を示します。
書き込みはメモリ上のデータベースに対して行うため、shop.db の内容は変更しません。

使い方::

    python ch14_pandas.py
"""

import sqlite3
from contextlib import closing
from pathlib import Path

import pandas as pd

DB_PATH = Path(__file__).resolve().parent / "shop.db"


def monthly_sales(conn: sqlite3.Connection, status: str) -> pd.DataFrame:
    """指定した状態の注文について、月ごとの売上金額を DataFrame で返します."""
    sql = """
        SELECT strftime('%Y-%m', o.ordered_on) AS month,
               SUM(oi.quantity * oi.unit_price) AS sales
        FROM orders AS o
        INNER JOIN order_items AS oi ON o.order_id = oi.order_id
        WHERE o.status = ?
        GROUP BY month
        ORDER BY month
    """
    return pd.read_sql_query(sql, conn, params=(status,))


def main() -> None:
    """読み込みと書き込みの例を実行します."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        print("--- SQL で集計した結果を読み込む")
        sales = monthly_sales(conn, "発送済")
        print(sales)

        print("--- テーブルを読み込んで pandas で集計する")
        products = pd.read_sql_query(
            "SELECT category_id, price FROM products", conn
        )
        print(products.groupby("category_id", dropna=False)["price"].mean())

    print("--- DataFrame をテーブルとして書き込む")
    targets = pd.DataFrame(
        {
            "month": ["2025-01", "2025-02", "2025-03"],
            "target": [3000, 3000, 4000],
        }
    )
    with closing(sqlite3.connect(":memory:")) as mem:
        targets.to_sql("sales_targets", mem, index=False)
        print(pd.read_sql_query("SELECT * FROM sales_targets", mem))


if __name__ == "__main__":
    main()
