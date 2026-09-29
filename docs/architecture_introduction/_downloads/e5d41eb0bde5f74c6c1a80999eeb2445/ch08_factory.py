"""Factory（生成の分離）の例.

設定の文字列から、どのクラスのオブジェクトを作るかを決める処理を
1 か所にまとめます。利用する側は、具体的なクラス名を知らずに済みます。

実行方法::

    python ch08_factory.py
"""

import json
from collections.abc import Callable
from typing import Protocol


class Exporter(Protocol):
    """データを文字列に書き出すもののインターフェースです."""

    def export(self, rows: list[dict[str, str]]) -> str:
        ...


class CsvExporter:
    """CSV 形式で書き出します."""

    def export(self, rows: list[dict[str, str]]) -> str:
        if not rows:
            return ""
        header = ",".join(rows[0])
        body = [",".join(row.values()) for row in rows]
        return "\n".join([header, *body])


class JsonExporter:
    """JSON 形式で書き出します."""

    def __init__(self, indent: int = 2) -> None:
        self._indent = indent

    def export(self, rows: list[dict[str, str]]) -> str:
        return json.dumps(rows, ensure_ascii=False, indent=self._indent)


# 形式の名前と、Exporter を作る関数の対応表
# 新しい形式は、この表に 1 行追加するだけで使えるようになります。
_EXPORTERS: dict[str, Callable[[], Exporter]] = {
    "csv": CsvExporter,
    "json": JsonExporter,
}


def create_exporter(format_name: str) -> Exporter:
    """形式の名前に対応する Exporter を作って返します."""
    try:
        factory = _EXPORTERS[format_name]
    except KeyError:
        supported = ", ".join(sorted(_EXPORTERS))
        raise ValueError(
            f"unsupported format: {format_name} (supported: {supported})"
        ) from None
    return factory()


def main() -> None:
    """設定された形式でデータを書き出します."""
    rows = [{"name": "apple", "price": "120"},
            {"name": "tea", "price": "150"}]
    for format_name in ("csv", "json"):
        print(f"--- {format_name} ---")
        print(create_exporter(format_name).export(rows))
    try:
        create_exporter("xml")
    except ValueError as error:
        print("エラー:", error)


if __name__ == "__main__":
    main()
