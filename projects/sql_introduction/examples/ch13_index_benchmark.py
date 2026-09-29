"""インデックスの有無による検索時間の違いを測定するスクリプト（13 章）.

メモリ上のデータベースに 100 万行のテーブルを作成し、
インデックスがない場合とある場合で、同じ検索にかかる時間を比べます。
測定結果は実行する環境によって異なります。

使い方::

    python ch13_index_benchmark.py
"""

import random
import sqlite3
import time
from collections.abc import Iterator

ROW_COUNT = 1_000_000
SEARCH_COUNT = 100


def generate_rows(count: int) -> Iterator[tuple[int, int, int]]:
    """(order_id, customer_id, amount) の組を count 件生成します."""
    rng = random.Random(0)  # 毎回同じデータになるよう乱数の種を固定します
    for order_id in range(1, count + 1):
        yield order_id, rng.randint(1, 100_000), rng.randint(100, 10_000)


def measure(conn: sqlite3.Connection, customer_ids: list[int]) -> float:
    """customer_id による検索を繰り返し、1 回あたりの平均時間（ミリ秒）を返します."""
    start = time.perf_counter()
    for customer_id in customer_ids:
        conn.execute(
            "SELECT order_id, amount FROM big_orders WHERE customer_id = ?",
            (customer_id,),
        ).fetchall()
    elapsed = time.perf_counter() - start
    return elapsed / len(customer_ids) * 1000


def show_plan(conn: sqlite3.Connection) -> None:
    """検索の実行計画を表示します."""
    rows = conn.execute(
        "EXPLAIN QUERY PLAN"
        " SELECT order_id, amount FROM big_orders WHERE customer_id = ?",
        (1,),
    ).fetchall()
    for row in rows:
        print(f"  実行計画: {row[3]}")


def main() -> None:
    """インデックスの作成前と作成後の検索時間を表示します."""
    conn = sqlite3.connect(":memory:")
    try:
        conn.execute(
            "CREATE TABLE big_orders ("
            " order_id INTEGER PRIMARY KEY,"
            " customer_id INTEGER NOT NULL,"
            " amount INTEGER NOT NULL)"
        )
        with conn:  # 100 万行の追加を 1 つのトランザクションで行います
            conn.executemany(
                "INSERT INTO big_orders VALUES (?, ?, ?)",
                generate_rows(ROW_COUNT),
            )
        print(f"{ROW_COUNT:,} 行のテーブルを作成しました。")

        customer_ids = random.Random(1).sample(range(1, 100_001), SEARCH_COUNT)

        print("インデックスなし:")
        show_plan(conn)
        print(f"  1 回の検索の平均時間: {measure(conn, customer_ids):.3f} ミリ秒")

        conn.execute(
            "CREATE INDEX idx_big_orders_customer_id"
            " ON big_orders (customer_id)"
        )

        print("インデックスあり:")
        show_plan(conn)
        print(f"  1 回の検索の平均時間: {measure(conn, customer_ids):.3f} ミリ秒")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
