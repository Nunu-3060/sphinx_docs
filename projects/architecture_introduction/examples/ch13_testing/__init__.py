"""テストしやすい設計と、テストダブルの例.

* checkout: テストしにくい実装（hard_to_test_checkout）と、依存するものを
  注入できるようにした実装（CheckoutService）
* test_checkout: CheckoutService の単体テスト

テストの実行方法（examples フォルダーで実行します）::

    python -m unittest ch13_testing.test_checkout -v
"""
