"""sqlite3 によるリレーショナルデータベースの基本操作を示すサンプル。

インメモリのデータベースに表を作成し、行の挿入、結合（JOIN）、
集計（GROUP BY）、NULL の扱い、プレースホルダによる
SQL インジェクション対策を順に示す。

実行方法: python ch11_sqlite_basics.py
関連する章: 第 11 章「データベース」
"""

import sqlite3

SCHEMA = """
CREATE TABLE department (
    dept_id INTEGER PRIMARY KEY,
    name    TEXT NOT NULL UNIQUE
);
CREATE TABLE employee (
    emp_id  INTEGER PRIMARY KEY,
    name    TEXT NOT NULL,
    dept_id INTEGER REFERENCES department(dept_id),
    salary  INTEGER
);
"""


def create_tables(conn: sqlite3.Connection) -> None:
    """DDL を実行して表を作成し、サンプルの行を挿入する。"""
    conn.execute("PRAGMA foreign_keys = ON")  # 外部キー制約を有効にする
    conn.executescript(SCHEMA)
    conn.executemany(
        "INSERT INTO department (dept_id, name) VALUES (?, ?)",
        [(1, "開発"), (2, "営業"), (3, "総務")],
    )
    conn.executemany(
        "INSERT INTO employee (emp_id, name, dept_id, salary)"
        " VALUES (?, ?, ?, ?)",
        [
            (101, "佐藤", 1, 500),
            (102, "鈴木", 1, 450),
            (103, "高橋", 2, 400),
            (104, "田中", 2, None),  # 給与が未登録（NULL）
            (105, "伊藤", None, 380),  # 所属部署が未定（NULL）
        ],
    )
    conn.commit()


def show(conn: sqlite3.Connection, title: str, sql: str) -> None:
    """SQL を実行し、見出しと結果の各行を表示する。"""
    print(f"-- {title}")
    for row in conn.execute(sql):
        print(row)


def demo_queries(conn: sqlite3.Connection) -> None:
    """結合・集計・NULL を含む問い合わせを実行する。"""
    show(conn, "内部結合（部署が未定の伊藤は現れない）",
         "SELECT e.name, d.name FROM employee AS e"
         " JOIN department AS d ON e.dept_id = d.dept_id"
         " ORDER BY e.emp_id")
    show(conn, "部署ごとの集計（左外部結合）",
         "SELECT d.name, COUNT(e.emp_id), COUNT(e.salary),"
         " AVG(e.salary)"
         " FROM department AS d"
         " LEFT JOIN employee AS e ON e.dept_id = d.dept_id"
         " GROUP BY d.dept_id ORDER BY d.dept_id")
    show(conn, "salary = NULL は常に真にならない",
         "SELECT COUNT(*) FROM employee WHERE salary = NULL")
    show(conn, "salary IS NULL",
         "SELECT name FROM employee WHERE salary IS NULL")


def find_unsafe(conn: sqlite3.Connection, name: str) -> list[str]:
    """文字列連結で SQL を組み立てる危険な検索（使ってはならない）。"""
    sql = f"SELECT name FROM employee WHERE name = '{name}'"
    return [row[0] for row in conn.execute(sql)]


def find_safe(conn: sqlite3.Connection, name: str) -> list[str]:
    """プレースホルダを使う安全な検索。"""
    sql = "SELECT name FROM employee WHERE name = ?"
    return [row[0] for row in conn.execute(sql, (name,))]


def demo_injection(conn: sqlite3.Connection) -> None:
    """SQL インジェクションの例と、プレースホルダによる対策を示す。"""
    attack = "' OR '1'='1"
    print("-- SQL インジェクション")
    print("連結     :", find_unsafe(conn, attack))
    print("プレース :", find_safe(conn, attack))


def demo_foreign_key(conn: sqlite3.Connection) -> None:
    """存在しない部署を参照する行の挿入が拒否されることを示す。"""
    print("-- 外部キー制約")
    try:
        conn.execute(
            "INSERT INTO employee VALUES (106, '渡辺', 99, 300)")
    except sqlite3.IntegrityError as e:
        print("拒否:", e)


def main() -> None:
    """サンプル全体を実行する。"""
    conn = sqlite3.connect(":memory:")  # メモリ上だけに存在する DB
    create_tables(conn)
    demo_queries(conn)
    demo_injection(conn)
    demo_foreign_key(conn)
    conn.close()


if __name__ == "__main__":
    main()
