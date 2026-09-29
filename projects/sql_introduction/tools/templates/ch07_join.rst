テーブルの結合
==============

.. sqlfile:: ch07_join 7 章 テーブルの結合

2 章で説明したとおり、リレーショナルデータベースでは、情報の重複を避けるためにデータを複数のテーブルに分けて格納します。たとえば ``orders`` テーブルには顧客の番号だけがあり、顧客の氏名は ``customers`` テーブルにあります。注文と顧客の氏名を一緒に表示するには、2 つのテーブルを組み合わせる必要があります。これを結合（join）と呼びます。

内部結合
--------

INNER JOIN
^^^^^^^^^^

``INNER JOIN`` は、2 つのテーブルの行のうち、指定した条件に一致する行どうしを組み合わせます。条件は ``ON`` の後に書きます。

.. sqlrun::

   SELECT orders.order_id,
          orders.ordered_on,
          customers.name
   FROM orders
   INNER JOIN customers ON orders.customer_id = customers.customer_id;

``orders`` テーブルの各行について、``customer_id`` が等しい ``customers`` テーブルの行が組み合わされています。2 つのテーブルに同じ名前の列（ここでは ``customer_id``）がある場合は、``orders.customer_id`` のように「テーブル名.列名」の形で、どちらのテーブルの列かを明示します。

``INNER JOIN`` の ``INNER`` は省略して ``JOIN`` と書くこともできます。

テーブルの別名
^^^^^^^^^^^^^^

テーブル名の後に別名を書くと、以降はその別名でテーブルを参照できます。結合を使う SQL 文では、テーブルに短い別名を付けるのが一般的です。

.. sqlrun::

   SELECT o.order_id, o.ordered_on, c.name
   FROM orders AS o
   INNER JOIN customers AS c ON o.customer_id = c.customer_id
   WHERE c.prefecture = '東京都'
   ORDER BY o.ordered_on;

この例のように、結合した結果に対して ``WHERE`` 句や ``ORDER BY`` 句を指定できます。

3 つ以上のテーブルの結合
^^^^^^^^^^^^^^^^^^^^^^^^

``JOIN`` を続けて書くと、3 つ以上のテーブルを結合できます。次の例は、注文明細に注文日と商品名を付けて表示します。

.. sqlrun::

   SELECT o.order_id,
          o.ordered_on,
          p.name AS product_name,
          oi.quantity,
          oi.unit_price
   FROM order_items AS oi
   INNER JOIN orders AS o ON oi.order_id = o.order_id
   INNER JOIN products AS p ON oi.product_id = p.product_id
   WHERE o.order_id <= 3
   ORDER BY o.order_id, p.product_id;

結合と集計を組み合わせることもできます。次の例は、顧客ごとの購入金額の合計を求めます。キャンセルされた注文は除きます。

.. sqlrun::

   SELECT c.name,
          SUM(oi.quantity * oi.unit_price) AS total_amount
   FROM customers AS c
   INNER JOIN orders AS o ON c.customer_id = o.customer_id
   INNER JOIN order_items AS oi ON o.order_id = oi.order_id
   WHERE o.status <> 'キャンセル'
   GROUP BY c.customer_id, c.name
   ORDER BY total_amount DESC;

``GROUP BY`` 句に ``c.name`` だけでなく ``c.customer_id`` も指定しているのは、同姓同名の顧客がいた場合に、別々の顧客として集計するためです。

外部結合
--------

LEFT JOIN
^^^^^^^^^

``INNER JOIN`` では、相手のテーブルに一致する行がない行は結果に含まれません。前の例では、一度も注文していない顧客（中村大輔）や、キャンセルした注文しかない顧客（田中健太）は結果に現れていません。

``LEFT JOIN`` は、左側（``FROM`` 句に書いた側）のテーブルの行をすべて残し、右側のテーブルに一致する行がない場合は、右側の列を NULL にして結果に含めます。このような結合を外部結合と呼びます。``LEFT OUTER JOIN`` と書くこともできます。

.. sqlrun::

   SELECT c.customer_id, c.name, o.order_id
   FROM customers AS c
   LEFT JOIN orders AS o ON c.customer_id = o.customer_id
   ORDER BY c.customer_id, o.order_id;

中村大輔（``customer_id`` が 8）の行は、``order_id`` が NULL になって結果に含まれています。

外部結合と集計を組み合わせると、注文のない顧客を 0 件として数えられます。

.. sqlrun::

   SELECT c.name, COUNT(o.order_id) AS order_count
   FROM customers AS c
   LEFT JOIN orders AS o ON c.customer_id = o.customer_id
   GROUP BY c.customer_id, c.name
   ORDER BY c.customer_id;

ここでは ``COUNT(*)`` ではなく ``COUNT(o.order_id)`` を使っている点に注意してください。``COUNT(*)`` は行数を数えるため、注文のない顧客も 1 と数えてしまいます。``COUNT(o.order_id)`` は NULL を数えないため、正しく 0 になります。

相手のない行を探す
^^^^^^^^^^^^^^^^^^

``LEFT JOIN`` の結果のうち、右側の列が NULL の行だけを取り出すと、「相手のテーブルに一致する行がない行」を探せます。次の例は、一度も注文されていない商品を探します。

.. sqlrun::

   SELECT p.product_id, p.name
   FROM products AS p
   LEFT JOIN order_items AS oi ON p.product_id = oi.product_id
   WHERE oi.product_id IS NULL;

ON 句と WHERE 句の違い
^^^^^^^^^^^^^^^^^^^^^^

外部結合では、条件を ``ON`` 句に書くか ``WHERE`` 句に書くかによって結果が変わります。次の 2 つの SQL 文は、どちらも「顧客ごとの、状態が「発送済」の注文の件数」を求めるつもりのものです。

.. sqlrun::

   -- 条件を WHERE 句に書いた場合
   SELECT c.name, COUNT(o.order_id) AS shipped_count
   FROM customers AS c
   LEFT JOIN orders AS o ON c.customer_id = o.customer_id
   WHERE o.status = '発送済'
   GROUP BY c.customer_id, c.name
   ORDER BY c.customer_id;

.. sqlrun::

   -- 条件を ON 句に書いた場合
   SELECT c.name, COUNT(o.order_id) AS shipped_count
   FROM customers AS c
   LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id AND o.status = '発送済'
   GROUP BY c.customer_id, c.name
   ORDER BY c.customer_id;

``WHERE`` 句に書いた場合は、結合した後に絞り込みが行われます。注文のない顧客の行は ``o.status`` が NULL になるため条件が UNKNOWN になり、状態が「発送済」の注文がない顧客の行は条件が FALSE になるため、どちらも除外されてしまいます。その結果、状態が「発送済」の注文が 0 件の顧客（田中健太、山本優子、中村大輔）が表示されません。

``ON`` 句に書いた場合は、状態が「発送済」の注文だけが結合の相手になり、左側の顧客の行はすべて残ります。外部結合で右側のテーブルを絞り込む条件は、``ON`` 句に書くのが基本です。

RIGHT JOIN と FULL JOIN
^^^^^^^^^^^^^^^^^^^^^^^

``RIGHT JOIN`` は、``LEFT JOIN`` とは逆に、右側のテーブルの行をすべて残します。``A RIGHT JOIN B`` は ``B LEFT JOIN A`` と同じ結果になるため、実際には ``LEFT JOIN`` で統一して書くことが多いです。

``FULL JOIN``（``FULL OUTER JOIN``）は、両方のテーブルの行をすべて残し、相手のない側の列を NULL にします。

SQLite では、``RIGHT JOIN`` と ``FULL JOIN`` はバージョン 3.39 から使用できます。MySQL は ``FULL JOIN`` に対応していません。

自己結合
--------

同じテーブルどうしを結合することもできます。これを自己結合と呼びます。自己結合では、同じテーブルに異なる別名を付けて区別します。

次の例は、``categories`` テーブルを自己結合して、各カテゴリの親カテゴリの名前を表示します。

.. sqlrun::

   SELECT child.name AS category, parent.name AS parent_category
   FROM categories AS child
   LEFT JOIN categories AS parent ON child.parent_id = parent.category_id
   ORDER BY child.category_id;

最上位のカテゴリも表示するため、``LEFT JOIN`` を使用しています。

交差結合
--------

``CROSS JOIN`` は、2 つのテーブルの行のすべての組み合わせを作ります。行数が :math:`m` 行と :math:`n` 行のテーブルを交差結合すると、結果は :math:`m \times n` 行になります。

.. sqlrun::

   SELECT c.name AS category, s.status
   FROM categories AS c
   CROSS JOIN (SELECT DISTINCT status FROM orders) AS s
   WHERE c.parent_id IS NULL
   ORDER BY c.category_id, s.status;

この例の ``(SELECT DISTINCT status FROM orders)`` は、``SELECT`` 文の結果をテーブルとして使うサブクエリです。サブクエリについては 8 章で説明します。

交差結合は、すべての組み合わせの一覧表を作る場合などに使用します。``INNER JOIN`` で ``ON`` 句の条件を書き忘れると、SQLite では交差結合と同じ結果になり、大きなテーブルどうしでは膨大な行数になるため注意してください。

集合演算
--------

集合演算は、2 つの ``SELECT`` 文の結果を、行の集合として組み合わせる操作です。結合が列を横に並べるのに対し、集合演算は行を縦に組み合わせます。2 つの ``SELECT`` 文の列の数は一致している必要があります。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 演算子
     - 結果
   * - ``UNION``
     - 両方の結果を合わせたもの（重複する行は 1 行にまとめます）
   * - ``UNION ALL``
     - 両方の結果を合わせたもの（重複する行もそのまま残します）
   * - ``INTERSECT``
     - 両方の結果に含まれる行
   * - ``EXCEPT``
     - 1 つ目の結果に含まれ、2 つ目の結果に含まれない行

次の例では、2025 年 1 月から 2 月に注文した顧客と、2025 年 5 月から 6 月に注文した顧客を比較します。

.. sqlrun::

   -- どちらかの期間に注文した顧客
   SELECT customer_id FROM orders
   WHERE ordered_on BETWEEN '2025-01-01' AND '2025-02-28'
   UNION
   SELECT customer_id FROM orders
   WHERE ordered_on BETWEEN '2025-05-01' AND '2025-06-30';

.. sqlrun::

   -- 両方の期間に注文した顧客
   SELECT customer_id FROM orders
   WHERE ordered_on BETWEEN '2025-01-01' AND '2025-02-28'
   INTERSECT
   SELECT customer_id FROM orders
   WHERE ordered_on BETWEEN '2025-05-01' AND '2025-06-30';

.. sqlrun::

   -- 1 月から 2 月に注文し、5 月から 6 月には注文していない顧客
   SELECT customer_id FROM orders
   WHERE ordered_on BETWEEN '2025-01-01' AND '2025-02-28'
   EXCEPT
   SELECT customer_id FROM orders
   WHERE ordered_on BETWEEN '2025-05-01' AND '2025-06-30';

``UNION`` は重複を取り除く処理が必要なため、重複がないことがわかっている場合や重複を残したい場合は、``UNION ALL`` を使うほうが効率的です。

pandas との対応
---------------

結合は、pandas の ``merge()`` に相当します。``orders`` と ``customers`` は、それぞれのテーブルの内容を格納した DataFrame とします。

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - SQL
     - pandas
   * - ``orders INNER JOIN customers ON orders.customer_id = customers.customer_id``
     - ``orders.merge(customers, on="customer_id", how="inner")``
   * - ``customers LEFT JOIN orders ON customers.customer_id = orders.customer_id``
     - ``customers.merge(orders, on="customer_id", how="left")``
   * - ``FULL JOIN``
     - ``how="outer"``
   * - ``CROSS JOIN``
     - ``how="cross"``
   * - ``UNION ALL``
     - ``pd.concat([df1, df2])``
   * - ``UNION``
     - ``pd.concat([df1, df2]).drop_duplicates()``

pandas の ``merge()`` では、両方の DataFrame に同じ名前の列があると、``name_x`` と ``name_y`` のように接尾辞が付けられます。SQL では、``SELECT`` 句で ``c.name`` のように、どちらのテーブルの列かを明示して選びます。

.. _exercises-ch07:

演習問題
--------

1. ``products`` テーブルと ``categories`` テーブルを結合し、商品名とカテゴリ名を表示してください。カテゴリのない商品も表示し、カテゴリ名は NULL としてください。
2. 注文番号 6 の注文について、商品名、数量、単価、小計（数量と単価を掛けた値）を表示してください。
3. カテゴリごとに、そのカテゴリに属する商品の数を求めてください。商品が 1 つもないカテゴリ（「食品」など）も 0 として表示してください。
4. 一度も注文していない顧客の氏名を、``LEFT JOIN`` を使って取り出してください。
5. 東京都の顧客が注文した商品の商品名を、重複なく取り出してください。キャンセルされた注文は除きます。

解答は :ref:`answers-ch07` にあります。
