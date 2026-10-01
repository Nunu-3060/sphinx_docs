"""循環 import を起こすプログラム（悪い例）.

customers を import すると、その途中で orders が import され、orders は
まだ初期化の終わっていない customers から Customer を import しようとして
ImportError になります。
"""

from .customers import Customer
from .orders import Order


def main() -> None:
    """顧客と注文を作ります（ここまで到達しません）."""
    customer = Customer("佐藤")
    customer.orders.append(Order("A-001", 1200, customer))
    print(customer.total_spent())


if __name__ == "__main__":
    main()
