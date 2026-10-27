"""第 2 章 集合と論理のサンプルコード。

Python の set 型で集合演算とド・モルガンの法則を確かめ、
命題論理の真理値表を生成して論理式の同値性を調べる。
"""

from collections.abc import Callable
from itertools import product

# 2 変数の論理式を表す型（p, q の真理値を受け取り、式の真理値を返す）
Formula = Callable[[bool, bool], bool]


def show_set_operations(a: set[int], b: set[int], universe: set[int]) -> None:
    """和集合・共通部分・差集合・補集合・対称差を表示する。"""
    print(f"A       = {sorted(a)}")
    print(f"B       = {sorted(b)}")
    print(f"A | B   = {sorted(a | b)}")
    print(f"A & B   = {sorted(a & b)}")
    print(f"A - B   = {sorted(a - b)}")
    print(f"U - A   = {sorted(universe - a)}")
    print(f"A ^ B   = {sorted(a ^ b)}")


def check_de_morgan(a: set[int], b: set[int], universe: set[int]) -> bool:
    """ド・モルガンの法則が成り立つかどうかを返す。"""
    law1 = universe - (a | b) == (universe - a) & (universe - b)
    law2 = universe - (a & b) == (universe - a) | (universe - b)
    return law1 and law2


def power_set(s: set[int]) -> list[set[int]]:
    """べき集合を返す。

    要素数 n の集合の部分集合は、n ビットの整数 mask と 1 対 1 に対応する。
    mask の i ビット目が 1 のとき、i 番目の要素を部分集合に含める。
    """
    elements = sorted(s)
    subsets: list[set[int]] = []
    for mask in range(2 ** len(elements)):
        subsets.append({e for i, e in enumerate(elements) if (mask >> i) & 1})
    return subsets


def implies(p: bool, q: bool) -> bool:
    """含意 p → q の真理値を返す。"""
    return (not p) or q


def print_truth_table(name: str, formula: Formula) -> None:
    """2 変数の論理式の真理値表を表示する。"""
    print(f"{'p':<6}{'q':<6}{name}")
    for p, q in product([True, False], repeat=2):
        print(f"{p!s:<6}{q!s:<6}{formula(p, q)}")


def is_equivalent(f: Formula, g: Formula) -> bool:
    """2 つの論理式が論理的に同値か（すべての真理値の組で一致するか）を返す。"""
    return all(f(p, q) == g(p, q) for p, q in product([True, False], repeat=2))


def main() -> None:
    universe = set(range(1, 11))
    a = {x for x in universe if x % 2 == 0}  # 偶数
    b = {x for x in universe if x % 3 == 0}  # 3 の倍数

    print("--- 集合演算 ---")
    show_set_operations(a, b, universe)
    print(f"ド・モルガンの法則: {check_de_morgan(a, b, universe)}")

    print("--- べき集合 ---")
    subsets = power_set({1, 2, 3})
    print([sorted(t) for t in subsets])
    print(f"要素数: {len(subsets)}")

    print("--- 含意の真理値表 ---")
    print_truth_table("p -> q", implies)

    print("--- 同値性の判定 ---")

    def contrapositive(p: bool, q: bool) -> bool:
        return implies(not q, not p)

    def converse(p: bool, q: bool) -> bool:
        return implies(q, p)

    print(f"p -> q と 対偶 (not q) -> (not p): {is_equivalent(implies, contrapositive)}")
    print(f"p -> q と 逆 q -> p: {is_equivalent(implies, converse)}")


if __name__ == "__main__":
    main()
