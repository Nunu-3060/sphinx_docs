"""第 2 章の数値実験：漸化式で定まる数列の収束の様子。

√2 に収束する 2 つの数列を比べる。

* 二分法：区間 [1, 2] を毎回半分にし、√2 を含む側を残す。誤差はおよそ毎回 1/2 倍になる（1 次収束）。
* ニュートン法：a_{n+1} = (a_n + 2 / a_n) / 2。正しい桁数がおよそ毎回 2 倍になる（2 次収束）。

真の値との誤差を正確に測るため、計算は Fraction（有理数）で行い、表示のときだけ小数に直す。

実行方法::

    python ch02_newton_sqrt2.py
"""

from decimal import Decimal, getcontext
from fractions import Fraction

# 誤差の評価に使う √2 の高精度な値（Decimal で 60 桁）
getcontext().prec = 60
SQRT2: Decimal = Decimal(2).sqrt()


def newton_sequence(a0: Fraction, steps: int) -> list[Fraction]:
    """ニュートン法の数列 a_0, a_1, ..., a_steps を返す。"""
    terms = [a0]
    for _ in range(steps):
        a = terms[-1]
        terms.append((a + 2 / a) / 2)
    return terms


def bisection_sequence(low: Fraction, high: Fraction, steps: int) -> list[Fraction]:
    """二分法で得られる区間の中点の列を返す。"""
    midpoints: list[Fraction] = []
    for _ in range(steps + 1):
        mid = (low + high) / 2
        midpoints.append(mid)
        # mid^2 < 2 なら √2 は右半分にある
        if mid * mid < 2:
            low = mid
        else:
            high = mid
    return midpoints


def error(x: Fraction) -> Decimal:
    """|x - √2| を Decimal で返す。"""
    value = Decimal(x.numerator) / Decimal(x.denominator)
    return abs(value - SQRT2)


def main() -> None:
    """2 つの数列の誤差を並べて表示する。"""
    steps = 6
    newton = newton_sequence(Fraction(2), steps)
    bisection = bisection_sequence(Fraction(1), Fraction(2), steps)

    print(" n   二分法の誤差   ニュートン法の誤差")
    for n in range(steps + 1):
        e_bis = float(error(bisection[n]))
        e_new = float(error(newton[n]))
        print(f"{n:2d}   {e_bis:12.3e}   {e_new:18.3e}")


if __name__ == "__main__":
    main()
