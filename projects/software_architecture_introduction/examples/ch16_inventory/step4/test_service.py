"""在庫管理 CLI のテストです.

サービスのテストでは InMemoryItemRepository を使うので、ファイルを
作らずに済みます。JSON ファイルのリポジトリは、一時フォルダーを使って
別にテストします。
"""

import io
import tempfile
import unittest
from pathlib import Path

from .cli import build_parser, execute
from .domain import InventoryError, Item
from .repository import InMemoryItemRepository, JsonFileItemRepository
from .service import InventoryService


class ItemTest(unittest.TestCase):
    """ドメインの規則のテストです."""

    def test_ship_more_than_stock_is_rejected(self) -> None:
        item = Item("A-1", "ボールペン", 3)
        with self.assertRaises(InventoryError):
            item.ship(4)
        self.assertEqual(item.quantity, 3)

    def test_quantity_must_be_positive(self) -> None:
        item = Item("A-1", "ボールペン")
        for quantity in (0, -1):
            with self.subTest(quantity=quantity):
                with self.assertRaises(InventoryError):
                    item.receive(quantity)

    def test_needs_reorder_below_reorder_point(self) -> None:
        self.assertTrue(Item("A-1", "ボールペン", 4).needs_reorder)
        self.assertFalse(Item("A-1", "ボールペン", 5).needs_reorder)


class InventoryServiceTest(unittest.TestCase):
    """ユースケースのテストです."""

    def setUp(self) -> None:
        self.service = InventoryService(InMemoryItemRepository())
        self.service.register("A-1", "ボールペン")

    def test_receive_and_ship(self) -> None:
        self.service.receive("A-1", 10)
        item = self.service.ship("A-1", 7)
        self.assertEqual(item.quantity, 3)

    def test_register_twice_is_rejected(self) -> None:
        with self.assertRaises(InventoryError):
            self.service.register("A-1", "ボールペン")

    def test_unknown_item_is_rejected(self) -> None:
        with self.assertRaises(InventoryError):
            self.service.receive("Z-9", 1)

    def test_list_items_is_sorted_by_sku(self) -> None:
        self.service.register("B-1", "ノート")
        self.service.register("A-0", "消しゴム")
        skus = [item.sku for item in self.service.list_items()]
        self.assertEqual(skus, ["A-0", "A-1", "B-1"])


class JsonFileItemRepositoryTest(unittest.TestCase):
    """JSON ファイルのリポジトリのテストです."""

    def test_saved_item_can_be_loaded(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "inventory.json"
            JsonFileItemRepository(path).save(Item("A-1", "ボールペン", 8))
            loaded = JsonFileItemRepository(path).get("A-1")
        self.assertEqual(loaded, Item("A-1", "ボールペン", 8))


class CliTest(unittest.TestCase):
    """CLI の表示と終了コードのテストです."""

    def run_cli(self, service: InventoryService,
                *argv: str) -> tuple[int, str]:
        out = io.StringIO()
        code = execute(build_parser().parse_args(argv), service, out)
        return code, out.getvalue()

    def test_list_shows_reorder_mark(self) -> None:
        service = InventoryService(InMemoryItemRepository())
        self.run_cli(service, "register", "A-1", "ボールペン")
        self.run_cli(service, "receive", "A-1", "3")
        code, output = self.run_cli(service, "list")
        self.assertEqual(code, 0)
        self.assertEqual(output, "A-1 ボールペン: 3（要発注）\n")

    def test_error_returns_exit_code_1(self) -> None:
        service = InventoryService(InMemoryItemRepository())
        code, output = self.run_cli(service, "ship", "A-1", "1")
        self.assertEqual(code, 1)
        self.assertEqual(output, "エラー: A-1 は登録されていません\n")


if __name__ == "__main__":
    unittest.main()
