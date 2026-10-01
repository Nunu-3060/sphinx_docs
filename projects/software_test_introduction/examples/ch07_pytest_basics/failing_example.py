"""失敗したときの出力を確認するためのテスト.

ファイル名が test_ で始まらないため、引数なしで pytest を実行したときは
収集されない。次のようにファイルを指定して実行する。

    python -m pytest ch07_pytest_basics/failing_example.py
"""

from shop.cart import Cart, Item


def test_subtotal_with_wrong_expectation() -> None:
    cart = Cart()
    cart.add(Item("りんご", 150), 3)
    assert cart.subtotal() == 400  # 正しくは 450
