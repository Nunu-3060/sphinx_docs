"""CLI: コマンドライン引数を解析し、サービスを呼び、結果を表示します."""

import argparse
from typing import TextIO

from .domain import InventoryError, Item
from .service import InventoryService

DEFAULT_FILE = "inventory.json"


def build_parser() -> argparse.ArgumentParser:
    """コマンドライン引数の解析器を作ります."""
    parser = argparse.ArgumentParser(description="在庫管理 CLI")
    parser.add_argument("--file", default=DEFAULT_FILE,
                        help=f"在庫を保存するファイル（既定: {DEFAULT_FILE}）")
    commands = parser.add_subparsers(dest="command", required=True)
    register = commands.add_parser("register", help="商品を登録する")
    register.add_argument("sku", help="商品コード")
    register.add_argument("name", help="商品名")
    for name, help_text in (("receive", "入庫する"), ("ship", "出庫する")):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("sku", help="商品コード")
        command.add_argument("quantity", type=int, help="数量")
    commands.add_parser("list", help="在庫の一覧を表示する")
    return parser


def format_item(item: Item) -> str:
    """商品を 1 行の文字列にします."""
    mark = "（要発注）" if item.needs_reorder else ""
    return f"{item.sku} {item.name}: {item.quantity}{mark}"


def execute(args: argparse.Namespace, service: InventoryService,
            out: TextIO) -> int:
    """解析済みの引数に従ってコマンドを実行し、終了コードを返します."""
    try:
        if args.command == "register":
            item = service.register(args.sku, args.name)
            print(f"{item.sku} を登録しました", file=out)
        elif args.command == "receive":
            item = service.receive(args.sku, args.quantity)
            print(f"{item.sku} を {args.quantity} 個入庫しました"
                  f"（在庫 {item.quantity} 個）", file=out)
        elif args.command == "ship":
            item = service.ship(args.sku, args.quantity)
            print(f"{item.sku} を {args.quantity} 個出庫しました"
                  f"（在庫 {item.quantity} 個）", file=out)
        elif args.command == "list":
            for item in service.list_items():
                print(format_item(item), file=out)
    except InventoryError as error:
        print(f"エラー: {error}", file=out)
        return 1
    return 0
