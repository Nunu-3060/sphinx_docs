付録 C サンプルコードの一覧
===========================

本書のサンプルコードの一覧である。ファイル名を選ぶと、そのファイルをダウンロードできる。すべてのファイルは :download:`examples.zip <../build/extra/examples.zip>` から一括でダウンロードできる。

テストは ``examples`` フォルダーで ``python -m pytest`` を実行すると、まとめて実行できる（1.6 節）。ファイル名が ``test_`` で始まらない ``failing_example.py`` と ``buggy_codec_example.py`` は、失敗する様子を確かめるためのものであり、まとめて実行するときには収集されない。

C.1 共通
--------

.. list-table::
   :header-rows: 1
   :widths: 45 35 20

   * - ファイル
     - 内容
     - 説明している章
   * - :download:`pyproject.toml <../examples/pyproject.toml>`
     - pytest、mypy、coverage.py の設定
     - 7 章、14 章、17 章
   * - :download:`setup.cfg <../examples/setup.cfg>`
     - flake8 の設定
     - 13 章、17 章
   * - :download:`requirements-dev.txt <../examples/requirements-dev.txt>`
     - テストと静的解析に使うパッケージの一覧
     - 17 章

C.2 題材（shop パッケージ）
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 45 35 20

   * - ファイル
     - 内容
     - 説明している章
   * - :download:`shop/__init__.py <../examples/shop/__init__.py>`
     - パッケージの初期化
     - 1 章
   * - :download:`shop/shipping.py <../examples/shop/shipping.py>`
     - 送料の計算
     - 4 章
   * - :download:`shop/cart.py <../examples/shop/cart.py>`
     - ショッピングカート
     - 6 章
   * - :download:`shop/member.py <../examples/shop/member.py>`
     - 会員ランクの判定
     - 5 章
   * - :download:`shop/order.py <../examples/shop/order.py>`
     - 注文の状態の管理
     - 4 章、8 章

C.3 テストとサンプル
--------------------

.. list-table::
   :header-rows: 1
   :widths: 45 35 20

   * - ファイル
     - 内容
     - 説明している章
   * - :download:`ch06_unittest/test_cart_unittest.py <../examples/ch06_unittest/test_cart_unittest.py>`
     - unittest によるカートのテスト
     - 6 章
   * - :download:`ch07_pytest_basics/test_cart_pytest.py <../examples/ch07_pytest_basics/test_cart_pytest.py>`
     - pytest によるカートのテスト
     - 7 章
   * - :download:`ch07_pytest_basics/test_approx.py <../examples/ch07_pytest_basics/test_approx.py>`
     - 浮動小数点数の比較
     - 7 章
   * - :download:`ch07_pytest_basics/failing_example.py <../examples/ch07_pytest_basics/failing_example.py>`
     - 失敗したときの出力の確認用
     - 7 章
   * - :download:`ch08_pytest_advanced/conftest.py <../examples/ch08_pytest_advanced/conftest.py>`
     - 共有する fixture
     - 8 章
   * - :download:`ch08_pytest_advanced/test_cart_fixture.py <../examples/ch08_pytest_advanced/test_cart_fixture.py>`
     - fixture を使ったカートのテスト
     - 8 章
   * - :download:`ch08_pytest_advanced/test_shipping_table.py <../examples/ch08_pytest_advanced/test_shipping_table.py>`
     - 境界値分析とデシジョンテーブルのテスト
     - 8 章
   * - :download:`ch08_pytest_advanced/test_order_state.py <../examples/ch08_pytest_advanced/test_order_state.py>`
     - 状態遷移テスト
     - 8 章
   * - :download:`ch08_pytest_advanced/test_markers.py <../examples/ch08_pytest_advanced/test_markers.py>`
     - マーカーの使用例
     - 8 章
   * - :download:`ch08_pytest_advanced/test_builtin_fixtures.py <../examples/ch08_pytest_advanced/test_builtin_fixtures.py>`
     - 組み込みの fixture の使用例
     - 8 章
   * - :download:`ch09_test_double/order_notifier.py <../examples/ch09_test_double/order_notifier.py>`
     - 発送の通知（テスト対象）
     - 9 章
   * - :download:`ch09_test_double/test_order_notifier.py <../examples/ch09_test_double/test_order_notifier.py>`
     - テストダブルと Mock の使用例
     - 9 章
   * - :download:`ch09_test_double/lottery.py <../examples/ch09_test_double/lottery.py>`
     - 抽選（テスト対象）
     - 9 章
   * - :download:`ch09_test_double/test_lottery.py <../examples/ch09_test_double/test_lottery.py>`
     - patch の使用例
     - 9 章
   * - :download:`ch10_testable_design/campaign_before.py <../examples/ch10_testable_design/campaign_before.py>`
     - テストしにくいコード（改善前）
     - 10 章
   * - :download:`ch10_testable_design/campaign.py <../examples/ch10_testable_design/campaign.py>`
     - テストしやすいコード（改善後）
     - 10 章
   * - :download:`ch10_testable_design/test_campaign.py <../examples/ch10_testable_design/test_campaign.py>`
     - 改善後のコードのテスト
     - 10 章
   * - :download:`ch11_integration/sales_report.py <../examples/ch11_integration/sales_report.py>`
     - 売上の CSV ファイルの集計（テスト対象）
     - 11 章
   * - :download:`ch11_integration/test_sales_report.py <../examples/ch11_integration/test_sales_report.py>`
     - ファイルを使うテスト
     - 11 章
   * - :download:`ch11_integration/order_repository.py <../examples/ch11_integration/order_repository.py>`
     - 注文のデータベースへの保存（テスト対象）
     - 11 章
   * - :download:`ch11_integration/test_order_repository.py <../examples/ch11_integration/test_order_repository.py>`
     - データベースを使うテスト
     - 11 章
   * - :download:`ch11_integration/exchange_client.py <../examples/ch11_integration/exchange_client.py>`
     - 為替レートの API のクライアント（テスト対象）
     - 11 章
   * - :download:`ch11_integration/test_exchange_client.py <../examples/ch11_integration/test_exchange_client.py>`
     - HTTP の API を使うテスト
     - 11 章
   * - :download:`ch12_techniques/text_utils.py <../examples/ch12_techniques/text_utils.py>`
     - doctest の例
     - 12 章
   * - :download:`ch12_techniques/run_length.py <../examples/ch12_techniques/run_length.py>`
     - ランレングス符号化（テスト対象）
     - 12 章
   * - :download:`ch12_techniques/test_run_length_properties.py <../examples/ch12_techniques/test_run_length_properties.py>`
     - Hypothesis によるプロパティベーステスト
     - 12 章
   * - :download:`ch12_techniques/test_run_length_random.py <../examples/ch12_techniques/test_run_length_random.py>`
     - 標準ライブラリによる簡易なプロパティベーステスト
     - 12 章
   * - :download:`ch12_techniques/buggy_codec_example.py <../examples/ch12_techniques/buggy_codec_example.py>`
     - Hypothesis が欠陥を見つける例
     - 12 章
   * - :download:`ch12_techniques/receipt.py <../examples/ch12_techniques/receipt.py>`
     - 領収書の文面の作成（テスト対象）
     - 12 章
   * - :download:`ch12_techniques/test_receipt_golden.py <../examples/ch12_techniques/test_receipt_golden.py>`
     - ゴールデンテスト
     - 12 章
   * - :download:`ch12_techniques/golden/receipt.txt <../examples/ch12_techniques/golden/receipt.txt>`
     - ゴールデンファイル
     - 12 章
   * - :download:`ch14_coverage/test_member_rank_partial.py <../examples/ch14_coverage/test_member_rank_partial.py>`
     - 不十分なテスト（カバレッジの計測用）
     - 14 章
   * - :download:`ch14_coverage/test_member_rank_mcdc.py <../examples/ch14_coverage/test_member_rank_mcdc.py>`
     - MC/DC を満たすテスト
     - 14 章
   * - :download:`ch15_tdd/password_policy.py <../examples/ch15_tdd/password_policy.py>`
     - パスワードの規則の検査（最終版）
     - 15 章
   * - :download:`ch15_tdd/test_password_policy.py <../examples/ch15_tdd/test_password_policy.py>`
     - TDD で書いたテスト（最終版）
     - 15 章
   * - :download:`ch16_good_tests/test_good_practices.py <../examples/ch16_good_tests/test_good_practices.py>`
     - よいテストの書き方の例
     - 16 章
   * - :download:`ch17_automation/pre-commit-config.yaml <../examples/ch17_automation/pre-commit-config.yaml>`
     - pre-commit の設定の例
     - 17 章
   * - :download:`ch17_automation/test.yml <../examples/ch17_automation/test.yml>`
     - GitHub Actions の設定の例
     - 17 章
   * - :download:`ch17_automation/Jenkinsfile <../examples/ch17_automation/Jenkinsfile>`
     - Jenkins の設定の例
     - 17 章
