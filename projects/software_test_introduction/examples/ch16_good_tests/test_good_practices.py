"""よいテストの書き方の例（AAA パターンと、振る舞いを表すテスト名）."""

import pytest

from shop.cart import Cart, Item
from shop.shipping import calc_shipping_fee


def make_cart(*prices: int) -> Cart:
    """指定した単価の商品を 1 個ずつ入れたカートを作る."""
    cart = Cart()
    for i, price in enumerate(prices):
        cart.add(Item(f"商品{i}", price))
    return cart


def test_regular_member_gets_free_shipping_at_5000_yen() -> None:
    # Arrange（準備）
    cart = make_cart(3000, 2000)

    # Act（実行）
    fee = calc_shipping_fee(cart.subtotal(), is_premium=False,
                            is_remote=False)

    # Assert（検証）
    assert fee == 0


def test_remote_surcharge_applies_even_when_shipping_is_free() -> None:
    cart = make_cart(5000)

    fee = calc_shipping_fee(cart.subtotal(), is_premium=False,
                            is_remote=True)

    assert fee == 1000


def test_removing_item_decreases_subtotal() -> None:
    cart = Cart()
    apple = Item("りんご", 150)
    cart.add(apple, 2)
    cart.add(Item("メロン", 2000))

    cart.remove(apple)

    # 内部の辞書（cart._quantities）ではなく、公開された振る舞いで検証する
    assert cart.subtotal() == 2000
    assert cart.quantity_of(apple) == 0


def test_adding_negative_quantity_is_rejected() -> None:
    cart = Cart()

    with pytest.raises(ValueError):
        cart.add(Item("りんご", 150), -1)

    assert cart.is_empty()
