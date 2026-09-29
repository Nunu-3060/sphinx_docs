"""Template Method パターンの例.

処理の大まかな手順（解析 → 検証 → 結果の報告）を基底クラスで
決め、手順の一部だけをサブクラスで実装します。手順を定めた run には
typing.final を付けたので、サブクラスで run を上書きすると mypy が
エラーにします。これにより、処理の流れがサブクラスごとにばらつきません。

実行方法::

    python ch08_template_method.py
"""

from abc import ABC, abstractmethod
from typing import final


class Importer(ABC):
    """データの取り込みの手順を定めた基底クラスです."""

    @final
    def run(self, text: str) -> list[dict[str, str]]:
        """テンプレートメソッドです. 手順の順序はここで固定します."""
        rows = self.parse(text)
        valid_rows = [row for row in rows if self.validate(row)]
        print(f"[{type(self).__name__}] {len(rows)} 件中 "
              f"{len(valid_rows)} 件を取り込みました")
        return valid_rows

    @abstractmethod
    def parse(self, text: str) -> list[dict[str, str]]:
        """テキストを行のリストに変換します（サブクラスで実装）."""

    def validate(self, row: dict[str, str]) -> bool:
        """行が正しいかを返します. 必要ならサブクラスで上書きします."""
        return all(row.values())


class CsvImporter(Importer):
    """カンマ区切りのテキストを取り込みます."""

    def parse(self, text: str) -> list[dict[str, str]]:
        header, *lines = text.strip().splitlines()
        keys = header.split(",")
        return [dict(zip(keys, line.split(","))) for line in lines]


class KeyValueImporter(Importer):
    """「キー=値; キー=値」形式のテキストを取り込みます."""

    def parse(self, text: str) -> list[dict[str, str]]:
        rows = []
        for line in text.strip().splitlines():
            pairs = (item.split("=", 1) for item in line.split(";"))
            rows.append({key.strip(): value.strip() for key, value in pairs})
        return rows

    def validate(self, row: dict[str, str]) -> bool:
        return super().validate(row) and "name" in row


def main() -> None:
    """2 種類の形式のデータを、同じ手順で取り込みます."""
    print(CsvImporter().run("name,price\napple,120\ntea,\n"))
    print(KeyValueImporter().run("name=apple; price=120\nprice=150\n"))


if __name__ == "__main__":
    main()
