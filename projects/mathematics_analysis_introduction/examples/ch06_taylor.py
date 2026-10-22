"""テイラー多項式による近似精度と、ニュートン法の 2 次収束を調べる。

1. exp(x) のマクローリン多項式の次数と誤差の関係を、
   ラグランジュ形の剰余項による誤差の上界と並べて表示する。
2. f(x) = x^2 - 2 にニュートン法を適用し、誤差 e_n と比 e_{n+1} / e_n^2 を表示する。

実行方法:
    python ch06_taylor.py
"""

import math
from fractions import Fraction


def exp_taylor(x: float, n: int) -> float:
    """exp(x) の n 次マクローリン多項式の値 sum_{k=0}^{n} x^k / k! を返す。"""
    total = 0.0
    term = 1.0  # x^k / k!（k = 0 から始める）
    for k in range(n + 1):
        total += term
        term *= x / (k + 1)
    return total


def exp_remainder_bound(x: float, n: int) -> float:
    """ラグランジュ形の剰余項による誤差の上界 e^{max(x, 0)} |x|^{n+1} / (n+1)! を返す。"""
    return math.exp(max(x, 0.0)) * abs(x) ** (n + 1) / math.factorial(n + 1)


def show_taylor_table(x: float) -> None:
    """exp(x) の近似誤差と誤差の上界を次数ごとに表示する。"""
    exact = math.exp(x)
    print(f"exp({x}) = {exact:.16f}")
    print(f"{'n':>3} | {'approximation':>20} | {'error':>10} | {'bound':>10}")
    print("-" * 54)
    for n in range(0, 16, 1):
        approx = exp_taylor(x, n)
        err = abs(approx - exact)
        bound = exp_remainder_bound(x, n)
        print(f"{n:>3} | {approx:20.16f} | {err:10.3e} | {bound:10.3e}")


def show_newton_table(x0: Fraction, steps: int) -> None:
    """x^2 - 2 = 0 にニュートン法を適用し、誤差の推移を表示する。

    丸め誤差の影響を避けるため、反復は有理数（Fraction）で厳密に計算する。
    """
    alpha = math.sqrt(2.0)
    x = x0
    print(f"Newton: x_(n+1) = x_n - (x_n^2 - 2) / (2 x_n), x_0 = {x0}")
    print(f"{'n':>3} | {'x_n':>20} | {'e_n':>10} | {'e_n / e_(n-1)^2':>15}")
    print("-" * 59)
    prev_err: float | None = None
    for n in range(steps + 1):
        # 誤差 x_n - sqrt(2) を (x_n^2 - 2) / (x_n + sqrt(2)) として計算し、桁落ちを避ける
        err = float(x * x - 2) / (float(x) + alpha)
        ratio = "" if prev_err is None or prev_err == 0.0 else f"{err / prev_err ** 2:.6f}"
        print(f"{n:>3} | {float(x):20.16f} | {err:10.3e} | {ratio:>15}")
        prev_err = err
        x = x - (x * x - 2) / (2 * x)
    print(f"limit f''(a) / (2 f'(a)) = 1 / (2 sqrt(2)) = {1.0 / (2.0 * alpha):.6f}")


def main() -> None:
    """2 つの数値実験を順に実行する。"""
    show_taylor_table(1.0)
    print()
    show_newton_table(Fraction(2), 5)


if __name__ == "__main__":
    main()
