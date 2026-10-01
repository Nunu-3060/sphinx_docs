"""conftest.py の fixture を使って Cart をテストする."""

from shop.cart import Cart, Item


def test_new_cart_is_empty(cart: Cart) -> None:
    assert cart.is_empty()


def test_subtotal(cart_with_apples: Cart) -> None:
    assert cart_with_apples.subtotal() == 450


def test_remove(cart_with_apples: Cart, apple: Item) -> None:
    cart_with_apples.remove(apple)
    assert cart_with_apples.is_empty()


def test_fixture_is_created_for_each_test(cart_with_apples: Cart,
                                          apple: Item) -> None:
    # 前のテストで remove しても、このテストには影響しない
    assert cart_with_apples.quantity_of(apple) == 3
