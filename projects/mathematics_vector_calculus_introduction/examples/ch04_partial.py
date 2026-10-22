"""偏微分、偏微分の順序交換、1 次近似、連鎖律を SymPy と数値計算で確かめる.

使い方: python ch04_partial.py
"""

import numpy as np
import sympy as sp

import vc_plot


def f(x: float, y: float) -> float:
    """数値計算で使う関数 f(x, y) = x^2 y + sin(xy)."""
    return float(x**2 * y + np.sin(x * y))


def central_difference_x(x: float, y: float, h: float) -> float:
    """x についての偏微分を、中心差分 (f(x + h, y) - f(x - h, y)) / 2h で近似する."""
    return (f(x + h, y) - f(x - h, y)) / (2.0 * h)


def report() -> None:
    """偏導関数、順序交換、数値微分、1 次近似の誤差、連鎖律を順に確かめる."""
    x, y, t = sp.symbols("x y t")
    expr = x**2 * y + sp.sin(x * y)
    fx = sp.diff(expr, x)
    fy = sp.diff(expr, y)
    print(f"f   = {expr}")
    print(f"f_x = {fx}")
    print(f"f_y = {fy}")

    # 偏微分の順序交換（シュワルツの定理）
    fxy = sp.diff(expr, x, y)  # x で微分してから y で微分する
    fyx = sp.diff(expr, y, x)  # y で微分してから x で微分する
    print(f"f_xy = {fxy}")
    print(f"f_yx - f_xy = {sp.simplify(fyx - fxy)}")

    # 中心差分による数値微分
    exact = float(fx.subs({x: 1, y: 2}))
    print(f"点 (1, 2) での f_x：厳密値 {exact:.8f}")
    for h in (1e-1, 1e-2, 1e-3):
        print(f"  h = {h:.0e} の中心差分 {central_difference_x(1.0, 2.0, h):.8f}")

    # 全微分による 1 次近似 f(a + dx, b + dy) ≈ f(a, b) + f_x dx + f_y dy
    a, b = 1.0, 2.0
    gx = float(fx.subs({x: a, y: b}))
    gy = float(fy.subs({x: a, y: b}))
    for d in (0.1, 0.01):
        approx = f(a, b) + gx * d + gy * d
        actual = f(a + d, b + d)
        print(f"dx = dy = {d}：f の値 {actual:.8f}、1 次近似 {approx:.8f}、誤差 {actual - approx:.2e}")

    # 連鎖律：曲線 x = cos t, y = sin t に沿った df/dt
    on_curve = expr.subs({x: sp.cos(t), y: sp.sin(t)})
    direct = sp.diff(on_curve, t)
    chain = (fx * sp.diff(sp.cos(t), t) + fy * sp.diff(sp.sin(t), t)).subs({x: sp.cos(t), y: sp.sin(t)})
    print(f"df/dt（直接微分） - df/dt（連鎖律） = {sp.simplify(direct - chain)}")


def main() -> None:
    vc_plot.setup_font()
    report()


if __name__ == "__main__":
    main()
