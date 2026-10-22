"""数値微分の誤差と刻み幅の関係を調べる。

f(x) = exp(x) の x = 1 における微分係数 f'(1) = e を、
前進差分と中心差分で近似し、刻み幅 h ごとの誤差を表にして表示する。

実行方法:
    python ch05_numerical_diff.py
"""

import math
import sys
from collections.abc import Callable


def forward_difference(f: Callable[[float], float], x: float, h: float) -> float:
    """前進差分 (f(x + h) - f(x)) / h を返す。"""
    return (f(x + h) - f(x)) / h


def central_difference(f: Callable[[float], float], x: float, h: float) -> float:
    """中心差分 (f(x + h) - f(x - h)) / (2h) を返す。"""
    return (f(x + h) - f(x - h)) / (2.0 * h)


def main() -> None:
    """刻み幅 h = 10^-1, ..., 10^-16 について誤差を表示する。"""
    x = 1.0
    exact = math.exp(x)  # f'(x) = exp(x)
    eps = sys.float_info.epsilon  # 機械イプシロン 2^-52

    print(f"f(x) = exp(x), x = {x}, f'(x) = {exact:.16f}")
    print(f"{'h':>8} | {'forward error':>14} | {'central error':>14}")
    print("-" * 42)
    for k in range(1, 17):
        h = 10.0 ** (-k)
        err_forward = abs(forward_difference(math.exp, x, h) - exact)
        err_central = abs(central_difference(math.exp, x, h) - exact)
        print(f"{h:8.0e} | {err_forward:14.3e} | {err_central:14.3e}")

    # 誤差の上界を最小にする刻み幅の目安（本文の式を参照）
    # 関数値の誤差を eps * |f(x)|、2 階・3 階導関数の大きさを |f(x)| と見積もる
    h_forward = 2.0 * math.sqrt(eps)
    h_central = (3.0 * eps) ** (1.0 / 3.0)
    print()
    print(f"machine epsilon           : {eps:.3e}")
    print(f"optimal h (forward, est.) : {h_forward:.3e}")
    print(f"optimal h (central, est.) : {h_central:.3e}")


if __name__ == "__main__":
    main()
