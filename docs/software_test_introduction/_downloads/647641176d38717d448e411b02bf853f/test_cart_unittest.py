"""unittest で Cart をテストする."""

import unittest

from shop.cart import Cart, Item


class TestCart(unittest.TestCase):
    """Cart のテスト."""

    def setUp(self) -> None:
        """各テストの前に、空のカートと商品を用意する."""
        self.cart = Cart()
        self.apple = Item("りんご", 150)
        self.melon = Item("メロン", 2000)

    def test_new_cart_is_empty(self) -> None:
        self.assertTrue(self.cart.is_empty())
        self.assertEqual(self.cart.subtotal(), 0)

    def test_add_same_item_accumulates_quantity(self) -> None:
        self.cart.add(self.apple, 2)
        self.cart.add(self.apple, 3)
        self.assertEqual(self.cart.quantity_of(self.apple), 5)

    def test_subtotal_is_sum_of_price_times_quantity(self) -> None:
        self.cart.add(self.apple, 2)
        self.cart.add(self.melon)
        self.assertEqual(self.cart.subtotal(), 150 * 2 + 2000)

    def test_add_zero_quantity_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            self.cart.add(self.apple, 0)

    def test_remove_item_not_in_cart_raises_key_error(self) -> None:
        with self.assertRaises(KeyError):
            self.cart.remove(self.melon)


if __name__ == "__main__":
    unittest.main()
