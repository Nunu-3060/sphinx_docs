"""ダイスの和の分布を計算し、実際に振った結果と比べる（5 章）。

実行方法:
    py dice.py           1d6、2d6、3d6 の分布、期待値、分散を表示する
    py dice.py 2 1000    2d6 を 1000 回振った結果を理論値と比べる
"""

import random
import sys
from collections import Counter
from fractions import Fraction


def sum_distribution(dice: int, faces: int = 6) -> dict[int, Fraction]:
    """dice 個の faces 面ダイスの和が各値になる確率を返す。

    1 個ずつ足していく（畳み込み）ので、全組合せを列挙するより速い。
    """
    dist: dict[int, Fraction] = {0: Fraction(1)}
    for _ in range(dice):
        nxt: dict[int, Fraction] = {}
        for total, p in dist.items():
            for face in range(1, faces + 1):
                nxt[total + face] = nxt.get(total + face, Fraction(0)) + p / faces
        dist = nxt
    return dist


def mean(dist: dict[int, Fraction]) -> Fraction:
    return sum((v * p for v, p in dist.items()), Fraction(0))


def variance(dist: dict[int, Fraction]) -> Fraction:
    m = mean(dist)
    return sum(((v - m) ** 2 * p for v, p in dist.items()), Fraction(0))


def roll(dice: int, times: int, faces: int = 6) -> Counter[int]:
    """dice 個のダイスを times 回振り、和の出現回数を返す。"""
    return Counter(sum(random.randint(1, faces) for _ in range(dice)) for _ in range(times))


def show_theory() -> None:
    for n in (1, 2, 3):
        dist = sum_distribution(n)
        print(f"{n}d6: 期待値 {float(mean(dist)):.2f}、分散 {float(variance(dist)):.3f}")
        for v, p in sorted(dist.items()):
            print(f"  {v:2d}: {float(p):.3f} {'#' * round(float(p) * 100)}")


def compare(dice: int, times: int) -> None:
    dist = sum_distribution(dice)
    counts = roll(dice, times)
    print(f"{dice}d6 を {times} 回振った結果（理論値との比較）")
    for v, p in sorted(dist.items()):
        print(f"  {v:2d}: {counts[v]:5d} 回  割合 {counts[v] / times:.3f}  理論値 {float(p):.3f}")


def main() -> None:
    if len(sys.argv) == 3:
        compare(int(sys.argv[1]), int(sys.argv[2]))
    else:
        show_theory()


if __name__ == "__main__":
    main()
