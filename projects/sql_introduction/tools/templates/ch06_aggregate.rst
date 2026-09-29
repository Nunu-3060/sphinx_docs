集計とグループ化
================

.. sqlfile:: ch06_aggregate 6 章 集計とグループ化

本章では、複数の行をまとめて合計や平均などを求める方法を説明します。

集約関数
--------

複数の行の値から 1 つの値を求める関数を、集約関数と呼びます。主な集約関数は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 関数
     - 説明
   * - ``COUNT(*)``
     - 行数
   * - ``COUNT(列)``
     - 列の値が NULL でない行の数
   * - ``SUM(列)``
     - 列の値の合計
   * - ``AVG(列)``
     - 列の値の平均
   * - ``MIN(列)``
     - 列の値の最小値
   * - ``MAX(列)``
     - 列の値の最大値

集約関数を使うと、テーブル全体が 1 行にまとめられます。

.. sqlrun::

   SELECT COUNT(*) AS product_count,
          SUM(stock) AS total_stock,
          AVG(price) AS avg_price,
          MIN(price) AS min_price,
          MAX(price) AS max_price
   FROM products;

``WHERE`` 句と組み合わせると、条件に合う行だけを集計できます。

.. sqlrun::

   SELECT COUNT(*) AS order_count
   FROM orders
   WHERE status = '発送済';

集約関数と NULL
^^^^^^^^^^^^^^^

``COUNT(*)`` 以外の集約関数は、NULL の値を無視して計算します。``COUNT(*)`` と ``COUNT(email)`` の結果を比べると、違いがわかります。

.. sqlrun::

   SELECT COUNT(*) AS customer_count,
          COUNT(email) AS email_count
   FROM customers;

``AVG()`` も NULL の行を除いて平均を求めます。NULL を 0 とみなして平均を求めたい場合は、``AVG(COALESCE(列, 0))`` のように書きます。また、対象の行が 1 行もない場合、``COUNT()`` は 0 を返しますが、``SUM()`` や ``AVG()`` などは NULL を返します。

.. sqlrun::

   SELECT COUNT(*) AS cnt, SUM(price) AS total
   FROM products
   WHERE price > 10000;

重複を除いて数える
^^^^^^^^^^^^^^^^^^

``COUNT(DISTINCT 列)`` と書くと、重複を除いた値の種類の数を数えます。次の例は、注文したことのある顧客の人数を求めます。

.. sqlrun::

   SELECT COUNT(*) AS order_count,
          COUNT(DISTINCT customer_id) AS customer_count
   FROM orders;

グループごとに集計する
----------------------

GROUP BY 句
^^^^^^^^^^^

``GROUP BY`` 句を使うと、指定した列の値が等しい行をグループにまとめ、グループごとに集計できます。次の例は、注文の状態ごとに注文の件数を求めます。

.. sqlrun::

   SELECT status, COUNT(*) AS order_count
   FROM orders
   GROUP BY status;

``GROUP BY status`` によって、``orders`` テーブルの行が ``status`` 列の値ごとにグループに分けられ、``COUNT(*)`` はグループごとの行数を返します。

次の例は、注文ごとの合計金額を求めます。合計金額は、注文明細の数量と単価を掛けた値の合計です。

.. sqlrun::

   SELECT order_id,
          COUNT(*) AS item_count,
          SUM(quantity * unit_price) AS amount
   FROM order_items
   GROUP BY order_id;

複数の列を指定すると、それらの列の値の組ごとにグループを作ります。次の例は、注文日の年月と状態の組ごとに注文の件数を求めます。

.. sqlrun::

   SELECT strftime('%Y-%m', ordered_on) AS month,
          status,
          COUNT(*) AS order_count
   FROM orders
   GROUP BY month, status
   ORDER BY month, status;

この例のように、``GROUP BY`` 句には列名だけでなく式や列の別名も指定できます。ただし、``GROUP BY`` 句で ``SELECT`` 句の別名を使えない DBMS もあります。その場合は ``GROUP BY strftime('%Y-%m', ordered_on), status`` のように式をそのまま書きます。

NULL のグループ
^^^^^^^^^^^^^^^

``GROUP BY`` 句では、NULL の値どうしは同じグループにまとめられます。

.. sqlrun::

   SELECT category_id, COUNT(*) AS product_count
   FROM products
   GROUP BY category_id;

SELECT 句に書ける列
^^^^^^^^^^^^^^^^^^^

``GROUP BY`` 句を使う場合、``SELECT`` 句に書けるのは、原則として ``GROUP BY`` 句に指定した列と集約関数だけです。たとえば、次の SQL 文の ``name`` 列は、グループ内に複数の値があるため、どの値を表示すればよいかが決まりません。

.. code-block:: sql
   :linenos:

   -- 誤った例
   SELECT category_id, name, COUNT(*)
   FROM products
   GROUP BY category_id;

多くの DBMS では、この SQL 文はエラーになります。SQLite ではエラーにならず、グループ内のいずれかの行の値が表示されますが、どの行の値になるかは保証されません。このような書き方は避けてください。

グループを絞り込む
------------------

HAVING 句
^^^^^^^^^

集計した結果に対して条件を指定するには、``HAVING`` 句を使用します。次の例は、2 回以上注文した顧客を取り出します。

.. sqlrun::

   SELECT customer_id, COUNT(*) AS order_count
   FROM orders
   GROUP BY customer_id
   HAVING COUNT(*) >= 2;

WHERE 句と HAVING 句の違い
^^^^^^^^^^^^^^^^^^^^^^^^^^

``WHERE`` 句と ``HAVING`` 句は、どちらも条件で絞り込みを行いますが、絞り込む対象が異なります。

* ``WHERE`` 句は、グループにまとめる前の個々の行を絞り込みます。そのため、集約関数は使えません。
* ``HAVING`` 句は、グループにまとめた後のグループを絞り込みます。

次の例は、状態が「発送済」の注文だけを対象にしたうえで（``WHERE`` 句）、2 回以上注文した顧客（``HAVING`` 句）を取り出します。

.. sqlrun::

   SELECT customer_id, COUNT(*) AS order_count
   FROM orders
   WHERE status = '発送済'
   GROUP BY customer_id
   HAVING COUNT(*) >= 2;

個々の行に対する条件は ``HAVING`` 句にも書けますが、``WHERE`` 句に書くほうが、集計の対象となる行が先に減るため効率的です。

SELECT 文の評価順序
-------------------

``SELECT`` 文の各句は、書く順序とは異なる次の順序で評価されると考えることができます。

.. list-table::
   :header-rows: 1
   :widths: 10 30 60

   * - 順序
     - 句
     - 処理
   * - 1
     - ``FROM``
     - 対象のテーブルを決めます
   * - 2
     - ``WHERE``
     - 行を絞り込みます
   * - 3
     - ``GROUP BY``
     - 行をグループにまとめます
   * - 4
     - ``HAVING``
     - グループを絞り込みます
   * - 5
     - ``SELECT``
     - 結果の列を計算します
   * - 6
     - ``ORDER BY``
     - 結果を並べ替えます
   * - 7
     - ``LIMIT``
     - 結果の行数を制限します

この順序は論理的なものであり、DBMS が実際にこの順序で処理するとは限りません。しかし、この順序を知っていると、次のような規則を理解しやすくなります。

* ``WHERE`` 句で集約関数を使えないのは、``WHERE`` 句の評価がグループ化より前に行われるためです。
* ``ORDER BY`` 句で ``SELECT`` 句の別名を使えるのは、``ORDER BY`` 句の評価が ``SELECT`` 句より後に行われるためです。
* 標準 SQL では、``WHERE`` 句で ``SELECT`` 句の別名を使えません。``WHERE`` 句の評価が ``SELECT`` 句より前に行われるためです。SQLite では例外的に使えますが、他の DBMS との互換性のため避けることをお勧めします。

pandas との対応
---------------

本章で説明した操作は、pandas では次のように書けます。``orders`` は ``orders`` テーブルの内容を格納した DataFrame とします。

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - SQL
     - pandas
   * - ``SELECT COUNT(*) FROM orders``
     - ``len(orders)``
   * - ``SELECT COUNT(DISTINCT customer_id) FROM orders``
     - ``orders["customer_id"].nunique()``
   * - ``SELECT status, COUNT(*) FROM orders GROUP BY status``
     - ``orders.groupby("status").size()``
   * - ``... GROUP BY customer_id HAVING COUNT(*) >= 2``
     - ``s = orders.groupby("customer_id").size()`` の後に ``s[s >= 2]``

pandas の ``groupby()`` は、既定では NULL（欠損値）のグループを結果から除外します。SQL と同じように欠損値のグループを残すには、``groupby("category_id", dropna=False)`` のように指定します。

.. _exercises-ch06:

演習問題
--------

1. ``products`` テーブルから、在庫金額（価格と在庫数を掛けた値）の合計を求めてください。
2. ``customers`` テーブルから、都道府県ごとの顧客数を、顧客数の多い順に求めてください。顧客数が同じ場合は、都道府県名の順に並べてください。
3. ``order_items`` テーブルから、商品ごとの販売数量の合計を求め、合計が 5 個以上の商品の商品番号と販売数量の合計を取り出してください。
4. ``orders`` テーブルから、キャンセルされた注文を除き、月ごとの注文件数を求めてください。月は ``2025-01`` の形式で表示してください。

解答は :ref:`answers-ch06` にあります。
