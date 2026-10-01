"""売上レポートを出力するスクリプト（設計を考えずに書いた例）.

CSV の読み込み、集計、表示がひとつの流れに混ざっています。
動作はしますが、「集計の方法だけを変えたい」「表示先をファイルに変えたい」
といった変更のたびに、全体を読み直す必要があります。

実行方法::

    python ch02_report_script.py
"""

import csv
import io

SALES_CSV = """date,category,product,price,quantity
2026-04-01,food,apple,120,10
2026-04-01,drink,tea,150,4
2026-04-02,food,bread,200,3
2026-04-02,drink,coffee,300,5
2026-04-03,food,apple,120,-1
2026-04-03,goods,pen,100,7
"""

totals: dict[str, int] = {}
reader = csv.DictReader(io.StringIO(SALES_CSV))
for row in reader:
    q = int(row["quantity"])
    if q > 0:
        if row["category"] in totals:
            totals[row["category"]] = (
                totals[row["category"]] + int(row["price"]) * q
            )
        else:
            totals[row["category"]] = int(row["price"]) * q
    else:
        print("skip:", row)
print("=== 売上レポート ===")
grand = 0
for k in sorted(totals, key=lambda c: totals[c], reverse=True):
    print(f"{k:<8}{totals[k]:>8,} 円")
    grand = grand + totals[k]
print(f"{'合計':<7}{grand:>8,} 円")
