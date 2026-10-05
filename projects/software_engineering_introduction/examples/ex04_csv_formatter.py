"""演習問題 4-1 の解答例: CSV 形式で整形するクラスの追加（第 4 章）.

``ch04_srp_after.py`` の既存のクラスは一切変更せずに、
新しい整形クラスを追加するだけで CSV 形式の出力に対応できる。
"""

import csv
import io

from ch04_srp_after import SalesSummary


class CsvFormatter:
    """売上データを CSV 形式に整形する."""

    def format(self, summary: SalesSummary) -> str:
        """見出し行と各商品の行、合計行からなる CSV 文字列を返す."""
        buffer = io.StringIO()
        writer = csv.writer(buffer, lineterminator="\n")
        writer.writerow(["商品", "金額"])
        for name, amount in summary.sales.items():
            writer.writerow([name, amount])
        writer.writerow(["合計", summary.total()])
        return buffer.getvalue()


if __name__ == "__main__":
    summary = SalesSummary({"りんご": 1200, "みかん": 800})
    print(CsvFormatter().format(summary))
