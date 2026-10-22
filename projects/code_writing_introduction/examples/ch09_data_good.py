"""第 9 章「データの扱い方」の良い例。"""

from dataclasses import dataclass
from enum import Enum


def visit(visit_count: int) -> int:
    return visit_count + 1


def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    if tags is None:
        tags = []
    tags.append(tag)
    return tags


@dataclass
class Book:
    title: str
    price: int
    is_available: bool


def describe_book(book: Book) -> str:
    if book.is_available:
        return f"{book.title}（{book.price}円）は貸し出しできる"
    return f"{book.title}（{book.price}円）は貸し出し中である"


class OrderStatus(Enum):
    SHIPPED = "shipped"
    DELIVERED = "delivered"


STATUS_MESSAGES = {
    OrderStatus.SHIPPED: "発送済み",
    OrderStatus.DELIVERED: "配達済み",
}


def status_message(status: OrderStatus) -> str:
    return STATUS_MESSAGES[status]


if __name__ == "__main__":
    count = 0
    count = visit(count)
    count = visit(count)
    print(count)
    print(add_tag("Python"))
    print(add_tag("入門"))
    print(describe_book(Book(title="Python 入門", price=2000, is_available=True)))
    print(status_message(OrderStatus.SHIPPED))
