"""アプリケーションサービス: 在庫管理のユースケースです.

リポジトリのインターフェースだけに依存し、保存の方法も表示の方法も
知りません。
"""

from .domain import InventoryError, Item, ItemRepository


class InventoryService:
    """商品の登録、入庫、出庫、一覧のユースケースです."""

    def __init__(self, repository: ItemRepository) -> None:
        self._repository = repository

    def register(self, sku: str, name: str) -> Item:
        """商品を登録します."""
        if self._repository.get(sku) is not None:
            raise InventoryError(f"{sku} は登録済みです")
        item = Item(sku, name)
        self._repository.save(item)
        return item

    def receive(self, sku: str, quantity: int) -> Item:
        """入庫します."""
        item = self._find(sku)
        item.receive(quantity)
        self._repository.save(item)
        return item

    def ship(self, sku: str, quantity: int) -> Item:
        """出庫します."""
        item = self._find(sku)
        item.ship(quantity)
        self._repository.save(item)
        return item

    def list_items(self) -> list[Item]:
        """すべての商品を返します."""
        return self._repository.list_all()

    def _find(self, sku: str) -> Item:
        item = self._repository.get(sku)
        if item is None:
            raise InventoryError(f"{sku} は登録されていません")
        return item
