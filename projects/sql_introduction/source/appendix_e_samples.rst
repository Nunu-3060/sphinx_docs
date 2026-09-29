付録 E サンプルファイル一覧
===========================

本資料で使用するサンプルファイルの一覧です。ファイル名のリンクから個別にダウンロードできます。すべてのファイルをまとめた ZIP ファイルは `examples.zip <examples.zip>`_ からダウンロードできます。

ファイルの使い方は 3 章（:doc:`ch03_setup`）を参照してください。Python のファイルは、flake8 と mypy で問題が検出されないことを確認しています。``setup.cfg`` は、flake8 と mypy の設定ファイルです。``examples`` フォルダーで ``python -m flake8 .`` と ``python -m mypy .`` を実行すると、同じ確認ができます。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - ファイル
     - 内容
   * - :download:`create_shop_db.py <../examples/create_shop_db.py>`
     - サンプルデータベース ``shop.db`` を作成するスクリプト（3 章）
   * - :download:`run_query.py <../examples/run_query.py>`
     - SQL を実行して結果を表形式で表示するスクリプト（3 章）
   * - :download:`schema.sql <../examples/schema.sql>`
     - サンプルデータベースのテーブル定義
   * - :download:`data.sql <../examples/data.sql>`
     - サンプルデータベースのデータ
   * - :download:`ch03_first_query.py <../examples/ch03_first_query.py>`
     - Python から SQL を実行する最小の例（3 章）
   * - :download:`ch13_index_benchmark.py <../examples/ch13_index_benchmark.py>`
     - インデックスの有無による検索時間の比較（13 章）
   * - :download:`ch14_basics.py <../examples/ch14_basics.py>`
     - ``sqlite3`` モジュールの基本的な使い方（14 章）
   * - :download:`ch14_injection.py <../examples/ch14_injection.py>`
     - SQL インジェクションとその対策（14 章）
   * - :download:`ch14_transaction.py <../examples/ch14_transaction.py>`
     - Python からのトランザクションの制御（14 章）
   * - :download:`ch14_repository.py <../examples/ch14_repository.py>`
     - 型ヒントを付けたデータアクセス関数（14 章）
   * - :download:`ch14_pandas.py <../examples/ch14_pandas.py>`
     - pandas と SQL の組み合わせ（14 章）
   * - :download:`answers_ch14.py <../examples/answers_ch14.py>`
     - 14 章の演習問題の解答例
   * - :download:`setup.cfg <../examples/setup.cfg>`
     - flake8 と mypy の設定

``sql`` フォルダーには、各章の SQL の例と演習問題の解答を収録しています。``python run_query.py sql/ch04_select.sql`` のように実行できます。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - ファイル
     - 内容
   * - :download:`ch03_setup.sql <../examples/sql/ch03_setup.sql>`
     - 3 章 環境の準備
   * - :download:`ch04_select.sql <../examples/sql/ch04_select.sql>`
     - 4 章 データの取得
   * - :download:`ch05_null.sql <../examples/sql/ch05_null.sql>`
     - 5 章 NULL の扱い
   * - :download:`ch06_aggregate.sql <../examples/sql/ch06_aggregate.sql>`
     - 6 章 集計とグループ化
   * - :download:`ch07_join.sql <../examples/sql/ch07_join.sql>`
     - 7 章 テーブルの結合
   * - :download:`ch08_subquery.sql <../examples/sql/ch08_subquery.sql>`
     - 8 章 サブクエリと共通テーブル式
   * - :download:`ch09_window.sql <../examples/sql/ch09_window.sql>`
     - 9 章 ウィンドウ関数
   * - :download:`ch10_modify.sql <../examples/sql/ch10_modify.sql>`
     - 10 章 データの追加・更新・削除
   * - :download:`ch11_ddl.sql <../examples/sql/ch11_ddl.sql>`
     - 11 章 テーブルの設計と定義
   * - :download:`ch12_transaction.sql <../examples/sql/ch12_transaction.sql>`
     - 12 章 トランザクション
   * - :download:`ch13_index.sql <../examples/sql/ch13_index.sql>`
     - 13 章 インデックスと性能
   * - :download:`answers_ch04.sql <../examples/sql/answers_ch04.sql>`
     - 4 章 データの取得 演習問題の解答
   * - :download:`answers_ch05.sql <../examples/sql/answers_ch05.sql>`
     - 5 章 NULL の扱い 演習問題の解答
   * - :download:`answers_ch06.sql <../examples/sql/answers_ch06.sql>`
     - 6 章 集計とグループ化 演習問題の解答
   * - :download:`answers_ch07.sql <../examples/sql/answers_ch07.sql>`
     - 7 章 テーブルの結合 演習問題の解答
   * - :download:`answers_ch08.sql <../examples/sql/answers_ch08.sql>`
     - 8 章 サブクエリと共通テーブル式 演習問題の解答
   * - :download:`answers_ch09.sql <../examples/sql/answers_ch09.sql>`
     - 9 章 ウィンドウ関数 演習問題の解答
   * - :download:`answers_ch10.sql <../examples/sql/answers_ch10.sql>`
     - 10 章 データの追加・更新・削除 演習問題の解答
   * - :download:`answers_ch11.sql <../examples/sql/answers_ch11.sql>`
     - 11 章 テーブルの設計と定義 演習問題の解答
   * - :download:`answers_ch12.sql <../examples/sql/answers_ch12.sql>`
     - 12 章 トランザクション 演習問題の解答
   * - :download:`answers_ch13.sql <../examples/sql/answers_ch13.sql>`
     - 13 章 インデックスと性能 演習問題の解答

テーブル定義とデータ
--------------------

schema.sql
^^^^^^^^^^

.. literalinclude:: ../examples/schema.sql
   :language: sql
   :linenos:

data.sql
^^^^^^^^

.. literalinclude:: ../examples/data.sql
   :language: sql
   :linenos:

スクリプト
----------

本文で内容を示していないスクリプトを掲載します。

create_shop_db.py
^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/create_shop_db.py
   :language: python
   :linenos:

run_query.py
^^^^^^^^^^^^

.. literalinclude:: ../examples/run_query.py
   :language: python
   :linenos:

各章の SQL
----------

ch03_setup.sql
^^^^^^^^^^^^^^

.. literalinclude:: ../examples/sql/ch03_setup.sql
   :language: sql
   :linenos:

ch04_select.sql
^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/sql/ch04_select.sql
   :language: sql
   :linenos:

ch05_null.sql
^^^^^^^^^^^^^

.. literalinclude:: ../examples/sql/ch05_null.sql
   :language: sql
   :linenos:

ch06_aggregate.sql
^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/sql/ch06_aggregate.sql
   :language: sql
   :linenos:

ch07_join.sql
^^^^^^^^^^^^^

.. literalinclude:: ../examples/sql/ch07_join.sql
   :language: sql
   :linenos:

ch08_subquery.sql
^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/sql/ch08_subquery.sql
   :language: sql
   :linenos:

ch09_window.sql
^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/sql/ch09_window.sql
   :language: sql
   :linenos:

ch10_modify.sql
^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/sql/ch10_modify.sql
   :language: sql
   :linenos:

ch11_ddl.sql
^^^^^^^^^^^^

.. literalinclude:: ../examples/sql/ch11_ddl.sql
   :language: sql
   :linenos:

ch12_transaction.sql
^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/sql/ch12_transaction.sql
   :language: sql
   :linenos:

ch13_index.sql
^^^^^^^^^^^^^^

.. literalinclude:: ../examples/sql/ch13_index.sql
   :language: sql
   :linenos:

answers_ch04.sql
^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/sql/answers_ch04.sql
   :language: sql
   :linenos:

answers_ch05.sql
^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/sql/answers_ch05.sql
   :language: sql
   :linenos:

answers_ch06.sql
^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/sql/answers_ch06.sql
   :language: sql
   :linenos:

answers_ch07.sql
^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/sql/answers_ch07.sql
   :language: sql
   :linenos:

answers_ch08.sql
^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/sql/answers_ch08.sql
   :language: sql
   :linenos:

answers_ch09.sql
^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/sql/answers_ch09.sql
   :language: sql
   :linenos:

answers_ch10.sql
^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/sql/answers_ch10.sql
   :language: sql
   :linenos:

answers_ch11.sql
^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/sql/answers_ch11.sql
   :language: sql
   :linenos:

answers_ch12.sql
^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/sql/answers_ch12.sql
   :language: sql
   :linenos:

answers_ch13.sql
^^^^^^^^^^^^^^^^

.. literalinclude:: ../examples/sql/answers_ch13.sql
   :language: sql
   :linenos:
