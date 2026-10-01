"""リファクタリングの例.

* before: コードの臭いのある請求書の作成処理
* after: 振る舞いを変えずに書き換えた請求書の作成処理
* test_invoice: before と after の出力が一致することを確かめるテスト
  （仕様化テスト）

テストの実行方法（examples フォルダーで実行します）::

    python -m unittest ch14_refactoring.test_invoice -v
"""
