"""第 7 章：台形公式とシンプソン公式の誤差の次数を調べる。

定積分 ∫_0^1 e^x dx = e - 1 を、分割数 n を 2 倍ずつ増やしながら台形公式とシンプソン公式で近似し、
誤差の絶対値と「n を 2 倍にしたときに誤差が何分の 1 になったか（誤差の比）」を表示する。
誤差の比が 4 に近ければ誤差は刻み幅 h の 2 乗に比例し、16 に近ければ h の 4 乗に比例している。

表の列の意味:
    n           分割数
    h           刻み幅 (b - a) / n
    trap_err    台形公式の誤差の絶対値
    simp_err    シンプソン公式の誤差の絶対値
    ratio       1 つ上の行の誤差 ÷ この行の誤差

実行方法:
    python ch07_numerical_integration.py
"""

import math
from collections.abc import Callable

import numpy as np
import numpy.typing as npt

FloatArray = npt.NDArray[np.float64]
Integrand = Callable[[FloatArray], FloatArray]


def trapezoid(f: Integrand, a: float, b: float, n: int) -> float:
    """区間 [a, b] を n 等分した複合台形公式で f の積分を近似する。"""
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return float(h * (0.5 * y[0] + y[1:-1].sum() + 0.5 * y[-1]))


def simpson(f: Integrand, a: float, b: float, n: int) -> float:
    """区間 [a, b] を n 等分（n は偶数）した複合シンプソン公式で f の積分を近似する。"""
    if n % 2 != 0:
        raise ValueError("シンプソン公式の分割数 n は偶数でなければならない")
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    # 奇数番目の点に重み 4、内部の偶数番目の点に重み 2 を掛ける
    return float(h / 3 * (y[0] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum() + y[-1]))


def integrand(x: FloatArray) -> FloatArray:
    """被積分関数 e^x。"""
    return np.exp(x)


def main() -> None:
    """分割数ごとの誤差と誤差の比を表形式で表示する。"""
    a, b = 0.0, 1.0
    exact = math.e - 1.0

    print(f"{'n':>6} {'h':>10} {'trap_err':>12} {'ratio':>6} {'simp_err':>12} {'ratio':>6}")
    prev_trap: float | None = None
    prev_simp: float | None = None
    for k in range(1, 11):
        n = 2**k
        h = (b - a) / n
        err_trap = abs(trapezoid(integrand, a, b, n) - exact)
        err_simp = abs(simpson(integrand, a, b, n) - exact)
        # 1 つ前の n での誤差との比（最初の行は比を表示しない）
        ratio_trap = f"{prev_trap / err_trap:6.2f}" if prev_trap is not None else " " * 6
        ratio_simp = f"{prev_simp / err_simp:6.2f}" if prev_simp is not None else " " * 6
        print(f"{n:>6} {h:>10.3e} {err_trap:>12.3e} {ratio_trap} {err_simp:>12.3e} {ratio_simp}")
        prev_trap, prev_simp = err_trap, err_simp


if __name__ == "__main__":
    main()
