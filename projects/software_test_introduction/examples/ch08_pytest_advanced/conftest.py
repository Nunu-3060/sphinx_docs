"""ch08_pytest_advanced フォルダーのテストで共有する fixture."""

import pytest

from shop.cart import Cart, Item


@pytest.fixture
def apple() -> Item:
    """単価 150 円の商品."""
    return Item("りんご", 150)


@pytest.fixture
def cart() -> Cart:
    """空のカート."""
    return Cart()


@pytest.fixture
def cart_with_apples(cart: Cart, apple: Item) -> Cart:
    """りんごを 3 個入れたカート（fixture は別の fixture を利用できる）."""
    cart.add(apple, 3)
    return cart
