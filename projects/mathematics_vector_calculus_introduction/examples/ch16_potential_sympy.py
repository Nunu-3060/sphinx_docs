"""原点から直線に沿って積分する公式で、スカラーポテンシャルとベクトルポテンシャルを SymPy で求める.

使い方: python ch16_potential_sympy.py
"""

import sympy as sp

import vc_plot

x, y, z, t = sp.symbols("x y z t", real=True)
R = sp.Matrix([x, y, z])  # 位置ベクトル


def grad(f: sp.Expr) -> sp.Matrix:
    """スカラー場 f の勾配."""
    return sp.Matrix([sp.diff(f, v) for v in (x, y, z)])


def div(f: sp.Matrix) -> sp.Expr:
    """ベクトル場 f の発散."""
    return sp.diff(f[0], x) + sp.diff(f[1], y) + sp.diff(f[2], z)


def rot(f: sp.Matrix) -> sp.Matrix:
    """ベクトル場 f の回転."""
    return sp.Matrix([
        sp.diff(f[2], y) - sp.diff(f[1], z),
        sp.diff(f[0], z) - sp.diff(f[2], x),
        sp.diff(f[1], x) - sp.diff(f[0], y),
    ])


def at_tr(f: sp.Matrix) -> sp.Matrix:
    """場 f(r) の r を t r に置き換えた f(t r) を返す."""
    return f.subs({x: t * x, y: t * y, z: t * z}, simultaneous=True)


def scalar_potential(f: sp.Matrix) -> sp.Expr:
    """∇×F = 0 の場 F に対し、φ(r) = ∫_0^1 F(t r)·r dt を求める（∇φ = F となる）."""
    return sp.expand(sp.integrate(at_tr(f).dot(R), (t, 0, 1)))


def vector_potential(b: sp.Matrix) -> sp.Matrix:
    """∇·B = 0 の場 B に対し、A(r) = ∫_0^1 t B(t r) × r dt を求める（∇×A = B となる）."""
    integrand = t * at_tr(b).cross(R)
    return sp.Matrix([sp.expand(sp.integrate(c, (t, 0, 1))) for c in integrand])


def report() -> None:
    """ポテンシャルを求め、微分すると元の場に戻ることを確かめる."""
    f = sp.Matrix([2 * x * y + z, x**2 + 3 * z, x + 3 * y])
    print(f"F = {list(f)}")
    print(f"  ∇×F = {list(sp.simplify(rot(f)))}")
    phi = scalar_potential(f)
    print(f"  φ = {phi}")
    print(f"  ∇φ - F = {list(sp.simplify(grad(phi) - f))}")

    b = sp.Matrix([y, z, x])
    print(f"B = {list(b)}")
    print(f"  ∇·B = {div(b)}")
    a = vector_potential(b)
    print(f"  A = {list(a)}")
    print(f"  ∇×A - B = {list(sp.simplify(rot(a) - b))}")
    # 任意のスカラー場の勾配を足しても回転は変わらない（ゲージの自由度）
    chi = x * y * z
    print(f"  ∇×(A + ∇(xyz)) - B = {list(sp.simplify(rot(a + grad(chi)) - b))}")


def main() -> None:
    vc_plot.setup_font()
    report()


if __name__ == "__main__":
    main()
