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
SQLFILE_ROWS

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

SQLFILE_INCLUDES
