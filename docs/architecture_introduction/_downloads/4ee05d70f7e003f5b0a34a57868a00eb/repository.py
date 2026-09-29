"""リポジトリ: 商品の保存を受け持ちます.

インターフェース（ItemRepository）は domain に定義しており、このモジュール
には、その実装（アダプター）だけを置きます。
"""

import copy
import json
from pathlib import Path

from .domain import Item


class InMemoryItemRepository:
    """商品をメモリ上に保存します（テスト用）."""

    def __init__(self) -> None:
        self._items: dict[str, Item] = {}

    def get(self, sku: str) -> Item | None:
        item = self._items.get(sku)
        return copy.copy(item) if item is not None else None

    def save(self, item: Item) -> None:
        self._items[item.sku] = copy.copy(item)

    def list_all(self) -> list[Item]:
        return [copy.copy(self._items[sku]) for sku in sorted(self._items)]


class JsonFileItemRepository:
    """商品を JSON ファイルに保存します."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def get(self, sku: str) -> Item | None:
        return self._load().get(sku)

    def save(self, item: Item) -> None:
        items = self._load()
        items[item.sku] = item
        records = {key: {"name": value.name, "quantity": value.quantity}
                   for key, value in sorted(items.items())}
        self._path.write_text(
            json.dumps(records, ensure_ascii=False, indent=2),
            encoding="utf-8")

    def list_all(self) -> list[Item]:
        items = self._load()
        return [items[sku] for sku in sorted(items)]

    def _load(self) -> dict[str, Item]:
        if not self._path.exists():
            return {}
        records = json.loads(self._path.read_text(encoding="utf-8"))
        return {sku: Item(sku, record["name"], record["quantity"])
                for sku, record in records.items()}
