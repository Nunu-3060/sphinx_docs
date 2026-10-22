"""スケール因子から、直交曲線座標系での勾配・発散・回転・ラプラシアンを SymPy で計算する.

使い方: python ch09_orthogonal_ops.py
"""

from typing import Any

import sympy as sp

# SymPy の式には型ヒントがないため、式の型は Any として扱う
Expr = Any
Vector = tuple[Expr, Expr, Expr]

rho, r = sp.symbols("rho r", positive=True)
phi, theta, z = sp.symbols("phi theta z", real=True)


def scale_factors(position: Vector, coords: Vector) -> Vector:
    """位置ベクトル (x, y, z) を座標 (u1, u2, u3) で偏微分し、スケール因子 h_i = |∂r/∂u_i| を求める."""
    pos = sp.Matrix(position)
    # 本書で扱う座標の範囲（0 <= θ <= π など）では各因子が 0 以上なので、絶対値を外す
    h = [sp.simplify(pos.diff(u).norm()).replace(sp.Abs, lambda a: a) for u in coords]
    return (h[0], h[1], h[2])


def gradient(f: Expr, coords: Vector, h: Vector) -> Vector:
    """勾配の成分 (1/h_i) ∂f/∂u_i を返す."""
    g = [sp.simplify(sp.diff(f, u) / hi) for u, hi in zip(coords, h)]
    return (g[0], g[1], g[2])


def divergence(field: Vector, coords: Vector, h: Vector) -> Expr:
    """発散 (1/(h1 h2 h3)) Σ ∂(h1 h2 h3 F_i / h_i)/∂u_i を返す."""
    jac = h[0] * h[1] * h[2]
    return sp.simplify(sum(sp.diff(jac / hi * fi, u) for fi, u, hi in zip(field, coords, h)) / jac)


def rotation(field: Vector, coords: Vector, h: Vector) -> Vector:
    """回転の成分を返す（i, j, k は 1, 2, 3 の巡回的な並び）."""
    result = []
    for i in range(3):
        j, k = (i + 1) % 3, (i + 2) % 3
        comp = (sp.diff(h[k] * field[k], coords[j]) - sp.diff(h[j] * field[j], coords[k])) / (h[j] * h[k])
        result.append(sp.simplify(comp))
    return (result[0], result[1], result[2])


def laplacian(f: Expr, coords: Vector, h: Vector) -> Expr:
    """ラプラシアン = 勾配の発散 を返す."""
    return divergence(gradient(f, coords, h), coords, h)


def report() -> None:
    """円柱座標と球座標のスケール因子と、代表的な場の計算結果を表示する."""
    cyl: Vector = (rho, phi, z)
    h_cyl = scale_factors((rho * sp.cos(phi), rho * sp.sin(phi), z), cyl)
    sph: Vector = (r, theta, phi)
    h_sph = scale_factors((r * sp.sin(theta) * sp.cos(phi), r * sp.sin(theta) * sp.sin(phi),
                           r * sp.cos(theta)), sph)
    print("スケール因子")
    print("  円柱座標 (rho, phi, z):", h_cyl)
    print("  球座標 (r, theta, phi):", h_sph)

    omega, gamma, v_max, radius = sp.symbols("omega Gamma v_max R", positive=True)
    print("円柱座標")
    print("  剛体回転 v = omega*rho e_phi の回転:", rotation((0, omega * rho, 0), cyl, h_cyl))
    print("  自由渦 v = Gamma/(2*pi*rho) e_phi の回転:",
          rotation((0, gamma / (2 * sp.pi * rho), 0), cyl, h_cyl))
    pipe = v_max * (1 - rho**2 / radius**2)
    print("  円管の流れ v = v_max*(1 - rho^2/R^2) e_z")
    print("    発散:", divergence((0, 0, pipe), cyl, h_cyl))
    print("    回転:", rotation((0, 0, pipe), cyl, h_cyl))
    print("    v_z のラプラシアン:", laplacian(pipe, cyl, h_cyl))

    q, eps0 = sp.symbols("q epsilon_0", positive=True)
    print("球座標")
    print("  1/r の勾配:", gradient(1 / r, sph, h_sph))
    print("  点電荷の電場 E = q/(4*pi*epsilon_0*r^2) e_r の発散:",
          divergence((q / (4 * sp.pi * eps0 * r**2), 0, 0), sph, h_sph))
    print("  1/r のラプラシアン:", laplacian(1 / r, sph, h_sph))

    # 直交座標で計算した結果と比べる：f = x^2 y + z^2 のラプラシアンは 2y + 2
    x_s = r * sp.sin(theta) * sp.cos(phi)
    y_s = r * sp.sin(theta) * sp.sin(phi)
    z_s = r * sp.cos(theta)
    f_sph = x_s**2 * y_s + z_s**2
    print("確認: f = x^2*y + z^2 のラプラシアン")
    print("  球座標の公式で計算して 2*y + 2 を引いた差:", sp.simplify(laplacian(f_sph, sph, h_sph) - (2 * y_s + 2)))


def main() -> None:
    report()


if __name__ == "__main__":
    main()
