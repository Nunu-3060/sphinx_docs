付録 A 演習問題の解答
=====================

各章の演習問題の解答例を示します。解答は一例であり、同じ結果が得られる別の書き方もあります。解答例の SQL は、``examples/sql`` フォルダーの ``answers_ch04.sql`` から ``answers_ch13.sql`` に章ごとに収録しています。各ファイルは、サンプルデータベースの初期状態から実行するものとします。

.. _answers-ch04:

4 章 データの取得
-----------------

.. sqlfile:: answers_ch04 4 章 データの取得 演習問題の解答

問題 1
^^^^^^

.. sqlrun::

   SELECT name, registered_on
   FROM customers
   WHERE registered_on >= '2024-01-01' AND registered_on < '2025-01-01'
   ORDER BY registered_on;

``WHERE registered_on BETWEEN '2024-01-01' AND '2024-12-31'`` と書くこともできます。ただし、値に時刻を含む ``'2024-12-31 10:00:00'`` のような形式の場合、この値は ``'2024-12-31'`` より大きいため、``BETWEEN`` では 12 月 31 日の行が漏れてしまいます。「翌年 1 月 1 日より前」という条件にしておくと、値に時刻が含まれていても正しく判定できます。

問題 2
^^^^^^

.. sqlrun::

   SELECT name, stock
   FROM products
   WHERE stock <= 20;

問題 3
^^^^^^

.. sqlrun::

   SELECT name, price
   FROM products
   WHERE name LIKE '%チョコ%' OR price <= 100;

問題 4
^^^^^^

.. sqlrun::

   SELECT name, price * stock AS stock_value
   FROM products
   ORDER BY stock_value DESC, product_id
   LIMIT 3;

``ORDER BY`` 句では、``SELECT`` 句で付けた別名を使用できます。この例では、ドリップコーヒーとボールペンの在庫金額がどちらも 20000 で並んでいます。``LIMIT`` 句で行数を制限すると、値が同じ行のうちどれが結果に残るかは保証されないため、``product_id`` を並べ替えの条件に加えて順序を確定させています。

問題 5
^^^^^^

.. sqlrun::

   SELECT name,
          CASE
              WHEN stock = 0 THEN '在庫なし'
              WHEN stock < 50 THEN '残りわずか'
              ELSE '在庫あり'
          END AS stock_status
   FROM products;

``CASE`` 式の条件は上から順に調べられるため、2 つ目の条件を ``stock > 0 AND stock < 50`` と書く必要はありません。

.. _answers-ch05:

5 章 NULL の扱い
----------------

.. sqlfile:: answers_ch05 5 章 NULL の扱い 演習問題の解答

問題 1
^^^^^^

.. sqlrun::

   SELECT name
   FROM categories
   WHERE parent_id IS NULL;

``WHERE parent_id = NULL`` と書くと、結果は 1 行もありません。

問題 2
^^^^^^

.. sqlrun::

   SELECT name, COALESCE(category_id, 0) AS category_id
   FROM products;

問題 3
^^^^^^

結果は 6 行です。``email`` が NULL の 2 行では、``email = email`` が ``NULL = NULL`` となり、結果が UNKNOWN になるため除外されます。

.. sqlrun::

   SELECT name FROM customers WHERE email = email;

問題 4
^^^^^^

.. sqlrun::

   SELECT name, category_id
   FROM products
   WHERE category_id <> 3 OR category_id IS NULL;

標準 SQL の ``IS DISTINCT FROM`` を使って、``WHERE category_id IS DISTINCT FROM 3`` と書くこともできます。``IS DISTINCT FROM`` は、NULL どうしを等しいとみなし、NULL と NULL 以外の値を異なるとみなして比較する演算子で、結果は必ず TRUE か FALSE になります。SQLite ではバージョン 3.39 から使用できます。

.. _answers-ch06:

6 章 集計とグループ化
---------------------

.. sqlfile:: answers_ch06 6 章 集計とグループ化 演習問題の解答

問題 1
^^^^^^

.. sqlrun::

   SELECT SUM(price * stock) AS total_stock_value
   FROM products;

問題 2
^^^^^^

.. sqlrun::

   SELECT prefecture, COUNT(*) AS customer_count
   FROM customers
   GROUP BY prefecture
   ORDER BY customer_count DESC, prefecture;

問題 3
^^^^^^

.. sqlrun::

   SELECT product_id, SUM(quantity) AS total_quantity
   FROM order_items
   GROUP BY product_id
   HAVING SUM(quantity) >= 5
   ORDER BY product_id;

集計した値に対する条件なので、``WHERE`` 句ではなく ``HAVING`` 句に書きます。

問題 4
^^^^^^

.. sqlrun::

   SELECT strftime('%Y-%m', ordered_on) AS month,
          COUNT(*) AS order_count
   FROM orders
   WHERE status <> 'キャンセル'
   GROUP BY month
   ORDER BY month;

``strftime('%Y-%m', ordered_on)`` の代わりに ``substr(ordered_on, 1, 7)`` と書いても同じ結果になります。

.. _answers-ch07:

7 章 テーブルの結合
-------------------

.. sqlfile:: answers_ch07 7 章 テーブルの結合 演習問題の解答

問題 1
^^^^^^

.. sqlrun::

   SELECT p.name AS product_name, c.name AS category_name
   FROM products AS p
   LEFT JOIN categories AS c ON p.category_id = c.category_id
   ORDER BY p.product_id;

``INNER JOIN`` を使うと、カテゴリのない福袋が結果に含まれません。

問題 2
^^^^^^

.. sqlrun::

   SELECT p.name,
          oi.quantity,
          oi.unit_price,
          oi.quantity * oi.unit_price AS subtotal
   FROM order_items AS oi
   INNER JOIN products AS p ON oi.product_id = p.product_id
   WHERE oi.order_id = 6
   ORDER BY p.product_id;

問題 3
^^^^^^

.. sqlrun::

   SELECT c.category_id, c.name, COUNT(p.product_id) AS product_count
   FROM categories AS c
   LEFT JOIN products AS p ON c.category_id = p.category_id
   GROUP BY c.category_id, c.name
   ORDER BY c.category_id;

「食品」や「飲料」には直接属する商品がないため、0 になります。8 章の再帰 CTE を応用すると、下位のカテゴリの商品も含めて数えることもできます。

問題 4
^^^^^^

.. sqlrun::

   SELECT c.name
   FROM customers AS c
   LEFT JOIN orders AS o ON c.customer_id = o.customer_id
   WHERE o.order_id IS NULL;

問題 5
^^^^^^

.. sqlrun::

   SELECT DISTINCT p.name
   FROM customers AS c
   INNER JOIN orders AS o ON c.customer_id = o.customer_id
   INNER JOIN order_items AS oi ON o.order_id = oi.order_id
   INNER JOIN products AS p ON oi.product_id = p.product_id
   WHERE c.prefecture = '東京都' AND o.status <> 'キャンセル'
   ORDER BY p.name;

同じ商品を複数回注文している場合があるため、``DISTINCT`` で重複を取り除いています。

.. _answers-ch08:

8 章 サブクエリと共通テーブル式
-------------------------------

.. sqlfile:: answers_ch08 8 章 サブクエリと共通テーブル式 演習問題の解答

問題 1
^^^^^^

.. sqlrun::

   SELECT name, price
   FROM products
   WHERE price = (SELECT MAX(price) FROM products);

``ORDER BY price DESC LIMIT 1`` と異なり、最高価格の商品が複数ある場合は、そのすべてが結果に含まれます。

問題 2
^^^^^^

.. sqlrun::

   SELECT c.name
   FROM customers AS c
   WHERE EXISTS (
       SELECT 1
       FROM orders AS o
       WHERE o.customer_id = c.customer_id AND o.status = 'キャンセル'
   );

問題 3
^^^^^^

.. sqlrun::

   SELECT p.name,
          p.price,
          (SELECT MAX(p2.price)
           FROM products AS p2
           WHERE p2.category_id = p.category_id) AS max_price_in_category
   FROM products AS p
   WHERE p.category_id IS NOT NULL
   ORDER BY p.category_id, p.price DESC;

9 章で説明するウィンドウ関数を使うと、``MAX(price) OVER (PARTITION BY category_id)`` と書けます。

問題 4
^^^^^^

.. sqlrun::

   WITH order_amounts AS (
       SELECT o.order_id,
              SUM(oi.quantity * oi.unit_price) AS amount
       FROM orders AS o
       INNER JOIN order_items AS oi ON o.order_id = oi.order_id
       WHERE o.status <> 'キャンセル'
       GROUP BY o.order_id
   )
   SELECT COUNT(*) AS order_count
   FROM order_amounts
   WHERE amount >= 1000;

問題 5
^^^^^^

.. sqlrun::

   WITH RECURSIVE sub_categories (category_id, name) AS (
       SELECT category_id, name
       FROM categories
       WHERE category_id = 1
       UNION ALL
       SELECT c.category_id, c.name
       FROM categories AS c
       INNER JOIN sub_categories AS s ON c.parent_id = s.category_id
   )
   SELECT category_id, name
   FROM sub_categories
   ORDER BY category_id;

.. _answers-ch09:

9 章 ウィンドウ関数
-------------------

.. sqlfile:: answers_ch09 9 章 ウィンドウ関数 演習問題の解答

問題 1
^^^^^^

.. sqlrun::

   SELECT name,
          price,
          round(price * 100.0 / SUM(price) OVER (), 1) AS ratio
   FROM products
   ORDER BY price DESC;

``price * 100`` と書くと整数どうしの割り算になり、小数点以下が切り捨てられてしまうため、``100.0`` と書いて実数の計算にしています。

問題 2
^^^^^^

.. sqlrun::

   SELECT ROW_NUMBER() OVER (ORDER BY registered_on, customer_id) AS row_num,
          name,
          registered_on
   FROM customers
   ORDER BY row_num;

登録日が同じ顧客がいた場合にも番号の付け方が決まるよう、``customer_id`` を並べ替えの条件に加えています。

問題 3
^^^^^^

.. sqlrun::

   SELECT prefecture,
          ROW_NUMBER() OVER (
              PARTITION BY prefecture ORDER BY registered_on, customer_id
          ) AS row_num,
          name,
          registered_on
   FROM customers
   ORDER BY prefecture, row_num;

問題 4
^^^^^^

.. sqlrun::

   WITH ranked AS (
       SELECT order_id,
              product_id,
              quantity * unit_price AS subtotal,
              ROW_NUMBER() OVER (
                  PARTITION BY order_id ORDER BY quantity * unit_price DESC
              ) AS row_num
       FROM order_items
   )
   SELECT order_id, product_id, subtotal
   FROM ranked
   WHERE row_num = 1
   ORDER BY order_id;

同じ注文の中に小計が同じ明細が複数ある場合に、そのすべてを取り出したいときは、``ROW_NUMBER()`` の代わりに ``RANK()`` を使います。

問題 5
^^^^^^

.. sqlrun::

   WITH with_prev AS (
       SELECT customer_id,
              order_id,
              ordered_on,
              LAG(ordered_on) OVER (
                  PARTITION BY customer_id ORDER BY ordered_on
              ) AS prev_ordered_on
       FROM orders
   )
   SELECT customer_id,
          order_id,
          ordered_on,
          prev_ordered_on,
          julianday(ordered_on) - julianday(prev_ordered_on) AS days
   FROM with_prev
   ORDER BY customer_id, ordered_on;

``julianday()`` は、日付をユリウス日（グレゴリオ暦の紀元前 4714 年 11 月 24 日正午からの日数）に変換する SQLite の関数です。2 つの日付のユリウス日の差を求めると、日数の差が得られます。各顧客の最初の注文では ``prev_ordered_on`` が NULL になるため、``days`` も NULL になります。

.. _answers-ch10:

10 章 データの追加・更新・削除
------------------------------

.. sqlfile:: answers_ch10 10 章 データの追加・更新・削除 演習問題の解答

問題 1
^^^^^^

.. sqlrun::

   INSERT INTO customers (customer_id, name, prefecture, email, registered_on)
   VALUES (9, '木村蓮', '京都府', NULL, '2025-04-10');

.. sqlrun::

   SELECT * FROM customers;

``email`` を列名の並びから省略しても、既定値がないため NULL が設定されます。

問題 2
^^^^^^

.. sqlrun::

   UPDATE products
   SET price = price * 110 / 100
   WHERE category_id = 3;

.. sqlrun::

   SELECT product_id, name, price FROM products WHERE category_id = 3;

整数どうしの計算の結果は小数点以下が切り捨てられるため、1 円未満の切り捨てが自動的に行われます。``price * 1.1`` と書くと結果が実数になり、``110.00000000000001`` のような値が格納されてしまいます。

問題 3
^^^^^^

注文明細が注文を参照しているため、先に注文明細を削除し、その後で注文を削除します。

.. sqlrun::

   DELETE FROM order_items
   WHERE order_id IN (SELECT order_id FROM orders WHERE status = 'キャンセル');

.. sqlrun::

   DELETE FROM orders
   WHERE status = 'キャンセル';

.. sqlrun::

   SELECT COUNT(*) AS cancelled_count FROM orders WHERE status = 'キャンセル';

実際のシステムでは、2 つの ``DELETE`` 文を 1 つのトランザクション（12 章）にまとめて実行します。

問題 4
^^^^^^

.. sqlrun::

   INSERT INTO products (product_id, name, category_id, price, stock)
   VALUES (5, '味噌', 5, 500, 20)
   ON CONFLICT (product_id) DO UPDATE SET stock = stock + excluded.stock;

.. sqlrun::

   SELECT product_id, name, stock FROM products WHERE product_id = 5;

.. _answers-ch11:

11 章 テーブルの設計と定義
--------------------------

.. sqlfile:: answers_ch11 11 章 テーブルの設計と定義 演習問題の解答

問題 1
^^^^^^

.. sqlrun::

   CREATE TABLE favorites (
       customer_id INTEGER NOT NULL REFERENCES customers (customer_id),
       product_id  INTEGER NOT NULL REFERENCES products (product_id),
       added_on    TEXT    NOT NULL,
       PRIMARY KEY (customer_id, product_id)
   );

問題 2
^^^^^^

.. sqlrun::

   INSERT INTO favorites (customer_id, product_id, added_on)
   VALUES (1, 6, '2025-06-01');

同じデータをもう一度登録しようとすると、主キーの値が重複するため、エラーになります。

.. sqlrun::
   :error:

   INSERT INTO favorites (customer_id, product_id, added_on)
   VALUES (1, 6, '2025-06-01');

問題 3
^^^^^^

.. sqlrun::

   ALTER TABLE products ADD COLUMN description TEXT;

.. sqlrun::

   SELECT name, type FROM pragma_table_info('products');

問題 4
^^^^^^

.. sqlrun::

   CREATE VIEW customer_summary AS
   SELECT c.customer_id,
          c.name,
          COUNT(DISTINCT o.order_id) AS order_count,
          COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_amount
   FROM customers AS c
   LEFT JOIN orders AS o
       ON c.customer_id = o.customer_id AND o.status <> 'キャンセル'
   LEFT JOIN order_items AS oi ON o.order_id = oi.order_id
   GROUP BY c.customer_id, c.name;

.. sqlrun::

   SELECT * FROM customer_summary ORDER BY customer_id;

注意する点は次の 3 つです。

* キャンセルを除く条件を ``WHERE`` 句に書くと、注文のない顧客が除外されてしまうため、``ON`` 句に書きます（7 章を参照）。
* 注文と注文明細を結合すると、明細の数だけ注文の行が繰り返されるため、注文件数は ``COUNT(DISTINCT o.order_id)`` で数えます。
* 注文のない顧客では ``SUM()`` の結果が NULL になるため、``COALESCE()`` で 0 に置き換えます。

.. _answers-ch12:

12 章 トランザクション
----------------------

.. sqlfile:: answers_ch12 12 章 トランザクション 演習問題の解答

問題 1
^^^^^^

.. sqlrun::

   SELECT SUM(stock) AS total_stock FROM products;

.. sqlrun::

   BEGIN;
   UPDATE products SET stock = 0;

.. sqlrun::

   SELECT SUM(stock) AS total_stock FROM products;

.. sqlrun::

   ROLLBACK;

.. sqlrun::

   SELECT SUM(stock) AS total_stock FROM products;

問題 2
^^^^^^

.. sqlrun::

   BEGIN;
   INSERT INTO orders (order_id, customer_id, ordered_on, status)
   VALUES (13, 8, '2025-07-05', '受付済');
   INSERT INTO order_items (order_id, product_id, quantity, unit_price)
   VALUES (13, 10, 3, 180);
   UPDATE products SET stock = stock - 3 WHERE product_id = 10;
   COMMIT;

.. sqlrun::

   SELECT * FROM order_items WHERE order_id = 13;

.. sqlrun::

   SELECT product_id, name, stock FROM products WHERE product_id = 10;

問題 3
^^^^^^

SQLite では、トランザクションの途中で文がエラーになった場合、原則としてエラーになった文の変更だけが取り消され、トランザクションは継続します。それまでに実行した文の変更は残っているため、そのまま ``COMMIT`` を実行すると、一連の処理の一部だけが確定してしまいます。

アプリケーションは、エラーが発生したことを検出したら ``ROLLBACK`` を実行し、トランザクション全体を取り消す必要があります。Python の ``sqlite3`` モジュールでは、接続オブジェクトを ``with`` 文で使うと、例外が発生したときに自動的に ``rollback()`` が呼ばれます（14 章を参照）。

.. _answers-ch13:

13 章 インデックスと性能
------------------------

.. sqlfile:: answers_ch13 13 章 インデックスと性能 演習問題の解答

問題 1
^^^^^^

.. sqlrun::

   EXPLAIN QUERY PLAN
   SELECT * FROM order_items WHERE product_id = 1;

``order_items`` テーブルには主キー（``order_id`` と ``product_id`` の組）のインデックスがありますが、``product_id`` は 2 番目の列なので、このインデックスを使った検索はできません。``product_id`` 列のインデックスを作成します。

.. sqlrun::

   CREATE INDEX idx_order_items_product_id ON order_items (product_id);

.. sqlrun::

   EXPLAIN QUERY PLAN
   SELECT * FROM order_items WHERE product_id = 1;

問題 2
^^^^^^

``=`` で比較する ``prefecture`` 列を先に、範囲で比較する ``registered_on`` 列を後に指定します。

.. sqlrun::

   CREATE INDEX idx_customers_pref_registered
   ON customers (prefecture, registered_on);

.. sqlrun::

   EXPLAIN QUERY PLAN
   SELECT name FROM customers
   WHERE prefecture = '東京都' AND registered_on >= '2024-06-01';

問題 3
^^^^^^

条件の中で ``price`` 列に演算（``* 1.1``）を適用しているため、インデックスに格納された ``price`` の値そのものでは探せないからです。演算を右辺に移して、列をそのまま比較する形に書き換えます。両辺を 1.1 で割ると ``price >= 500`` になるので、次のように書けます。

.. sqlrun::

   CREATE INDEX idx_products_price ON products (price);

.. sqlrun::

   EXPLAIN QUERY PLAN
   SELECT name, price FROM products WHERE price * 1.1 >= 550;

.. sqlrun::

   EXPLAIN QUERY PLAN
   SELECT name, price FROM products WHERE price >= 500;

.. _answers-ch14:

14 章 Python から SQL を使う
----------------------------

問題 1、2、4 の解答例は ``examples/answers_ch14.py`` に収録しています。

.. literalinclude:: ../examples/answers_ch14.py
   :language: python
   :caption: answers_ch14.py
   :linenos:

実行結果は次のとおりです。

.. pyoutput:: answers_ch14.py

問題 1
^^^^^^

``customers_in()`` 関数を参照してください。都道府県名はプレースホルダーで渡しています。

問題 2
^^^^^^

問題の関数は、引数 ``keyword`` を f 文字列で SQL 文に直接埋め込んでいるため、SQL インジェクションの危険があります。たとえば ``keyword`` に ``' OR '1'='1`` のような文字列が渡されると、SQL 文の意味が変わってしまいます。

``find_products_by_name()`` 関数のように、``%`` を付けたパターンの文字列を Python 側で作り、プレースホルダーで渡すように修正します。なお、``keyword`` に ``%`` や ``_`` が含まれていると、それらはワイルドカードとして扱われます。これらの文字そのものを検索したい場合は、``LIKE ? ESCAPE '\'`` のように ``ESCAPE`` 句を指定し、``keyword`` の中の ``%`` と ``_`` の前に ``\`` を付けてから渡します。

問題 3
^^^^^^

既定の設定（``autocommit`` が ``sqlite3.LEGACY_TRANSACTION_CONTROL``）では、``INSERT`` 文を実行する前にトランザクションが自動的に開始されます。``commit()`` を呼ばずに接続を閉じたため、トランザクションが確定せず、追加した行が失われました。

次のように、接続オブジェクトを ``with`` 文で使ってトランザクションを確定させ、``contextlib.closing()`` で接続を閉じるように修正します。``conn.execute()`` の後に ``conn.commit()`` を呼ぶ方法でもかまいません。

.. code-block:: python
   :linenos:

   import sqlite3
   from contextlib import closing

   with closing(sqlite3.connect("shop.db")) as conn:
       with conn:  # ブロックを正常に抜けると commit() が呼ばれます
           conn.execute(
               "INSERT INTO categories (name, parent_id) VALUES ('ジュース', 2)"
           )

この修正版を実行すると ``shop.db`` にカテゴリが追加されます。初期状態に戻すには ``create_shop_db.py`` を実行してください。

問題 4
^^^^^^

``category_summary()`` 関数を参照してください。集計は SQL で行い、結果だけを DataFrame として読み込んでいます。
