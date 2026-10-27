"""対角線論法とカントールの定理を有限の場合で確かめるサンプル。"""

from collections.abc import Sequence
from itertools import product


def diagonal(sequences: Sequence[Sequence[int]]) -> list[int]:
    """n 個の 0-1 列の n 番目の項を反転させた列を返す。

    返す列は、i 番目の列と i 番目の項が異なるので、どの列とも一致しない。
    """
    return [1 - s[i] for i, s in enumerate(sequences)]


def cantor_counterexample(a: Sequence[int], f: dict[int, frozenset[int]]) -> frozenset[int]:
    """写像 f: A → P(A) に対し、D = {x ∈ A | x ∉ f(x)} を返す。"""
    return frozenset(x for x in a if x not in f[x])


def main() -> None:
    sequences = [
        [0, 1, 1, 0, 1],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
    ]
    d = diagonal(sequences)
    print("対角線から作った列:", d)
    print("一覧に含まれるか:", d in sequences)

    # A = {0, 1, 2} から P(A) へのすべての写像について、D が像に含まれないことを確かめる。
    a = [0, 1, 2]
    # 各要素を含むか（1）含まないか（0）の組から、A の部分集合をすべて作る。
    subsets = [
        frozenset(x for x, bit in zip(a, bits) if bit)
        for bits in product((0, 1), repeat=len(a))
    ]
    count = 0
    for values in product(subsets, repeat=len(a)):
        f = dict(zip(a, values))
        assert cantor_counterexample(a, f) not in f.values()
        count += 1
    print(f"{count} 個の写像 A → P(A) のいずれも全射でない")


if __name__ == "__main__":
    main()
