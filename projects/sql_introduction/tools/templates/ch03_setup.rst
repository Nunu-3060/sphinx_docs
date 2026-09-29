環境の準備
==========

.. sqlfile:: ch03_setup 3 章 環境の準備

サンプルファイルの入手
----------------------

本資料で使用するサンプルファイルは、:doc:`appendix_e_samples` からダウンロードできます。すべてのファイルをまとめた ZIP ファイルも用意しています。ZIP ファイルを展開すると、次のようなフォルダー構成になります。

.. code-block:: text

   examples/
   ├── create_shop_db.py    サンプルデータベースを作成するスクリプト
   ├── run_query.py         SQL を実行して結果を表示するスクリプト
   ├── schema.sql           サンプルデータベースのテーブル定義
   ├── data.sql             サンプルデータベースのデータ
   ├── ch03_first_query.py  Python から SQL を実行する例（本章）
   ├── ch13_*.py, ch14_*.py 13 章と 14 章で使用する Python のサンプル
   └── sql/                 各章の SQL の例と演習問題の解答

以降の説明では、コマンドはすべて ``examples`` フォルダーで実行するものとします。

バージョンの確認
----------------

まず、Python と、Python に付属する SQLite のバージョンを確認します。ターミナル（Windows ではコマンドプロンプトや PowerShell）で次のコマンドを実行してください。

.. code-block:: console

   $ python --version
   Python 3.14.6
   $ python -c "import sqlite3; print(sqlite3.sqlite_version)"
   3.50.4

表示されるバージョンは環境によって異なります。Python が 3.12 以上、SQLite が 3.39 以上であれば、本資料のすべての例を実行できます。環境によっては、``python`` の代わりに ``python3`` や ``py`` と入力する必要があります。

サンプルデータベースの作成
--------------------------

次のコマンドを実行すると、``examples`` フォルダーにサンプルデータベースのファイル ``shop.db`` が作成されます。

.. code-block:: console

   $ python create_shop_db.py

実行すると、次のように各テーブルの行数が表示されます。

.. pyoutput:: create_shop_db.py

``create_shop_db.py`` は、既存の ``shop.db`` を削除してから作り直します。10 章以降でデータを変更した後に初期状態へ戻したいときにも、このスクリプトを実行してください。

SQL の実行方法
--------------

run_query.py を使う方法
^^^^^^^^^^^^^^^^^^^^^^^

本資料では、SQL の実行に ``run_query.py`` を使用します。``-e`` オプションの後に SQL 文を指定すると、その SQL 文を実行して結果を表示します。

.. code-block:: console

   $ python run_query.py -e "SELECT * FROM categories;"

.. pyoutput:: run_query.py -e "SELECT * FROM categories;"

``>>>`` の後に実行した SQL 文が表示され、その下に結果が表示されます。

SQL 文をファイルに書いておき、ファイル名を指定して実行することもできます。ファイルに複数の SQL 文が書かれている場合は、1 文ずつ順に実行して結果を表示します。各章の SQL の例は ``sql`` フォルダーに収録しているので、次のようにして本文の例をまとめて実行できます。

.. code-block:: console

   $ python run_query.py sql/ch04_select.sql

``run_query.py`` は、``shop.db`` をメモリ上に複製してから SQL を実行します。そのため、データを変更する SQL（10 章で説明します）を実行しても、``shop.db`` の内容は変わりません。変更を ``shop.db`` に保存したい場合は ``--save`` オプションを指定します。

Python から実行する方法
^^^^^^^^^^^^^^^^^^^^^^^

Python のプログラムから SQL を実行するには、標準ライブラリの ``sqlite3`` モジュールを使用します。次のプログラムは、価格が 500 円以上の商品を価格の高い順に表示します。

.. literalinclude:: ../examples/ch03_first_query.py
   :language: python
   :caption: ch03_first_query.py
   :linenos:

実行結果は次のとおりです。

.. pyoutput:: ch03_first_query.py

``sqlite3.connect()`` でデータベースに接続し、``execute()`` メソッドで SQL を実行しています。``sqlite3`` モジュールの詳しい使い方は、14 章（:doc:`ch14_python`）で説明します。

その他のツール
^^^^^^^^^^^^^^

SQLite のデータベースは、次のようなツールでも操作できます。本資料の学習には必須ではありませんが、必要に応じて利用してください。

* sqlite3 コマンド：`SQLite の公式サイト <https://www.sqlite.org/download.html>`_ で配布されている対話型のツールです。``sqlite3 shop.db`` のように実行すると、SQL を 1 文ずつ入力して実行できます。
* `DB Browser for SQLite <https://sqlitebrowser.org/>`_：テーブルの内容を画面上で確認したり、SQL を実行したりできる GUI ツールです。

サンプルデータの確認
--------------------

ここで、サンプルデータベースの全データを確認しておきます。以降の章の実行結果を読むときに、必要に応じて参照してください。

.. sqlrun::

   SELECT * FROM categories;

.. sqlrun::

   SELECT * FROM products;

.. sqlrun::

   SELECT * FROM customers;

.. sqlrun::

   SELECT * FROM orders;

.. sqlrun::

   SELECT * FROM order_items;

``SELECT * FROM テーブル名;`` は、テーブルのすべての列とすべての行を取り出す SQL 文です。``SELECT`` 文については次の章で詳しく説明します。

SQL の書き方の基本
------------------

SQL を書く際の基本的な規則を説明します。

文の区切り
   SQL の文の終わりにはセミコロン（``;``）を付けます。1 文だけを実行する場合は省略できるツールもありますが、本資料では常に付けます。

改行と空白
   SQL では、改行と空白は単語の区切りとしてのみ扱われます。そのため、長い SQL 文は適宜改行して読みやすく書けます。次の 2 つの文は同じ意味です。

   .. code-block:: sql
      :linenos:

      SELECT name, price FROM products WHERE price >= 500;

      SELECT name, price
      FROM products
      WHERE price >= 500;

大文字と小文字
   キーワード、テーブル名、列名の大文字と小文字は区別されません。ただし、文字列の値は区別されます。たとえば、``'abc'`` と ``'ABC'`` は異なる値です。

文字列
   文字列は単一引用符（``'``）で囲みます。文字列の中に単一引用符を含める場合は、``'It''s'`` のように 2 つ重ねます。

識別子
   テーブル名や列名などを識別子と呼びます。空白を含む名前や、キーワードと同じ名前を識別子として使う場合は、二重引用符（``"``）で囲みます。

コメント
   ``--`` から行末まで、または ``/*`` から ``*/`` までがコメントになります。

   .. code-block:: sql
      :linenos:

      -- 価格が 500 円以上の商品
      SELECT name, price
      FROM products
      WHERE price >= 500;  /* 500 円ちょうどを含む */

.. warning::

   SQLite では、二重引用符で囲んだ文字列が識別子として解釈できない場合に、文字列の値として扱われます。たとえば、``SELECT * FROM products WHERE name = "福袋";`` は SQLite ではエラーにならずに動作しますが、PostgreSQL などの標準 SQL に従う DBMS ではエラーになります（MySQL は、既定の設定では二重引用符で囲んだ値を文字列として扱います）。また、列名を書き間違えたときに、エラーにならずに誤った結果を返す原因にもなります。文字列の値は必ず単一引用符で囲んでください。
