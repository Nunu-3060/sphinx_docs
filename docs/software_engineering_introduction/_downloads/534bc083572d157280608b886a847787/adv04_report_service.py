"""発展課題 4-A の解答例: 保存先を差し替えられるレポート出力（第 4 章）.

``ReportService`` は整形方法（``Formatter``）と保存先（``Writer``）の
どちらにも、具体的なクラスではなく抽象に依存する。
そのため、テストではファイルを作らずにメモリー上で結果を確認できる。
"""

from pathlib import Path
from typing import Protocol

from ch04_srp_after import SalesSummary, TextFormatter


class Formatter(Protocol):
    """売上データを文字列に整形する手段の抽象."""

    def format(self, summary: SalesSummary) -> str:
        """整形済みの文字列を返す."""
        ...


class Writer(Protocol):
    """文字列を保存する手段の抽象."""

    def write(self, name: str, text: str) -> None:
        """``text`` を ``name`` という名前で保存する."""
        ...


class FileWriter:
    """指定したフォルダーにファイルとして保存する."""

    def __init__(self, directory: Path) -> None:
        self.directory = directory

    def write(self, name: str, text: str) -> None:
        (self.directory / name).write_text(text, encoding="utf-8")


class MemoryWriter:
    """保存した内容をメモリー上に保持する（テスト用）."""

    def __init__(self) -> None:
        self.files: dict[str, str] = {}

    def write(self, name: str, text: str) -> None:
        self.files[name] = text


class ReportService:
    """売上レポートを整形して保存する."""

    def __init__(self, formatter: Formatter, writer: Writer) -> None:
        self.formatter = formatter
        self.writer = writer

    def publish(self, summary: SalesSummary, name: str) -> None:
        """レポートを整形し、``name`` という名前で保存する."""
        self.writer.write(name, self.formatter.format(summary))


if __name__ == "__main__":
    memory = MemoryWriter()
    service = ReportService(TextFormatter(), memory)
    service.publish(SalesSummary({"りんご": 1200, "みかん": 800}), "report.txt")
    print(memory.files["report.txt"])
