"""単一責任の原則を適用する前のコード（第 4 章）.

1 つのクラスが「売上の集計」「レポートの整形」「ファイルへの保存」という
3 つの責任を持っている。どれか 1 つの仕様が変わるだけでこのクラスを
修正する必要があり、変更の影響範囲が広くなる。
"""

from pathlib import Path


class SalesReport:
    """売上の集計・整形・保存をすべて担当するクラス."""

    def __init__(self, sales: dict[str, int]) -> None:
        self.sales = sales

    def total(self) -> int:
        """売上の合計を返す."""
        return sum(self.sales.values())

    def to_text(self) -> str:
        """レポートを文字列に整形する."""
        lines = [f"{name}: {amount} 円" for name, amount in self.sales.items()]
        lines.append(f"合計: {self.total()} 円")
        return "\n".join(lines)

    def save(self, path: Path) -> None:
        """レポートをファイルに保存する."""
        path.write_text(self.to_text(), encoding="utf-8")


if __name__ == "__main__":
    report = SalesReport({"りんご": 1200, "みかん": 800})
    print(report.to_text())
