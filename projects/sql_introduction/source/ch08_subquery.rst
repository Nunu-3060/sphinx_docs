サブクエリと共通テーブル式
==========================

SQL 文の中に括弧で囲んで書いた ``SELECT`` 文を、サブクエリと呼びます。サブクエリを使うと、「平均より高い価格の商品」のように、別のクエリの結果を条件や計算に利用できます。本章では、サブクエリと、サブクエリを読みやすく書くための共通テーブル式（CTE）を説明します。

スカラーサブクエリ
------------------

結果が 1 行 1 列になるサブクエリを、スカラーサブクエリと呼びます。スカラーサブクエリは、1 つの値として式の中で使用できます。

次の例は、価格が全商品の平均価格より高い商品を取り出します。

.. code-block:: sql
   :linenos:

   SELECT name, price
   FROM products
   WHERE price > (SELECT AVG(price) FROM products)
   ORDER BY price DESC;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - name
     - price
   * - 福袋
     - 3000
   * - ドリップコーヒー
     - 800
   * - 緑茶ティーバッグ
     - 600

先にサブクエリ ``(SELECT AVG(price) FROM products)`` が評価されて平均価格が求まり、その値と各行の ``price`` が比較されます。6 章で説明したとおり ``WHERE`` 句では集約関数を使えないため、``WHERE price > AVG(price)`` とは書けません。

スカラーサブクエリは ``SELECT`` 句にも書けます。

.. code-block:: sql
   :linenos:

   SELECT name,
          price,
          price - (SELECT AVG(price) FROM products) AS diff_from_avg
   FROM products
   WHERE category_id = 8;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - name
     - price
     - diff\_from\_avg
   * - ミルクチョコレート
     - 200
     - -354.16666666666663
   * - ビターチョコレート
     - 250
     - -304.16666666666663

複数行を返すサブクエリ
----------------------

IN とサブクエリ
^^^^^^^^^^^^^^^

``IN`` の括弧内にサブクエリを書くと、サブクエリの結果のいずれかと等しい行を取り出せます。次の例は、「ドリップコーヒー」（``product_id`` が 6）を注文したことのある顧客を取り出します。

.. code-block:: sql
   :linenos:

   SELECT customer_id, name
   FROM customers
   WHERE customer_id IN (
       SELECT o.customer_id
       FROM orders AS o
       INNER JOIN order_items AS oi ON o.order_id = oi.order_id
       WHERE oi.product_id = 6
   );

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - customer\_id
     - name
   * - 1
     - 佐藤花子
   * - 2
     - 鈴木一郎

``IN`` に使うサブクエリは、1 列の結果を返す必要があります。

EXISTS
^^^^^^

``EXISTS (サブクエリ)`` は、サブクエリの結果が 1 行以上あれば TRUE、1 行もなければ FALSE になります。``NOT EXISTS`` はその逆です。次の例は、一度も注文していない顧客を取り出します。

.. code-block:: sql
   :linenos:

   SELECT c.customer_id, c.name
   FROM customers AS c
   WHERE NOT EXISTS (
       SELECT 1
       FROM orders AS o
       WHERE o.customer_id = c.customer_id
   );

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - customer\_id
     - name
   * - 8
     - 中村大輔

``EXISTS`` は行があるかどうかだけを調べるため、サブクエリの ``SELECT`` 句には何を書いてもかまいません。慣例として ``SELECT 1`` と書くことが多いです。

このサブクエリの中では、外側のクエリの ``c.customer_id`` を参照しています。このように外側のクエリの値を参照するサブクエリを、相関サブクエリと呼びます。相関サブクエリは、外側のクエリの行ごとに評価されると考えることができます。

NOT IN と NOT EXISTS
^^^^^^^^^^^^^^^^^^^^

「一度も注文されていない商品」は、``NOT IN`` を使って次のように書くこともできます。

.. code-block:: sql
   :linenos:

   SELECT product_id, name
   FROM products
   WHERE product_id NOT IN (SELECT product_id FROM order_items);

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - product\_id
     - name
   * - 12
     - 抹茶ラテ

ただし、5 章で説明したとおり、``NOT IN`` のサブクエリの結果に NULL が含まれると、結果は 1 行もなくなります。次の例は、どの商品にも使われていないカテゴリを探すつもりの SQL 文ですが、``products`` テーブルの ``category_id`` 列には NULL（福袋）が含まれるため、結果が空になります。

.. code-block:: sql
   :linenos:

   SELECT category_id, name
   FROM categories
   WHERE category_id NOT IN (SELECT category_id FROM products);

結果は 0 行です。

``NOT EXISTS`` を使えば、NULL の影響を受けずに正しい結果が得られます。

.. code-block:: sql
   :linenos:

   SELECT c.category_id, c.name
   FROM categories AS c
   WHERE NOT EXISTS (
       SELECT 1 FROM products AS p WHERE p.category_id = c.category_id
   );

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - category\_id
     - name
   * - 1
     - 食品
   * - 2
     - 飲料

サブクエリの結果に NULL が含まれる可能性がある場合は、``NOT IN`` ではなく ``NOT EXISTS`` を使うことをお勧めします。

相関サブクエリ
--------------

相関サブクエリは、``EXISTS`` 以外でも使用できます。次の例は、同じカテゴリの商品の平均価格より高い商品を取り出します。

.. code-block:: sql
   :linenos:

   SELECT p.name, p.category_id, p.price
   FROM products AS p
   WHERE p.price > (
       SELECT AVG(p2.price)
       FROM products AS p2
       WHERE p2.category_id = p.category_id
   )
   ORDER BY p.category_id;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - name
     - category\_id
     - price
   * - ノート
     - 3
     - 180
   * - 味噌
     - 5
     - 500
   * - ドリップコーヒー
     - 6
     - 800
   * - 緑茶ティーバッグ
     - 7
     - 600
   * - ビターチョコレート
     - 8
     - 250

サブクエリ内の ``p2.category_id = p.category_id`` によって、外側の行と同じカテゴリの商品だけの平均価格が求められます。同じ処理は、9 章で説明するウィンドウ関数を使っても書けます。

FROM 句のサブクエリ
-------------------

``FROM`` 句にサブクエリを書くと、サブクエリの結果をテーブルのように扱えます。このようなサブクエリには別名を付けます。次の例は、顧客ごとの購入金額を求めた結果から、購入金額の平均を求めます。

.. code-block:: sql
   :linenos:

   SELECT COUNT(*) AS customer_count,
          AVG(total_amount) AS avg_amount
   FROM (
       SELECT o.customer_id,
              SUM(oi.quantity * oi.unit_price) AS total_amount
       FROM orders AS o
       INNER JOIN order_items AS oi ON o.order_id = oi.order_id
       WHERE o.status <> 'キャンセル'
       GROUP BY o.customer_id
   ) AS customer_totals;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - customer\_count
     - avg\_amount
   * - 6
     - 2325.0

集計した結果をさらに集計する場合は、このように ``FROM`` 句のサブクエリを使用します。

共通テーブル式
--------------

WITH 句
^^^^^^^

サブクエリを何重にも入れ子にすると、SQL 文が読みにくくなります。``WITH`` 句を使うと、サブクエリに名前を付けて、本体のクエリより前に書けます。``WITH`` 句で定義した一時的な結果を、共通テーブル式（CTE、Common Table Expression）と呼びます。

前の節の例は、``WITH`` 句を使って次のように書けます。

.. code-block:: sql
   :linenos:

   WITH customer_totals AS (
       SELECT o.customer_id,
              SUM(oi.quantity * oi.unit_price) AS total_amount
       FROM orders AS o
       INNER JOIN order_items AS oi ON o.order_id = oi.order_id
       WHERE o.status <> 'キャンセル'
       GROUP BY o.customer_id
   )
   SELECT COUNT(*) AS customer_count,
          AVG(total_amount) AS avg_amount
   FROM customer_totals;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - customer\_count
     - avg\_amount
   * - 6
     - 2325.0

処理の流れを上から下へ読めるため、Python で中間結果を変数に代入しながら処理を進めるのと同じ感覚で書けます。

複数の CTE
^^^^^^^^^^

コンマで区切って複数の CTE を定義できます。後の CTE では、前に定義した CTE を参照できます。次の例は、購入金額が平均以上の顧客の氏名を取り出します。

.. code-block:: sql
   :linenos:

   WITH customer_totals AS (
       SELECT o.customer_id,
              SUM(oi.quantity * oi.unit_price) AS total_amount
       FROM orders AS o
       INNER JOIN order_items AS oi ON o.order_id = oi.order_id
       WHERE o.status <> 'キャンセル'
       GROUP BY o.customer_id
   ),
   average AS (
       SELECT AVG(total_amount) AS avg_amount FROM customer_totals
   )
   SELECT c.name, t.total_amount
   FROM customer_totals AS t
   INNER JOIN customers AS c ON t.customer_id = c.customer_id
   CROSS JOIN average AS a
   WHERE t.total_amount >= a.avg_amount
   ORDER BY t.total_amount DESC;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - name
     - total\_amount
   * - 佐藤花子
     - 3870
   * - 鈴木一郎
     - 3500
   * - 伊藤さくら
     - 2880

再帰 CTE
--------

``WITH RECURSIVE`` を使うと、CTE の中で自分自身を参照する再帰的なクエリを書けます。再帰 CTE は、階層構造のデータをたどる場合によく使用します。

再帰 CTE は、次の 2 つの部分を ``UNION ALL`` でつないで書きます。

* 初期部分：再帰の出発点となる行を求める ``SELECT`` 文
* 再帰部分：CTE 自身を参照し、前の段階で得られた行から次の行を求める ``SELECT`` 文

再帰部分が新しい行を返さなくなった時点で、処理が終了します。

簡単な例として、1 から 5 までの整数を生成します。

.. code-block:: sql
   :linenos:

   WITH RECURSIVE numbers (n) AS (
       SELECT 1                              -- 初期部分
       UNION ALL
       SELECT n + 1 FROM numbers WHERE n < 5 -- 再帰部分
   )
   SELECT n FROM numbers;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - n
   * - 1
   * - 2
   * - 3
   * - 4
   * - 5

CTE 名の後の ``(n)`` は、CTE の列名を指定しています。初期部分で ``n`` が 1 の行ができ、再帰部分が ``n`` が 5 になるまで 1 ずつ増やした行を追加します。``WHERE n < 5`` の終了条件を書き忘れると、無限に行が生成されるので注意してください。

次の例は、``categories`` テーブルの階層をたどり、各カテゴリの最上位からの経路を求めます。

.. code-block:: sql
   :linenos:

   WITH RECURSIVE category_path (category_id, name, path, depth) AS (
       -- 初期部分：最上位のカテゴリ
       SELECT category_id, name, name, 1
       FROM categories
       WHERE parent_id IS NULL
       UNION ALL
       -- 再帰部分：1 つ上の段階で得られたカテゴリの子カテゴリ
       SELECT c.category_id, c.name, cp.path || ' > ' || c.name, cp.depth + 1
       FROM categories AS c
       INNER JOIN category_path AS cp ON c.parent_id = cp.category_id
   )
   SELECT category_id, path, depth
   FROM category_path
   ORDER BY path;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - category\_id
     - path
     - depth
   * - 3
     - 文房具
     - 1
   * - 1
     - 食品
     - 1
   * - 4
     - 食品 \> 菓子
     - 2
   * - 8
     - 食品 \> 菓子 \> チョコレート
     - 3
   * - 5
     - 食品 \> 調味料
     - 2
   * - 2
     - 飲料
     - 1
   * - 7
     - 飲料 \> お茶
     - 2
   * - 6
     - 飲料 \> コーヒー
     - 2

初期部分で最上位の 3 つのカテゴリが得られ、再帰部分で「その子カテゴリ」「さらにその子カテゴリ」と順にたどっていきます。子カテゴリがなくなると再帰部分が行を返さなくなり、処理が終了します。

.. _exercises-ch08:

演習問題
--------

1. 最も価格の高い商品の商品名と価格を、サブクエリを使って取り出してください（``ORDER BY`` 句と ``LIMIT`` 句は使わないでください）。
2. 一度でも「キャンセル」の注文をしたことがある顧客の氏名を、``EXISTS`` を使って取り出してください。
3. 各商品について、商品名、価格、同じカテゴリの商品の最高価格を表示してください。カテゴリのない商品は除いてください。
4. ``WITH`` 句を使い、注文ごとの合計金額を求めたうえで、合計金額が 1000 円以上の注文の件数を求めてください。キャンセルされた注文は除きます。
5. 再帰 CTE を使い、「食品」カテゴリ（``category_id`` が 1）とその下位のすべてのカテゴリの ``category_id`` と名前を取り出してください。

解答は :ref:`answers-ch08` にあります。
