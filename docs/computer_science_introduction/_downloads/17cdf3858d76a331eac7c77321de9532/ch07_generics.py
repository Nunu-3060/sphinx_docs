"""ジェネリックな関数とクラスのサンプル。

Python 3.12 の型パラメータ構文を使って、要素の型に依存しない関数と
クラスを定義する。mypy --strict で検査すると、型の誤りが無いことを
確認できる。main() の中のコメントにした行を有効にすると mypy がエラーを報告する。

実行方法: python ch07_generics.py
型検査: python -m mypy ch07_generics.py
関連する章: 第 7 章「プログラミング言語処理系」
"""

from collections.abc import Callable
from typing import Any, Protocol


def first[T](xs: list[T]) -> T:
    """リストの先頭の要素を返す。戻り値の型は要素の型と同じになる。"""
    return xs[0]


def map_list[T, U](f: Callable[[T], U], xs: list[T]) -> list[U]:
    """各要素に f を適用したリストを返す。"""
    return [f(x) for x in xs]


class Stack[T]:
    """要素の型を型パラメータ T で表すスタック。"""

    def __init__(self) -> None:
        """空のスタックを作る。"""
        self._items: list[T] = []

    def push(self, item: T) -> None:
        """要素を積む。"""
        self._items.append(item)

    def pop(self) -> T:
        """最後に積んだ要素を取り出す。"""
        return self._items.pop()

    def __len__(self) -> int:
        """要素数を返す。"""
        return len(self._items)


class Comparable(Protocol):
    """< で比較できる型を表すプロトコル。"""

    def __lt__(self, other: Any, /) -> bool:
        """自身が other より小さければ True を返す。"""
        ...


def max_of[C: Comparable](xs: list[C]) -> C:
    """最大の要素を返す。C は比較できる型に制限されている（上限付き）。"""
    best = xs[0]
    for x in xs[1:]:
        if best < x:
            best = x
    return best


def main() -> None:
    """ジェネリックな関数とクラスを異なる型で使う。"""
    n: int = first([10, 20, 30])
    s: str = first(["a", "b"])
    lengths: list[int] = map_list(len, ["apple", "kiwi"])
    print(n, s, lengths)

    ints: Stack[int] = Stack()
    ints.push(1)
    ints.push(2)
    print(ints.pop() + 10, len(ints))

    words: Stack[str] = Stack()
    words.push("hello")
    print(words.pop().upper())
    # ints.push("three")  # mypy: incompatible type "str"; expected "int"

    print(max_of([3, 9, 4]), max_of(["pear", "apple"]))


if __name__ == "__main__":
    main()
