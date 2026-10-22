"""SymPy で多変数関数を偏微分する最小の例.

使い方: python ch01_sympy_partial.py
"""

import sympy as sp

import vc_plot


def report() -> None:
    """f(x, y) = x^2 y + sin(xy) の偏導関数を記号計算で求め、点 (1, 2) での値を表示する."""
    x, y = sp.symbols("x y")
    f = x**2 * y + sp.sin(x * y)
    fx = sp.diff(f, x)  # x で偏微分する
    fy = sp.diff(f, y)  # y で偏微分する
    print(f"f    = {f}")
    print(f"f_x  = {fx}")
    print(f"f_y  = {fy}")
    value = fx.subs({x: 1, y: 2})
    print(f"f_x(1, 2) = {value} = {float(value):.6f}")


def main() -> None:
    vc_plot.setup_font()
    report()


if __name__ == "__main__":
    main()
