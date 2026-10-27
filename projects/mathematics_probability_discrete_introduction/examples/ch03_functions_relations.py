"""第 3 章 写像と関係のサンプルコード。

有限集合の間の写像を dict で表し、単射・全射を判定する。
また、関係を順序対の集合で表し、同値関係の性質と同値類を調べる。
"""

from typing import TypeVar

X = TypeVar("X")
Y = TypeVar("Y")
Z = TypeVar("Z")

# 集合 A 上の関係（A × A の部分集合）
Relation = set[tuple[int, int]]


def is_injective(f: dict[X, Y]) -> bool:
    """写像 f が単射かどうかを返す（異なる元の像がすべて異なるか）。"""
    return len(set(f.values())) == len(f)


def is_surjective(f: dict[X, Y], codomain: set[Y]) -> bool:
    """写像 f が終域 codomain への全射かどうかを返す。"""
    return set(f.values()) == codomain


def compose(g: dict[Y, Z], f: dict[X, Y]) -> dict[X, Z]:
    """合成写像 g ∘ f を返す。"""
    return {x: g[f[x]] for x in f}


def inverse(f: dict[X, Y]) -> dict[Y, X]:
    """全単射 f の逆写像を返す。"""
    if not is_injective(f):
        raise ValueError("単射でない写像の逆写像は定義できない")
    return {y: x for x, y in f.items()}


def is_reflexive(r: Relation, elements: set[int]) -> bool:
    """反射律: すべての a について (a, a) ∈ R。"""
    return all((a, a) in r for a in elements)


def is_symmetric(r: Relation) -> bool:
    """対称律: (a, b) ∈ R ならば (b, a) ∈ R。"""
    return all((b, a) in r for a, b in r)


def is_antisymmetric(r: Relation) -> bool:
    """反対称律: (a, b) ∈ R かつ (b, a) ∈ R ならば a = b。"""
    return all(a == b for a, b in r if (b, a) in r)


def is_transitive(r: Relation) -> bool:
    """推移律: (a, b) ∈ R かつ (b, c) ∈ R ならば (a, c) ∈ R。"""
    return all((a, d) in r for a, b in r for c, d in r if b == c)


def equivalence_classes(r: Relation, elements: set[int]) -> list[set[int]]:
    """同値関係 r による同値類の一覧を返す。"""
    classes: list[set[int]] = []
    for a in sorted(elements):
        if any(a in c for c in classes):
            continue
        classes.append({b for b in elements if (a, b) in r})
    return classes


def main() -> None:
    print("--- 写像の性質 ---")
    codomain = {1, 2, 3}
    f = {"a": 1, "b": 2, "c": 3}
    g = {"a": 1, "b": 1, "c": 2}
    for name, h in [("f", f), ("g", g)]:
        print(f"{name}: 単射={is_injective(h)}, 全射={is_surjective(h, codomain)}")

    double = {1: 2, 2: 4, 3: 6}
    print(f"f の逆写像: {inverse(f)}")
    print(f"double ∘ f: {compose(double, f)}")

    print("--- 合同関係 (mod 4) ---")
    elements = set(range(12))
    congruence = {(a, b) for a in elements for b in elements if (a - b) % 4 == 0}
    print(f"反射律={is_reflexive(congruence, elements)}, "
          f"対称律={is_symmetric(congruence)}, 推移律={is_transitive(congruence)}")
    for c in equivalence_classes(congruence, elements):
        print(f"  [{min(c)}] = {sorted(c)}")

    print("--- 整除関係（12 の約数） ---")
    divisors = {d for d in range(1, 13) if 12 % d == 0}
    divides = {(a, b) for a in divisors for b in divisors if b % a == 0}
    print(f"反射律={is_reflexive(divides, divisors)}, "
          f"反対称律={is_antisymmetric(divides)}, 推移律={is_transitive(divides)}")
    print(f"対称律={is_symmetric(divides)}")


if __name__ == "__main__":
    main()
