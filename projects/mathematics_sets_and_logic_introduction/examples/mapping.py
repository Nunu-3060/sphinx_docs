"""有限集合間の写像を辞書で表し、単射・全射を判定するサンプル。"""

from typing import Generic, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


class Mapping(Generic[A, B]):
    """定義域・終域・対応表の組で表した写像。"""

    def __init__(self, domain: set[A], codomain: set[B], table: dict[A, B]) -> None:
        # 写像の条件: 定義域のすべての要素に、終域の要素がちょうど 1 つ対応する。
        # dict のキーは重複しないため、キーの集合が定義域と一致すれば十分である。
        if set(table) != domain:
            raise ValueError("対応表のキーが定義域と一致しない")
        if not set(table.values()) <= codomain:
            raise ValueError("終域に含まれない値がある")
        self.domain = domain
        self.codomain = codomain
        self.table = table

    def __call__(self, x: A) -> B:
        return self.table[x]

    def image(self, xs: set[A]) -> set[B]:
        """部分集合 xs の像 f(xs) を返す。"""
        return {self.table[x] for x in xs}

    def preimage(self, ys: set[B]) -> set[A]:
        """部分集合 ys の逆像 f⁻¹(ys) を返す。"""
        return {x for x in self.domain if self.table[x] in ys}

    def is_injective(self) -> bool:
        """単射であるか: 異なる要素の像が常に異なる。"""
        return len(set(self.table.values())) == len(self.domain)

    def is_surjective(self) -> bool:
        """全射であるか: 像が終域全体に一致する。"""
        return self.image(self.domain) == self.codomain

    def is_bijective(self) -> bool:
        """全単射であるか。"""
        return self.is_injective() and self.is_surjective()

    def inverse(self) -> "Mapping[B, A]":
        """逆写像を返す。全単射でなければ ValueError を送出する。"""
        if not self.is_bijective():
            raise ValueError("全単射でないので逆写像は存在しない")
        return Mapping(self.codomain, self.domain, {y: x for x, y in self.table.items()})


def compose(g: Mapping[B, C], f: Mapping[A, B]) -> Mapping[A, C]:
    """合成写像 g ∘ f を返す。f の終域と g の定義域が一致していなければならない。"""
    if f.codomain != g.domain:
        raise ValueError("f の終域と g の定義域が一致しない")
    return Mapping(f.domain, g.codomain, {x: g(f(x)) for x in f.domain})


def describe(name: str, f: Mapping[A, B]) -> None:
    print(f"{name}: 単射={f.is_injective()}, 全射={f.is_surjective()}, 全単射={f.is_bijective()}")


def main() -> None:
    a = {-2, -1, 0, 1, 2}
    square = Mapping(a, {0, 1, 4}, {x: x * x for x in a})
    describe("f(x) = x²（{-2, ..., 2} → {0, 1, 4}）", square)
    print("  f({-1, 0, 1}) =", sorted(square.image({-1, 0, 1})))
    print("  f⁻¹({4}) =", sorted(square.preimage({4})))

    shift = Mapping(a, {-1, 0, 1, 2, 3}, {x: x + 1 for x in a})
    describe("g(x) = x + 1（{-2, ..., 2} → {-1, ..., 3}）", shift)
    g_inv = shift.inverse()
    print("  g⁻¹(3) =", g_inv(3))

    h = compose(square, Mapping(a, a, {x: -x for x in a}))
    print("(f ∘ (x ↦ -x))(2) =", h(2))


if __name__ == "__main__":
    main()
