"""インターフェース分離の原則（ISP）の例.

悪い例の BadMachine インターフェースは印刷、スキャン、ファクスのすべてを
要求するので、印刷しかできないプリンターも、使わないメソッドを
実装しなければなりません。良い例では、利用者ごとに必要なメソッドだけを
持つ小さなインターフェースに分けます。

実行方法::

    python ch07_isp.py
"""

from abc import ABC, abstractmethod
from typing import Protocol

# ---------------------------------------------------------------------------
# 悪い例: 大きすぎるインターフェース
# ---------------------------------------------------------------------------


class BadMachine(ABC):
    """複合機のインターフェース（悪い例）."""

    @abstractmethod
    def print_document(self, document: str) -> None:
        ...

    @abstractmethod
    def scan(self) -> str:
        ...

    @abstractmethod
    def fax(self, number: str, document: str) -> None:
        ...


class BadSimplePrinter(BadMachine):
    """印刷しかできないプリンター（悪い例）."""

    def print_document(self, document: str) -> None:
        print(f"[print] {document}")

    def scan(self) -> str:
        raise NotImplementedError("scan is not supported")

    def fax(self, number: str, document: str) -> None:
        raise NotImplementedError("fax is not supported")


# ---------------------------------------------------------------------------
# 良い例: 利用者の必要に合わせた小さなインターフェース
# ---------------------------------------------------------------------------


class Printer(Protocol):
    """印刷のできるもの."""

    def print_document(self, document: str) -> None:
        ...


class Scanner(Protocol):
    """スキャンのできるもの."""

    def scan(self) -> str:
        ...


class SimplePrinter:
    """印刷しかできないプリンターです. 使わないメソッドを持ちません."""

    def print_document(self, document: str) -> None:
        print(f"[print] {document}")


class MultiFunctionPrinter:
    """印刷とスキャンのできる複合機です."""

    def print_document(self, document: str) -> None:
        print(f"[mfp print] {document}")

    def scan(self) -> str:
        return "scanned document"


def print_report(printer: Printer) -> None:
    """レポートを印刷します. 印刷の能力だけを要求します."""
    printer.print_document("月次レポート")


def copy_document(scanner: Scanner, printer: Printer) -> None:
    """スキャンした文書を印刷します."""
    printer.print_document(scanner.scan())


def main() -> None:
    """小さなインターフェースを使って、機器を組み合わせます."""
    BadSimplePrinter().print_document("月次レポート")

    simple = SimplePrinter()
    mfp = MultiFunctionPrinter()
    print_report(simple)
    print_report(mfp)
    copy_document(mfp, simple)


if __name__ == "__main__":
    main()
