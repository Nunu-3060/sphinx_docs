"""有限集合上の二項関係の性質を判定し、同値類と推移閉包を求めるサンプル。

集合 A 上の二項関係 R は、A × A の部分集合（順序対の集合）として表す。
"""

from collections.abc import Callable, Iterable
from typing import TypeVar

T = TypeVar("T")
Relation = set[tuple[T, T]]


def relation_from(a: Iterable[T], predicate: Callable[[T, T], bool]) -> Relation[T]:
    """集合 a 上で predicate(x, y) が真になる順序対 (x, y) の集合を返す。"""
    elements = list(a)
    return {(x, y) for x in elements for y in elements if predicate(x, y)}


def is_reflexive(a: set[T], r: Relation[T]) -> bool:
    """反射律: すべての x について x R x。"""
    return all((x, x) in r for x in a)


def is_symmetric(r: Relation[T]) -> bool:
    """対称律: x R y ならば y R x。"""
    return all((y, x) in r for x, y in r)


def is_antisymmetric(r: Relation[T]) -> bool:
    """反対称律: x R y かつ y R x ならば x = y。"""
    return all(x == y for x, y in r if (y, x) in r)


def is_transitive(r: Relation[T]) -> bool:
    """推移律: x R y かつ y R z ならば x R z。"""
    return all((x, z) in r for x, y in r for y2, z in r if y == y2)


def is_equivalence(a: set[T], r: Relation[T]) -> bool:
    """同値関係（反射律・対称律・推移律）であるかを判定する。"""
    return is_reflexive(a, r) and is_symmetric(r) and is_transitive(r)


def is_partial_order(a: set[T], r: Relation[T]) -> bool:
    """半順序（反射律・反対称律・推移律）であるかを判定する。"""
    return is_reflexive(a, r) and is_antisymmetric(r) and is_transitive(r)


def equivalence_classes(a: set[T], r: Relation[T]) -> set[frozenset[T]]:
    """同値関係 r による a の同値類全体（商集合）を返す。"""
    return {frozenset(y for y in a if (x, y) in r) for x in a}


def compose(s: Relation[T], r: Relation[T]) -> Relation[T]:
    """合成 S ∘ R = {(x, z) | ある y について x R y かつ y S z} を返す。"""
    return {(x, z) for x, y in r for y2, z in s if y == y2}


def transitive_closure(r: Relation[T]) -> Relation[T]:
    """推移閉包（r を含む最小の推移的な関係）を返す。

    合成で得られる順序対を、新しい順序対が増えなくなるまで追加する。
    """
    closure = set(r)
    while True:
        extended = closure | compose(r, closure)
        if extended == closure:
            return closure
        closure = extended


def main() -> None:
    a = set(range(9))
    mod3 = relation_from(a, lambda x, y: (x - y) % 3 == 0)
    print("x ≡ y (mod 3) は同値関係か:", is_equivalence(a, mod3))
    for cls in sorted(equivalence_classes(a, mod3), key=min):
        print("  同値類:", sorted(cls))

    divisors = {1, 2, 3, 4, 6, 12}
    divides = relation_from(divisors, lambda x, y: y % x == 0)
    print("整除関係は半順序か:", is_partial_order(divisors, divides))
    print("整除関係は同値関係か:", is_equivalence(divisors, divides))

    # 直接の依存関係から、間接的なものを含む依存関係を求める。
    depends = {("app", "web"), ("web", "http"), ("http", "socket"), ("app", "db")}
    for x, y in sorted(transitive_closure(depends)):
        mark = "" if (x, y) in depends else "（間接）"
        print(f"  {x} は {y} に依存する{mark}")


if __name__ == "__main__":
    main()
