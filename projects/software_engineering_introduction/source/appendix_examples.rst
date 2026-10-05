サンプルコード一覧
==================

本書で使用したサンプルコードと、演習問題・発展課題の解答例のコードの一覧を次に示す。ファイル名が ``ch`` で始まるものは本文のサンプル、``ex`` で始まるものは演習問題、``adv`` で始まるものは発展課題に関するものである。ファイル名のリンクからダウンロードできる。すべてのサンプルコードは Python 3.10 以降で動作し、標準ライブラリのみを使用している。解答例のコードの一部は本文のサンプルを import して利用するため、同じフォルダーに置いて実行する。

.. list-table:: サンプルコード一覧
   :header-rows: 1
   :widths: 35 15 50

   * - ファイル
     - 章
     - 内容
   * - :download:`ch04_srp_before.py <../examples/ch04_srp_before.py>`
     - 第 4 章
     - 単一責任の原則を適用する前のコード
   * - :download:`ch04_srp_after.py <../examples/ch04_srp_after.py>`
     - 第 4 章
     - 単一責任の原則を適用した後のコード
   * - :download:`ch04_dip.py <../examples/ch04_dip.py>`
     - 第 4 章
     - 依存性逆転の原則と依存性の注入
   * - :download:`ch05_strategy.py <../examples/ch05_strategy.py>`
     - 第 5 章
     - Strategy パターン
   * - :download:`ch05_observer.py <../examples/ch05_observer.py>`
     - 第 5 章
     - Observer パターン
   * - :download:`ch06_type_hints.py <../examples/ch06_type_hints.py>`
     - 第 6 章
     - 型ヒントと静的型検査
   * - :download:`ch07_boundary.py <../examples/ch07_boundary.py>`
     - 第 7 章
     - 境界値分析の対象となる関数
   * - :download:`ch07_test_boundary.py <../examples/ch07_test_boundary.py>`
     - 第 7 章
     - 境界値分析に基づくテスト
   * - :download:`ch07_stack.py <../examples/ch07_stack.py>`
     - 第 7 章
     - テスト駆動開発で作成したスタック
   * - :download:`ch07_test_stack.py <../examples/ch07_test_stack.py>`
     - 第 7 章
     - スタックのテスト
   * - :download:`ch09_refactoring_before.py <../examples/ch09_refactoring_before.py>`
     - 第 9 章
     - リファクタリング前のコード
   * - :download:`ch09_refactoring_after.py <../examples/ch09_refactoring_after.py>`
     - 第 9 章
     - リファクタリング後のコード
   * - :download:`ch10_cyclomatic.py <../examples/ch10_cyclomatic.py>`
     - 第 10 章
     - サイクロマティック複雑度の簡易計算
   * - :download:`ch10_availability.py <../examples/ch10_availability.py>`
     - 第 10 章
     - 可用性の計算
   * - :download:`ch11_cocomo.py <../examples/ch11_cocomo.py>`
     - 第 11 章
     - 基本 COCOMO による見積もり
   * - :download:`ex04_csv_formatter.py <../examples/ex04_csv_formatter.py>`
     - 第 4 章
     - 演習問題 4-1 の解答例（CSV 形式の整形）
   * - :download:`ex05_tiered_rate.py <../examples/ex05_tiered_rate.py>`
     - 第 5 章
     - 演習問題 5-1 の解答例（段階的な送料の戦略）
   * - :download:`ex05_temperature_logger.py <../examples/ex05_temperature_logger.py>`
     - 第 5 章
     - 演習問題 5-2 の解答例（温度の履歴を記録する観察者）
   * - :download:`ex07_shipping.py <../examples/ex07_shipping.py>`
     - 第 7 章
     - 演習問題 7-3 の対象となる関数
   * - :download:`ex07_test_shipping.py <../examples/ex07_test_shipping.py>`
     - 第 7 章
     - 演習問題 7-3 の解答例（デシジョンテーブルに基づくテスト）
   * - :download:`ex07_stack_peek.py <../examples/ex07_stack_peek.py>`
     - 第 7 章
     - 演習問題 7-4 の解答例（peek メソッドの追加）
   * - :download:`ex07_test_stack_peek.py <../examples/ex07_test_stack_peek.py>`
     - 第 7 章
     - 演習問題 7-4 の解答例（peek メソッドのテスト）
   * - :download:`adv04_report_service.py <../examples/adv04_report_service.py>`
     - 第 4 章
     - 発展課題 4-A の解答例（保存先を差し替えられるレポート出力）
   * - :download:`adv04_test_report_service.py <../examples/adv04_test_report_service.py>`
     - 第 4 章
     - 発展課題 4-A の解答例（テスト）
   * - :download:`adv05_function_strategy.py <../examples/adv05_function_strategy.py>`
     - 第 5 章
     - 発展課題 5-A の解答例（関数による Strategy パターン）
   * - :download:`adv06_check.py <../examples/adv06_check.py>`
     - 第 6 章
     - 発展課題 6-A の解答例（品質検査をまとめて実行するスクリプト）
   * - :download:`adv07_test_random_fee.py <../examples/adv07_test_random_fee.py>`
     - 第 7 章
     - 発展課題 7-A の解答例（ランダムな入力によるテスト）
   * - :download:`adv09_invoice_before.py <../examples/adv09_invoice_before.py>`
     - 第 9 章
     - 発展課題 9-A の対象となるレガシーコード
   * - :download:`adv09_invoice_after.py <../examples/adv09_invoice_after.py>`
     - 第 9 章
     - 発展課題 9-A の解答例（リファクタリング後）
   * - :download:`adv09_test_invoice.py <../examples/adv09_test_invoice.py>`
     - 第 9 章
     - 発展課題 9-A の解答例（仕様化テスト）
   * - :download:`adv10_complexity_gate.py <../examples/adv10_complexity_gate.py>`
     - 第 10 章
     - 発展課題 10-A の解答例（複雑度の上限の検査）
   * - :download:`adv11_monte_carlo.py <../examples/adv11_monte_carlo.py>`
     - 第 11 章
     - 発展課題 11-A の解答例（モンテカルロ法による見積もり）

実行方法
--------

各サンプルコードは、ダウンロードしたフォルダーで次のように実行できる。

.. code-block:: text
   :linenos:

   python ch05_strategy.py

テストのサンプル（ファイル名に ``_test_`` を含むもの）は、テスト対象のファイルと同じフォルダーに置き、次のように実行する。このコマンドは、フォルダー内のすべてのテストをまとめて実行する。

.. code-block:: text
   :linenos:

   python -m unittest discover -p "*_test_*.py"

``ch10_cyclomatic.py`` は、解析するファイルを引数に指定して実行する。

.. code-block:: text
   :linenos:

   python ch10_cyclomatic.py ch07_boundary.py
