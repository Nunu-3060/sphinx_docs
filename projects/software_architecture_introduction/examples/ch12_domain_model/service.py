"""アプリケーションサービス: 注文のユースケースを実装します.

リポジトリから集約を取り出し、集約のメソッドを呼び、保存する、という
手順を受け持ちます。ドメインの規則そのものは、ここには書きません。
"""

from .model import DomainError, Money, Order, OrderRepository, shipping_fee


class OrderService:
    """注文の作成、商品の追加、確定のユースケースです."""

    def __init__(self, repository: OrderRepository) -> None:
        self._repository = repository

    def create_order(self, customer_id: str) -> str:
        """新しい注文を作り、その ID を返します."""
        order = Order(self._repository.next_id(), customer_id)
        self._repository.save(order)
        return order.order_id

    def add_item(self, order_id: str, product_id: str, unit_price: int,
                 quantity: int) -> None:
        """注文に商品を追加します."""
        order = self._get(order_id)
        order.add_line(product_id, Money(unit_price), quantity)
        self._repository.save(order)

    def place_order(self, order_id: str, region: str) -> Money:
        """注文を確定し、送料を含む請求額を返します."""
        order = self._get(order_id)
        fee = shipping_fee(order, region)
        order.place()
        self._repository.save(order)
        return order.total + fee

    def _get(self, order_id: str) -> Order:
        order = self._repository.get(order_id)
        if order is None:
            raise DomainError(f"注文 {order_id} はありません")
        return order
