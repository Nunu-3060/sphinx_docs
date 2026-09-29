"""サンプルデータベース shop.db を作成するスクリプト.

schema.sql（テーブル定義）と data.sql（データ）を読み込み、
このスクリプトと同じフォルダーに shop.db を作成します。
shop.db が既にある場合は削除してから作り直すため、
データを変更してしまったときに初期状態へ戻す用途にも使えます。

使い方::

    python create_shop_db.py
"""

import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / "shop.db"
SQL_FILES = [HERE / "schema.sql", HERE / "data.sql"]


def create_database(db_path: Path, sql_files: list[Path]) -> None:
    """SQL ファイルを順に実行してデータベースを作成します."""
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        for sql_file in sql_files:
            conn.executescript(sql_file.read_text(encoding="utf-8"))
        conn.commit()
    finally:
        conn.close()


def main() -> None:
    """shop.db を作成し、各テーブルの行数を表示します."""
    create_database(DB_PATH, SQL_FILES)

    conn = sqlite3.connect(DB_PATH)
    try:
        tables = [
            "categories", "products", "customers", "orders", "order_items",
        ]
        print(f"{DB_PATH.name} を作成しました。")
        for table in tables:
            # テーブル名はプレースホルダーで渡せないため文字列に埋め込みます。
            # 埋め込むのは上で定義した固定の名前だけなので安全です。
            (count,) = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
            print(f"  {table}: {count} 行")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
