"""注文のドメインモデルを、2 種類のリポジトリで動かします."""

import sqlite3

from .model import DomainError, OrderRepository
from .repository import InMemoryOrderRepository, SqliteOrderRepository
from .service import OrderService


def run(repository: OrderRepository) -> None:
    """注文を作って確定し、確定後の変更が拒否されることを示します."""
    service = OrderService(repository)
    order_id = service.create_order("C-1")
    service.add_item(order_id, "apple", 120, 10)
    service.add_item(order_id, "tea", 450, 2)
    service.add_item(order_id, "apple", 120, 5)
    print(f"{order_id} の請求額: {service.place_order(order_id, 'local')}")

    order = repository.get(order_id)
    assert order is not None
    for line in order.lines:
        print(f"  {line.product_id} x {line.quantity} = {line.subtotal}")
    try:
        service.add_item(order_id, "coffee", 300, 1)
    except DomainError as error:
        print("  エラー:", error)


def main() -> None:
    """メモリ版と SQLite 版のリポジトリで、同じユースケースを実行します."""
    print("=== InMemoryOrderRepository ===")
    run(InMemoryOrderRepository())

    print("=== SqliteOrderRepository ===")
    connection = sqlite3.connect(":memory:")
    try:
        run(SqliteOrderRepository(connection))
    finally:
        connection.close()


if __name__ == "__main__":
    main()
