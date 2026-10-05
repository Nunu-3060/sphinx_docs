"""第 11 章: 充足可能性問題 (SAT) の検証器と総当たり。

CNF (連言標準形) の論理式を整数のリストのリストで表す (DIMACS 形式と同じ)。
正の整数 i は変数 x_i、負の整数 -i は否定 ¬x_i を表す。

    (x1 ∨ ¬x2) ∧ (x2 ∨ x3) ∧ (¬x1 ∨ ¬x3)  ->  [[1, -2], [2, 3], [-1, -3]]

* verify: 割り当てが式を満たすかを多項式時間で確かめる (NP の「検証器」)。
* brute_force_sat: 2^n 通りの割り当てを全て試す (指数時間)。

実行例::

    python ch11_sat_bruteforce.py
"""

from __future__ import annotations

from itertools import product

CNF = list[list[int]]
Assignment = dict[int, bool]


def variables(cnf: CNF) -> list[int]:
    """式に現れる変数の番号を昇順に返す。"""
    return sorted({abs(literal) for clause in cnf for literal in clause})


def verify(cnf: CNF, assignment: Assignment) -> bool:
    """全ての節で、少なくとも 1 つのリテラルが真になれば True。"""
    return all(
        any(assignment[abs(lit)] == (lit > 0) for lit in clause)
        for clause in cnf
    )


def brute_force_sat(cnf: CNF) -> Assignment | None:
    """式を満たす割り当てを 1 つ返す。存在しなければ None。"""
    names = variables(cnf)
    for values in product([False, True], repeat=len(names)):
        assignment = dict(zip(names, values))
        if verify(cnf, assignment):
            return assignment
    return None


def main() -> None:
    satisfiable: CNF = [[1, -2], [2, 3], [-1, -3]]
    print("充足可能な例:", brute_force_sat(satisfiable))

    # x1 と x2 の 4 通りの組み合わせを全て禁止する式は充足不能。
    unsatisfiable: CNF = [[1, 2], [1, -2], [-1, 2], [-1, -2]]
    print("充足不能な例:", brute_force_sat(unsatisfiable))

    certificate = {1: True, 2: True, 3: False}
    print("証拠の検証:", verify(satisfiable, certificate))


if __name__ == "__main__":
    main()
