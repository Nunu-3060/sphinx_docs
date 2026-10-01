"""顧客と注文を組み合わせた集計を行うモジュール."""

from collections.abc import Iterable

from .customers import Customer
from .orders import Order


def total_spent(customer: Customer, orders: Iterable[Order]) -> int:
    """顧客のこれまでの注文の合計金額を返します."""
    return sum(order.amount for order in orders
               if order.customer.customer_id == customer.customer_id)


def format_total(customer: Customer, orders: Iterable[Order]) -> str:
    """顧客の合計金額を表示用の文字列にします."""
    return f"{customer.name} 様: {_yen(total_spent(customer, orders))}"


def _yen(amount: int) -> str:
    """金額を円の表記にします（モジュールの内部だけで使います）."""
    return f"{amount:,} 円"
