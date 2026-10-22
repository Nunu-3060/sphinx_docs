"""保存場 F = (2xy + z, x^2 + 2yz, x + y^2 + 3z^2) のポテンシャルを SymPy で求める.

使い方: python ch11_potential.py
"""

import sympy as sp

x, y, z = sp.symbols("x y z", real=True)


def report() -> None:
    """回転が 0 であることを確かめ、成分を順に積分してポテンシャルを求める."""
    fx, fy, fz = 2 * x * y + z, x**2 + 2 * y * z, x + y**2 + 3 * z**2
    curl = (sp.diff(fz, y) - sp.diff(fy, z), sp.diff(fx, z) - sp.diff(fz, x), sp.diff(fy, x) - sp.diff(fx, y))
    print("F =", (fx, fy, fz))
    print("rot F =", curl)

    # 手順 1：F_x を x で積分する。積分定数は y と z の関数 g(y, z) になる
    phi = sp.integrate(fx, x)
    print("手順 1: ∫F_x dx =", phi, "+ g(y, z)")
    # 手順 2：∂φ/∂y = F_y から ∂g/∂y を求め、y で積分する
    g_y = sp.simplify(fy - sp.diff(phi, y))
    phi = phi + sp.integrate(g_y, y)
    print("手順 2: ∂g/∂y =", g_y)
    # 手順 3：∂φ/∂z = F_z から残りの z だけの関数を求める
    h_z = sp.simplify(fz - sp.diff(phi, z))
    phi = phi + sp.integrate(h_z, z)
    print("手順 3: ∂h/∂z =", h_z)
    print("ポテンシャル φ =", phi, "+ 定数")

    grad = tuple(sp.simplify(sp.diff(phi, v)) for v in (x, y, z))
    print("確認: ∇φ =", grad)
    a, b = {x: 0, y: 0, z: 0}, {x: 1, y: 2, z: 3}
    print("(0, 0, 0) から (1, 2, 3) までの線積分 = φ(1, 2, 3) - φ(0, 0, 0) =", phi.subs(b) - phi.subs(a))


def main() -> None:
    report()


if __name__ == "__main__":
    main()
