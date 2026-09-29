ウィンドウ関数
==============

6 章で説明した ``GROUP BY`` 句を使うと、グループごとに 1 行にまとめた集計結果が得られます。しかし、「各商品の価格と、その商品が属するカテゴリの平均価格を並べて表示する」のように、元の行を残したまま集計した値を使いたい場合もあります。このような場合に使用するのがウィンドウ関数です。

ウィンドウ関数の基本
--------------------

OVER 句
^^^^^^^

集約関数の後に ``OVER`` 句を付けると、ウィンドウ関数として動作します。ウィンドウ関数は、行をまとめずに、各行に集計結果を付け加えます。

.. code-block:: sql
   :linenos:

   SELECT name,
          price,
          AVG(price) OVER () AS avg_price
   FROM products
   ORDER BY product_id;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - name
     - price
     - avg\_price
   * - ミルクチョコレート
     - 200
     - 554.1666666666666
   * - ビターチョコレート
     - 250
     - 554.1666666666666
   * - ポテトチップス
     - 150
     - 554.1666666666666
   * - 醤油
     - 400
     - 554.1666666666666
   * - 味噌
     - 500
     - 554.1666666666666
   * - ドリップコーヒー
     - 800
     - 554.1666666666666
   * - 缶コーヒー
     - 120
     - 554.1666666666666
   * - 緑茶ティーバッグ
     - 600
     - 554.1666666666666
   * - ボールペン
     - 100
     - 554.1666666666666
   * - ノート
     - 180
     - 554.1666666666666
   * - 福袋
     - 3000
     - 554.1666666666666
   * - 抹茶ラテ
     - 350
     - 554.1666666666666

``OVER ()`` の括弧内が空の場合、すべての行が集計の対象になります。集計の対象となる行の範囲をウィンドウと呼びます。``GROUP BY`` 句を使った場合と異なり、結果の行数は元のテーブルと同じです。

PARTITION BY
^^^^^^^^^^^^

``OVER`` 句の中に ``PARTITION BY`` を書くと、指定した列の値ごとに行を区切り、区切った範囲ごとに集計します。``GROUP BY`` 句と似ていますが、行はまとめられません。

.. code-block:: sql
   :linenos:

   SELECT name,
          category_id,
          price,
          AVG(price) OVER (PARTITION BY category_id) AS category_avg,
          price - AVG(price) OVER (PARTITION BY category_id) AS diff
   FROM products
   WHERE category_id IS NOT NULL
   ORDER BY category_id, price;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - name
     - category\_id
     - price
     - category\_avg
     - diff
   * - ボールペン
     - 3
     - 100
     - 140.0
     - -40.0
   * - ノート
     - 3
     - 180
     - 140.0
     - 40.0
   * - ポテトチップス
     - 4
     - 150
     - 150.0
     - 0.0
   * - 醤油
     - 5
     - 400
     - 450.0
     - -50.0
   * - 味噌
     - 5
     - 500
     - 450.0
     - 50.0
   * - 缶コーヒー
     - 6
     - 120
     - 460.0
     - -340.0
   * - ドリップコーヒー
     - 6
     - 800
     - 460.0
     - 340.0
   * - 抹茶ラテ
     - 7
     - 350
     - 475.0
     - -125.0
   * - 緑茶ティーバッグ
     - 7
     - 600
     - 475.0
     - 125.0
   * - ミルクチョコレート
     - 8
     - 200
     - 225.0
     - -25.0
   * - ビターチョコレート
     - 8
     - 250
     - 225.0
     - 25.0

8 章では、同じカテゴリの平均価格と比較するために相関サブクエリを使いましたが、ウィンドウ関数を使うと、より簡潔に書けます。

順位を付ける
------------

``OVER`` 句の中に ``ORDER BY`` を書くと、行の順序を考慮した計算ができます。順位を付ける次の関数は、``OVER`` 句の中の ``ORDER BY`` と組み合わせて使用します。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 関数
     - 説明
   * - ``ROW_NUMBER()``
     - 1 から始まる連番。値が同じ行にも異なる番号を付けます
   * - ``RANK()``
     - 順位。値が同じ行には同じ順位を付け、次の順位は同順位の行数だけ飛ばします（1, 2, 2, 4）
   * - ``DENSE_RANK()``
     - 順位。値が同じ行には同じ順位を付け、次の順位は飛ばしません（1, 2, 2, 3）

次の例は、顧客を注文回数の多い順に並べ、3 種類の方法で順位を付けます。

.. code-block:: sql
   :linenos:

   WITH order_counts AS (
       SELECT customer_id, COUNT(*) AS order_count
       FROM orders
       GROUP BY customer_id
   )
   SELECT customer_id,
          order_count,
          ROW_NUMBER() OVER (ORDER BY order_count DESC, customer_id) AS row_num,
          RANK() OVER (ORDER BY order_count DESC) AS rank_no,
          DENSE_RANK() OVER (ORDER BY order_count DESC) AS dense_rank_no
   FROM order_counts
   ORDER BY order_count DESC, customer_id;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - customer\_id
     - order\_count
     - row\_num
     - rank\_no
     - dense\_rank\_no
   * - 1
     - 3
     - 1
     - 1
     - 1
   * - 2
     - 2
     - 2
     - 2
     - 2
   * - 3
     - 2
     - 3
     - 2
     - 2
   * - 5
     - 2
     - 4
     - 2
     - 2
   * - 4
     - 1
     - 5
     - 5
     - 3
   * - 6
     - 1
     - 6
     - 5
     - 3
   * - 7
     - 1
     - 7
     - 5
     - 3

``ROW_NUMBER()`` では、注文回数が同じ顧客にも異なる番号が付きます。この例では、番号の付け方を確定させるため、``ROW_NUMBER()`` の ``OVER`` 句の ``ORDER BY`` に ``customer_id`` を追加しています。追加しない場合、注文回数が同じ顧客のうち、どの顧客にどの番号が付くかは保証されません。

``PARTITION BY`` と組み合わせると、グループごとに順位を付けられます。次の例は、カテゴリごとに価格の高い順の順位を付けます。

.. code-block:: sql
   :linenos:

   SELECT name,
          category_id,
          price,
          RANK() OVER (PARTITION BY category_id ORDER BY price DESC) AS price_rank
   FROM products
   WHERE category_id IS NOT NULL
   ORDER BY category_id, price_rank;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - name
     - category\_id
     - price
     - price\_rank
   * - ノート
     - 3
     - 180
     - 1
   * - ボールペン
     - 3
     - 100
     - 2
   * - ポテトチップス
     - 4
     - 150
     - 1
   * - 味噌
     - 5
     - 500
     - 1
   * - 醤油
     - 5
     - 400
     - 2
   * - ドリップコーヒー
     - 6
     - 800
     - 1
   * - 缶コーヒー
     - 6
     - 120
     - 2
   * - 緑茶ティーバッグ
     - 7
     - 600
     - 1
   * - 抹茶ラテ
     - 7
     - 350
     - 2
   * - ビターチョコレート
     - 8
     - 250
     - 1
   * - ミルクチョコレート
     - 8
     - 200
     - 2

グループごとの上位の行を取り出す
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

「カテゴリごとに最も高い商品」のように、グループごとの上位の行を取り出したい場合があります。ウィンドウ関数は ``WHERE`` 句では使えないため、次のように CTE（またはサブクエリ）で順位を求めてから絞り込みます。

.. code-block:: sql
   :linenos:

   WITH ranked AS (
       SELECT name,
              category_id,
              price,
              ROW_NUMBER() OVER (
                  PARTITION BY category_id ORDER BY price DESC
              ) AS row_num
       FROM products
       WHERE category_id IS NOT NULL
   )
   SELECT name, category_id, price
   FROM ranked
   WHERE row_num = 1
   ORDER BY category_id;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - name
     - category\_id
     - price
   * - ノート
     - 3
     - 180
   * - ポテトチップス
     - 4
     - 150
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

ウィンドウ関数を ``WHERE`` 句で使えないのは、6 章で説明した評価順序で、ウィンドウ関数が ``SELECT`` 句と同じ段階（``WHERE`` 句より後）で評価されるためです。

累計と移動平均
--------------

累計
^^^^

``SUM()`` などの集約関数を、``ORDER BY`` を含む ``OVER`` 句と組み合わせると、先頭の行から現在の行までの累計を求められます。次の例は、月ごとの売上金額と、その累計を求めます。キャンセルされた注文は除きます。

.. code-block:: sql
   :linenos:

   WITH monthly_sales AS (
       SELECT strftime('%Y-%m', o.ordered_on) AS month,
              SUM(oi.quantity * oi.unit_price) AS sales
       FROM orders AS o
       INNER JOIN order_items AS oi ON o.order_id = oi.order_id
       WHERE o.status <> 'キャンセル'
       GROUP BY month
   )
   SELECT month,
          sales,
          SUM(sales) OVER (ORDER BY month) AS cumulative_sales
   FROM monthly_sales
   ORDER BY month;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - month
     - sales
     - cumulative\_sales
   * - 2025-01
     - 3100
     - 3100
   * - 2025-02
     - 2070
     - 5170
   * - 2025-03
     - 1900
     - 7070
   * - 2025-04
     - 2350
     - 9420
   * - 2025-05
     - 2940
     - 12360
   * - 2025-06
     - 1590
     - 13950

フレーム
^^^^^^^^

ウィンドウの中で、実際に集計の対象とする行の範囲をフレームと呼びます。``OVER`` 句で ``ORDER BY`` を指定した場合、既定のフレームは「先頭の行から、現在の行と ``ORDER BY`` の値が等しい最後の行まで」です。前の例で累計が求められたのは、この既定のフレームによるものです。

フレームは、``ROWS BETWEEN 開始 AND 終了`` の形で明示的に指定できます。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 指定
     - 意味
   * - ``UNBOUNDED PRECEDING``
     - ウィンドウの先頭の行
   * - ``n PRECEDING``
     - 現在の行の n 行前
   * - ``CURRENT ROW``
     - 現在の行
   * - ``n FOLLOWING``
     - 現在の行の n 行後
   * - ``UNBOUNDED FOLLOWING``
     - ウィンドウの最後の行

次の例は、直前の 2 か月と当月の 3 か月分の売上金額の平均（3 か月移動平均）を求めます。

.. code-block:: sql
   :linenos:

   WITH monthly_sales AS (
       SELECT strftime('%Y-%m', o.ordered_on) AS month,
              SUM(oi.quantity * oi.unit_price) AS sales
       FROM orders AS o
       INNER JOIN order_items AS oi ON o.order_id = oi.order_id
       WHERE o.status <> 'キャンセル'
       GROUP BY month
   )
   SELECT month,
          sales,
          round(AVG(sales) OVER (
              ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
          ), 1) AS moving_avg
   FROM monthly_sales
   ORDER BY month;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - month
     - sales
     - moving\_avg
   * - 2025-01
     - 3100
     - 3100.0
   * - 2025-02
     - 2070
     - 2585.0
   * - 2025-03
     - 1900
     - 2356.7
   * - 2025-04
     - 2350
     - 2106.7
   * - 2025-05
     - 2940
     - 2396.7
   * - 2025-06
     - 1590
     - 2293.3

最初の 2 か月は、前の月が 2 か月分そろっていないため、存在する行だけで平均が計算されます。

.. note::

   既定のフレームでは、``ORDER BY`` の値が等しい行はまとめて扱われます。そのため、``ORDER BY`` の値に重複があると、累計の途中の値が期待どおりにならないことがあります。重複がありうる場合は、``ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`` を明示的に指定すると、1 行ずつ累計できます。

前後の行を参照する
------------------

``LAG(列, n)`` は現在の行の n 行前の値を、``LEAD(列, n)`` は n 行後の値を返します。n を省略すると 1 とみなされます。該当する行がない場合は NULL を返します。次の例は、前月の売上金額と、前月からの増減を求めます。

.. code-block:: sql
   :linenos:

   WITH monthly_sales AS (
       SELECT strftime('%Y-%m', o.ordered_on) AS month,
              SUM(oi.quantity * oi.unit_price) AS sales
       FROM orders AS o
       INNER JOIN order_items AS oi ON o.order_id = oi.order_id
       WHERE o.status <> 'キャンセル'
       GROUP BY month
   )
   SELECT month,
          sales,
          LAG(sales) OVER (ORDER BY month) AS prev_sales,
          sales - LAG(sales) OVER (ORDER BY month) AS diff
   FROM monthly_sales
   ORDER BY month;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - month
     - sales
     - prev\_sales
     - diff
   * - 2025-01
     - 3100
     - NULL
     - NULL
   * - 2025-02
     - 2070
     - 3100
     - -1030
   * - 2025-03
     - 1900
     - 2070
     - -170
   * - 2025-04
     - 2350
     - 1900
     - 450
   * - 2025-05
     - 2940
     - 2350
     - 590
   * - 2025-06
     - 1590
     - 2940
     - -1350

最初の月には前月の行がないため、``prev_sales`` と ``diff`` は NULL になります。

pandas との対応
---------------

ウィンドウ関数の多くは、pandas の ``groupby()`` と ``transform()``、``rank()``、``cumsum()``、``shift()``、``rolling()`` などに対応します。``df`` は ``products`` テーブルの内容を、``sales`` は月ごとの売上金額を格納した DataFrame とします。

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - SQL
     - pandas
   * - ``AVG(price) OVER (PARTITION BY category_id)``
     - ``df.groupby("category_id")["price"].transform("mean")``
   * - ``RANK() OVER (ORDER BY price DESC)``
     - ``df["price"].rank(method="min", ascending=False)``
   * - ``DENSE_RANK() OVER (ORDER BY price DESC)``
     - ``df["price"].rank(method="dense", ascending=False)``
   * - ``ROW_NUMBER() OVER (ORDER BY price DESC)``
     - ``df["price"].rank(method="first", ascending=False)``
   * - ``SUM(sales) OVER (ORDER BY month)``
     - ``sales.sort_values("month")["sales"].cumsum()``
   * - ``AVG(sales) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)``
     - ``sales.sort_values("month")["sales"].rolling(3, min_periods=1).mean()``
   * - ``LAG(sales) OVER (ORDER BY month)``
     - ``sales.sort_values("month")["sales"].shift(1)``

.. _exercises-ch09:

演習問題
--------

1. 各商品について、商品名、価格、全商品の価格の合計に対する割合（パーセント、小数点以下 1 桁）を表示してください。
2. 顧客を登録日の古い順に並べ、1 から始まる連番を付けてください。
3. 都道府県ごとに、顧客を登録日の古い順に並べ、都道府県内での連番を付けてください。
4. 注文明細から、注文ごとに小計（数量と単価を掛けた値）が最も大きい明細の注文番号、商品番号、小計を取り出してください。
5. 各顧客の注文を注文日の順に並べ、前回の注文日と、前回の注文からの経過日数を表示してください。経過日数は ``julianday(ordered_on) - julianday(前回の注文日)`` で求められます。

解答は :ref:`answers-ch09` にあります。
