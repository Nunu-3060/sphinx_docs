データの取得
============

.. sqlfile:: ch04_select 4 章 データの取得

本章では、テーブルからデータを取り出す ``SELECT`` 文の基本を説明します。本章以降の SQL の例は、``examples/sql`` フォルダーに章ごとに収録しています（本章の例は ``ch04_select.sql``）。

列を選択する
------------

``SELECT`` 文の最も基本的な形は次のとおりです。

.. code-block:: text
   :linenos:

   SELECT 列名1, 列名2, ... FROM テーブル名;

``SELECT`` の後に取り出したい列をコンマで区切って並べ、``FROM`` の後にテーブル名を書きます。``SELECT`` や ``FROM`` から始まる部分を、それぞれ ``SELECT`` 句、``FROM`` 句と呼びます。

.. sqlrun::

   SELECT name, price FROM products;

列名の代わりに ``*`` を書くと、すべての列を取り出します。

.. sqlrun::

   SELECT * FROM categories;

``*`` は手軽ですが、テーブルに列が追加されると結果の列も変わってしまいます。プログラムに組み込む SQL では、必要な列を明示するのが一般的です。

式と列の別名
------------

``SELECT`` 句には、列名だけでなく計算式も書けます。``AS`` を使うと、結果の列に別名を付けられます。

.. sqlrun::

   SELECT name, price, price * 1.1 AS price_with_tax
   FROM products;

``price * 1.1`` の結果に ``220.00000000000003`` のような値が現れるのは、実数（浮動小数点数）の計算誤差によるものです。Python で ``200 * 1.1`` を計算した場合も同じ結果になります。端数の処理には、後述する ``round()`` 関数を使用します。

別名を付けない場合、結果の列名は ``price * 1.1`` のような式そのものになります。``AS`` は省略して ``price * 1.1 price_with_tax`` と書くこともできますが、読みやすさのため本資料では省略しません。

.. note::

   SQLite では、整数どうしの割り算の結果は整数になり、小数点以下は切り捨てられます。Python の ``//`` 演算子とは異なり、負の数も 0 に近い方向へ切り捨てられます。小数の結果が必要な場合は、どちらかを ``2.0`` のように実数にします。

   .. sqlrun::

      SELECT 7 / 2, -7 / 2, 7 / 2.0, 7 % 2;

   Python では ``7 / 2`` は ``3.5``、``-7 // 2`` は ``-4`` になるため、同じ感覚で書くと誤った結果になります。

行を絞り込む
------------

WHERE 句
^^^^^^^^

``WHERE`` 句を使うと、条件に合う行だけを取り出せます。

.. sqlrun::

   SELECT name, price
   FROM products
   WHERE price >= 500;

条件には次の比較演算子を使用できます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 演算子
     - 意味
   * - ``=``
     - 等しい
   * - ``<>`` または ``!=``
     - 等しくない
   * - ``<``
     - より小さい
   * - ``<=``
     - 以下
   * - ``>``
     - より大きい
   * - ``>=``
     - 以上

等しいことを表す演算子は、Python の ``==`` ではなく ``=`` です。SQLite は ``==`` も受け付けますが、多くの DBMS では使えません。「等しくない」を表す演算子は、標準 SQL では ``<>`` です。

文字列と比較する場合は、値を単一引用符で囲みます。

.. sqlrun::

   SELECT customer_id, name, prefecture
   FROM customers
   WHERE prefecture = '東京都';

SQLite には日付専用のデータ型がないため、サンプルデータベースでは日付を ``'2025-01-10'`` のような「年-月-日」形式の文字列で格納しています。月と日を 2 桁で表したこの形式の文字列は、文字列として大小を比較した結果が日付の前後関係と一致します。

.. sqlrun::

   SELECT order_id, ordered_on
   FROM orders
   WHERE ordered_on < '2025-02-01';

AND、OR、NOT
^^^^^^^^^^^^

複数の条件を組み合わせるには、``AND``（かつ）、``OR``（または）、``NOT``（否定）を使用します。

.. sqlrun::

   SELECT name, price, stock
   FROM products
   WHERE price >= 200 AND stock < 30;

``AND`` は ``OR`` より優先して評価されます。次の 2 つの文は結果が異なります。

.. sqlrun::

   -- category_id = 3 の商品と、「category_id = 8 かつ price >= 250」の商品
   SELECT name, category_id, price
   FROM products
   WHERE category_id = 3 OR category_id = 8 AND price >= 250;

.. sqlrun::

   -- 「category_id が 3 または 8」かつ「price >= 250」の商品
   SELECT name, category_id, price
   FROM products
   WHERE (category_id = 3 OR category_id = 8) AND price >= 250;

意図しない評価順序を避けるため、``AND`` と ``OR`` を組み合わせるときは括弧を付けることをお勧めします。

BETWEEN、IN、LIKE
^^^^^^^^^^^^^^^^^

よく使う条件には、短く書ける演算子が用意されています。

``BETWEEN a AND b`` は、値が ``a`` 以上 ``b`` 以下であることを表します。両端の値を含む点に注意してください。

.. sqlrun::

   SELECT name, price
   FROM products
   WHERE price BETWEEN 150 AND 250;

``IN (値1, 値2, ...)`` は、値が括弧内のいずれかと等しいことを表します。Python の ``in`` 演算子と同じ考え方です。

.. sqlrun::

   SELECT customer_id, name, prefecture
   FROM customers
   WHERE prefecture IN ('大阪府', '福岡県');

``LIKE`` は、文字列がパターンに一致することを表します。パターンでは、``%`` が 0 文字以上の任意の文字列を、``_`` が任意の 1 文字を表します。

.. sqlrun::

   -- 名前に「コーヒー」を含む商品
   SELECT name
   FROM products
   WHERE name LIKE '%コーヒー%';

.. sqlrun::

   -- 名前が「チョコレート」で終わる商品
   SELECT name
   FROM products
   WHERE name LIKE '%チョコレート';

SQLite の ``LIKE`` は、英字（ASCII 文字）の大文字と小文字を区別しません。この動作は DBMS によって異なります。

``NOT`` を付けて、``NOT BETWEEN``、``NOT IN``、``NOT LIKE`` のように否定することもできます。

行を並べ替える
--------------

リレーショナルデータベースのテーブルの行には順序がありません。``SELECT`` 文の結果の順序も、指定しなければ保証されません。ここまでの例では主キーの順に表示されていますが、これはたまたまそうなっているだけです。

結果を並べ替えるには ``ORDER BY`` 句を使用します。``ASC`` を付けると昇順（小さい順）、``DESC`` を付けると降順（大きい順）になります。省略した場合は昇順です。

.. sqlrun::

   SELECT name, price
   FROM products
   ORDER BY price DESC;

複数の列を指定すると、最初の列の値が等しい行どうしを、次の列で並べ替えます。

.. sqlrun::

   SELECT name, prefecture, registered_on
   FROM customers
   ORDER BY prefecture, registered_on DESC;

SQLite では、文字列の並べ替えは既定で文字コードの順になります（他の DBMS では、照合順序の設定によって異なります）。そのため、都道府県名のような漢字の文字列は、読み方の順（五十音順）には並びません。

行数を制限する
--------------

``LIMIT`` 句を使うと、結果の行数を制限できます。``ORDER BY`` 句と組み合わせると、「価格の高い上位 3 件」のような取り出し方ができます。

.. sqlrun::

   SELECT name, price
   FROM products
   ORDER BY price DESC
   LIMIT 3;

``OFFSET`` を付けると、先頭から指定した行数を読み飛ばします。次の例は、価格が 4 番目から 6 番目に高い商品を取り出します。

.. sqlrun::

   SELECT name, price
   FROM products
   ORDER BY price DESC
   LIMIT 3 OFFSET 3;

``LIMIT`` 句は SQLite、PostgreSQL、MySQL などで使えますが、標準 SQL では ``FETCH FIRST 3 ROWS ONLY`` と書きます。SQLite は ``FETCH FIRST`` に対応していません。

重複を取り除く
--------------

``SELECT`` の直後に ``DISTINCT`` を付けると、重複する行を取り除きます。次の例は、顧客が住んでいる都道府県の一覧を取り出します。

.. sqlrun::

   SELECT DISTINCT prefecture
   FROM customers
   ORDER BY prefecture;

複数の列を指定した場合は、すべての列の値の組が等しい行を重複とみなします。

関数
----

SQL には、値を加工するための関数が用意されています。関数の種類と名前は DBMS によって異なります。ここでは SQLite の主な関数を紹介します。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 関数
     - 説明
   * - ``length(s)``
     - 文字列 ``s`` の文字数
   * - ``upper(s)``、``lower(s)``
     - 英字を大文字または小文字に変換した文字列
   * - ``substr(s, start, n)``
     - 文字列 ``s`` の ``start`` 文字目（先頭は 1）から ``n`` 文字
   * - ``replace(s, a, b)``
     - 文字列 ``s`` の中の ``a`` を ``b`` に置換した文字列
   * - ``round(x, n)``
     - 数値 ``x`` を小数点以下 ``n`` 桁に丸めた値（``n`` を省略すると 0 桁）
   * - ``abs(x)``
     - 数値 ``x`` の絶対値
   * - ``date(d, 修飾子)``
     - 日付 ``d`` に修飾子（``'+7 days'`` など）を適用した日付
   * - ``strftime(書式, d)``
     - 日付 ``d`` を書式に従って変換した文字列

また、``||`` 演算子で文字列を連結できます。数値は自動的に文字列に変換されます。

.. sqlrun::

   SELECT name || '（' || price || '円）' AS label,
          length(name) AS name_length
   FROM products
   WHERE category_id = 8;

``substr()`` の文字位置は、Python のインデックスと異なり 1 から始まります。

日付の関数を使うと、日付の計算ができます。次の例は、注文日の 7 日後の日付と、注文日の月を求めます。

.. sqlrun::

   SELECT order_id,
          ordered_on,
          date(ordered_on, '+7 days') AS due_on,
          strftime('%m', ordered_on) AS month
   FROM orders
   WHERE order_id <= 3;

``round()`` は、指定した桁数に数値を丸めます。

.. sqlrun::

   SELECT name, price, round(price * 1.1) AS price_with_tax
   FROM products
   WHERE category_id = 8;

Python の ``round()`` は偶数への丸め（``round(2.5)`` は ``2``）を行いますが、SQLite の ``round()`` は四捨五入（``round(2.5)`` は ``3.0``）を行います。また、SQLite の ``round()`` は実数を返すため、結果は ``220.0`` のように表示されます。

CASE 式
-------

``CASE`` 式を使うと、条件に応じて異なる値を返せます。Python の ``if`` 文や条件式に相当します。

.. code-block:: text
   :linenos:

   CASE
       WHEN 条件1 THEN 値1
       WHEN 条件2 THEN 値2
       ELSE 値3
   END

条件は上から順に調べられ、最初に成り立った条件の値が返されます。どの条件も成り立たない場合は ``ELSE`` の値が返されます。

.. sqlrun::

   SELECT name,
          price,
          CASE
              WHEN price >= 1000 THEN '高'
              WHEN price >= 300 THEN '中'
              ELSE '低'
          END AS price_rank
   FROM products
   ORDER BY price DESC;

``CASE`` 式は ``SELECT`` 句だけでなく、``WHERE`` 句や ``ORDER BY`` 句など、値を書ける場所であればどこでも使用できます。

SELECT 文の句の順序
-------------------

本章で説明した句は、次の順序で書く必要があります。順序を入れ替えるとエラーになります。

.. code-block:: text
   :linenos:

   SELECT 列や式
   FROM テーブル名
   WHERE 条件
   ORDER BY 並べ替えの列
   LIMIT 行数 OFFSET 読み飛ばす行数;

``SELECT`` 句以外は、必要なものだけを書けば十分です。6 章では、``WHERE`` 句と ``ORDER BY`` 句の間に入る ``GROUP BY`` 句と ``HAVING`` 句を説明します。

pandas との対応
---------------

本章で説明した操作は、pandas では次のように書けます。``df`` は ``products`` テーブル（``DISTINCT`` の行のみ ``customers`` テーブル）の内容を格納した DataFrame とします。

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - SQL
     - pandas
   * - ``SELECT name, price FROM products``
     - ``df[["name", "price"]]``
   * - ``WHERE price >= 500``
     - ``df[df["price"] >= 500]``
   * - ``WHERE price >= 200 AND stock < 30``
     - ``df[(df["price"] >= 200) & (df["stock"] < 30)]``
   * - ``WHERE category_id IN (3, 8)``
     - ``df[df["category_id"].isin([3, 8])]``
   * - ``WHERE name LIKE '%コーヒー%'``
     - ``df[df["name"].str.contains("コーヒー")]``
   * - ``ORDER BY price DESC``
     - ``df.sort_values("price", ascending=False)``
   * - ``LIMIT 3``
     - ``df.head(3)``
   * - ``SELECT DISTINCT prefecture``
     - ``df["prefecture"].drop_duplicates()``

.. _exercises-ch04:

演習問題
--------

1. ``customers`` テーブルから、2024 年に登録した顧客の氏名と登録日を、登録日の古い順に取り出してください。
2. ``products`` テーブルから、在庫数（``stock``）が 20 以下の商品の商品名と在庫数を取り出してください。
3. ``products`` テーブルから、商品名に「チョコ」を含むか、価格が 100 円以下の商品の商品名と価格を取り出してください。
4. ``products`` テーブルから、価格と在庫数を掛けた金額（在庫金額）が大きい順に、上位 3 件の商品名と在庫金額を取り出してください。在庫金額の列には ``stock_value`` という別名を付けてください。
5. ``products`` テーブルから、商品名と、在庫の状態を表す列 ``stock_status`` を取り出してください。``stock_status`` は、在庫数が 0 なら「在庫なし」、50 未満なら「残りわずか」、それ以外は「在庫あり」とします。

解答は :ref:`answers-ch04` にあります。
