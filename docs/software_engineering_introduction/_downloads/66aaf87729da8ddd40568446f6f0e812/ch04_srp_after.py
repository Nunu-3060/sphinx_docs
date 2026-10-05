"""単一責任の原則を適用した後のコード（第 4 章）.

集計・整形・保存の責任を別々のクラスに分けた。
例えばレポートの書式を変えたいときは ``TextFormatter`` だけを修正すればよい。
"""

from pathlib import Path


class SalesSummary:
    """売上データを保持し、集計する."""

    def __init__(self, sales: dict[str, int]) -> None:
        self.sales = sales

    def total(self) -> int:
        """売上の合計を返す."""
        return sum(self.sales.values())


class TextFormatter:
    """売上データをテキスト形式に整形する."""

    def format(self, summary: SalesSummary) -> str:
        """整形済みの文字列を返す."""
        lines = [
            f"{name}: {amount} 円" for name, amount in summary.sales.items()
        ]
        lines.append(f"合計: {summary.total()} 円")
        return "\n".join(lines)


class FileWriter:
    """文字列をファイルに保存する."""

    def write(self, path: Path, text: str) -> None:
        """``text`` を UTF-8 で ``path`` に書き込む."""
        path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    summary = SalesSummary({"りんご": 1200, "みかん": 800})
    print(TextFormatter().format(summary))
