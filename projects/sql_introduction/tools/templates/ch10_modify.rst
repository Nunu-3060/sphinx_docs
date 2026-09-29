データの追加・更新・削除
========================

.. sqlfile:: ch10_modify 10 章 データの追加・更新・削除

本章では、テーブルにデータを追加する ``INSERT`` 文、データを変更する ``UPDATE`` 文、データを削除する ``DELETE`` 文を説明します。

本章の例は、前の例を実行した後のデータに対して、順に実行していくものとします。``run_query.py`` で実行した場合は ``shop.db`` の内容は変わりませんが、``--save`` オプションを付けて実行したり、他のツールで実行したりしてデータが変わった場合は、``create_shop_db.py`` を実行すると初期状態に戻せます。

データを追加する
----------------

INSERT 文
^^^^^^^^^

``INSERT`` 文は、テーブルに行を追加します。

.. code-block:: text
   :linenos:

   INSERT INTO テーブル名 (列名1, 列名2, ...) VALUES (値1, 値2, ...);

列名の並びと値の並びは、順番に対応させます。

.. sqlrun::

   INSERT INTO customers (customer_id, name, prefecture, email, registered_on)
   VALUES (9, '小林真由', '神奈川県', 'mayu@example.com', '2025-03-01');

追加されたことを確認します。

.. sqlrun::

   SELECT * FROM customers WHERE customer_id = 9;

テーブル名の後の列名の並びは省略でき、その場合はテーブルのすべての列に、定義された順に値を指定します。しかし、テーブルの列の構成が変わると SQL 文が動かなくなるため、列名は明示することをお勧めします。

省略した列の値
^^^^^^^^^^^^^^

列名の並びに含めなかった列には、テーブルの定義で指定された既定値が設定されます。既定値が指定されていない列には NULL が設定されます。

サンプルデータベースの ``products`` テーブルの ``stock`` 列には、既定値として 0 が指定されています（:doc:`appendix_e_samples` の ``schema.sql`` を参照）。また、SQLite では ``INTEGER PRIMARY KEY`` と定義した列の値を省略すると、通常は既存の最大値に 1 を加えた値が自動的に設定されます。

.. sqlrun::

   INSERT INTO products (name, category_id, price)
   VALUES ('ほうじ茶', 7, 450);

.. sqlrun::

   SELECT * FROM products WHERE name = 'ほうじ茶';

``product_id`` には 13 が、``stock`` には既定値の 0 が設定されています。主キーを自動的に採番する方法は DBMS によって異なります（:doc:`appendix_b_dialects` を参照）。

複数の行を追加する
^^^^^^^^^^^^^^^^^^

``VALUES`` の後に、値の組をコンマで区切って並べると、1 つの文で複数の行を追加できます。

.. sqlrun::

   INSERT INTO categories (category_id, name, parent_id)
   VALUES (9, 'ジュース', 2),
          (10, '紅茶', 2);

SELECT 文の結果を追加する
^^^^^^^^^^^^^^^^^^^^^^^^^

``VALUES`` の代わりに ``SELECT`` 文を書くと、その結果の行をまとめて追加できます。次の例は、伊藤さくら（``customer_id`` が 5）の注文 12 と同じ商品を、現在の価格で再注文する注文 13 を作成します。

.. sqlrun::

   INSERT INTO orders (order_id, customer_id, ordered_on, status)
   VALUES (13, 5, '2025-07-01', '受付済');

.. sqlrun::

   INSERT INTO order_items (order_id, product_id, quantity, unit_price)
   SELECT 13, oi.product_id, oi.quantity, p.price
   FROM order_items AS oi
   INNER JOIN products AS p ON oi.product_id = p.product_id
   WHERE oi.order_id = 12;

.. sqlrun::

   SELECT * FROM order_items WHERE order_id IN (12, 13);

注文 12 では ``unit_price`` が 180 だったミルクチョコレートが、注文 13 では現在の価格の 200 になっています。

追加した行を確認する
^^^^^^^^^^^^^^^^^^^^

``RETURNING`` 句を付けると、追加した行の値を ``SELECT`` 文のように結果として受け取れます。自動的に採番された主キーの値を知りたい場合に便利です。

.. sqlrun::

   INSERT INTO products (name, category_id, price, stock)
   VALUES ('玄米茶', 7, 400, 30)
   RETURNING product_id, name;

``RETURNING`` 句は、``UPDATE`` 文と ``DELETE`` 文でも使用できます。SQLite ではバージョン 3.35 から使用でき、PostgreSQL でも使用できますが、MySQL は対応していません。

データを更新する
----------------

UPDATE 文
^^^^^^^^^

``UPDATE`` 文は、既存の行の値を変更します。

.. code-block:: text
   :linenos:

   UPDATE テーブル名 SET 列名1 = 値1, 列名2 = 値2, ... WHERE 条件;

``WHERE`` 句の条件に合う行だけが変更されます。次の例は、注文 10 の状態を「発送済」に変更します。

.. sqlrun::

   UPDATE orders
   SET status = '発送済'
   WHERE order_id = 10;

.. sqlrun::

   SELECT * FROM orders WHERE order_id = 10;

値には、現在の列の値を使った式も書けます。次の例は、「チョコレート」カテゴリの商品の価格を 30 円上げ、在庫数を 10 個増やします。

.. sqlrun::

   UPDATE products
   SET price = price + 30,
       stock = stock + 10
   WHERE category_id = 8;

.. sqlrun::

   SELECT product_id, name, price, stock FROM products WHERE category_id = 8;

``SET`` 句の右辺の ``price`` や ``stock`` は、更新前の値を表します。

サブクエリを使った更新
^^^^^^^^^^^^^^^^^^^^^^

``WHERE`` 句や ``SET`` 句にはサブクエリも書けます。次の例は、一度も注文されていない商品の価格を 1 割引きにします。

.. sqlrun::

   UPDATE products
   SET price = price * 90 / 100
   WHERE product_id NOT IN (SELECT product_id FROM order_items);

.. sqlrun::

   SELECT product_id, name, price FROM products WHERE product_id >= 12;

``price * 90 / 100`` は整数どうしの計算なので、結果は小数点以下を切り捨てた整数になります（4 章を参照）。抹茶ラテの価格は 350 円から 315 円に、ほうじ茶は 450 円から 405 円に、玄米茶は 400 円から 360 円になりました。

データを削除する
----------------

DELETE 文
^^^^^^^^^

``DELETE`` 文は、条件に合う行を削除します。

.. code-block:: text
   :linenos:

   DELETE FROM テーブル名 WHERE 条件;

次の例は、注文 13 から醤油（``product_id`` が 4）の明細を削除します。

.. sqlrun::

   DELETE FROM order_items
   WHERE order_id = 13 AND product_id = 4;

.. sqlrun::

   SELECT * FROM order_items WHERE order_id = 13;

WHERE 句を忘れない
^^^^^^^^^^^^^^^^^^

``UPDATE`` 文や ``DELETE`` 文で ``WHERE`` 句を書き忘れると、テーブルのすべての行が変更・削除されます。たとえば ``DELETE FROM order_items;`` を実行すると、すべての注文明細が削除されます。自動コミット（12 章で説明します）によって確定した変更を、後から元に戻す機能はありません。

誤操作を防ぐため、次のような習慣を身につけることをお勧めします。

* ``UPDATE`` 文や ``DELETE`` 文を実行する前に、同じ ``WHERE`` 句を付けた ``SELECT`` 文を実行し、対象の行が意図したとおりかを確認します。
* 重要なデータを変更するときは、トランザクション（12 章で説明します）の中で実行し、結果を確認してから確定します。
* 作業前にデータベースのバックアップを取ります。SQLite では、データベースのファイルをコピーするだけでバックアップになります。

外部キーと削除
^^^^^^^^^^^^^^

他のテーブルから外部キーで参照されている行は、そのままでは削除できません。次の例では、佐藤花子（``customer_id`` が 1）の注文が ``orders`` テーブルに残っているため、エラーになります。

.. sqlrun::
   :error:

   DELETE FROM customers WHERE customer_id = 1;

このように、外部キーの制約は、参照先のない不正なデータ（存在しない顧客の注文など）ができることを防ぎます。注文のない中村大輔（``customer_id`` が 8）は削除できます。

.. sqlrun::

   DELETE FROM customers WHERE customer_id = 8;

.. note::

   SQLite では、外部キーの制約は既定で無効になっており、接続ごとに ``PRAGMA foreign_keys = ON;`` を実行して有効にする必要があります。``run_query.py`` と ``create_shop_db.py`` は、接続時にこの設定を行っています。外部キーの制約については 11 章でも説明します。

追加と更新を 1 つの文で行う
---------------------------

「行がなければ追加し、あれば更新する」処理を UPSERT（update と insert を組み合わせた言葉）と呼びます。SQLite と PostgreSQL では、``INSERT`` 文に ``ON CONFLICT`` 句を付けて UPSERT を行えます。

次の例は、商品番号 12 の商品を登録しようとし、すでに登録されている場合は在庫数を 10 個増やします。

.. sqlrun::

   INSERT INTO products (product_id, name, category_id, price, stock)
   VALUES (12, '抹茶ラテ', 7, 315, 10)
   ON CONFLICT (product_id) DO UPDATE SET stock = stock + excluded.stock;

.. sqlrun::

   SELECT product_id, name, price, stock FROM products WHERE product_id = 12;

``ON CONFLICT (product_id)`` は、``product_id`` の値が重複して追加できない場合の処理を指定します。``DO UPDATE SET`` の中の ``excluded`` は、追加しようとした行を表します。``DO UPDATE`` の代わりに ``DO NOTHING`` と書くと、重複する場合は何もしません。

SQLite には、``INSERT OR REPLACE`` や ``INSERT OR IGNORE`` という独自の書き方もあります。``INSERT OR REPLACE`` は、重複する既存の行を削除してから新しい行を追加するため、指定しなかった列の値が既定値に戻る点に注意が必要です。

.. _exercises-ch10:

演習問題
--------

各問題は、サンプルデータベースの初期状態から実行するものとします。

1. ``customers`` テーブルに、次の顧客を追加してください。顧客番号 9、氏名「木村蓮」、都道府県「京都府」、メールアドレスなし、登録日「2025-04-10」。追加した後、``customers`` テーブルの内容を確認してください。
2. 「文房具」カテゴリ（``category_id`` が 3）の商品の価格を 1 割上げてください。1 円未満は切り捨てます。
3. キャンセルされた注文を、その注文の明細とともに削除してください。外部キーの制約があるため、削除する順序に注意してください。
4. ``ON CONFLICT`` 句を使い、商品番号 5（味噌）の在庫数を 20 個増やしてください。

解答は :ref:`answers-ch10` にあります。
