"""第 5 章: 数値微分と数値積分の誤差を確かめる。

1. 数値微分: sin x の x = 1 での微分を、前進差分と中心差分で
   計算し、刻み幅 h を小さくしすぎると丸め誤差で精度が悪化する
   ことを確かめる
2. 数値積分: sin x を 0 から π まで積分し (厳密値 2)、台形公式と
   シンプソン公式の誤差を比べる

実行例::

    python ch05_derivative.py
"""

from __future__ import annotations

import math
from collections.abc import Callable

Function = Callable[[float], float]


def forward_difference(f: Function, x: float, h: float) -> float:
    """前進差分 (f(x + h) - f(x)) / h。誤差は h に比例する。"""
    return (f(x + h) - f(x)) / h


def central_difference(f: Function, x: float, h: float) -> float:
    """中心差分 (f(x + h) - f(x - h)) / 2h。誤差は h^2 に比例する。"""
    return (f(x + h) - f(x - h)) / (2 * h)


def trapezoid(f: Function, a: float, b: float, n: int) -> float:
    """台形公式で区間 [a, b] を n 等分して積分する。"""
    h = (b - a) / n
    inner = sum(f(a + i * h) for i in range(1, n))
    return h * (f(a) / 2 + inner + f(b) / 2)


def simpson(f: Function, a: float, b: float, n: int) -> float:
    """シンプソン公式で区間 [a, b] を n 等分 (n は偶数) して積分する。"""
    if n % 2 != 0:
        raise ValueError("n は偶数にしてください。")
    h = (b - a) / n
    odd = sum(f(a + i * h) for i in range(1, n, 2))
    even = sum(f(a + i * h) for i in range(2, n, 2))
    return h / 3 * (f(a) + 4 * odd + 2 * even + f(b))


def main() -> None:
    exact_derivative = math.cos(1.0)
    print("1. sin x の x = 1 での微分の誤差")
    print("   刻み幅 h   前進差分    中心差分")
    for exponent in range(1, 15, 2):
        h = 10.0 ** -exponent
        forward = abs(forward_difference(math.sin, 1.0, h)
                      - exact_derivative)
        central = abs(central_difference(math.sin, 1.0, h)
                      - exact_derivative)
        print(f"   {h:8.0e}  {forward:10.2e}  {central:10.2e}")

    print("2. sin x の 0 から π までの積分の誤差 (厳密値 2)")
    print("   分割数 n   台形公式    シンプソン公式")
    for n in (4, 8, 16, 32, 64):
        t_error = abs(trapezoid(math.sin, 0.0, math.pi, n) - 2.0)
        s_error = abs(simpson(math.sin, 0.0, math.pi, n) - 2.0)
        print(f"   {n:8d}  {t_error:10.2e}  {s_error:10.2e}")


if __name__ == "__main__":
    main()
