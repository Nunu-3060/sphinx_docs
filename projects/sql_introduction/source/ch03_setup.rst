環境の準備
==========

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

.. code-block:: text

   shop.db を作成しました。
     categories: 8 行
     products: 12 行
     customers: 8 行
     orders: 12 行
     order_items: 21 行

``create_shop_db.py`` は、既存の ``shop.db`` を削除してから作り直します。10 章以降でデータを変更した後に初期状態へ戻したいときにも、このスクリプトを実行してください。

SQL の実行方法
--------------

run_query.py を使う方法
^^^^^^^^^^^^^^^^^^^^^^^

本資料では、SQL の実行に ``run_query.py`` を使用します。``-e`` オプションの後に SQL 文を指定すると、その SQL 文を実行して結果を表示します。

.. code-block:: console

   $ python run_query.py -e "SELECT * FROM categories;"

.. code-block:: text

   >>> SELECT * FROM categories;
   category_id | name         | parent_id
   ------------+--------------+----------
   1           | 食品         | NULL     
   2           | 飲料         | NULL     
   3           | 文房具       | NULL     
   4           | 菓子         | 1        
   5           | 調味料       | 1        
   6           | コーヒー     | 2        
   7           | お茶         | 2        
   8           | チョコレート | 4        
   (8 行)

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

.. code-block:: text

   福袋: 3000 円
   ドリップコーヒー: 800 円
   緑茶ティーバッグ: 600 円
   味噌: 500 円

``sqlite3.connect()`` でデータベースに接続し、``execute()`` メソッドで SQL を実行しています。``sqlite3`` モジュールの詳しい使い方は、14 章（:doc:`ch14_python`）で説明します。

その他のツール
^^^^^^^^^^^^^^

SQLite のデータベースは、次のようなツールでも操作できます。本資料の学習には必須ではありませんが、必要に応じて利用してください。

* sqlite3 コマンド：`SQLite の公式サイト <https://www.sqlite.org/download.html>`_ で配布されている対話型のツールです。``sqlite3 shop.db`` のように実行すると、SQL を 1 文ずつ入力して実行できます。
* `DB Browser for SQLite <https://sqlitebrowser.org/>`_：テーブルの内容を画面上で確認したり、SQL を実行したりできる GUI ツールです。

サンプルデータの確認
--------------------

ここで、サンプルデータベースの全データを確認しておきます。以降の章の実行結果を読むときに、必要に応じて参照してください。

.. code-block:: sql
   :linenos:

   SELECT * FROM categories;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - category\_id
     - name
     - parent\_id
   * - 1
     - 食品
     - NULL
   * - 2
     - 飲料
     - NULL
   * - 3
     - 文房具
     - NULL
   * - 4
     - 菓子
     - 1
   * - 5
     - 調味料
     - 1
   * - 6
     - コーヒー
     - 2
   * - 7
     - お茶
     - 2
   * - 8
     - チョコレート
     - 4

.. code-block:: sql
   :linenos:

   SELECT * FROM products;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - product\_id
     - name
     - category\_id
     - price
     - stock
   * - 1
     - ミルクチョコレート
     - 8
     - 200
     - 50
   * - 2
     - ビターチョコレート
     - 8
     - 250
     - 30
   * - 3
     - ポテトチップス
     - 4
     - 150
     - 80
   * - 4
     - 醤油
     - 5
     - 400
     - 20
   * - 5
     - 味噌
     - 5
     - 500
     - 0
   * - 6
     - ドリップコーヒー
     - 6
     - 800
     - 25
   * - 7
     - 缶コーヒー
     - 6
     - 120
     - 100
   * - 8
     - 緑茶ティーバッグ
     - 7
     - 600
     - 15
   * - 9
     - ボールペン
     - 3
     - 100
     - 200
   * - 10
     - ノート
     - 3
     - 180
     - 120
   * - 11
     - 福袋
     - NULL
     - 3000
     - 5
   * - 12
     - 抹茶ラテ
     - 7
     - 350
     - 40

.. code-block:: sql
   :linenos:

   SELECT * FROM customers;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - customer\_id
     - name
     - prefecture
     - email
     - registered\_on
   * - 1
     - 佐藤花子
     - 東京都
     - hanako\@example.com
     - 2024-01-15
   * - 2
     - 鈴木一郎
     - 大阪府
     - ichiro\@example.com
     - 2024-02-03
   * - 3
     - 高橋美咲
     - 東京都
     - NULL
     - 2024-03-20
   * - 4
     - 田中健太
     - 愛知県
     - kenta\@example.com
     - 2024-05-11
   * - 5
     - 伊藤さくら
     - 大阪府
     - sakura\@example.com
     - 2024-07-01
   * - 6
     - 渡辺翔
     - 福岡県
     - NULL
     - 2024-09-09
   * - 7
     - 山本優子
     - 東京都
     - yuko\@example.com
     - 2025-01-05
   * - 8
     - 中村大輔
     - 北海道
     - daisuke\@example.com
     - 2025-02-14

.. code-block:: sql
   :linenos:

   SELECT * FROM orders;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - order\_id
     - customer\_id
     - ordered\_on
     - status
   * - 1
     - 1
     - 2025-01-10
     - 発送済
   * - 2
     - 2
     - 2025-01-15
     - 発送済
   * - 3
     - 1
     - 2025-02-02
     - 発送済
   * - 4
     - 3
     - 2025-02-20
     - 発送済
   * - 5
     - 4
     - 2025-03-05
     - キャンセル
   * - 6
     - 5
     - 2025-03-18
     - 発送済
   * - 7
     - 2
     - 2025-04-01
     - 発送済
   * - 8
     - 6
     - 2025-04-22
     - 発送済
   * - 9
     - 1
     - 2025-05-09
     - 発送済
   * - 10
     - 7
     - 2025-05-30
     - 受付済
   * - 11
     - 3
     - 2025-06-12
     - 受付済
   * - 12
     - 5
     - 2025-06-25
     - 受付済

.. code-block:: sql
   :linenos:

   SELECT * FROM order_items;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - order\_id
     - product\_id
     - quantity
     - unit\_price
   * - 1
     - 1
     - 2
     - 200
   * - 1
     - 6
     - 1
     - 800
   * - 2
     - 9
     - 10
     - 100
   * - 2
     - 10
     - 5
     - 180
   * - 3
     - 3
     - 3
     - 150
   * - 3
     - 7
     - 6
     - 120
   * - 4
     - 4
     - 1
     - 400
   * - 4
     - 5
     - 1
     - 500
   * - 5
     - 11
     - 1
     - 3000
   * - 6
     - 1
     - 4
     - 200
   * - 6
     - 2
     - 2
     - 250
   * - 6
     - 8
     - 1
     - 600
   * - 7
     - 6
     - 2
     - 800
   * - 8
     - 3
     - 5
     - 150
   * - 9
     - 8
     - 2
     - 600
   * - 9
     - 9
     - 3
     - 100
   * - 10
     - 7
     - 12
     - 120
   * - 11
     - 2
     - 1
     - 250
   * - 11
     - 10
     - 2
     - 180
   * - 12
     - 1
     - 1
     - 180
   * - 12
     - 4
     - 2
     - 400

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
