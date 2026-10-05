"""発展課題 4-A の解答例: ReportService のテスト（第 4 章）.

``MemoryWriter`` を渡すことで、ファイルを作らずにテストできる。
実行方法: ``python -m unittest adv04_test_report_service``
"""

import unittest

from adv04_report_service import MemoryWriter, ReportService
from ch04_srp_after import SalesSummary, TextFormatter
from ex04_csv_formatter import CsvFormatter


class TestReportService(unittest.TestCase):
    """``ReportService`` のテスト."""

    def setUp(self) -> None:
        self.summary = SalesSummary({"りんご": 1200, "みかん": 800})
        self.writer = MemoryWriter()

    def test_publish_text_report(self) -> None:
        """テキスト形式のレポートが指定した名前で保存される."""
        ReportService(TextFormatter(), self.writer).publish(
            self.summary, "report.txt"
        )
        self.assertIn("合計: 2000 円", self.writer.files["report.txt"])

    def test_publish_csv_report(self) -> None:
        """整形方法を差し替えると CSV 形式で保存される."""
        ReportService(CsvFormatter(), self.writer).publish(
            self.summary, "report.csv"
        )
        self.assertIn("合計,2000", self.writer.files["report.csv"])


if __name__ == "__main__":
    unittest.main()
