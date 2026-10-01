"""独自例外の階層を設計する例.

アプリケーションの例外を 1 つの基底クラスにまとめると、呼び出し側は
「このアプリケーションが意図して送出したエラー」を一括して捕捉できます。
また、例外に必要な情報を属性として持たせると、メッセージの文字列を
解析しなくても原因を判別できます。

実行方法::

    python ch04_exceptions.py
"""


class ShopError(Exception):
    """このアプリケーションが送出する例外の基底クラスです."""


class OutOfStockError(ShopError):
    """在庫が足りないときに送出します."""

    def __init__(self, product: str, requested: int, available: int) -> None:
        super().__init__(
            f"{product} の在庫が足りません"
            f"（要求 {requested} 個、在庫 {available} 個）"
        )
        self.product = product
        self.requested = requested
        self.available = available


class UnknownProductError(ShopError):
    """存在しない商品が指定されたときに送出します."""

    def __init__(self, product: str) -> None:
        super().__init__(f"{product} という商品はありません")
        self.product = product


def reserve(stock: dict[str, int], product: str, quantity: int) -> int:
    """在庫を引き当て、引き当て後の在庫数を返します.

    Raises:
        ValueError: quantity が正の整数でない場合（呼び出し側の誤り）
        UnknownProductError: 商品が存在しない場合
        OutOfStockError: 在庫が足りない場合
    """
    if quantity <= 0:
        raise ValueError(f"quantity must be positive: {quantity}")
    if product not in stock:
        raise UnknownProductError(product)
    if stock[product] < quantity:
        raise OutOfStockError(product, quantity, stock[product])
    stock[product] -= quantity
    return stock[product]


def main() -> None:
    """いくつかの注文を処理し、エラーの種類に応じて対処します."""
    stock = {"apple": 5, "banana": 0}
    orders = [("apple", 3), ("banana", 1), ("cherry", 2), ("apple", 3)]
    for product, quantity in orders:
        try:
            remaining = reserve(stock, product, quantity)
        except OutOfStockError as error:
            # 属性から不足数を求め、入荷待ちの手配などに使える
            shortage = error.requested - error.available
            print(f"エラー: {error}（不足 {shortage} 個）")
        except ShopError as error:
            print(f"エラー: {error}")
        else:
            print(f"{product} を {quantity} 個引き当てました"
                  f"（残り {remaining} 個）")


if __name__ == "__main__":
    main()
