"""第 1 章の数値実験：浮動小数点数と実数の違い。

次の 4 つを確かめる。

1. 0.1 を 10 回足しても 1.0 にならない。
2. 機械イプシロン（1 + eps > 1 となる最小の 2 のべき eps）を求める。
3. 浮動小数点数の加算は結合法則を満たさない。
4. 近い数どうしの引き算で有効桁が失われる（桁落ち）。

実行方法::

    python ch01_float_error.py
"""

import math
import sys
from fractions import Fraction


def sum_of_tenths(count: int) -> float:
    """0.1 を count 回足した値を返す。"""
    total = 0.0
    for _ in range(count):
        total += 0.1
    return total


def machine_epsilon() -> float:
    """1.0 + eps > 1.0 を満たす最小の 2 のべき eps を求める。"""
    eps = 1.0
    # eps を半分にしても 1.0 と区別できるうちは半分にし続ける
    while 1.0 + eps / 2 > 1.0:
        eps /= 2
    return eps


def show_sum_of_tenths() -> None:
    """実験 1：0.1 を 10 回足す。"""
    total = sum_of_tenths(10)
    print("[1] 0.1 を 10 回足す")
    print(f"    結果           : {total!r}")
    print(f"    1.0 と等しいか : {total == 1.0}")
    # 0.1 として実際に格納されている値を有理数で正確に表示する
    print(f"    0.1 の実際の値 : {Fraction(0.1)}")
    print()


def show_machine_epsilon() -> None:
    """実験 2：機械イプシロン。"""
    eps = machine_epsilon()
    print("[2] 機械イプシロン")
    print(f"    求めた値               : {eps!r}")
    print(f"    sys.float_info.epsilon : {sys.float_info.epsilon!r}")
    print(f"    2 ** -52               : {2.0 ** -52!r}")
    print()


def show_associativity() -> None:
    """実験 3：結合法則が成り立たない例。"""
    a, b, c = 1.0e16, -1.0e16, 1.0
    left = (a + b) + c
    right = a + (b + c)
    print("[3] 結合法則")
    print(f"    (a + b) + c = {left!r}")
    print(f"    a + (b + c) = {right!r}")
    print()


def show_cancellation() -> None:
    """実験 4：桁落ち。(1 - cos x) / x**2 は x -> 0 で 1/2 に近づくはずである。"""
    print("[4] 桁落ち：(1 - cos x) / x^2（真の極限値は 0.5）")
    print("           x                直接計算      2 sin^2(x/2) / x^2")
    for k in range(1, 10):
        x = 10.0 ** (-k)
        direct = (1.0 - math.cos(x)) / x**2
        # 半角の公式 1 - cos x = 2 sin^2(x/2) を使うと引き算を避けられる
        stable = 2.0 * math.sin(x / 2) ** 2 / x**2
        print(f"    {x:8.0e}  {direct:22.15f}  {stable:22.15f}")


def main() -> None:
    """すべての実験を順に実行する。"""
    show_sum_of_tenths()
    show_machine_epsilon()
    show_associativity()
    show_cancellation()


if __name__ == "__main__":
    main()
