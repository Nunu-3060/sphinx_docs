"""売上レポートを出力するスクリプト（役割ごとに分割した例）.

ch02_report_script.py と同じレポートを、次の 3 つの役割に分けて出力します。

* 読み込み: CSV の文字列から Sale のリストを作る
* 集計: カテゴリごとの売上を求める
* 表示: 集計結果を文字列に整形する

役割ごとに関数が分かれているので、変更の影響が及ぶ範囲が限られます。
また、集計の関数は入出力を持たないので、単体でテストできます。

実行方法::

    python ch02_report_structured.py
"""

import csv
import io
from collections.abc import Iterable
from dataclasses import dataclass

SALES_CSV = """date,category,product,price,quantity
2026-04-01,food,apple,120,10
2026-04-01,drink,tea,150,4
2026-04-02,food,bread,200,3
2026-04-02,drink,coffee,300,5
2026-04-03,food,apple,120,-1
2026-04-03,goods,pen,100,7
"""


@dataclass(frozen=True)
class Sale:
    """1 件の売上を表します."""

    category: str
    product: str
    price: int
    quantity: int

    @property
    def amount(self) -> int:
        """売上金額（単価 × 数量）を返します."""
        return self.price * self.quantity


def load_sales(text: str) -> list[Sale]:
    """CSV の文字列を読み込み、Sale のリストを返します."""
    reader = csv.DictReader(io.StringIO(text))
    return [
        Sale(
            category=row["category"],
            product=row["product"],
            price=int(row["price"]),
            quantity=int(row["quantity"]),
        )
        for row in reader
    ]


def is_valid(sale: Sale) -> bool:
    """集計の対象にする売上かどうかを返します（数量が正のものだけ）."""
    return sale.quantity > 0


def total_by_category(sales: Iterable[Sale]) -> dict[str, int]:
    """カテゴリごとの売上金額の合計を返します."""
    totals: dict[str, int] = {}
    for sale in sales:
        totals[sale.category] = totals.get(sale.category, 0) + sale.amount
    return totals


def format_report(totals: dict[str, int]) -> str:
    """集計結果を、売上の多い順に並べたレポートの文字列にします."""
    lines = ["=== 売上レポート ==="]
    for category, amount in sorted(
        totals.items(), key=lambda item: item[1], reverse=True
    ):
        lines.append(f"{category:<8}{amount:>8,} 円")
    lines.append(f"{'合計':<7}{sum(totals.values()):>8,} 円")
    return "\n".join(lines)


def main() -> None:
    """売上を読み込み、不正なデータを除いて集計し、レポートを表示します."""
    sales = load_sales(SALES_CSV)
    for sale in sales:
        if not is_valid(sale):
            print("skip:", sale)
    totals = total_by_category(sale for sale in sales if is_valid(sale))
    print(format_report(totals))


if __name__ == "__main__":
    main()
