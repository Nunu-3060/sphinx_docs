"""在庫管理 CLI（段階 1: 1 本のスクリプト）.

思いつくままに上から順に書いたスクリプトです。動作はしますが、
コマンドの解析、在庫の規則、保存、表示がすべて混ざっています。

実行方法（このファイルのあるフォルダーで実行します）::

    python inventory.py register A-1 ボールペン
    python inventory.py receive A-1 10
    python inventory.py ship A-1 7
    python inventory.py list
"""

import json
import sys
from pathlib import Path
from typing import Any

path = Path("inventory.json")
data: dict[str, Any]
if path.exists():
    data = json.loads(path.read_text(encoding="utf-8"))
else:
    data = {}

args = sys.argv[1:]
if len(args) == 0:
    print("使い方: inventory.py register|receive|ship|list ...")
    sys.exit(1)

if args[0] == "register":
    if len(args) != 3:
        print("使い方: inventory.py register 商品コード 商品名")
        sys.exit(1)
    if args[1] in data:
        print(f"エラー: {args[1]} は登録済みです")
        sys.exit(1)
    data[args[1]] = {"name": args[2], "quantity": 0}
    print(f"{args[1]} を登録しました")
elif args[0] == "receive":
    if len(args) != 3:
        print("使い方: inventory.py receive 商品コード 数量")
        sys.exit(1)
    if args[1] not in data:
        print(f"エラー: {args[1]} は登録されていません")
        sys.exit(1)
    q = int(args[2])
    if q <= 0:
        print("エラー: 数量は 1 以上です")
        sys.exit(1)
    data[args[1]]["quantity"] += q
    print(f"{args[1]} を {q} 個入庫しました")
elif args[0] == "ship":
    if len(args) != 3:
        print("使い方: inventory.py ship 商品コード 数量")
        sys.exit(1)
    if args[1] not in data:
        print(f"エラー: {args[1]} は登録されていません")
        sys.exit(1)
    q = int(args[2])
    if q <= 0:
        print("エラー: 数量は 1 以上です")
        sys.exit(1)
    if data[args[1]]["quantity"] < q:
        print(f"エラー: {args[1]} の在庫が足りません")
        sys.exit(1)
    data[args[1]]["quantity"] -= q
    print(f"{args[1]} を {q} 個出庫しました")
elif args[0] == "list":
    for sku in sorted(data):
        mark = "（要発注）" if data[sku]["quantity"] < 5 else ""
        print(f"{sku} {data[sku]['name']}: {data[sku]['quantity']}{mark}")
else:
    print(f"エラー: 不明なコマンドです: {args[0]}")
    sys.exit(1)

path.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8")
