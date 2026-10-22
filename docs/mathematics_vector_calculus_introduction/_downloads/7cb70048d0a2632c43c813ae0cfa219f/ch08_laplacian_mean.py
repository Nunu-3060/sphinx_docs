"""小さな円の上での平均と中心の値の差から、ラプラシアンを求める.

使い方: python ch08_laplacian_mean.py
"""

import math
from collections.abc import Callable

import sympy as sp
from scipy import integrate

import vc_plot

x, y = sp.symbols("x y")


def circle_mean(f_num: Callable[[float, float], float], cx: float, cy: float, h: float) -> float:
    """中心 (cx, cy)、半径 h の円周上での関数 f_num の平均値を数値積分で求める."""
    total = integrate.quad(lambda t: f_num(cx + h * math.cos(t), cy + h * math.sin(t)), 0.0, 2.0 * math.pi,
                           epsabs=1.0e-12, epsrel=1.0e-12)[0]
    return float(total / (2.0 * math.pi))


def report() -> None:
    """4 (平均 - 中心の値) / h^2 が、h を小さくするとラプラシアンに近づくことを示す."""
    cx, cy = 1.0, 0.5
    examples = [x**3 + x * y**2 + sp.sin(y), x**2 - y**2]
    for f in examples:
        lap = sp.diff(f, x, 2) + sp.diff(f, y, 2)
        f_num = sp.lambdify((x, y), f)
        center = float(f.subs({x: cx, y: cy}))
        print(f"f = {f}")
        print(f"  ラプラシアン = {lap},  点 ({cx}, {cy}) での値 = {float(lap.subs({x: cx, y: cy})):.6f}")
        for h in (0.5, 0.1, 0.01):
            mean = circle_mean(f_num, cx, cy, h)
            estimate = 4.0 * (mean - center) / h**2
            print(f"  h = {h:<5}  円周上の平均 - 中心の値 = {round(mean - center, 8) + 0.0:.8f},  "
                  f"4 (平均 - 中心の値) / h^2 = {round(estimate, 6) + 0.0:.6f}")


def main() -> None:
    vc_plot.setup_font()
    report()


if __name__ == "__main__":
    main()
