"""ファイルの読み書きを含めて sales_report をテストする."""

from pathlib import Path

import pytest

from sales_report import load_sales, write_summary


@pytest.fixture
def sales_csv(tmp_path: Path) -> Path:
    """テスト用の売上ファイルを一時フォルダーに作る."""
    path = tmp_path / "sales.csv"
    path.write_text(
        "product,amount\n"
        "りんご,300\n"
        "メロン,2000\n"
        "りんご,450\n",
        encoding="utf-8",
    )
    return path


def test_load_sales(sales_csv: Path) -> None:
    assert load_sales(sales_csv) == [
        ("りんご", 300), ("メロン", 2000), ("りんご", 450)]


def test_load_sales_with_invalid_amount(tmp_path: Path) -> None:
    path = tmp_path / "broken.csv"
    path.write_text("product,amount\nりんご,三百\n", encoding="utf-8")
    with pytest.raises(ValueError, match="2 行目"):
        load_sales(path)


def test_load_and_write_summary(sales_csv: Path, tmp_path: Path) -> None:
    output = tmp_path / "summary.csv"

    write_summary(load_sales(sales_csv), output)

    assert output.read_text(encoding="utf-8").splitlines() == [
        "product,total",
        "メロン,2000",
        "りんご,750",
    ]
