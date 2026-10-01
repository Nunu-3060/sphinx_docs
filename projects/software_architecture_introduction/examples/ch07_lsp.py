"""リスコフの置換原則（LSP）の例.

悪い例の BadReadOnlyFile は、BadFile を継承しているのに write を呼ぶと
例外を送出します。BadFile を受け取る関数に BadReadOnlyFile を渡すと、
その関数が壊れます。これは「サブクラスは基底クラスの代わりに使えなければ
ならない」という原則に反しています。

良い例では、読み込みと書き込みの能力を別々のインターフェースに分け、
書き込みが必要な関数は書き込みのできる型だけを受け取るようにします。

実行方法::

    python ch07_lsp.py
"""

from typing import Protocol

# ---------------------------------------------------------------------------
# 悪い例: サブクラスが基底クラスの約束を破る
# ---------------------------------------------------------------------------


class BadFile:
    """読み書きできるファイル（悪い例）."""

    def __init__(self) -> None:
        self._data = ""

    def read(self) -> str:
        return self._data

    def write(self, text: str) -> None:
        self._data += text


class BadReadOnlyFile(BadFile):
    """読み込み専用のファイル（悪い例）. write の約束を破っています."""

    def write(self, text: str) -> None:
        raise PermissionError("read-only file")


def bad_append_log(file: BadFile, message: str) -> None:
    """ファイルにログを追記します. 型の上では BadReadOnlyFile も渡せます."""
    file.write(message + "\n")


# ---------------------------------------------------------------------------
# 良い例: 能力ごとにインターフェースを分ける
# ---------------------------------------------------------------------------


class Readable(Protocol):
    """読み込みのできるもの."""

    def read(self) -> str:
        ...


class Writable(Protocol):
    """書き込みのできるもの."""

    def write(self, text: str) -> None:
        ...


class MemoryFile:
    """読み書きできるファイルです（Readable と Writable の両方を満たす）."""

    def __init__(self, data: str = "") -> None:
        self._data = data

    def read(self) -> str:
        return self._data

    def write(self, text: str) -> None:
        self._data += text


class ReadOnlyFile:
    """読み込み専用のファイルです（Readable だけを満たす）."""

    def __init__(self, data: str) -> None:
        self._data = data

    def read(self) -> str:
        return self._data


def append_log(file: Writable, message: str) -> None:
    """ファイルにログを追記します. ReadOnlyFile を渡すと mypy が検出します."""
    file.write(message + "\n")


def show(file: Readable) -> None:
    """ファイルの内容を表示します. どちらのファイルも渡せます."""
    print(repr(file.read()))


def main() -> None:
    """悪い例が実行時に失敗し、良い例では型の検査で防げることを示します."""
    try:
        bad_append_log(BadReadOnlyFile(), "start")
    except PermissionError as error:
        print("悪い例は実行時に失敗します:", error)

    log = MemoryFile()
    append_log(log, "start")
    show(log)
    show(ReadOnlyFile("settings"))
    # append_log(ReadOnlyFile("settings"), "start")  # mypy がエラーにする


if __name__ == "__main__":
    main()
