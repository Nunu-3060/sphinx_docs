NULL の扱い
===========

SQL には、値が存在しないことや不明であることを表す NULL という特別な値があります。NULL は多くの初学者がつまずく点であり、後の章で説明する集計や結合の結果にも影響します。本章では、NULL の性質と扱い方を説明します。

NULL とは
---------

サンプルデータベースでは、次の値が NULL になっています。

* ``customers`` テーブルの ``email`` 列のうち、メールアドレスを登録していない顧客の値
* ``products`` テーブルの ``category_id`` 列のうち、どのカテゴリにも属さない商品（福袋）の値
* ``categories`` テーブルの ``parent_id`` 列のうち、最上位のカテゴリの値

.. code-block:: sql
   :linenos:

   SELECT customer_id, name, email
   FROM customers;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - customer\_id
     - name
     - email
   * - 1
     - 佐藤花子
     - hanako\@example.com
   * - 2
     - 鈴木一郎
     - ichiro\@example.com
   * - 3
     - 高橋美咲
     - NULL
   * - 4
     - 田中健太
     - kenta\@example.com
   * - 5
     - 伊藤さくら
     - sakura\@example.com
   * - 6
     - 渡辺翔
     - NULL
   * - 7
     - 山本優子
     - yuko\@example.com
   * - 8
     - 中村大輔
     - daisuke\@example.com

NULL は、数値の 0 や空文字列（``''``）とは異なります。0 は「0 という値がある」ことを、空文字列は「長さ 0 の文字列がある」ことを表しますが、NULL は「値がない」ことを表します。Python の ``None`` に近い概念ですが、次に説明するように、比較や計算での振る舞いは大きく異なります。

NULL を含む比較と計算
---------------------

メールアドレスを登録していない顧客を探すつもりで、次のように書いてみます。

.. code-block:: sql
   :linenos:

   SELECT customer_id, name
   FROM customers
   WHERE email = NULL;

結果は 0 行です。

1 行も取り出されないのは、NULL との比較の結果が、真（TRUE）でも偽（FALSE）でもなく、NULL になるためです。値が不明なので、比較の結果も不明になると考えてください。

.. code-block:: sql
   :linenos:

   SELECT NULL = NULL, NULL <> 1, NULL + 1, NULL || 'abc';

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - NULL = NULL
     - NULL \<\> 1
     - NULL + 1
     - NULL \|\| 'abc'
   * - NULL
     - NULL
     - NULL
     - NULL

NULL どうしの比較も NULL になります。算術演算や文字列の連結でも、どちらかが NULL であれば結果は NULL になります。

Python では ``None == None`` は ``True`` になり、``None + 1`` は ``TypeError`` になります。SQL の NULL は、エラーにならずに静かに NULL を広げていく点に注意が必要です。

IS NULL と IS NOT NULL
----------------------

値が NULL かどうかを調べるには、``IS NULL`` または ``IS NOT NULL`` を使用します。

.. code-block:: sql
   :linenos:

   SELECT customer_id, name
   FROM customers
   WHERE email IS NULL;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - customer\_id
     - name
   * - 3
     - 高橋美咲
   * - 6
     - 渡辺翔

.. code-block:: sql
   :linenos:

   SELECT customer_id, name, email
   FROM customers
   WHERE email IS NOT NULL;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - customer\_id
     - name
     - email
   * - 1
     - 佐藤花子
     - hanako\@example.com
   * - 2
     - 鈴木一郎
     - ichiro\@example.com
   * - 4
     - 田中健太
     - kenta\@example.com
   * - 5
     - 伊藤さくら
     - sakura\@example.com
   * - 7
     - 山本優子
     - yuko\@example.com
   * - 8
     - 中村大輔
     - daisuke\@example.com

``IS NULL`` と ``IS NOT NULL`` の結果は、必ず TRUE か FALSE のどちらかになります。

三値論理
--------

SQL の条件式は、TRUE、FALSE に加えて、不明を表す UNKNOWN の 3 つの値をとります。NULL との比較の結果は UNKNOWN です。このような論理を三値論理と呼びます。SQLite では、UNKNOWN は NULL として表されます。

``AND``、``OR``、``NOT`` の結果は、次のようになります。

.. list-table:: AND の結果
   :header-rows: 1
   :stub-columns: 1

   * - ``AND``
     - TRUE
     - FALSE
     - UNKNOWN
   * - TRUE
     - TRUE
     - FALSE
     - UNKNOWN
   * - FALSE
     - FALSE
     - FALSE
     - FALSE
   * - UNKNOWN
     - UNKNOWN
     - FALSE
     - UNKNOWN

.. list-table:: OR の結果
   :header-rows: 1
   :stub-columns: 1

   * - ``OR``
     - TRUE
     - FALSE
     - UNKNOWN
   * - TRUE
     - TRUE
     - TRUE
     - TRUE
   * - FALSE
     - TRUE
     - FALSE
     - UNKNOWN
   * - UNKNOWN
     - TRUE
     - UNKNOWN
     - UNKNOWN

.. list-table:: NOT の結果
   :header-rows: 1

   * - 値
     - ``NOT`` を適用した結果
   * - TRUE
     - FALSE
   * - FALSE
     - TRUE
   * - UNKNOWN
     - UNKNOWN

「UNKNOWN は TRUE にも FALSE にもなり得る値」と考えると理解しやすくなります。たとえば「FALSE AND UNKNOWN」は、UNKNOWN が TRUE と FALSE のどちらであっても FALSE になるため、結果は FALSE です。一方、「TRUE AND UNKNOWN」は、UNKNOWN の値によって結果が変わるため、UNKNOWN です。

``WHERE`` 句は、条件が TRUE になる行だけを結果に含めます。条件が FALSE の行だけでなく、UNKNOWN の行も除外されます。

否定の条件と NULL
-----------------

三値論理の影響で、否定の条件を使うと、NULL の行が意図せず除外されることがあります。次の例は、「チョコレート」カテゴリ（``category_id`` が 8）以外の商品を取り出すつもりの SQL です。

.. code-block:: sql
   :linenos:

   SELECT name, category_id
   FROM products
   WHERE category_id <> 8;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - name
     - category\_id
   * - ポテトチップス
     - 4
   * - 醤油
     - 5
   * - 味噌
     - 5
   * - ドリップコーヒー
     - 6
   * - 缶コーヒー
     - 6
   * - 緑茶ティーバッグ
     - 7
   * - ボールペン
     - 3
   * - ノート
     - 3
   * - 抹茶ラテ
     - 7

``category_id`` が NULL の「福袋」は結果に含まれていません。``NULL <> 8`` が UNKNOWN になるためです。NULL の行も含めたい場合は、次のように明示的に条件を追加します。

.. code-block:: sql
   :linenos:

   SELECT name, category_id
   FROM products
   WHERE category_id <> 8 OR category_id IS NULL;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - name
     - category\_id
   * - ポテトチップス
     - 4
   * - 醤油
     - 5
   * - 味噌
     - 5
   * - ドリップコーヒー
     - 6
   * - 缶コーヒー
     - 6
   * - 緑茶ティーバッグ
     - 7
   * - ボールペン
     - 3
   * - ノート
     - 3
   * - 福袋
     - NULL
   * - 抹茶ラテ
     - 7

``NOT IN`` の括弧内に NULL が含まれる場合は、さらに注意が必要です。

.. code-block:: sql
   :linenos:

   SELECT name, category_id
   FROM products
   WHERE category_id NOT IN (8, NULL);

結果は 0 行です。

``category_id NOT IN (8, NULL)`` は ``category_id <> 8 AND category_id <> NULL`` と同じ意味であり、``category_id <> NULL`` が常に UNKNOWN になるため、条件全体が TRUE になることがないからです。括弧内に NULL を直接書くことはまれですが、8 章で説明するサブクエリの結果に NULL が含まれる場合に、この問題が起こります。

NULL を別の値に置き換える
-------------------------

``COALESCE()`` 関数は、引数を左から順に調べ、最初の NULL でない値を返します。NULL を別の値に置き換えて表示したい場合に使用します。

.. code-block:: sql
   :linenos:

   SELECT name, COALESCE(email, '（未登録）') AS email
   FROM customers;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - name
     - email
   * - 佐藤花子
     - hanako\@example.com
   * - 鈴木一郎
     - ichiro\@example.com
   * - 高橋美咲
     - （未登録）
   * - 田中健太
     - kenta\@example.com
   * - 伊藤さくら
     - sakura\@example.com
   * - 渡辺翔
     - （未登録）
   * - 山本優子
     - yuko\@example.com
   * - 中村大輔
     - daisuke\@example.com

SQLite では ``IFNULL(x, y)`` も使えますが、``COALESCE()`` は標準 SQL の関数であり、多くの DBMS で使用できます。

逆に、``NULLIF(a, b)`` 関数は、``a`` と ``b`` が等しい場合に NULL を、そうでない場合に ``a`` を返します。0 による割り算を避けたい場合などに使用します。SQLite では 0 で割った結果は NULL になりますが、DBMS によってはエラーになるため、``x / NULLIF(y, 0)`` のように書いておくと安全です。

.. code-block:: sql
   :linenos:

   SELECT name, stock, 1000 / NULLIF(stock, 0) AS ratio
   FROM products
   WHERE category_id = 5;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - name
     - stock
     - ratio
   * - 醤油
     - 20
     - 50
   * - 味噌
     - 0
     - NULL

NULL の並べ替え
---------------

``ORDER BY`` 句で並べ替えると、SQLite では NULL は最も小さい値として扱われ、昇順では先頭に並びます。``NULLS FIRST`` または ``NULLS LAST`` を指定すると、NULL の位置を明示できます。

.. code-block:: sql
   :linenos:

   SELECT name, category_id
   FROM products
   ORDER BY category_id NULLS LAST;

.. list-table::
   :header-rows: 1
   :class: sql-result

   * - name
     - category\_id
   * - ボールペン
     - 3
   * - ノート
     - 3
   * - ポテトチップス
     - 4
   * - 醤油
     - 5
   * - 味噌
     - 5
   * - ドリップコーヒー
     - 6
   * - 缶コーヒー
     - 6
   * - 緑茶ティーバッグ
     - 7
   * - 抹茶ラテ
     - 7
   * - ミルクチョコレート
     - 8
   * - ビターチョコレート
     - 8
   * - 福袋
     - NULL

NULL を先頭と末尾のどちらに並べるかの既定の動作は、DBMS によって異なります。たとえば PostgreSQL では、昇順で NULL は末尾に並びます。

pandas の欠損値との違い
-----------------------

pandas では、欠損値は ``NaN``、``None``、``pd.NA`` などで表されます。SQL の NULL と pandas の欠損値には、次のような対応関係があります。

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - SQL
     - pandas
   * - ``email IS NULL``
     - ``df["email"].isna()``
   * - ``email IS NOT NULL``
     - ``df["email"].notna()``
   * - ``COALESCE(email, '（未登録）')``
     - ``df["email"].fillna("（未登録）")``

pandas でも、``NaN == NaN`` は ``False`` になり、欠損値との比較で意図しない結果になる点は SQL と共通しています。ただし、NumPy の型の列（欠損値が ``NaN``）では、比較演算の結果は ``True`` か ``False`` のどちらかになり、SQL のような三値論理にはなりません。一方、欠損値を ``pd.NA`` で表す型（``Int64`` 型や ``boolean`` 型など）では、欠損値との比較の結果は ``<NA>`` になり、SQL に近い三値論理で扱われます。

.. _exercises-ch05:

演習問題
--------

1. ``categories`` テーブルから、最上位のカテゴリ（親カテゴリがないカテゴリ）の名前を取り出してください。
2. ``products`` テーブルから、商品名と、カテゴリ番号を表す列を取り出してください。カテゴリ番号が NULL の場合は 0 と表示してください。
3. 次の SQL 文の結果が何行になるかを、実行する前に考えてください。その後、実際に実行して確かめてください。

   .. code-block:: sql
      :linenos:

      SELECT name FROM customers WHERE email = email;

4. ``products`` テーブルから、カテゴリ番号が 3 でない商品の商品名を、カテゴリ番号が NULL の商品も含めて取り出してください。

解答は :ref:`answers-ch05` にあります。
