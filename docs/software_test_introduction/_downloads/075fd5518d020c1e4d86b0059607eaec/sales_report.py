"""売上の CSV ファイルを読み込み、商品別の集計をファイルに書き出す."""

import csv
from collections import defaultdict
from pathlib import Path


def load_sales(path: Path) -> list[tuple[str, int]]:
    """売上の CSV ファイル（列: product, amount）を読み込む.

    Raises:
        ValueError: amount が整数として読めない行がある場合。
    """
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows: list[tuple[str, int]] = []
        for line_no, row in enumerate(reader, start=2):
            try:
                rows.append((row["product"], int(row["amount"])))
            except ValueError as e:
                raise ValueError(f"{line_no} 行目の金額が不正です") from e
        return rows


def write_summary(sales: list[tuple[str, int]], path: Path) -> None:
    """商品別の売上合計を、金額の大きい順に CSV ファイルへ書き出す."""
    totals: defaultdict[str, int] = defaultdict(int)
    for product, amount in sales:
        totals[product] += amount
    ranking = sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["product", "total"])
        writer.writerows(ranking)
