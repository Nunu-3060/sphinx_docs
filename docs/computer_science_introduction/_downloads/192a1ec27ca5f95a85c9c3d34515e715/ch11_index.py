"""インデックスの有無による実行計画と検索時間の違いを示すサンプル。

SQLite の EXPLAIN QUERY PLAN を使い、インデックスが無いときは
表全体の走査（SCAN）、インデックスがあるときはインデックスを
使った検索（SEARCH）になることを確認する。また、インデックスが
使われない典型的な書き方の例も示す。

実行方法: python ch11_index.py
関連する章: 第 11 章「データベース」
"""

import random
import sqlite3
import time

N_ROWS = 200_000


def build(conn: sqlite3.Connection) -> None:
    """注文表を作成し、乱数で生成した行を挿入する。"""
    rng = random.Random(0)  # 結果を再現できるようシードを固定する
    conn.execute(
        "CREATE TABLE orders ("
        " order_id INTEGER PRIMARY KEY,"
        " customer TEXT NOT NULL,"
        " amount INTEGER NOT NULL)"
    )
    rows = (
        (i, f"C{rng.randrange(50_000):05d}", rng.randrange(1, 10_000))
        for i in range(N_ROWS)
    )
    conn.executemany("INSERT INTO orders VALUES (?, ?, ?)", rows)
    conn.commit()


def plan(conn: sqlite3.Connection, sql: str) -> str:
    """EXPLAIN QUERY PLAN の detail 列を連結して返す。"""
    rows = conn.execute("EXPLAIN QUERY PLAN " + sql).fetchall()
    return " / ".join(str(row[3]) for row in rows)


def measure(conn: sqlite3.Connection, sql: str) -> float:
    """問い合わせを 100 回実行し、1 回あたりの時間をミリ秒で返す。"""
    start = time.perf_counter()
    for _ in range(100):
        conn.execute(sql).fetchall()
    return (time.perf_counter() - start) / 100 * 1000


def main() -> None:
    """インデックス作成前後の実行計画と時間を表示する。"""
    conn = sqlite3.connect(":memory:")
    build(conn)
    query = "SELECT * FROM orders WHERE customer = 'C01234'"

    print("[インデックスなし]")
    print("計画:", plan(conn, query))
    print(f"時間: {measure(conn, query):.3f} ms")

    conn.execute("CREATE INDEX idx_orders_customer ON orders(customer)")
    print("[インデックスあり]")
    print("計画:", plan(conn, query))
    print(f"時間: {measure(conn, query):.3f} ms")

    # インデックスが使われない典型例
    examples = {
        "列に関数を適用": "SELECT * FROM orders"
                   " WHERE lower(customer) = 'c01234'",
        "後方一致の LIKE": "SELECT * FROM orders"
                      " WHERE customer LIKE '%1234'",
        "主キーで検索": "SELECT * FROM orders WHERE order_id = 42",
    }
    print("[その他の問い合わせ]")
    for label, sql in examples.items():
        print(f"{label}: {plan(conn, sql)}")
    conn.close()


if __name__ == "__main__":
    main()
