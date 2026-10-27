"""真理値表から選言標準形・連言標準形を作るサンプル。"""

from collections.abc import Callable, Sequence
from itertools import product

Formula = Callable[..., bool]


def literal(name: str, positive: bool) -> str:
    """命題変数 name のリテラル（name または ¬name）を返す。"""
    return name if positive else "¬" + name


def dnf(formula: Formula, names: Sequence[str]) -> str:
    """formula と同値な選言標準形を返す。

    真になる行ごとに「その行でだけ真になるリテラルの論理積」を作り、それらの論理和をとる。
    """
    terms = []
    for values in product((True, False), repeat=len(names)):
        if formula(*values):
            literals = [literal(n, v) for n, v in zip(names, values)]
            terms.append("(" + " ∧ ".join(literals) + ")")
    # 真になる行が無ければ、空の論理和すなわち恒偽 ⊥ になる。
    return " ∨ ".join(terms) if terms else "⊥"


def cnf(formula: Formula, names: Sequence[str]) -> str:
    """formula と同値な連言標準形を返す。

    偽になる行ごとに「その行でだけ偽になるリテラルの論理和」を作り、それらの論理積をとる。
    """
    clauses = []
    for values in product((True, False), repeat=len(names)):
        if not formula(*values):
            literals = [literal(n, not v) for n, v in zip(names, values)]
            clauses.append("(" + " ∨ ".join(literals) + ")")
    # 偽になる行が無ければ、空の論理積すなわち恒真 ⊤ になる。
    return " ∧ ".join(clauses) if clauses else "⊤"


def main() -> None:
    examples: list[tuple[str, Formula, list[str]]] = [
        ("P ↔ Q", lambda p, q: p == q, ["P", "Q"]),
        ("P ⊕ Q（排他的論理和）", lambda p, q: p != q, ["P", "Q"]),
        ("(P ∧ Q) ∨ R", lambda p, q, r: (p and q) or r, ["P", "Q", "R"]),
    ]
    for label, formula, names in examples:
        print(label)
        print("  選言標準形:", dnf(formula, names))
        print("  連言標準形:", cnf(formula, names))


if __name__ == "__main__":
    main()
