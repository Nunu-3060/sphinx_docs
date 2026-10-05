"""第 5 章: 浮動小数点数の落とし穴を確かめる。

コンピューターの浮動小数点数 (IEEE 754 倍精度) は有限の桁数しか
持たないため、次のような現象が起きます。

1. 10 進数の 0.1 を正確に表せない
2. 大きさの違う数を足すと、小さい数が失われる (情報落ち)
3. 値の近い数を引くと、有効数字が失われる (桁落ち)
4. 足す順番によって合計が変わる

あわせて、固定幅の整数が桁あふれする例も示します。

実行例::

    python ch05_float.py
"""

from __future__ import annotations

import math
import sys
from decimal import Decimal

import numpy as np


def representation() -> None:
    """0.1 が 2 進数で正確に表せないことを確かめる。"""
    print("1. 0.1 の表現")
    print(f"   0.1 + 0.2 == 0.3       -> {0.1 + 0.2 == 0.3}")
    print(f"   0.1 + 0.2              -> {0.1 + 0.2!r}")
    print(f"   0.1 の内部の値          -> {Decimal(0.1)}")
    print(f"   math.isclose(0.1 + 0.2, 0.3) -> "
          f"{math.isclose(0.1 + 0.2, 0.3)}")
    print(f"   計算機イプシロン        -> {sys.float_info.epsilon!r}")


def absorption() -> None:
    """大きな数に小さな数を足すと失われることを確かめる。"""
    print("2. 情報落ち")
    big = 1.0e16
    print(f"   (1e16 + 1) - 1e16       -> {(big + 1.0) - big}")
    print(f"   (1e16 - 1e16) + 1       -> {(big - big) + 1.0}")


def quadratic_roots_naive(a: float, b: float,
                          c: float) -> tuple[float, float]:
    """解の公式をそのまま使って 2 次方程式の実数解を求める。"""
    d = math.sqrt(b * b - 4 * a * c)
    return (-b + d) / (2 * a), (-b - d) / (2 * a)


def quadratic_roots_stable(a: float, b: float,
                           c: float) -> tuple[float, float]:
    """桁落ちを避けて 2 次方程式の実数解を求める。

    絶対値の大きい解を先に求め、もう一方は解と係数の関係
    (x1 * x2 = c / a) から求めます。
    """
    d = math.sqrt(b * b - 4 * a * c)
    q = -(b + math.copysign(d, b)) / 2
    return c / q, q / a


def cancellation() -> None:
    """値の近い数の引き算で有効数字が失われることを確かめる。"""
    print("3. 桁落ち (x^2 + 1e8 x + 1 = 0 の解)")
    a, b, c = 1.0, 1.0e8, 1.0
    naive = quadratic_roots_naive(a, b, c)
    stable = quadratic_roots_stable(a, b, c)
    print(f"   解の公式そのまま -> 小さい解 = {naive[0]!r}")
    print(f"   桁落ちを避けた式 -> 小さい解 = {stable[0]!r}")
    print("   (真の値は約 -1.00000000000000e-08)")


def naive_sum(values: list[float]) -> float:
    """先頭から順に 1 つずつ足す (誤差の補正をしない)。"""
    total = 0.0
    for value in values:
        total += value
    return total


def summation() -> None:
    """足す順番によって合計が変わることを確かめる。

    Python 3.12 以降の組み込み関数 sum() は、浮動小数点数の誤差を
    補正しながら足します。ここでは、多くの言語の単純なループと同じ
    結果になるように、naive_sum() で 1 つずつ足します。
    """
    print("4. 足す順番と合計")
    values = [0.1] * 10
    print(f"   0.1 を 10 回足す        -> {naive_sum(values)!r}")
    print(f"   math.fsum で足す        -> {math.fsum(values)!r}")

    mixed = [1.0e16, 1.0, -1.0e16, 1.0]
    print(f"   [1e16, 1, -1e16, 1] の和 -> {naive_sum(mixed)!r}")
    sorted_values = sorted(mixed, key=abs)
    print(f"   絶対値の小さい順に足す  -> {naive_sum(sorted_values)!r}")
    print(f"   math.fsum で足す        -> {math.fsum(mixed)!r}")


def overflow() -> None:
    """固定幅の整数が桁あふれすることを確かめる。

    Python の int は桁数に上限がありませんが、NumPy の整数配列や
    C 言語の整数は固定幅です。16 ビット符号付き整数の範囲は
    -32768〜32767 で、これを超えると例外にならずに値が折り返します。
    """
    print("5. 整数の桁あふれ (16 ビット符号付き整数)")
    a = np.array([30000], dtype=np.int16)
    print(f"   30000 + 30000 (Python の int) -> {30000 + 30000}")
    print(f"   30000 + 30000 (np.int16)      -> {(a + a)[0]}")


def main() -> None:
    representation()
    absorption()
    cancellation()
    summation()
    overflow()


if __name__ == "__main__":
    main()
