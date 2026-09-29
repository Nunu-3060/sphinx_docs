"""循環 import を解消したパッケージを使うプログラム."""

from . import Customer, Order
from .reports import format_total


def main() -> None:
    """顧客と注文を作り、顧客ごとの合計金額を表示します."""
    sato = Customer("C-1", "佐藤")
    suzuki = Customer("C-2", "鈴木")
    orders = [
        Order("A-001", 1200, sato),
        Order("A-002", 3000, suzuki),
        Order("A-003", 800, sato),
    ]
    for order in orders:
        print(order.label())
    for customer in (sato, suzuki):
        print(format_total(customer, orders))


if __name__ == "__main__":
    main()
