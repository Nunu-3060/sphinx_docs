"""pytest で Cart をテストする（6 章の unittest 版と同じ内容）."""

import pytest

from shop.cart import Cart, Item

APPLE = Item("りんご", 150)
MELON = Item("メロン", 2000)


def test_new_cart_is_empty() -> None:
    cart = Cart()
    assert cart.is_empty()
    assert cart.subtotal() == 0


def test_add_same_item_accumulates_quantity() -> None:
    cart = Cart()
    cart.add(APPLE, 2)
    cart.add(APPLE, 3)
    assert cart.quantity_of(APPLE) == 5


def test_subtotal_is_sum_of_price_times_quantity() -> None:
    cart = Cart()
    cart.add(APPLE, 2)
    cart.add(MELON)
    assert cart.subtotal() == 150 * 2 + 2000


def test_add_zero_quantity_raises_value_error() -> None:
    cart = Cart()
    with pytest.raises(ValueError, match="1 以上"):
        cart.add(APPLE, 0)


def test_remove_item_not_in_cart_raises_key_error() -> None:
    cart = Cart()
    with pytest.raises(KeyError):
        cart.remove(MELON)
