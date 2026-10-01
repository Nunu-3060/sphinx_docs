"""在庫管理 CLI（段階 3: データをクラスにする）.

段階 2 の辞書を、商品を表すクラス Item に置き換えました。入庫と出庫の
規則は Item のメソッドになり、在庫の数が負になるような操作は Item の
中で防ぎます。コマンドの解析には argparse を使います。

実行方法（このファイルのあるフォルダーで実行します）::

    python inventory.py register A-1 ボールペン
    python inventory.py list
"""

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

DATA_FILE = Path("inventory.json")
REORDER_POINT = 5  # 在庫がこの数を下回ったら発注する


class InventoryError(Exception):
    """在庫の操作ができないときに送出します."""


@dataclass
class Item:
    """在庫を管理する商品です."""

    sku: str
    name: str
    quantity: int = 0

    @property
    def needs_reorder(self) -> bool:
        """発注が必要かどうかを返します."""
        return self.quantity < REORDER_POINT

    def receive(self, quantity: int) -> None:
        """入庫します."""
        _check_positive(quantity)
        self.quantity += quantity

    def ship(self, quantity: int) -> None:
        """出庫します."""
        _check_positive(quantity)
        if self.quantity < quantity:
            raise InventoryError(f"{self.sku} の在庫が足りません")
        self.quantity -= quantity


def _check_positive(quantity: int) -> None:
    if quantity <= 0:
        raise InventoryError("数量は 1 以上です")


def load_items(path: Path) -> dict[str, Item]:
    """ファイルから商品を読み込みます."""
    if not path.exists():
        return {}
    records = json.loads(path.read_text(encoding="utf-8"))
    return {sku: Item(sku, record["name"], record["quantity"])
            for sku, record in records.items()}


def save_items(path: Path, items: dict[str, Item]) -> None:
    """商品をファイルに保存します."""
    records = {sku: {"name": items[sku].name, "quantity": items[sku].quantity}
               for sku in sorted(items)}
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2),
                    encoding="utf-8")


def find(items: dict[str, Item], sku: str) -> Item:
    """商品コードに一致する商品を返します."""
    try:
        return items[sku]
    except KeyError:
        raise InventoryError(f"{sku} は登録されていません") from None


def format_item(item: Item) -> str:
    """商品を 1 行の文字列にします."""
    mark = "（要発注）" if item.needs_reorder else ""
    return f"{item.sku} {item.name}: {item.quantity}{mark}"


def build_parser() -> argparse.ArgumentParser:
    """コマンドライン引数の解析器を作ります."""
    parser = argparse.ArgumentParser(description="在庫管理 CLI")
    commands = parser.add_subparsers(dest="command", required=True)
    register = commands.add_parser("register", help="商品を登録する")
    register.add_argument("sku")
    register.add_argument("name")
    for name, help_text in (("receive", "入庫する"), ("ship", "出庫する")):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("sku")
        command.add_argument("quantity", type=int)
    commands.add_parser("list", help="在庫の一覧を表示する")
    return parser


def main(argv: list[str]) -> int:
    """コマンドを実行し、終了コードを返します."""
    args = build_parser().parse_args(argv)
    items = load_items(DATA_FILE)
    try:
        if args.command == "register":
            if args.sku in items:
                raise InventoryError(f"{args.sku} は登録済みです")
            items[args.sku] = Item(args.sku, args.name)
            print(f"{args.sku} を登録しました")
        elif args.command == "receive":
            find(items, args.sku).receive(args.quantity)
            print(f"{args.sku} を {args.quantity} 個入庫しました")
        elif args.command == "ship":
            find(items, args.sku).ship(args.quantity)
            print(f"{args.sku} を {args.quantity} 個出庫しました")
        elif args.command == "list":
            for sku in sorted(items):
                print(format_item(items[sku]))
    except InventoryError as error:
        print(f"エラー: {error}")
        return 1
    save_items(DATA_FILE, items)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
