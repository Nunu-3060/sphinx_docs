"""第 12 章: DPLL アルゴリズムによる SAT ソルバ。

総当たりと同じく変数の値を順に決めていくが、次の 2 つの規則で探索を減らす。

* 単位伝播: リテラルが 1 つしか残っていない節 (単位節) があれば、
  そのリテラルを真にするしかない。
* 純リテラル除去: 肯定か否定の一方でしか現れない変数は、そのリテラルを
  真にしてよい。

CNF の表し方は ch11_sat_bruteforce.py と同じ。

実行例::

    python ch12_dpll.py
"""

from __future__ import annotations

import time

CNF = list[list[int]]


def simplify(cnf: CNF, literal: int) -> CNF | None:
    """literal を真としたときの式を返す。空の節ができたら None (矛盾)。"""
    result: CNF = []
    for clause in cnf:
        if literal in clause:
            continue  # 節が真になったので取り除く
        reduced = [lit for lit in clause if lit != -literal]
        if not reduced:
            return None
        result.append(reduced)
    return result


def dpll(cnf: CNF, assignment: dict[int, bool] | None = None
         ) -> dict[int, bool] | None:
    """式を満たす割り当てを返す。充足不能なら None を返す。"""
    assignment = dict(assignment or {})
    while True:  # 単位伝播と純リテラル除去を、適用できなくなるまで繰り返す
        unit = next((c[0] for c in cnf if len(c) == 1), None)
        if unit is None:
            literals = {lit for clause in cnf for lit in clause}
            unit = next((lit for lit in literals if -lit not in literals),
                        None)
        if unit is None:
            break
        assignment[abs(unit)] = unit > 0
        simplified = simplify(cnf, unit)
        if simplified is None:
            return None
        cnf = simplified
    if not cnf:
        return assignment  # 全ての節が満たされた
    literal = cnf[0][0]  # 分岐: まず真を試し、だめなら偽を試す
    for choice in (literal, -literal):
        simplified = simplify(cnf, choice)
        if simplified is not None:
            result = dpll(simplified, {**assignment, abs(choice): choice > 0})
            if result is not None:
                return result
    return None


def pigeonhole(n: int) -> CNF:
    """n + 1 羽の鳩を n 個の巣に 1 羽ずつ入れる問題 (常に充足不能)。

    変数 p(i, j) は「鳩 i が巣 j に入る」ことを表す。
    """
    def var(i: int, j: int) -> int:
        return i * n + j + 1

    cnf: CNF = [[var(i, j) for j in range(n)] for i in range(n + 1)]
    for j in range(n):
        for i in range(n + 1):
            for k in range(i + 1, n + 1):
                cnf.append([-var(i, j), -var(k, j)])
    return cnf


def main() -> None:
    print("充足可能な例:", dpll([[1, -2], [2, 3], [-1, -3]]))
    for n in range(1, 9):
        start = time.perf_counter()
        verdict = "充足不能" if dpll(pigeonhole(n)) is None else "充足可能"
        elapsed = time.perf_counter() - start
        print(f"鳩の巣原理 n = {n}: {verdict} ({elapsed:.3f} 秒)")


if __name__ == "__main__":
    main()
