"""トランザクションのコミットとロールバックを示すサンプル。

口座間の送金を 1 つのトランザクションとして実行する。途中で
エラーが起きた場合はロールバックし、残高が送金前の状態に
戻ること（原子性）を確認する。

実行方法: python ch11_transaction.py
関連する章: 第 11 章「データベース」
"""

import sqlite3


def setup(conn: sqlite3.Connection) -> None:
    """口座表を作成し、2 つの口座を登録する。"""
    conn.execute(
        "CREATE TABLE account ("
        " name TEXT PRIMARY KEY,"
        " balance INTEGER NOT NULL CHECK (balance >= 0))"
    )
    conn.executemany("INSERT INTO account VALUES (?, ?)",
                     [("A", 1000), ("B", 500)])
    conn.commit()


def transfer(conn: sqlite3.Connection, src: str, dst: str,
             amount: int) -> None:
    """src から dst へ amount を送金する。

    入金を先に、出金を後に行う。出金で CHECK 制約に違反すると
    例外が発生し、with 文がトランザクション全体をロールバックする。
    """
    with conn:  # 正常終了でコミット、例外でロールバック
        conn.execute(
            "UPDATE account SET balance = balance + ? WHERE name = ?",
            (amount, dst))
        conn.execute(
            "UPDATE account SET balance = balance - ? WHERE name = ?",
            (amount, src))


def show(conn: sqlite3.Connection, label: str) -> None:
    """全口座の残高を表示する。"""
    rows = conn.execute(
        "SELECT name, balance FROM account ORDER BY name").fetchall()
    print(f"{label}: {rows}")


def main() -> None:
    """成功する送金と失敗する送金を順に実行する。"""
    conn = sqlite3.connect(":memory:")
    setup(conn)
    show(conn, "初期状態")

    transfer(conn, "A", "B", 300)
    show(conn, "300 送金後")

    try:
        transfer(conn, "A", "B", 5000)  # 残高不足で失敗する
    except sqlite3.IntegrityError as e:
        print("エラー:", e)
    show(conn, "5000 送金失敗後")
    conn.close()


if __name__ == "__main__":
    main()
