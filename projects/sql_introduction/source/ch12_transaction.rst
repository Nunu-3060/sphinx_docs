トランザクション
================

本章の例は、サンプルデータベースの初期状態から始めて、前の例を実行した後のデータに対して順に実行していくものとします。

トランザクションが必要な理由
----------------------------

ネットショップで商品が注文されたときには、たとえば次の処理を行う必要があります。

1. ``orders`` テーブルに注文を追加します。
2. ``order_items`` テーブルに注文明細を追加します。
3. ``products`` テーブルの在庫数を減らします。

もし 2 の処理の後でプログラムが異常終了し、3 の処理が行われなかったとすると、注文は記録されているのに在庫数は減っていない、という矛盾した状態になります。

このような問題を防ぐには、一連の処理を「すべて成功する」か「すべて行われなかったことになる」かのどちらかにする必要があります。このように、分割できない一連の処理のまとまりをトランザクションと呼びます。

ACID 特性
---------

トランザクションが備えるべき性質は、それぞれの頭文字をとって ACID 特性と呼ばれます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 性質
     - 内容
   * - 原子性（Atomicity）
     - トランザクション内の処理は、すべて実行されるか、まったく実行されないかのどちらかです。
   * - 一貫性（Consistency）
     - トランザクションの前後で、データは制約などの規則を満たした状態に保たれます。
   * - 独立性（Isolation）
     - 同時に実行される複数のトランザクションは、互いに干渉しません。
   * - 永続性（Durability）
     - 確定したトランザクションの結果は、その後に障害が発生しても失われません。

トランザクションの制御
----------------------

BEGIN、COMMIT、ROLLBACK
^^^^^^^^^^^^^^^^^^^^^^^

トランザクションは、次の文で制御します。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 文
     - 内容
   * - ``BEGIN``
     - トランザクションを開始します。
   * - ``COMMIT``
     - トランザクション内の変更を確定します。
   * - ``ROLLBACK``
     - トランザクション内の変更をすべて取り消し、トランザクションを開始する前の状態に戻します。

``BEGIN`` は、DBMS によっては ``BEGIN TRANSACTION`` や ``START TRANSACTION`` と書きます。

まず、ミルクチョコレート（``product_id`` が 1）の現在の在庫数を確認します。

.. code-block:: sql
   :linenos:

   SELECT product_id, name, stock FROM products WHERE product_id = 1;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - product\_id
     - name
     - stock
   * - 1
     - ミルクチョコレート
     - 50

トランザクションを開始し、注文の追加と在庫数の更新を行います。

.. code-block:: sql
   :linenos:

   BEGIN;
   INSERT INTO orders (order_id, customer_id, ordered_on, status)
   VALUES (13, 2, '2025-07-01', '受付済');
   INSERT INTO order_items (order_id, product_id, quantity, unit_price)
   VALUES (13, 1, 5, 200);
   UPDATE products SET stock = stock - 5 WHERE product_id = 1;

トランザクションの中では、変更後のデータを参照できます。

.. code-block:: sql
   :linenos:

   SELECT product_id, name, stock FROM products WHERE product_id = 1;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - product\_id
     - name
     - stock
   * - 1
     - ミルクチョコレート
     - 45

ここで ``ROLLBACK`` を実行すると、トランザクション内のすべての変更が取り消されます。

.. code-block:: sql
   :linenos:

   ROLLBACK;

.. code-block:: sql
   :linenos:

   SELECT product_id, name, stock FROM products WHERE product_id = 1;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - product\_id
     - name
     - stock
   * - 1
     - ミルクチョコレート
     - 50

.. code-block:: sql
   :linenos:

   SELECT * FROM orders WHERE order_id = 13;

結果は 0 行です。

在庫数は元の 50 に戻り、注文 13 も存在しません。``ROLLBACK`` の代わりに ``COMMIT`` を実行していれば、変更が確定します。

.. code-block:: sql
   :linenos:

   BEGIN;
   INSERT INTO orders (order_id, customer_id, ordered_on, status)
   VALUES (13, 2, '2025-07-01', '受付済');
   INSERT INTO order_items (order_id, product_id, quantity, unit_price)
   VALUES (13, 1, 5, 200);
   UPDATE products SET stock = stock - 5 WHERE product_id = 1;
   COMMIT;

.. code-block:: sql
   :linenos:

   SELECT product_id, name, stock FROM products WHERE product_id = 1;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - product\_id
     - name
     - stock
   * - 1
     - ミルクチョコレート
     - 45

確定した変更は、``ROLLBACK`` を実行しても取り消せません。

トランザクションの途中でエラーが発生した場合
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

トランザクションの途中で文がエラーになったとき、SQLite では、原則としてエラーになった文の変更だけが取り消され、トランザクションは継続します。次の例では、2 つ目の ``INSERT`` 文が外部キーの制約に違反します。

.. code-block:: sql
   :linenos:

   BEGIN;
   INSERT INTO orders (order_id, customer_id, ordered_on, status)
   VALUES (14, 3, '2025-07-02', '受付済');

.. code-block:: sql
   :linenos:

   -- 存在しない商品（product_id が 99）の明細
   INSERT INTO order_items (order_id, product_id, quantity, unit_price)
   VALUES (14, 99, 1, 100);

.. code-block:: text

   sqlite3.IntegrityError: FOREIGN KEY constraint failed

この時点でも、トランザクションは継続しており、注文 14 の追加は取り消されていません。このまま ``COMMIT`` を実行すると、明細のない注文 14 が確定してしまいます。エラーが発生した場合は、アプリケーションの側で ``ROLLBACK`` を実行し、トランザクション全体を取り消す必要があります。

.. code-block:: sql
   :linenos:

   ROLLBACK;

.. code-block:: sql
   :linenos:

   SELECT * FROM orders WHERE order_id = 14;

結果は 0 行です。

エラーが発生したときの動作は DBMS によって異なります。たとえば PostgreSQL では、トランザクション内でエラーが発生すると、そのトランザクションでは ``ROLLBACK`` 以外の文を実行できなくなります。

自動コミット
^^^^^^^^^^^^

``BEGIN`` を実行せずに ``INSERT`` 文などを実行した場合、SQLite はその文だけを含むトランザクションを自動的に開始し、文の実行が終わると自動的に確定します。これを自動コミットと呼びます。10 章と 11 章の例は、自動コミットによって 1 文ごとに確定していました。

複数の文を 1 つずつ自動コミットで実行するよりも、1 つのトランザクションにまとめて実行するほうが、確定の処理が 1 回で済むため、大幅に速くなります。大量の行を追加する場合は、トランザクションにまとめることをお勧めします。

.. note::

   Python の ``sqlite3`` モジュールでは、トランザクションの扱いが SQL を直接実行する場合と異なります。詳しくは 14 章（:doc:`ch14_python`）で説明します。

セーブポイント
^^^^^^^^^^^^^^

``SAVEPOINT`` 文を使うと、トランザクションの途中に名前付きの地点（セーブポイント）を設定できます。``ROLLBACK TO セーブポイント名`` を実行すると、トランザクション全体ではなく、セーブポイント以降の変更だけを取り消せます。

.. code-block:: sql
   :linenos:

   BEGIN;
   UPDATE products SET stock = stock + 100 WHERE product_id = 2;
   SAVEPOINT before_update_3;
   UPDATE products SET stock = stock + 100 WHERE product_id = 3;
   ROLLBACK TO before_update_3;
   COMMIT;

.. code-block:: sql
   :linenos:

   SELECT product_id, name, stock FROM products WHERE product_id IN (2, 3);

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - product\_id
     - name
     - stock
   * - 2
     - ビターチョコレート
     - 130
   * - 3
     - ポテトチップス
     - 80

``product_id`` が 2 の商品の変更は確定し、セーブポイントの後に行った ``product_id`` が 3 の商品の変更は取り消されています。

同時実行の制御
--------------

同時実行で起こる問題
^^^^^^^^^^^^^^^^^^^^

複数のトランザクションが同時に同じデータを読み書きすると、次のような問題が起こることがあります。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 問題
     - 内容
   * - ダーティリード
     - 他のトランザクションが確定していない変更を読んでしまいます。その変更が取り消されると、存在しなかったデータを読んだことになります。
   * - ノンリピータブルリード
     - 同じトランザクション内で同じ行を 2 回読んだとき、間に他のトランザクションが変更を確定したために、異なる値が読まれます。
   * - ファントムリード
     - 同じトランザクション内で同じ条件の検索を 2 回行ったとき、間に他のトランザクションが行を追加したために、1 回目にはなかった行が現れます。

分離レベル
^^^^^^^^^^

標準 SQL では、これらの問題をどこまで防ぐかによって、次の 4 つの分離レベルが定義されています。下にいくほど分離の度合いが高く、問題が起こりにくくなりますが、同時に実行できる処理が制限されやすくなります。

.. list-table::
   :header-rows: 1
   :widths: 31 23 23 23

   * - 分離レベル
     - ダーティリード
     - ノンリピータブルリード
     - ファントムリード
   * - READ UNCOMMITTED
     - 起こりえます
     - 起こりえます
     - 起こりえます
   * - READ COMMITTED
     - 起こりません
     - 起こりえます
     - 起こりえます
   * - REPEATABLE READ
     - 起こりません
     - 起こりません
     - 起こりえます
   * - SERIALIZABLE
     - 起こりません
     - 起こりません
     - 起こりません

既定の分離レベルは DBMS によって異なります。たとえば、PostgreSQL の既定は READ COMMITTED、MySQL（InnoDB）の既定は REPEATABLE READ です。

SQLite の同時実行
^^^^^^^^^^^^^^^^^

SQLite は、データベースのファイル全体に対するロックによって同時実行を制御します。書き込みを行えるトランザクションは、同時に 1 つだけです。そのため、SQLite のトランザクションは SERIALIZABLE に相当する分離を実現しています。

他の接続が書き込み中のときに書き込もうとすると、``database is locked`` というエラーになることがあります。Python の ``sqlite3.connect()`` の ``timeout`` 引数（既定は 5 秒）を指定すると、ロックが解除されるまで待つ時間を設定できます。

SQLite は、1 台のコンピューターで動くアプリケーションや、読み込みが中心の用途に適しています。多数のユーザーが同時に書き込むシステムでは、PostgreSQL や MySQL などのサーバー型の DBMS を使うのが一般的です。

.. _exercises-ch12:

演習問題
--------

1. トランザクションを開始し、すべての商品の在庫数を 0 に更新した後、``ROLLBACK`` で取り消してください。取り消す前と後で、在庫数の合計を確認してください。
2. 1 つのトランザクションで、次の処理を行ってください。

   * 顧客番号 8 の顧客の注文（注文番号 13、注文日 2025-07-05、状態「受付済」）を追加します。
   * 注文 13 に、ノート（商品番号 10）を 3 冊、単価 180 円で追加します。
   * ノートの在庫数を 3 減らします。

   最後に変更を確定し、注文 13 の明細とノートの在庫数を確認してください。

3. トランザクションの途中でエラーが発生した場合、SQLite ではトランザクションがどうなるかを説明してください。また、アプリケーションはどのように対処すべきかを説明してください。

解答は :ref:`answers-ch12` にあります。
