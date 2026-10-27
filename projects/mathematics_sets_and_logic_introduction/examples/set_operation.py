"""集合演算・べき集合・直積を計算するサンプル。"""

from collections.abc import Iterable
from itertools import chain, combinations, product
from typing import TypeVar

T = TypeVar("T")
U = TypeVar("U")


def power_set(a: Iterable[T]) -> set[frozenset[T]]:
    """集合 a のべき集合を返す。

    set の要素はハッシュ可能でなければならないため、部分集合は frozenset で表す。
    """
    elements = list(a)
    subsets = chain.from_iterable(combinations(elements, k) for k in range(len(elements) + 1))
    return {frozenset(s) for s in subsets}


def cartesian_product(a: Iterable[T], b: Iterable[U]) -> set[tuple[T, U]]:
    """集合 a と b の直積を返す。"""
    return set(product(a, b))


def show(label: str, s: Iterable[object]) -> None:
    """集合の要素を並べ替えて表示する。"""
    print(f"{label}: {sorted(s, key=repr)}")


def main() -> None:
    universe = set(range(10))  # 全体集合 U = {0, 1, ..., 9}
    a = {x for x in universe if x % 2 == 0}  # 偶数
    b = {x for x in universe if x % 3 == 0}  # 3 の倍数

    show("A", a)
    show("B", b)
    show("A ∪ B", a | b)
    show("A ∩ B", a & b)
    show("A ∖ B", a - b)
    show("A △ B", a ^ b)
    show("A の補集合", universe - a)

    # ド・モルガンの法則: (A ∪ B) の補集合 = A の補集合 ∩ B の補集合
    print("ド・モルガンの法則:", universe - (a | b) == (universe - a) & (universe - b))

    print("{0, 6} ⊆ A ∩ B:", {0, 6} <= a & b)

    p = power_set({"a", "b", "c"})
    print("べき集合の要素数:", len(p))
    for subset in sorted(p, key=lambda s: (len(s), sorted(s))):
        print("  ", "{" + ", ".join(sorted(subset)) + "}" if subset else "∅")

    c = cartesian_product({1, 2}, {"x", "y", "z"})
    print("直積の要素数:", len(c))
    show("{1, 2} × {x, y, z}", c)


if __name__ == "__main__":
    main()
