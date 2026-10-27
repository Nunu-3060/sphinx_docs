"""命題論理の真理値表を作り、恒真式・論理的同値を判定するサンプル。

論理式は「命題変数の真理値（bool）を受け取って bool を返す関数」として表す。
"""

from collections.abc import Callable, Iterator, Sequence
from itertools import product

# 命題変数の個数は論理式ごとに異なるため、引数の個数は固定しない。
Formula = Callable[..., bool]


def implies(p: bool, q: bool) -> bool:
    """含意 p → q の真理値を返す。"""
    return (not p) or q


def iff(p: bool, q: bool) -> bool:
    """同値 p ↔ q の真理値を返す。"""
    return p == q


def assignments(n: int) -> Iterator[tuple[bool, ...]]:
    """n 個の命題変数への真理値の割り当てを、すべて真の行から順に列挙する。"""
    return product((True, False), repeat=n)


def to_symbol(value: bool) -> str:
    """真理値を T または F で表す。"""
    return "T" if value else "F"


def print_truth_table(formula: Formula, names: Sequence[str], label: str) -> None:
    """論理式 formula の真理値表を表示する。"""
    print(" ".join(names), "|", label)
    for values in assignments(len(names)):
        cells = " ".join(to_symbol(v) for v in values)
        print(cells, "|", to_symbol(formula(*values)))


def is_tautology(formula: Formula, n: int) -> bool:
    """n 変数の論理式 formula が恒真式であるかを判定する。"""
    return all(formula(*values) for values in assignments(n))


def is_satisfiable(formula: Formula, n: int) -> bool:
    """n 変数の論理式 formula が充足可能であるかを判定する。"""
    return any(formula(*values) for values in assignments(n))


def are_equivalent(f: Formula, g: Formula, n: int) -> bool:
    """n 変数の論理式 f と g が論理的に同値であるかを判定する。"""
    return all(f(*values) == g(*values) for values in assignments(n))


def main() -> None:
    print("真理値表: P → Q")
    print_truth_table(implies, ["P", "Q"], "P → Q")
    print()

    print("排中律 P ∨ ¬P は恒真式か:", is_tautology(lambda p: p or not p, 1))
    print("P ∧ ¬P は充足可能か:", is_satisfiable(lambda p: p and not p, 1))

    # ド・モルガンの法則: ¬(P ∧ Q) ≡ ¬P ∨ ¬Q
    print("ド・モルガンの法則は成り立つか:",
          are_equivalent(lambda p, q: not (p and q), lambda p, q: (not p) or (not q), 2))

    # 対偶: P → Q ≡ ¬Q → ¬P、逆: P → Q と Q → P は同値でない
    print("P → Q と対偶 ¬Q → ¬P は同値か:",
          are_equivalent(implies, lambda p, q: implies(not q, not p), 2))
    print("P → Q と逆 Q → P は同値か:",
          are_equivalent(implies, lambda p, q: implies(q, p), 2))

    # 推論の妥当性: (P ∧ (P → Q)) → Q が恒真式ならモーダスポネンスは妥当
    print("モーダスポネンスは妥当か:",
          is_tautology(lambda p, q: implies(p and implies(p, q), q), 2))
    # 後件肯定: (Q ∧ (P → Q)) → P は恒真式でない
    print("後件肯定は妥当か:",
          is_tautology(lambda p, q: implies(q and implies(p, q), p), 2))


if __name__ == "__main__":
    main()
