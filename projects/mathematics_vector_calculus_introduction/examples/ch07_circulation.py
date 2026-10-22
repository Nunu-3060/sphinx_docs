"""微小な正方形を一周する循環を面積で割った値が、回転の z 成分に近づくことを確かめる.

使い方: python ch07_circulation.py
"""

from collections.abc import Callable

import sympy as sp
from scipy import integrate

import vc_plot

x, y, z = sp.symbols("x y z")


def curl(f: tuple[sp.Expr, sp.Expr, sp.Expr]) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    """ベクトル場 f = (F_x, F_y, F_z) の回転を記号計算で求める."""
    fx, fy, fz = f
    return (sp.simplify(sp.diff(fz, y) - sp.diff(fy, z)),
            sp.simplify(sp.diff(fx, z) - sp.diff(fz, x)),
            sp.simplify(sp.diff(fy, x) - sp.diff(fx, y)))


def circulation_square(fx: Callable[[float, float], float], fy: Callable[[float, float], float],
                       cx: float, cy: float, h: float) -> float:
    """中心 (cx, cy)、1 辺 h の正方形を反時計回りに一周する線積分（循環）を数値積分で求める."""
    x0, x1, y0, y1 = cx - h / 2, cx + h / 2, cy - h / 2, cy + h / 2
    bottom = integrate.quad(lambda s: fx(s, y0), x0, x1)[0]  # 下の辺：+x の向き
    right = integrate.quad(lambda s: fy(x1, s), y0, y1)[0]   # 右の辺：+y の向き
    top = -integrate.quad(lambda s: fx(s, y1), x0, x1)[0]    # 上の辺：-x の向き
    left = -integrate.quad(lambda s: fy(x0, s), y0, y1)[0]   # 左の辺：-y の向き
    return float(bottom + right + top + left)


def report() -> None:
    """4 つのベクトル場について、回転の z 成分と「循環 / 面積」を点 (1, 0.5) で比べる."""
    fields: dict[str, tuple[sp.Expr, sp.Expr, sp.Expr]] = {
        "剛体回転": (-y, x, sp.Integer(0)),
        "自由渦": (-y / (x**2 + y**2), x / (x**2 + y**2), sp.Integer(0)),
        "せん断流": (y, sp.Integer(0), sp.Integer(0)),
        "一般の場": (x * sp.sin(y), x**2 * y, sp.Integer(0)),
    }
    cx, cy = 1.0, 0.5
    for name, field in fields.items():
        rot = curl(field)
        rot_z = float(rot[2].subs({x: cx, y: cy}))
        fx = sp.lambdify((x, y), field[0])
        fy = sp.lambdify((x, y), field[1])
        print(f"{name}: F = {field}")
        print(f"  rot F = {rot},  点 ({cx}, {cy}) での z 成分 = {rot_z:.6f}")
        for h in (0.5, 0.1, 0.01):
            ratio = circulation_square(fx, fy, cx, cy, h) / h**2
            print(f"  h = {h:<5}  循環 / 面積 = {round(ratio, 6) + 0.0:.6f}")

    # 一定の角速度ベクトル Omega での剛体回転 v = Omega x r の回転は 2 Omega になる
    wx, wy, wz = sp.symbols("Omega_x Omega_y Omega_z")
    v = (wy * z - wz * y, wz * x - wx * z, wx * y - wy * x)  # Omega x r の成分
    print()
    print(f"v = Omega x r = {v}")
    print(f"rot v = {curl(v)}")


def main() -> None:
    vc_plot.setup_font()
    report()


if __name__ == "__main__":
    main()
