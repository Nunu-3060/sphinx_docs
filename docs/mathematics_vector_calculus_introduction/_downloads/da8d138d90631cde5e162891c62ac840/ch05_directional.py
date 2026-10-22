"""方向微分を勾配との内積で求め、差分による近似値と比べる.

使い方: python ch05_directional.py
"""

import math

import sympy as sp

import vc_plot


def report() -> None:
    """f(x, y) = x^2 y の点 (1, 2) での方向微分を、いくつかの向きで計算する."""
    x, y = sp.symbols("x y")
    f = x**2 * y
    grad = [sp.diff(f, x), sp.diff(f, y)]
    p = {x: 1, y: 2}
    gx = float(grad[0].subs(p))
    gy = float(grad[1].subs(p))
    print(f"grad f = ({grad[0]}, {grad[1]})")
    print(f"grad f(1, 2) = ({gx:.6f}, {gy:.6f}),  |grad f| = {math.hypot(gx, gy):.6f}")
    print()

    f_num = sp.lambdify((x, y), f)
    h = 1.0e-6
    steepest = math.degrees(math.atan2(gy, gx))  # 勾配の向きの角度
    print("角度[度]  内積 grad f . u   差分による近似")
    for degree in (0.0, steepest, 45.0, 90.0, steepest + 90.0, 180.0):
        theta = math.radians(degree)
        ux, uy = math.cos(theta), math.sin(theta)  # 単位ベクトル u
        by_gradient = gx * ux + gy * uy
        # 中心差分 (f(p + h u) - f(p - h u)) / (2h)
        by_difference = (f_num(1 + h * ux, 2 + h * uy) - f_num(1 - h * ux, 2 - h * uy)) / (2 * h)
        # round() と + 0.0 で、-0.000000 と表示されるのを防ぐ
        print(f"{degree:9.3f}  {round(by_gradient, 6) + 0.0:15.6f}  {round(by_difference, 6) + 0.0:15.6f}")


def main() -> None:
    vc_plot.setup_font()
    report()


if __name__ == "__main__":
    main()
