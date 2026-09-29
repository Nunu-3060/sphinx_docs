テーブルの設計と定義
====================

.. sqlfile:: ch11_ddl 11 章 テーブルの設計と定義

本章では、テーブルを作成・変更・削除する方法と、テーブルに設定する制約を説明します。また、テーブルを設計する際の基本的な考え方である正規化を紹介します。

本章の例は、サンプルデータベースの初期状態から始めて、前の例を実行した後のデータに対して順に実行していくものとします。

テーブルを作成する
------------------

CREATE TABLE 文
^^^^^^^^^^^^^^^

テーブルを作成するには、``CREATE TABLE`` 文を使用します。括弧内に、列名、データ型、制約をコンマで区切って並べます。

.. code-block:: text
   :linenos:

   CREATE TABLE テーブル名 (
       列名1 データ型 制約,
       列名2 データ型 制約,
       ...
   );

例として、商品のレビューを格納する ``reviews`` テーブルを作成します。

.. sqlrun::

   CREATE TABLE reviews (
       review_id   INTEGER PRIMARY KEY,
       product_id  INTEGER NOT NULL REFERENCES products (product_id),
       customer_id INTEGER NOT NULL REFERENCES customers (customer_id),
       rating      INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
       comment     TEXT,
       status      TEXT    NOT NULL DEFAULT '公開',
       UNIQUE (product_id, customer_id)
   );

各列の制約の意味は、この後の節で説明します。

同じ名前のテーブルがすでにある場合、``CREATE TABLE`` 文はエラーになります。``CREATE TABLE IF NOT EXISTS reviews (...)`` のように書くと、テーブルがない場合だけ作成します。

テーブルの定義を確認する
^^^^^^^^^^^^^^^^^^^^^^^^

SQLite では、``pragma_table_info()`` 関数でテーブルの列の一覧を確認できます。

.. sqlrun::

   SELECT name, type, "notnull", dflt_value, pk
   FROM pragma_table_info('reviews');

``notnull`` は NOT NULL 制約の有無、``dflt_value`` は既定値、``pk`` は主キーであるかどうかを表します。``notnull`` はキーワード ``NOTNULL`` と同じ綴りのため、二重引用符で囲んで列名であることを示しています。テーブルの定義を確認する方法は DBMS によって異なります。

データ型
--------

SQLite のデータ型
^^^^^^^^^^^^^^^^^

SQLite では、値は次の 5 種類のいずれかの形式（ストレージクラス）で格納されます。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - ストレージクラス
     - 内容
   * - ``NULL``
     - NULL
   * - ``INTEGER``
     - 符号付き整数（最大 8 バイト）
   * - ``REAL``
     - 浮動小数点数（8 バイト）
   * - ``TEXT``
     - 文字列
   * - ``BLOB``
     - バイナリデータ（入力されたとおりに格納）

日付や時刻、真偽値を表す専用の型はありません。日付や時刻は ``'2025-01-10'`` のような文字列（``TEXT``）で、真偽値は整数の 0 と 1（``INTEGER``）で表すのが一般的です。PostgreSQL や MySQL などには、``DATE``、``TIMESTAMP``、``BOOLEAN``、``VARCHAR(n)``、``DECIMAL(p, s)`` など、より多くのデータ型があります。

型アフィニティ
^^^^^^^^^^^^^^

多くの DBMS では、列に宣言したデータ型に変換できない値（``INTEGER`` 列に対する ``'abc'`` など）を格納しようとするとエラーになります。一方、SQLite の列のデータ型は「その列に格納する値の推奨される型」（型アフィニティ）を表すだけで、宣言と異なる型の値も格納できます。値の型は ``typeof()`` 関数で確認できます。

.. sqlrun::

   CREATE TABLE type_demo (i INTEGER, t TEXT);

.. sqlrun::

   INSERT INTO type_demo (i, t) VALUES ('123', 456), ('abc', 7.5);

.. sqlrun::

   SELECT i, typeof(i), t, typeof(t) FROM type_demo;

``INTEGER`` 列に格納した ``'123'`` は整数に変換されましたが、整数に変換できない ``'abc'`` は文字列のまま格納されています。``TEXT`` 列に格納した数値は文字列に変換されています。

STRICT テーブル
^^^^^^^^^^^^^^^

テーブルの定義の末尾に ``STRICT`` を付けると、型の検査が厳密になり、列の型に変換できない値を格納しようとするとエラーになります。``STRICT`` テーブルは SQLite 3.37 から使用できます。

.. sqlrun::

   CREATE TABLE strict_demo (i INTEGER, t TEXT) STRICT;

.. sqlrun::
   :error:

   INSERT INTO strict_demo (i, t) VALUES ('abc', 'text');

``STRICT`` テーブルでは、列のデータ型に ``INTEGER``、``REAL``、``TEXT``、``BLOB``、``ANY`` のいずれかを指定します。

制約
----

制約は、テーブルに格納できる値に対する規則です。制約に違反するデータを追加・更新しようとすると、エラーになり、その操作は行われません。制約によって、アプリケーションの不具合などによる不正なデータの混入を防げます。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 制約
     - 内容
   * - ``PRIMARY KEY``
     - 主キー。行を一意に識別します。値の重複を許しません
   * - ``NOT NULL``
     - NULL を許しません
   * - ``UNIQUE``
     - 値の重複を許しません（NULL は重複してもかまいません）
   * - ``CHECK (条件)``
     - 条件を満たさない値を許しません
   * - ``DEFAULT 値``
     - 値を指定せずに行を追加したときの既定値を設定します
   * - ``REFERENCES テーブル (列)``
     - 外部キー。参照先のテーブルに存在する値だけを許します

制約は列の定義の後に書くほか、``reviews`` テーブルの ``UNIQUE (product_id, customer_id)`` のように、列の定義とは別に書くこともできます。この書き方をすると、複数の列の組に対する制約を設定できます。``reviews`` テーブルでは、同じ顧客が同じ商品に 2 件以上のレビューを登録できないようにしています。

制約の動作を確認します。まず、正しいデータを追加します。

.. sqlrun::

   INSERT INTO reviews (product_id, customer_id, rating, comment)
   VALUES (1, 1, 5, 'おいしかったです。');

.. sqlrun::

   SELECT * FROM reviews;

``review_id`` は自動的に採番され、値を指定しなかった ``status`` には既定値の「公開」が設定されています。

次に、制約に違反するデータを追加してみます。``rating`` に 1 から 5 の範囲外の値を指定すると、``CHECK`` 制約に違反します。

.. sqlrun::
   :error:

   INSERT INTO reviews (product_id, customer_id, rating)
   VALUES (2, 1, 6);

``rating`` を省略すると、``NOT NULL`` 制約に違反します。

.. sqlrun::
   :error:

   INSERT INTO reviews (product_id, customer_id)
   VALUES (2, 1);

同じ顧客が同じ商品のレビューをもう一度登録すると、``UNIQUE`` 制約に違反します。

.. sqlrun::
   :error:

   INSERT INTO reviews (product_id, customer_id, rating)
   VALUES (1, 1, 4);

存在しない商品のレビューを登録すると、外部キーの制約に違反します。

.. sqlrun::
   :error:

   INSERT INTO reviews (product_id, customer_id, rating)
   VALUES (99, 1, 4);

主キーの補足
^^^^^^^^^^^^

SQLite では、``INTEGER PRIMARY KEY`` と定義した列は、各行に内部的に割り当てられる番号（rowid）の別名になります。値を省略して行を追加すると、通常は既存の最大値に 1 を加えた値が設定されます。削除された行の番号が再利用されないようにしたい場合は ``INTEGER PRIMARY KEY AUTOINCREMENT`` と定義しますが、処理がわずかに遅くなるため、必要な場合だけ使用します。

``order_items`` テーブルのように、複数の列の組を主キーにする場合は、``PRIMARY KEY (order_id, product_id)`` のように列の定義とは別に書きます。

外部キーの補足
^^^^^^^^^^^^^^

10 章で説明したとおり、SQLite では外部キーの制約は既定で無効になっており、接続ごとに ``PRAGMA foreign_keys = ON;`` を実行して有効にします。

外部キーには、参照先の行が削除・更新されたときの動作を指定できます。たとえば、``REFERENCES orders (order_id) ON DELETE CASCADE`` と定義すると、注文を削除したときに、その注文を参照する明細も自動的に削除されます。指定しない場合は、参照されている行の削除はエラーになります。

テーブルを変更・削除する
------------------------

ALTER TABLE 文
^^^^^^^^^^^^^^

作成済みのテーブルの構造を変更するには、``ALTER TABLE`` 文を使用します。SQLite では、次の変更ができます。

.. list-table::
   :header-rows: 1
   :widths: 55 45

   * - 文
     - 内容
   * - ``ALTER TABLE テーブル名 RENAME TO 新しい名前``
     - テーブル名を変更します
   * - ``ALTER TABLE テーブル名 RENAME COLUMN 列名 TO 新しい名前``
     - 列名を変更します
   * - ``ALTER TABLE テーブル名 ADD COLUMN 列の定義``
     - 列を追加します
   * - ``ALTER TABLE テーブル名 DROP COLUMN 列名``
     - 列を削除します

次の例は、``reviews`` テーブルに投稿日の列を追加します。既存の行の新しい列には NULL（既定値を指定した場合は既定値）が設定されます。

.. sqlrun::

   ALTER TABLE reviews ADD COLUMN posted_on TEXT;

.. sqlrun::

   SELECT * FROM reviews;

列のデータ型や制約の変更は、SQLite の ``ALTER TABLE`` 文ではできません。その場合は、新しい定義のテーブルを作成し、データを移してから古いテーブルを削除します。PostgreSQL や MySQL では、``ALTER TABLE`` 文でより多くの変更ができます。

DROP TABLE 文
^^^^^^^^^^^^^

テーブルを削除するには、``DROP TABLE`` 文を使用します。テーブルの定義とすべてのデータが削除されます。

.. sqlrun::

   DROP TABLE type_demo;

``DROP TABLE IF EXISTS テーブル名;`` と書くと、テーブルがない場合にエラーになりません。

ビュー
------

よく使う ``SELECT`` 文に名前を付けて保存したものをビューと呼びます。ビューは、テーブルと同じように ``SELECT`` 文の ``FROM`` 句に指定できます。ビューを作成するには ``CREATE VIEW`` 文を使用します。

次の例は、注文ごとの合計金額を求めるビューを作成します。

.. sqlrun::

   CREATE VIEW order_totals AS
   SELECT o.order_id,
          o.customer_id,
          o.ordered_on,
          o.status,
          SUM(oi.quantity * oi.unit_price) AS amount
   FROM orders AS o
   INNER JOIN order_items AS oi ON o.order_id = oi.order_id
   GROUP BY o.order_id, o.customer_id, o.ordered_on, o.status;

.. sqlrun::

   SELECT order_id, ordered_on, amount
   FROM order_totals
   WHERE amount >= 1000
   ORDER BY amount DESC;

ビューはデータそのものを保存するのではなく、``SELECT`` 文を保存します。ビューを参照するたびに ``SELECT`` 文が実行されるため、元のテーブルのデータが変わると、ビューの結果も変わります。複雑なクエリをビューにしておくと、利用する側の SQL 文を簡潔にできます。ビューを削除するには ``DROP VIEW`` 文を使用します。

正規化
------

テーブルの設計では、同じ情報を複数の場所に格納しないようにすることが重要です。同じ情報が複数の場所にあると、一部だけを更新した場合に矛盾が生じます。このような問題を防ぐためにテーブルを分割することを正規化と呼びます。正規化には段階があり、よく使われるのは第 1 正規形から第 3 正規形です。

正規化されていないテーブル
^^^^^^^^^^^^^^^^^^^^^^^^^^

注文の情報を、次のような 1 つのテーブルで管理する場合を考えます。

.. list-table::
   :header-rows: 1

   * - 注文番号
     - 注文日
     - 顧客番号
     - 顧客名
     - 商品
   * - 1
     - 2025-01-10
     - 1
     - 佐藤花子
     - ミルクチョコレート 200 円 × 2、ドリップコーヒー 800 円 × 1
   * - 3
     - 2025-02-02
     - 1
     - 佐藤花子
     - ポテトチップス 150 円 × 3、缶コーヒー 120 円 × 6

このテーブルには、次のような問題があります。

* 「商品」列に複数の商品がまとめて書かれているため、「ポテトチップスの販売数量の合計」のような集計が難しくなります。
* 顧客名が注文ごとに書かれているため、顧客が名前を変更したときに、すべての注文の行を修正する必要があります。

第 1 正規形
^^^^^^^^^^^

第 1 正規形は、すべての列の値が、それ以上分割できない単一の値である状態です。上の表の「商品」列を、1 行に 1 つの商品が入るように分割すると、次のようになります。

.. list-table::
   :header-rows: 1

   * - 注文番号
     - 商品番号
     - 注文日
     - 顧客番号
     - 顧客名
     - 商品名
     - 単価
     - 数量
   * - 1
     - 1
     - 2025-01-10
     - 1
     - 佐藤花子
     - ミルクチョコレート
     - 200
     - 2
   * - 1
     - 6
     - 2025-01-10
     - 1
     - 佐藤花子
     - ドリップコーヒー
     - 800
     - 1
   * - 3
     - 3
     - 2025-02-02
     - 1
     - 佐藤花子
     - ポテトチップス
     - 150
     - 3
   * - 3
     - 7
     - 2025-02-02
     - 1
     - 佐藤花子
     - 缶コーヒー
     - 120
     - 6

このテーブルの主キーは、注文番号と商品番号の組です。

第 2 正規形
^^^^^^^^^^^

第 2 正規形は、第 1 正規形であり、さらに主キーの一部だけで決まる列がない状態です。

上の表では、注文日、顧客番号、顧客名は注文番号だけで決まり、商品名は商品番号だけで決まります。そのため、注文日や商品名が何行にもわたって繰り返し格納されています。主キーの一部だけで決まる列を別のテーブルに分けると、次の 3 つのテーブルになります。

* 注文（注文番号、注文日、顧客番号、顧客名）
* 商品（商品番号、商品名）
* 注文明細（注文番号、商品番号、単価、数量）

単価は、注文した時点の単価を記録するため、注文明細に残しています。商品の現在の価格とは別の情報であり、重複ではありません。

第 3 正規形
^^^^^^^^^^^

第 3 正規形は、第 2 正規形であり、さらに主キー以外の列によって決まる列がない状態です。

上の「注文」テーブルでは、顧客名は顧客番号によって決まります。つまり、顧客名は主キー（注文番号）から顧客番号を経由して間接的に決まっています。顧客名を別のテーブルに分けると、次のようになります。

* 注文（注文番号、注文日、顧客番号）
* 顧客（顧客番号、顧客名）

こうして得られた構成は、サンプルデータベースの ``orders``、``customers``、``products``、``order_items`` テーブルの構成と同じです。

正規化のトレードオフ
^^^^^^^^^^^^^^^^^^^^

正規化するとデータの矛盾が起こりにくくなる一方で、データを取り出すときに結合が必要になります。集計や分析を高速に行うため、あえて正規化を崩した（非正規化した）テーブルを用意する場合もあります。まずは第 3 正規形を目安に設計し、性能上の問題がある場合に非正規化を検討するのが一般的です。

.. _exercises-ch11:

演習問題
--------

1. 顧客のお気に入り商品を管理する ``favorites`` テーブルを作成してください。列は ``customer_id``（顧客番号、``customers`` テーブルを参照）、``product_id``（商品番号、``products`` テーブルを参照）、``added_on``（追加日、文字列）とし、``customer_id`` と ``product_id`` の組を主キーとします。いずれの列も NULL を許さないものとします。
2. 1 で作成した ``favorites`` テーブルに、顧客番号 1 が商品番号 6 を 2025-06-01 に追加したデータを登録してください。その後、同じデータをもう一度登録しようとするとどうなるか確かめてください。
3. ``products`` テーブルに、商品の説明を格納する ``description`` 列（文字列）を追加してください。
4. 顧客ごとの注文件数と購入金額の合計（キャンセルされた注文を除く）を求めるビュー ``customer_summary`` を作成してください。注文のない顧客も、注文件数 0、購入金額 0 として含めてください。

解答は :ref:`answers-ch11` にあります。
