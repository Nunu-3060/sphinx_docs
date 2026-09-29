インデックスと性能
==================

.. sqlfile:: ch13_index 13 章 インデックスと性能

2 章で説明したとおり、SQL ではデータをどのような手順で探すかを DBMS が判断します。しかし、DBMS が効率よくデータを探せるかどうかは、テーブルの設計や SQL 文の書き方に左右されます。本章では、検索を高速にするためのインデックスと、DBMS がどのような手順で SQL 文を実行するかを確認する方法を説明します。

インデックスとは
----------------

インデックスの役割
^^^^^^^^^^^^^^^^^^

インデックスは、特定の列の値から行をすばやく見つけるためのデータ構造です。書籍の巻末にある索引と同じ役割を果たします。

インデックスがない場合、``WHERE customer_id = 1`` のような条件に合う行を見つけるには、テーブルのすべての行を先頭から順に調べる必要があります。これを全件走査（フルスキャン）と呼びます。全件走査にかかる時間は、行数 :math:`n` に比例します。

インデックスは、列の値を並べ替えた状態で保持しています。SQLite を含む多くの DBMS では、B-tree（B 木）と呼ばれる木構造が使われており、値を探すのにかかる時間は :math:`\log n` に比例する程度で済みます。たとえば :math:`n = 1{,}000{,}000` の場合、全件走査では最大で 100 万行を調べる必要がありますが、B-tree では数十回程度の比較で目的の行にたどり着けます。

Python にたとえると、インデックスのない検索はリストを先頭から順に調べる処理に、インデックスを使った検索は ``bisect`` モジュールで並べ替え済みのリストを二分探索する処理に近いものです。

インデックスの効果
^^^^^^^^^^^^^^^^^^

``ch13_index_benchmark.py`` は、100 万行のテーブルで、インデックスがない場合とある場合の検索時間を比較するスクリプトです。

.. literalinclude:: ../examples/ch13_index_benchmark.py
   :language: python
   :caption: ch13_index_benchmark.py
   :linenos:

実行結果の例を次に示します。測定される時間は、実行する環境によって異なります。

.. pyoutput:: ch13_index_benchmark.py

インデックスを作成すると、検索時間が大幅に短くなることがわかります。「実行計画」の行については、次の節で説明します。

実行計画を確認する
------------------

EXPLAIN QUERY PLAN
^^^^^^^^^^^^^^^^^^

DBMS が SQL 文をどのような手順で実行するかを、実行計画と呼びます。SQLite では、SQL 文の前に ``EXPLAIN QUERY PLAN`` を付けて実行すると、実行計画を確認できます。以降の例では、実行計画を sqlite3 コマンドと同様の形式で示します。

.. sqlrun::

   EXPLAIN QUERY PLAN
   SELECT * FROM orders WHERE customer_id = 1;

``SCAN orders`` は、``orders`` テーブルを全件走査することを表します。``orders`` テーブルの ``customer_id`` 列にはインデックスがないためです。

``run_query.py`` で ``EXPLAIN QUERY PLAN`` を実行すると、``id``、``parent``、``notused``、``detail`` の 4 列の表が表示されます。実行計画の内容は ``detail`` 列に表示されます。

インデックスを作成する
^^^^^^^^^^^^^^^^^^^^^^

インデックスを作成するには、``CREATE INDEX`` 文を使用します。

.. code-block:: text
   :linenos:

   CREATE INDEX インデックス名 ON テーブル名 (列名);

.. sqlrun::

   CREATE INDEX idx_orders_customer_id ON orders (customer_id);

インデックスを作成した後、同じ SQL 文の実行計画を確認します。

.. sqlrun::

   EXPLAIN QUERY PLAN
   SELECT * FROM orders WHERE customer_id = 1;

``SEARCH orders USING INDEX idx_orders_customer_id (customer_id=?)`` は、インデックス ``idx_orders_customer_id`` を使って、``customer_id`` が指定の値である行を探すことを表します。

インデックスを作成しても、SQL 文を書き換える必要はありません。DBMS が、利用できるインデックスを自動的に選んで使用します。インデックスを削除するには ``DROP INDEX インデックス名;`` を実行します。

自動的に作成されるインデックス
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

主キーと ``UNIQUE`` 制約を設定した列には、値の重複を効率よく検査するために、インデックスが自動的に作成されます。SQLite では、``sqlite_schema`` テーブルでインデックスの一覧を確認できます。

.. sqlrun::

   SELECT name, tbl_name
   FROM sqlite_schema
   WHERE type = 'index'
   ORDER BY tbl_name, name;

``sqlite_autoindex_`` で始まるものが、自動的に作成されたインデックスです。``categories`` テーブルでは ``name`` 列の ``UNIQUE`` 制約に対して、``customers`` テーブルでは ``email`` 列の ``UNIQUE`` 制約に対して、``order_items`` テーブルでは主キー（``order_id`` と ``product_id`` の組）に対して作成されています。``INTEGER PRIMARY KEY`` の列は rowid の別名（11 章を参照）であり、テーブル自体が rowid の順に格納されているため、別のインデックスは作成されません。

.. sqlrun::

   EXPLAIN QUERY PLAN
   SELECT * FROM products WHERE product_id = 3;

一方、外部キーの列には、インデックスは自動的に作成されません。``orders`` テーブルの ``customer_id`` 列のように、結合や検索の条件によく使う外部キーの列には、インデックスを作成することを検討してください。

結合の実行計画
^^^^^^^^^^^^^^

結合を含む SQL 文でも、インデックスが使われているかを確認できます。

.. sqlrun::

   EXPLAIN QUERY PLAN
   SELECT c.name, o.order_id, o.ordered_on
   FROM customers AS c
   INNER JOIN orders AS o ON c.customer_id = o.customer_id
   WHERE c.customer_id = 1;

``customers`` テーブルは主キーで 1 行を探し、``orders`` テーブルは ``idx_orders_customer_id`` を使って、その顧客の注文を探しています。

インデックスの使い方
--------------------

複合インデックス
^^^^^^^^^^^^^^^^

複数の列を組み合わせたインデックスを、複合インデックスと呼びます。

.. sqlrun::

   CREATE INDEX idx_orders_customer_date ON orders (customer_id, ordered_on);

複合インデックスは、列を指定した順に並べ替えた状態で保持しています。電話帳が「姓」で並び、姓が同じ人は「名」で並んでいるのと同じです。そのため、このインデックスは次の条件の検索に使えます。

* ``customer_id`` だけの条件
* ``customer_id`` と ``ordered_on`` の両方の条件

.. sqlrun::

   EXPLAIN QUERY PLAN
   SELECT * FROM orders
   WHERE customer_id = 1 AND ordered_on >= '2025-02-01';

一方、2 番目の列である ``ordered_on`` だけの条件では、このインデックスを使った効率のよい検索はできません。電話帳で「名」だけから人を探せないのと同じです。

.. sqlrun::

   EXPLAIN QUERY PLAN
   SELECT * FROM orders WHERE ordered_on = '2025-03-05';

複合インデックスを作成するときは、条件によく使う列、特に ``=`` で比較する列を先に指定します。

インデックスが使われない書き方
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

インデックスがあっても、SQL 文の書き方によっては使われないことがあります。代表的な例は、条件の中で列に関数や演算を適用する場合です。

``ordered_on`` 列にインデックスを作成し、2025 年 3 月の注文を探す 2 つの SQL 文の実行計画を比べます。

.. sqlrun::

   CREATE INDEX idx_orders_ordered_on ON orders (ordered_on);

.. sqlrun::

   -- 列に関数を適用した条件
   EXPLAIN QUERY PLAN
   SELECT * FROM orders WHERE substr(ordered_on, 1, 7) = '2025-03';

.. sqlrun::

   -- 列をそのまま比較する条件
   EXPLAIN QUERY PLAN
   SELECT * FROM orders
   WHERE ordered_on >= '2025-03-01' AND ordered_on < '2025-04-01';

インデックスは ``ordered_on`` の値そのものを並べ替えて保持しているため、``substr(ordered_on, 1, 7)`` の値で探すことはできず、全件走査になります。範囲の条件に書き換えると、インデックスが使われます。

同様に、``LIKE '%コーヒー'`` のように先頭が ``%`` のパターンでは、インデックスを使った検索はできません。なお、SQLite の ``LIKE`` は英字の大文字と小文字を区別しないため、先頭が ``%`` でないパターンでも、通常のインデックスは使われません。

カバリングインデックス
^^^^^^^^^^^^^^^^^^^^^^

インデックスには、インデックスを作成した列の値と、行の位置（rowid）が格納されています。SQL 文で必要な列がすべてインデックスに含まれている場合、DBMS はテーブル本体を読まずに、インデックスだけで結果を返せます。このように使われるインデックスをカバリングインデックスと呼びます。

.. sqlrun::

   EXPLAIN QUERY PLAN
   SELECT customer_id, ordered_on FROM orders WHERE customer_id = 1;

``USING COVERING INDEX`` は、インデックスだけで結果を求めていることを表します。``SELECT *`` のようにすべての列を取り出すと、カバリングインデックスは使えません。必要な列だけを指定することは、性能の面でも効果があります。

インデックスのコスト
--------------------

インデックスは検索を速くしますが、次のようなコストもあります。

* 行を追加・更新・削除するたびに、インデックスも更新する必要があるため、書き込みが遅くなります。
* インデックスを格納するための記憶領域が必要になります。

そのため、すべての列にインデックスを作成すればよいわけではありません。インデックスは、次のような列に作成するのが効果的です。

* ``WHERE`` 句の条件や結合の条件によく使われる列
* 値の種類が多く、条件によって行を大きく絞り込める列

性別のように値の種類が少ない列や、行数の少ないテーブルでは、インデックスの効果はほとんどありません。DBMS は、インデックスを使うより全件走査のほうが速いと判断した場合、インデックスがあっても使いません。

実際に性能の問題が起きたときは、推測でインデックスを作成するのではなく、``EXPLAIN QUERY PLAN`` で実行計画を確認し、実行時間を測定したうえで対策を検討してください。

.. _exercises-ch13:

演習問題
--------

1. 次の SQL 文の実行計画を確認してください。その後、実行計画が ``SEARCH`` になるようなインデックスを作成し、もう一度実行計画を確認してください。

   .. code-block:: sql
      :linenos:

      SELECT * FROM order_items WHERE product_id = 1;

2. ``customers`` テーブルで、``prefecture`` 列と ``registered_on`` 列を条件に使う次の SQL 文があります。この SQL 文に適した複合インデックスを作成し、実行計画を確認してください。

   .. code-block:: sql
      :linenos:

      SELECT name FROM customers
      WHERE prefecture = '東京都' AND registered_on >= '2024-06-01';

3. 次の SQL 文は、``products`` テーブルの ``price`` 列にインデックスがあっても、インデックスを使った検索になりません。理由を説明し、インデックスを使える形に書き換えてください。

   .. code-block:: sql
      :linenos:

      SELECT name, price FROM products WHERE price * 1.1 >= 550;

解答は :ref:`answers-ch13` にあります。
