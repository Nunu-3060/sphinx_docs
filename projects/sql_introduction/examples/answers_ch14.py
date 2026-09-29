"""14 章の演習問題の解答例.

問題 1、2、4 の解答例の関数を定義し、実行結果を表示します。
このスクリプトはデータを読み込むだけで、shop.db の内容は変更しません。

使い方::

    python answers_ch14.py
"""

import sqlite3
from contextlib import closing
from pathlib import Path

import pandas as pd

DB_PATH = Path(__file__).resolve().parent / "shop.db"


def customers_in(conn: sqlite3.Connection, prefecture: str) -> list[str]:
    """問題 1: 指定した都道府県の顧客の氏名のリストを返します."""
    rows = conn.execute(
        "SELECT name FROM customers WHERE prefecture = ? ORDER BY customer_id",
        (prefecture,),
    )
    return [row[0] for row in rows]


def find_products_by_name(conn: sqlite3.Connection, keyword: str) -> list[str]:
    """問題 2: 商品名に keyword を含む商品の商品名のリストを返します.

    % を付けたパターンの文字列を Python 側で作り、
    パターン全体を 1 つの値としてプレースホルダーで渡します。
    """
    sql = "SELECT name FROM products WHERE name LIKE ? ORDER BY product_id"
    return [row[0] for row in conn.execute(sql, (f"%{keyword}%",))]


def category_summary(conn: sqlite3.Connection) -> pd.DataFrame:
    """問題 4: カテゴリ名ごとの商品数と平均価格を DataFrame で返します."""
    sql = """
        SELECT c.name AS category,
               COUNT(*) AS product_count,
               AVG(p.price) AS avg_price
        FROM products AS p
        INNER JOIN categories AS c ON p.category_id = c.category_id
        GROUP BY c.category_id, c.name
        ORDER BY c.category_id
    """
    return pd.read_sql_query(sql, conn)


def main() -> None:
    """各関数を呼び出して結果を表示します."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        print("問題 1:", customers_in(conn, "大阪府"))
        print("問題 2:", find_products_by_name(conn, "コーヒー"))
        print("問題 2（悪意のある入力）:", find_products_by_name(conn, "' OR '1'='1"))
        print("問題 4:")
        print(category_summary(conn))


if __name__ == "__main__":
    main()
