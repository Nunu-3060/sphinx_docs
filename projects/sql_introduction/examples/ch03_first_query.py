"""Python から SQL を実行する最小の例（3 章）.

shop.db に接続し、価格が 500 円以上の商品を表示します。
先に create_shop_db.py を実行して shop.db を作成してください。
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "shop.db"


def main() -> None:
    """価格が 500 円以上の商品を価格の高い順に表示します."""
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.execute(
            "SELECT name, price FROM products"
            " WHERE price >= 500 ORDER BY price DESC"
        )
        for name, price in cursor:
            print(f"{name}: {price} 円")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
