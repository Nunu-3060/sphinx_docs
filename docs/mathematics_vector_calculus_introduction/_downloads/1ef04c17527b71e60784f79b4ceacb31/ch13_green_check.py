"""グリーンの定理の両辺を数値積分で別々に計算し、一致を確かめる.

使い方: python ch13_green_check.py
"""

from collections.abc import Callable

import numpy as np
from scipy import integrate

import vc_plot

Curve = Callable[[float], tuple[float, float]]


def field(x: float, y: float) -> tuple[float, float]:
    """ベクトル場 F = (P, Q) = (x - y^3, x^3 + y)."""
    return x - y**3, x**3 + y


def rot_z(x: float, y: float) -> float:
    """回転の z 成分 ∂Q/∂x - ∂P/∂y = 3x^2 + 3y^2."""
    return 3 * x**2 + 3 * y**2


def div(x: float, y: float) -> float:
    """発散 ∂P/∂x + ∂Q/∂y = 2."""
    return 2.0


def boundary_integrals(curve: Curve, velocity: Curve, t0: float, t1: float) -> tuple[float, float]:
    """曲線 curve(t)（t0 <= t <= t1）に沿った循環と、外向きの流束を返す.

    velocity(t) は curve の t による微分 (dx/dt, dy/dt) である。
    循環は ∫(P dx + Q dy)、流束は ∫(P dy - Q dx) で計算する。
    """
    def circulation_integrand(t: float) -> float:
        p, q = field(*curve(t))
        dx, dy = velocity(t)
        return p * dx + q * dy

    def flux_integrand(t: float) -> float:
        p, q = field(*curve(t))
        dx, dy = velocity(t)
        return p * dy - q * dx

    circulation = integrate.quad(circulation_integrand, t0, t1)[0]
    flux = integrate.quad(flux_integrand, t0, t1)[0]
    return float(circulation), float(flux)


def polygon_integrals(vertices: list[tuple[float, float]]) -> tuple[float, float]:
    """反時計回りに並べた多角形の頂点から、境界に沿った循環と外向きの流束を返す."""
    total_circulation = 0.0
    total_flux = 0.0
    for (xa, ya), (xb, yb) in zip(vertices, vertices[1:] + vertices[:1]):
        # 辺を t（0 <= t <= 1）で表す。xa などは既定引数で関数に固定する
        def edge(t: float, xa: float = xa, ya: float = ya, xb: float = xb,
                 yb: float = yb) -> tuple[float, float]:
            return xa + (xb - xa) * t, ya + (yb - ya) * t

        def edge_velocity(t: float, xa: float = xa, ya: float = ya, xb: float = xb,
                          yb: float = yb) -> tuple[float, float]:
            return xb - xa, yb - ya

        circulation, flux = boundary_integrals(edge, edge_velocity, 0.0, 1.0)
        total_circulation += circulation
        total_flux += flux
    return total_circulation, total_flux


def report() -> None:
    """単位円板と長方形の 2 つの領域で、グリーンの定理の両辺を比べる."""
    print("F = (x - y^3, x^3 + y)")

    # 単位円板：境界は (cos t, sin t)、0 <= t <= 2π（反時計回り）
    circ, flux = boundary_integrals(lambda t: (np.cos(t), np.sin(t)),
                                    lambda t: (-np.sin(t), np.cos(t)), 0.0, 2 * np.pi)
    # dblquad は被積分関数を f(y, x) の順で受け取る
    rot_area = integrate.dblquad(lambda y, x: rot_z(x, y), -1, 1,
                                 lambda x: -np.sqrt(1 - x**2), lambda x: np.sqrt(1 - x**2))[0]
    div_area = integrate.dblquad(lambda y, x: div(x, y), -1, 1,
                                 lambda x: -np.sqrt(1 - x**2), lambda x: np.sqrt(1 - x**2))[0]
    print("単位円板")
    print(f"  循環形  境界の線積分 = {circ:.6f}  領域の重積分 = {rot_area:.6f}  (厳密値 3π/2 = {1.5 * np.pi:.6f})")
    print(f"  流束形  境界の線積分 = {flux:.6f}  領域の重積分 = {div_area:.6f}  (厳密値 2π   = {2 * np.pi:.6f})")

    # 長方形 [0, 2] × [0, 1]
    circ, flux = polygon_integrals([(0.0, 0.0), (2.0, 0.0), (2.0, 1.0), (0.0, 1.0)])
    rot_area = integrate.dblquad(lambda y, x: rot_z(x, y), 0, 2, 0, 1)[0]
    div_area = integrate.dblquad(lambda y, x: div(x, y), 0, 2, 0, 1)[0]
    print("長方形 [0, 2] × [0, 1]")
    print(f"  循環形  境界の線積分 = {circ:.6f}  領域の重積分 = {rot_area:.6f}  (厳密値 10)")
    print(f"  流束形  境界の線積分 = {flux:.6f}  領域の重積分 = {div_area:.6f}  (厳密値 4)")


def main() -> None:
    vc_plot.setup_font()
    report()


if __name__ == "__main__":
    main()
