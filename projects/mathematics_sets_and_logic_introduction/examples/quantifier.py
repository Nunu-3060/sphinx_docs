"""有限の議論領域上で全称命題・存在命題を評価するサンプル。"""

from collections.abc import Callable, Iterable


def for_all(domain: Iterable[int], predicate: Callable[[int], bool]) -> bool:
    """∀x ∈ domain. predicate(x) の真理値を返す。"""
    return all(predicate(x) for x in domain)


def exists(domain: Iterable[int], predicate: Callable[[int], bool]) -> bool:
    """∃x ∈ domain. predicate(x) の真理値を返す。"""
    return any(predicate(x) for x in domain)


def main() -> None:
    domain = range(5)  # 議論領域 D = {0, 1, 2, 3, 4}

    def p(x: int, y: int) -> bool:
        return x + y == 4

    # ∀x ∃y P(x, y): どの x にも x + y = 4 となる y がある（y = 4 - x）。
    forall_exists = for_all(domain, lambda x: exists(domain, lambda y: p(x, y)))
    # ∃y ∀x P(x, y): どの x についても x + y = 4 となる共通の y がある。
    exists_forall = exists(domain, lambda y: for_all(domain, lambda x: p(x, y)))
    print("∀x ∃y (x + y = 4):", forall_exists)
    print("∃y ∀x (x + y = 4):", exists_forall)

    # 量化子の否定: ¬∀x P(x) と ∃x ¬P(x) は常に一致する。
    def is_even(x: int) -> bool:
        return x % 2 == 0

    print("¬∀x (x は偶数):", not for_all(domain, is_even))
    print("∃x ¬(x は偶数):", exists(domain, lambda x: not is_even(x)))

    # 空の議論領域: 全称命題は真、存在命題は偽になる。
    empty: list[int] = []
    print("∀x ∈ ∅ (x は偶数):", for_all(empty, is_even))
    print("∃x ∈ ∅ (x は偶数):", exists(empty, is_even))


if __name__ == "__main__":
    main()
