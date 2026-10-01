"""在庫管理 CLI（段階 2: 関数に分割）.

段階 1 のスクリプトを、役割ごとの関数に分けました。

* 保存: load_inventory, save_inventory
* 在庫の操作: register, receive, ship
* 表示: format_list
* コマンドの解析: main

エラーは例外 InventoryError で表し、表示は main でまとめて行います。
在庫のデータは、まだ辞書のままです。

実行方法（このファイルのあるフォルダーで実行します）::

    python inventory.py register A-1 ボールペン
    python inventory.py list
"""

import json
import sys
from pathlib import Path
from typing import Any

DATA_FILE = Path("inventory.json")
REORDER_POINT = 5  # 在庫がこの数を下回ったら発注する

Inventory = dict[str, dict[str, Any]]


class InventoryError(Exception):
    """在庫の操作ができないときに送出します."""


def load_inventory(path: Path) -> Inventory:
    """ファイルから在庫を読み込みます. ファイルがなければ空の在庫を返します."""
    if not path.exists():
        return {}
    result: Inventory = json.loads(path.read_text(encoding="utf-8"))
    return result


def save_inventory(path: Path, inventory: Inventory) -> None:
    """在庫をファイルに保存します."""
    path.write_text(json.dumps(inventory, ensure_ascii=False, indent=2),
                    encoding="utf-8")


def register(inventory: Inventory, sku: str, name: str) -> None:
    """商品を登録します."""
    if sku in inventory:
        raise InventoryError(f"{sku} は登録済みです")
    inventory[sku] = {"name": name, "quantity": 0}


def _check_quantity(inventory: Inventory, sku: str, quantity: int) -> None:
    if sku not in inventory:
        raise InventoryError(f"{sku} は登録されていません")
    if quantity <= 0:
        raise InventoryError("数量は 1 以上です")


def receive(inventory: Inventory, sku: str, quantity: int) -> None:
    """入庫します."""
    _check_quantity(inventory, sku, quantity)
    inventory[sku]["quantity"] += quantity


def ship(inventory: Inventory, sku: str, quantity: int) -> None:
    """出庫します."""
    _check_quantity(inventory, sku, quantity)
    if inventory[sku]["quantity"] < quantity:
        raise InventoryError(f"{sku} の在庫が足りません")
    inventory[sku]["quantity"] -= quantity


def format_list(inventory: Inventory) -> str:
    """在庫の一覧を文字列にします."""
    lines = []
    for sku in sorted(inventory):
        item = inventory[sku]
        mark = "（要発注）" if item["quantity"] < REORDER_POINT else ""
        lines.append(f"{sku} {item['name']}: {item['quantity']}{mark}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    """コマンドを実行し、終了コードを返します."""
    inventory = load_inventory(DATA_FILE)
    try:
        command, *params = argv
        if command == "register":
            sku, name = params
            register(inventory, sku, name)
            print(f"{sku} を登録しました")
        elif command == "receive":
            sku, quantity = params
            receive(inventory, sku, int(quantity))
            print(f"{sku} を {quantity} 個入庫しました")
        elif command == "ship":
            sku, quantity = params
            ship(inventory, sku, int(quantity))
            print(f"{sku} を {quantity} 個出庫しました")
        elif command == "list":
            print(format_list(inventory))
        else:
            raise InventoryError(f"不明なコマンドです: {command}")
    except InventoryError as error:
        print(f"エラー: {error}")
        return 1
    except ValueError:
        print("使い方: inventory.py register|receive|ship|list ...")
        return 1
    save_inventory(DATA_FILE, inventory)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
