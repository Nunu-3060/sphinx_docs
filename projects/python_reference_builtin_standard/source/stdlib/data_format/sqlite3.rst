sqlite3
=======

軽量なファイルベース（またはインメモリ）のリレーショナルデータベースである SQLite を操作するためのモジュール。追加のサーバープロセスを必要とせず、標準ライブラリのみでデータベースファイル 1 つに対して SQL を実行できる。

sqlite3.connect
-----------------

データベースファイルへの接続を確立する。ファイルが存在しなければ新規に作成される。``":memory:"`` を指定すると、ディスクに保存されないインメモリデータベースを作成できる（テストや一時的な集計に便利）。

.. code-block:: python
   :linenos:

   >>> import sqlite3
   >>> con = sqlite3.connect(":memory:")
   >>> con  # doctest: +SKIP
   <sqlite3.Connection object at ...>

   >>> con2 = sqlite3.connect("app.db")  # doctest: +SKIP

SQL の実行 / execute と executemany
--------------------------------------

``Connection.cursor()`` でカーソルを取得し、``execute()`` で SQL 文を 1 件実行する。パラメータには文字列フォーマットではなく ``?`` プレースホルダを使い、値はタプルで渡す。複数行をまとめて挿入したい場合は ``executemany()`` が便利。

.. code-block:: python
   :linenos:

   >>> cur = con.cursor()
   >>> cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")  # doctest: +ELLIPSIS
   <sqlite3.Cursor object at ...>
   >>> cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30))  # doctest: +ELLIPSIS
   <sqlite3.Cursor object at ...>
   >>> cur.executemany(
   ...     "INSERT INTO users (name, age) VALUES (?, ?)",
   ...     [("Bob", 25), ("Carol", 35)],
   ... )  # doctest: +ELLIPSIS
   <sqlite3.Cursor object at ...>
   >>> con.commit()

結果の取得 / fetchone・fetchall・反復
----------------------------------------

``SELECT`` を実行したあとは、カーソルから結果を取り出す。1 件ずつ取得するなら ``fetchone()``、まとめて取得するなら ``fetchall()``。カーソル自体をそのままイテレートして 1 行ずつ処理することもできる。

.. code-block:: python
   :linenos:

   >>> cur.execute("SELECT id, name, age FROM users WHERE age > ?", (26,))  # doctest: +ELLIPSIS
   <sqlite3.Cursor object at ...>
   >>> cur.fetchall()
   [(1, 'Alice', 30), (3, 'Carol', 35)]

   >>> cur.execute("SELECT id, name, age FROM users ORDER BY id")  # doctest: +ELLIPSIS
   <sqlite3.Cursor object at ...>
   >>> cur.fetchone()
   (1, 'Alice', 30)
   >>> cur.fetchone()
   (2, 'Bob', 25)

   >>> for row in cur.execute("SELECT name FROM users ORDER BY name"):
   ...     print(row)
   ...
   ('Alice',)
   ('Bob',)
   ('Carol',)

トランザクションと with 文
------------------------------

``Connection`` オブジェクトはコンテキストマネージャとして使うことができる。``with con:`` ブロックが正常に終了すると自動的に ``commit()`` が行われ、ブロック内で例外が発生した場合は自動的に ``rollback()`` される（ただし ``with`` を抜けても接続自体は閉じられない点に注意）。接続が不要になったら明示的に ``close()`` を呼ぶ。``with`` 文で接続を閉じるところまで行いたい場合は、``contextlib.closing(sqlite3.connect(...))`` を使う。

.. code-block:: python
   :linenos:

   >>> con2 = sqlite3.connect(":memory:")
   >>> con2.execute("CREATE TABLE t (x INTEGER)")  # doctest: +ELLIPSIS
   <sqlite3.Cursor object at ...>
   >>> try:  # doctest: +ELLIPSIS
   ...     with con2:
   ...         con2.execute("INSERT INTO t VALUES (1)")
   ...         raise ValueError("oops")
   ... except ValueError:
   ...     pass
   ...
   <sqlite3.Cursor object at ...>
   >>> con2.execute("SELECT * FROM t").fetchall()  # 例外発生でロールバックされている
   []

   >>> with con2:  # doctest: +ELLIPSIS
   ...     con2.execute("INSERT INTO t VALUES (2)")
   ...
   <sqlite3.Cursor object at ...>
   >>> con2.execute("SELECT * FROM t").fetchall()
   [(2,)]

   >>> con.close()
   >>> con2.close()

.. note::

   Python 3.12 で、``connect()`` の ``autocommit`` 引数と ``Connection.autocommit`` 属性が追加され、トランザクション制御はこちらで行うのが推奨されるようになった。``autocommit=False`` を指定すると、常にトランザクションが開かれた状態になる PEP 249 準拠の動作になり、``commit()`` / ``rollback()`` を呼ぶか ``with`` ブロックを抜けたときに確定・取り消しが行われる。現在のデフォルトは、3.11 以前と同じ ``isolation_level`` 属性に基づく動作を維持する ``sqlite3.LEGACY_TRANSACTION_CONTROL`` であり、本ページの例もこの動作を前提としている。このデフォルトは将来のバージョンで ``False`` に変更される予定である。

   .. code-block:: python
      :linenos:

      >>> con = sqlite3.connect(":memory:", autocommit=False)  # Python 3.12 以降

.. note::

   ``datetime.date`` / ``datetime.datetime`` を ``?`` プレースホルダにそのまま渡すと、組み込みのデフォルトアダプタによって ISO 8601 形式の文字列に変換されるが、このデフォルトのアダプタ・コンバータは Python 3.12 で非推奨になり、使用すると ``DeprecationWarning`` が発生する。日時を保存する場合は ``value.isoformat()`` のように自分で文字列に変換するか、``sqlite3.register_adapter()`` で変換関数を明示的に登録する。

.. warning::

   SQL 文の一部をユーザー入力の文字列連結や f-string で組み立てると、SQL インジェクション攻撃を許してしまう危険がある。

   .. code-block:: python
      :linenos:

      # 危険な例（絶対にやらないこと）
      name = "'; DROP TABLE users; --"
      cur.execute(f"SELECT * FROM users WHERE name = '{name}'")

   必ず ``?`` プレースホルダを使ったパラメータ化クエリで値を渡すこと。``execute()`` は値を SQL 文とは別に安全にバインドするため、ユーザー入力がそのまま SQL として解釈されることはない。

   .. code-block:: python
      :linenos:

      cur.execute("SELECT * FROM users WHERE name = ?", (name,))
