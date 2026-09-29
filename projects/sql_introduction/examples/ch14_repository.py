"""型ヒントを付けたデータアクセス関数の例（14 章）.

SQL の実行を関数にまとめ、結果をデータクラスに変換して返します。
呼び出す側は SQL を意識せずに、型の決まったオブジェクトとしてデータを扱えます。
このスクリプトはデータを読み込むだけで、shop.db の内容は変更しません。

使い方::

    python ch14_repository.py
"""

import sqlite3
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "shop.db"


@dataclass(frozen=True)
class Product:
    """商品を表すデータクラスです."""

    product_id: int
    name: str
    category_id: int | None  # カテゴリがない商品は None になります
    price: int
    stock: int


@dataclass(frozen=True)
class CustomerSales:
    """顧客ごとの購入金額を表すデータクラスです."""

    customer_id: int
    name: str
    total_amount: int


def find_products(
    conn: sqlite3.Connection, max_price: int, in_stock_only: bool = False
) -> list[Product]:
    """価格が max_price 以下の商品を、価格の安い順に返します."""
    sql = (
        "SELECT product_id, name, category_id, price, stock"
        " FROM products WHERE price <= ?"
    )
    params: list[int] = [max_price]
    if in_stock_only:
        # 条件を追加するときも、値はプレースホルダーで渡します。
        sql += " AND stock > ?"
        params.append(0)
    sql += " ORDER BY price, product_id"
    return [Product(*row) for row in conn.execute(sql, params)]


def top_customers(conn: sqlite3.Connection, limit: int) -> list[CustomerSales]:
    """購入金額（キャンセルを除く）の多い顧客を limit 人まで返します."""
    sql = """
        SELECT c.customer_id, c.name, SUM(oi.quantity * oi.unit_price)
        FROM customers AS c
        INNER JOIN orders AS o ON c.customer_id = o.customer_id
        INNER JOIN order_items AS oi ON o.order_id = oi.order_id
        WHERE o.status <> 'キャンセル'
        GROUP BY c.customer_id, c.name
        ORDER BY SUM(oi.quantity * oi.unit_price) DESC, c.customer_id
        LIMIT ?
    """
    return [CustomerSales(*row) for row in conn.execute(sql, (limit,))]


def main() -> None:
    """関数を呼び出して結果を表示します."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        print("価格が 200 円以下で在庫のある商品:")
        for product in find_products(conn, 200, in_stock_only=True):
            print(f"  {product.name}: {product.price} 円（在庫 {product.stock}）")

        print("購入金額の上位 3 人:")
        for rank, customer in enumerate(top_customers(conn, 3), start=1):
            print(f"  {rank} 位 {customer.name}: {customer.total_amount} 円")


if __name__ == "__main__":
    main()
