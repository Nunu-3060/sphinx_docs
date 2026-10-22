"""微小な直方体からの正味の流出量を体積で割った値が、発散に近づくことを確かめる.

使い方: python ch06_box_flux.py
"""

import sympy as sp

import vc_plot

x, y, z = sp.symbols("x y z")
F = (x**2 * y, y * z, x * z**2)  # ベクトル場 F = (F_x, F_y, F_z)
P = (1, 2, 3)  # 直方体の 1 つの頂点（x, y, z が最も小さい頂点）


def net_outflow(h: sp.Rational) -> sp.Expr:
    """頂点 P から各辺の長さ h の立方体について、6 つの面から出ていく流量の合計を厳密に計算する."""
    x0, y0, z0 = P
    total = sp.Integer(0)
    # x 軸に垂直な 2 つの面：x = x0 + h では外向き、x = x0 では内向き（符号が負）
    total += sp.integrate(F[0].subs(x, x0 + h) - F[0].subs(x, x0), (y, y0, y0 + h), (z, z0, z0 + h))
    total += sp.integrate(F[1].subs(y, y0 + h) - F[1].subs(y, y0), (x, x0, x0 + h), (z, z0, z0 + h))
    total += sp.integrate(F[2].subs(z, z0 + h) - F[2].subs(z, z0), (x, x0, x0 + h), (y, y0, y0 + h))
    return total


def report() -> None:
    """発散の値と、さまざまな大きさの立方体での「流出量 / 体積」を表示する."""
    div_f = sp.diff(F[0], x) + sp.diff(F[1], y) + sp.diff(F[2], z)
    exact = div_f.subs({x: P[0], y: P[1], z: P[2]})
    print(f"F = {F}")
    print(f"div F = {div_f}")
    print(f"div F{P} = {exact}")
    print()
    print("     h    流出量 / 体積      発散との差")
    for h in (sp.Integer(1), sp.Rational(1, 10), sp.Rational(1, 100), sp.Rational(1, 1000)):
        ratio = net_outflow(h) / h**3
        print(f"{float(h):6.3f}  {float(ratio):15.6f}  {float(ratio - exact):15.6f}")


def main() -> None:
    vc_plot.setup_font()
    report()


if __name__ == "__main__":
    main()
