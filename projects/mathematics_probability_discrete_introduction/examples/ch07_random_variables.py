"""第 7 章 確率変数と期待値のサンプルコード。

離散確率変数の分布を「値 → 確率」の dict で表し、fractions.Fraction で厳密に計算する。
"""

import math
from collections.abc import Callable, Iterable
from fractions import Fraction
from itertools import permutations, product
from typing import TypeVar

T = TypeVar("T")

# 確率変数の分布（値 → 確率）
Distribution = dict[int, Fraction]


def distribution_of(outcomes: Iterable[T], variable: Callable[[T], int]) -> Distribution:
    """同様に確からしい根元事象の一覧と確率変数から、確率変数の分布を作る。"""
    counts: dict[int, int] = {}
    total = 0
    for w in outcomes:
        x = variable(w)
        counts[x] = counts.get(x, 0) + 1
        total += 1
    return {x: Fraction(c, total) for x, c in sorted(counts.items())}


def expectation(dist: Distribution, g: Callable[[int], Fraction | int] = lambda x: x) -> Fraction:
    """g(X) の期待値 E[g(X)] = Σ g(x) P(X = x) を返す。"""
    return sum((Fraction(g(x)) * p for x, p in dist.items()), Fraction(0))


def variance(dist: Distribution) -> Fraction:
    """分散 V[X] = E[X^2] - (E[X])^2 を返す。"""
    mean = expectation(dist)
    return expectation(dist, lambda x: x * x) - mean * mean


def cdf(dist: Distribution, x: int) -> Fraction:
    """累積分布関数 F(x) = P(X <= x) を返す。"""
    return sum((p for v, p in dist.items() if v <= x), Fraction(0))


def main() -> None:
    print("--- サイコロ 1 個 ---")
    die = distribution_of(range(1, 7), lambda w: w)
    print(f"E[X] = {expectation(die)}, V[X] = {variance(die)}")
    print(f"F(2) = {cdf(die, 2)}, F(4) = {cdf(die, 4)}")

    print("--- サイコロ 2 個の和 ---")
    total = distribution_of(product(range(1, 7), repeat=2), lambda w: w[0] + w[1])
    print({x: str(p) for x, p in total.items()})
    print(f"E[S] = {expectation(total)}, V[S] = {variance(total)}")

    print("--- 期待値の線形性: 3 回投げて 6 が出る回数 ---")
    sixes = distribution_of(product(range(1, 7), repeat=3), lambda w: sum(1 for x in w if x == 6))
    print(f"全列挙による E[X] = {expectation(sixes)}, 線形性による 3 x (1/6) = {3 * Fraction(1, 6)}")

    print("--- 指示確率変数: ランダムな順列の不動点の個数 ---")
    for n in range(1, 8):
        fixed = distribution_of(permutations(range(n)), lambda p: sum(1 for i, x in enumerate(p) if i == x))
        print(f"n={n}: E[X] = {expectation(fixed)}, V[X] = {variance(fixed)}, P(X=0) = {float(fixed.get(0, 0)):.4f}")
    print(f"1/e = {1 / math.e:.4f}")


if __name__ == "__main__":
    main()
