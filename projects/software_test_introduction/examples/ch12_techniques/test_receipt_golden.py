"""領収書の文面をゴールデンファイル（期待する出力を保存したファイル）と比べる.

文面の変更が意図したものであれば、環境変数 UPDATE_GOLDEN=1 を設定して
テストを実行し、ゴールデンファイルを更新する。
"""

import os
from pathlib import Path

from receipt import format_receipt
from shop.cart import Cart, Item

GOLDEN = Path(__file__).parent / "golden" / "receipt.txt"


def test_receipt_matches_golden_file() -> None:
    apple = Item("りんご", 150)
    melon = Item("メロン", 2000)
    cart = Cart()
    cart.add(apple, 3)
    cart.add(melon)

    actual = format_receipt(cart, [apple, melon], shipping_fee=500)

    if os.environ.get("UPDATE_GOLDEN") == "1":
        GOLDEN.write_text(actual, encoding="utf-8")
    assert actual == GOLDEN.read_text(encoding="utf-8")
