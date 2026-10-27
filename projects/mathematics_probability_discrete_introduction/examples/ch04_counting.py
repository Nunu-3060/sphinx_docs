"""第 4 章 数え上げのサンプルコード。

itertools で実際に全列挙した個数と、公式による計算結果を照合する。
"""

import math
from functools import cache
from itertools import combinations, combinations_with_replacement, permutations, product


def check_basic_formulas(n: int, r: int) -> None:
    """順列・組合せ・重複順列・重複組合せの個数を全列挙と公式で比較する。"""
    items = range(n)
    rows = [
        ("順列 P(n, r)", len(list(permutations(items, r))), math.perm(n, r)),
        ("組合せ C(n, r)", len(list(combinations(items, r))), math.comb(n, r)),
        ("重複順列 n^r", len(list(product(items, repeat=r))), n ** r),
        ("重複組合せ H(n, r)", len(list(combinations_with_replacement(items, r))), math.comb(n + r - 1, r)),
    ]
    for name, enumerated, formula in rows:
        print(f"{name:<20} 全列挙={enumerated:>4}  公式={formula:>4}")


def pascal_triangle(rows: int) -> list[list[int]]:
    """漸化式 C(n, k) = C(n-1, k-1) + C(n-1, k) によりパスカルの三角形を作る。"""
    triangle = [[1]]
    for _ in range(1, rows):
        prev = triangle[-1]
        triangle.append([1] + [prev[k - 1] + prev[k] for k in range(1, len(prev))] + [1])
    return triangle


def derangements_brute_force(n: int) -> int:
    """どの i も位置 i に来ない順列（攪乱順列）を全列挙で数える。"""
    return sum(1 for p in permutations(range(n)) if all(p[i] != i for i in range(n)))


def derangements_formula(n: int) -> int:
    """包除原理による攪乱順列の個数 D(n) = Σ (-1)^k C(n, k) (n-k)!。"""
    return sum((-1) ** k * math.comb(n, k) * math.factorial(n - k) for k in range(n + 1))


def count_no_consecutive_ones_brute_force(n: int) -> int:
    """1 が連続しない長さ n の 0/1 列を全列挙で数える。"""
    return sum(1 for bits in product("01", repeat=n) if "11" not in "".join(bits))


@cache
def count_no_consecutive_ones(n: int) -> int:
    """漸化式 a(n) = a(n-1) + a(n-2), a(1) = 2, a(2) = 3 で数える。"""
    if n == 1:
        return 2
    if n == 2:
        return 3
    return count_no_consecutive_ones(n - 1) + count_no_consecutive_ones(n - 2)


def hanoi(n: int, source: str, target: str, spare: str, moves: list[tuple[str, str]]) -> None:
    """ハノイの塔の手順を moves に追加する。"""
    if n == 0:
        return
    hanoi(n - 1, source, spare, target, moves)
    moves.append((source, target))
    hanoi(n - 1, spare, target, source, moves)


def main() -> None:
    print("--- 基本公式 (n=5, r=3) ---")
    check_basic_formulas(5, 3)

    print("--- パスカルの三角形 ---")
    for row in pascal_triangle(7):
        print(" ".join(f"{c:>2}" for c in row))

    print("--- 攪乱順列 ---")
    for n in range(1, 9):
        d = derangements_formula(n)
        print(f"n={n}: 全列挙={derangements_brute_force(n):>5}  包除原理={d:>5}  D(n)/n!={d / math.factorial(n):.6f}")
    print(f"1/e = {1 / math.e:.6f}")

    print("--- 1 が連続しない 0/1 列 ---")
    for n in range(1, 11):
        print(f"n={n:>2}: 全列挙={count_no_consecutive_ones_brute_force(n):>3}  漸化式={count_no_consecutive_ones(n):>3}")

    print("--- ハノイの塔 ---")
    for n in range(1, 8):
        moves: list[tuple[str, str]] = []
        hanoi(n, "A", "C", "B", moves)
        print(f"n={n}: 手数={len(moves):>3}  2^n - 1={2 ** n - 1:>3}")


if __name__ == "__main__":
    main()
