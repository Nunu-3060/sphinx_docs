"""パラメーター表示された曲面の面積、スカラー場の面積分、ベクトル場の流束を数値計算する.

使い方: python ch12_surface_integrals.py
"""

import math
from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray
from scipy import integrate

Vec = NDArray[np.float64]
Surface = Callable[[float, float], Vec]
ScalarField = Callable[[Vec], float]
VectorField = Callable[[Vec], Vec]


def normal(surface: Surface, u: float, v: float, h: float = 1e-6) -> Vec:
    """法線ベクトル r_u × r_v を、中心差分で求めた r_u, r_v から計算する."""
    r_u = (surface(u + h, v) - surface(u - h, v)) / (2.0 * h)
    r_v = (surface(u, v + h) - surface(u, v - h)) / (2.0 * h)
    return np.cross(r_u, r_v)


def scalar_surface_integral(f: ScalarField, surface: Surface,
                            u_range: tuple[float, float], v_range: tuple[float, float]) -> float:
    """∬_S f dS = ∬ f(r(u, v)) |r_u × r_v| du dv を計算する."""
    def integrand(v: float, u: float) -> float:
        return f(surface(u, v)) * float(np.linalg.norm(normal(surface, u, v)))

    value, _ = integrate.dblquad(integrand, u_range[0], u_range[1], v_range[0], v_range[1])
    return float(value)


def flux(field: VectorField, surface: Surface,
         u_range: tuple[float, float], v_range: tuple[float, float]) -> float:
    """流束 ∬_S F·dS = ∬ F(r(u, v))·(r_u × r_v) du dv を計算する.

    曲面の向きは r_u × r_v の向きで決まる。
    """
    def integrand(v: float, u: float) -> float:
        return float(field(surface(u, v)) @ normal(surface, u, v))

    value, _ = integrate.dblquad(integrand, u_range[0], u_range[1], v_range[0], v_range[1])
    return float(value)


def sphere(radius: float) -> Surface:
    """半径 radius の球面 r(θ, φ)。r_θ × r_φ は外向きになる."""
    def r(theta: float, phi: float) -> Vec:
        return radius * np.array([math.sin(theta) * math.cos(phi), math.sin(theta) * math.sin(phi),
                                  math.cos(theta)])
    return r


def cylinder(radius: float) -> Surface:
    """半径 radius の円柱面 r(φ, z) = (R cosφ, R sinφ, z)。r_φ × r_z は外向きになる."""
    def r(phi: float, z: float) -> Vec:
        return np.array([radius * math.cos(phi), radius * math.sin(phi), z])
    return r


def paraboloid(rho: float, phi: float) -> Vec:
    """放物面 z = x^2 + y^2 を、円柱座標の (ρ, φ) でパラメーター表示する."""
    return np.array([rho * math.cos(phi), rho * math.sin(phi), rho**2])


def position(p: Vec) -> Vec:
    """位置ベクトル場 F = r = (x, y, z)."""
    return p


def inverse_square(p: Vec) -> Vec:
    """逆 2 乗の場 F = r / |r|^3 = e_r / r^2（点電荷の電場と同じ形）."""
    return p / float(np.linalg.norm(p))**3


def report() -> None:
    """計算結果を、手計算の値と並べて表示する."""
    two_pi, pi = 2.0 * math.pi, math.pi
    rows = [
        ("単位球面の面積",
         scalar_surface_integral(lambda p: 1.0, sphere(1.0), (0.0, pi), (0.0, two_pi)), 4.0 * pi, "4 pi"),
        ("放物面 z = x^2 + y^2 (z <= 1) の面積",
         scalar_surface_integral(lambda p: 1.0, paraboloid, (0.0, 1.0), (0.0, two_pi)),
         pi * (5.0 * math.sqrt(5.0) - 1.0) / 6.0, "pi (5 sqrt(5) - 1)/6"),
        ("面密度 z の半球面の質量",
         scalar_surface_integral(lambda p: float(p[2]), sphere(1.0), (0.0, pi / 2.0), (0.0, two_pi)), pi, "pi"),
        ("F = r の、半径 1 の球面を通る流束",
         flux(position, sphere(1.0), (0.0, pi), (0.0, two_pi)), 4.0 * pi, "4 pi R^3"),
        ("F = r の、半径 2 の球面を通る流束",
         flux(position, sphere(2.0), (0.0, pi), (0.0, two_pi)), 32.0 * pi, "4 pi R^3"),
        ("F = r の、円柱の側面 (R = 1, 0 <= z <= 2) を通る流束",
         flux(position, cylinder(1.0), (0.0, two_pi), (0.0, 2.0)), 4.0 * pi, "2 pi R^2 h"),
        ("F = e_r / r^2 の、半径 1 の球面を通る流束",
         flux(inverse_square, sphere(1.0), (0.0, pi), (0.0, two_pi)), 4.0 * pi, "4 pi"),
        ("F = e_r / r^2 の、半径 2 の球面を通る流束",
         flux(inverse_square, sphere(2.0), (0.0, pi), (0.0, two_pi)), 4.0 * pi, "4 pi"),
    ]
    for name, numeric, exact, formula in rows:
        print(name)
        print(f"  数値: {numeric:.6f}  厳密: {exact:.6f} = {formula}")


def main() -> None:
    report()


if __name__ == "__main__":
    main()
