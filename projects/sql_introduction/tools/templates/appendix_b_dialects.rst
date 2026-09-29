付録 B SQL の方言比較
=====================

本資料で使用した SQLite と、広く使われている PostgreSQL、MySQL の主な違いをまとめます。細かな動作はバージョンや設定によって異なるため、実際に使用する際は各 DBMS のドキュメントを確認してください。

データ型と定義
--------------

.. list-table::
   :header-rows: 1
   :widths: 22 26 26 26

   * - 項目
     - SQLite
     - PostgreSQL
     - MySQL
   * - 型の検査
     - 緩やか（型アフィニティ）。``STRICT`` テーブルでは厳密
     - 厳密
     - 厳密（SQL モードの設定による）
   * - 主キーの自動採番
     - ``INTEGER PRIMARY KEY``
     - ``GENERATED ALWAYS AS IDENTITY`` または ``SERIAL``
     - ``AUTO_INCREMENT``
   * - 日付・時刻の型
     - なし（``TEXT`` などで格納）
     - ``DATE``、``TIMESTAMP`` など
     - ``DATE``、``DATETIME`` など
   * - 真偽値の型
     - なし（``INTEGER`` の 0 と 1 で表す）
     - ``BOOLEAN``
     - ``BOOLEAN``（``TINYINT(1)`` の別名）
   * - 外部キーの制約
     - 既定で無効（``PRAGMA foreign_keys = ON;`` で有効化）
     - 常に有効
     - 常に有効（InnoDB の場合）
   * - 識別子の引用符
     - ``"name"``
     - ``"name"``
     - :code:`\`name\``（設定により ``"name"`` も可）

式と関数
--------

.. list-table::
   :header-rows: 1
   :widths: 22 26 26 26

   * - 項目
     - SQLite
     - PostgreSQL
     - MySQL
   * - 文字列の連結
     - ``a || b``
     - ``a || b``
     - ``CONCAT(a, b)``（``||`` は既定では論理和）
   * - 整数どうしの割り算（``7 / 2``）
     - ``3``
     - ``3``
     - ``3.5000``（整数の商は ``7 DIV 2``）
   * - ``LIKE`` の大文字と小文字
     - 英字は区別しません
     - 区別します（区別しない検索には ``ILIKE`` を使います）
     - 照合順序によります（既定では区別しません）
   * - 現在の日付
     - ``date('now')``
     - ``CURRENT_DATE``
     - ``CURRENT_DATE`` または ``CURDATE()``
   * - 日付の加算
     - ``date(d, '+7 days')``
     - ``d + INTERVAL '7 days'``
     - ``DATE_ADD(d, INTERVAL 7 DAY)``
   * - 日付の書式変換
     - ``strftime('%Y-%m', d)``
     - ``to_char(d, 'YYYY-MM')``
     - ``DATE_FORMAT(d, '%Y-%m')``

文と句
------

.. list-table::
   :header-rows: 1
   :widths: 22 26 26 26

   * - 項目
     - SQLite
     - PostgreSQL
     - MySQL
   * - 行数の制限
     - ``LIMIT n``
     - ``LIMIT n`` または ``FETCH FIRST n ROWS ONLY``
     - ``LIMIT n``
   * - UPSERT
     - ``ON CONFLICT ... DO UPDATE``
     - ``ON CONFLICT ... DO UPDATE``
     - ``ON DUPLICATE KEY UPDATE``
   * - ``RETURNING`` 句
     - 使用できます（3.35 以降）
     - 使用できます
     - 使用できません
   * - ``FULL JOIN``
     - 使用できます（3.39 以降）
     - 使用できます
     - 使用できません
   * - ``GROUP BY`` にない列の ``SELECT``
     - エラーになりません
     - エラー（主キーでグループ化した場合を除く）
     - エラー（``ONLY_FULL_GROUP_BY`` が有効な場合）
   * - ``ALTER TABLE`` でできる変更
     - 名前の変更、列の追加と削除
     - 型や制約の変更を含め、ほぼすべて
     - 型や制約の変更を含め、ほぼすべて

Python からの接続
-----------------

.. list-table::
   :header-rows: 1
   :widths: 22 26 26 26

   * - 項目
     - SQLite
     - PostgreSQL
     - MySQL
   * - 主なモジュール
     - ``sqlite3``（標準ライブラリ）
     - psycopg
     - mysqlclient、PyMySQL
   * - プレースホルダー
     - ``?`` または ``:name``
     - ``%s`` または ``%(name)s``
     - ``%s`` または ``%(name)s``
   * - サーバー
     - 不要（ファイルに直接アクセス）
     - 必要
     - 必要

プレースホルダーの書き方はモジュールによって異なりますが、「値を SQL 文に直接埋め込まずにプレースホルダーで渡す」という原則は共通です。
