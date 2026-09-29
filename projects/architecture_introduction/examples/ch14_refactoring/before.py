"""請求書を作る処理（リファクタリング前）.

次のようなコードの臭いがあります。

* 長い関数: 計算、割引、整形がすべて 1 つの関数にある
* マジックナンバー: 0.08、0.95、10000 などの意味が書かれていない
* 重複: 小計の計算が if と else の両方にある
* 意味の分からない名前: s、t、p、i
* フラグ引数: ja によって出力の形式が変わる
* 基本データ型への執着: 顧客や明細を辞書のまま扱っている
"""

from typing import Any


def make_invoice(customer: dict[str, str], items: list[dict[str, Any]],
                 ja: bool) -> str:
    s = ""
    t = 0.0
    for i in items:
        if i["type"] == "food":
            p = i["price"] * i["qty"]
            tax = p * 0.08
        else:
            p = i["price"] * i["qty"]
            tax = p * 0.1
        t += p + tax
        s = s + i["name"] + " x" + str(i["qty"]) + " " + str(int(p + tax))
        s = s + "\n"
    if customer["rank"] == "gold":
        t = t * 0.95
    if customer["rank"] == "gold" and t > 10000:
        t = t - 500
    if ja:
        s = s + "合計: " + str(int(t)) + " 円"
        s = customer["name"] + " 様\n" + s
    else:
        s = s + "Total: " + str(int(t)) + " JPY"
        s = "Dear " + customer["name"] + "\n" + s
    return s
