"""更新の喪失と、悲観的ロック・楽観的ロックによる防止を示すサンプル。

1 つのデータベースファイルに 2 つの接続 A と B を開き、同じ商品の
在庫を同時に減らす状況を、処理の順序を固定して再現する。

1. ロックなし: 両者が同じ値を読んで書き戻し、一方の更新が失われる。
2. 悲観的ロック: BEGIN IMMEDIATE で書き込みロックを先に取得する。
3. 楽観的ロック: バージョン列を条件に UPDATE し、更新件数が 0 なら
   競合とみなして読み直し、再試行する。

実行方法: python ch11_optimistic_lock.py
関連する章: 第 11 章「データベース」
"""

import sqlite3
import tempfile
from pathlib import Path


def connect(path: Path) -> sqlite3.Connection:
    """自動コミットモードで接続する（トランザクションは明示的に書く）。

    timeout=0 なので、ロックを取得できないときは待たずに例外になる。
    """
    return sqlite3.connect(path, timeout=0, isolation_level=None)


def reset(path: Path) -> None:
    """商品表を作り直し、在庫 10、バージョン 1 の商品を登録する。"""
    conn = connect(path)
    conn.execute("DROP TABLE IF EXISTS item")
    conn.execute(
        "CREATE TABLE item (id INTEGER PRIMARY KEY,"
        " stock INTEGER NOT NULL, version INTEGER NOT NULL)")
    conn.execute("INSERT INTO item VALUES (1, 10, 1)")
    conn.close()


def read_item(conn: sqlite3.Connection) -> tuple[int, int]:
    """商品 1 の（在庫, バージョン）を返す。"""
    row = conn.execute(
        "SELECT stock, version FROM item WHERE id = 1").fetchone()
    return int(row[0]), int(row[1])


def lost_update(path: Path) -> None:
    """A が 3 個、B が 5 個を減らす。どちらも古い値をもとに書き戻す。"""
    a, b = connect(path), connect(path)
    stock_a, _ = read_item(a)  # A が 10 を読む
    stock_b, _ = read_item(b)  # B も 10 を読む
    a.execute("UPDATE item SET stock = ? WHERE id = 1", (stock_a - 3,))
    b.execute("UPDATE item SET stock = ? WHERE id = 1", (stock_b - 5,))
    print(f"最終在庫: {read_item(a)[0]}（正しくは 2）")
    a.close()
    b.close()


def pessimistic(path: Path) -> None:
    """BEGIN IMMEDIATE で書き込みロックを取ってから読み、更新する。"""
    a, b = connect(path), connect(path)
    a.execute("BEGIN IMMEDIATE")  # A が書き込みロックを取得する
    stock_a, _ = read_item(a)
    try:
        b.execute("BEGIN IMMEDIATE")  # B はロックを取得できない
    except sqlite3.OperationalError as e:
        print(f"B: {e}（A のコミットを待つ）")
    a.execute("UPDATE item SET stock = ? WHERE id = 1", (stock_a - 3,))
    a.execute("COMMIT")
    b.execute("BEGIN IMMEDIATE")  # A の終了後なら取得できる
    stock_b, _ = read_item(b)  # A の更新後の値 7 を読む
    b.execute("UPDATE item SET stock = ? WHERE id = 1", (stock_b - 5,))
    b.execute("COMMIT")
    print(f"最終在庫: {read_item(a)[0]}")
    a.close()
    b.close()


def decrement_optimistic(conn: sqlite3.Connection, name: str, amount: int,
                         snapshot: tuple[int, int],
                         max_retries: int = 3) -> None:
    """読み出し時のバージョンを条件に在庫を減らす。

    更新件数が 0 なら、読んだ後に他者が更新したと判断して読み直す。
    """
    stock, version = snapshot
    for attempt in range(1, max_retries + 1):
        cur = conn.execute(
            "UPDATE item SET stock = ?, version = version + 1"
            " WHERE id = 1 AND version = ?", (stock - amount, version))
        if cur.rowcount == 1:
            print(f"{name}: {attempt} 回目で成功"
                  f"（在庫 {stock} -> {stock - amount}、"
                  f"バージョン {version} -> {version + 1}）")
            return
        print(f"{name}: {attempt} 回目は更新件数 0"
              f"（バージョン {version} は古い）")
        stock, version = read_item(conn)  # 最新の値を読み直す
    raise RuntimeError("再試行の上限に達した")


def optimistic(path: Path) -> None:
    """A と B が同じバージョンを読み、先に更新した A だけが成功する。"""
    a, b = connect(path), connect(path)
    snap_a = read_item(a)  # A が (10, 1) を読む
    snap_b = read_item(b)  # B も (10, 1) を読む
    decrement_optimistic(a, "A", 3, snap_a)
    decrement_optimistic(b, "B", 5, snap_b)
    print(f"最終在庫: {read_item(a)[0]}")
    a.close()
    b.close()


def main() -> None:
    """3 つの方式を順に実行する。"""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "shop.db"
        for title, demo in [("ロックなし（更新の喪失）", lost_update),
                            ("悲観的ロック", pessimistic),
                            ("楽観的ロック", optimistic)]:
            print(f"[{title}]")
            reset(path)
            demo(path)


if __name__ == "__main__":
    main()
