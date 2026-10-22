"""ストークスの定理の両辺を数値積分で別々に計算し、境界が同じなら曲面によらないことを確かめる.

使い方: python ch15_stokes_check.py
"""

from collections.abc import Callable

import numpy as np
from numpy.typing import NDArray
from scipy import integrate

import vc_plot

Surface = Callable[[float, float], NDArray[np.float64]]


def field(p: NDArray[np.float64]) -> NDArray[np.float64]:
    """ベクトル場 F = (-y, x, xz)."""
    x, y, z = p
    return np.array([-y, x, x * z])


def rot_field(p: NDArray[np.float64]) -> NDArray[np.float64]:
    """F の回転 ∇×F = (0, -z, 2)."""
    return np.array([0.0, -p[2], 2.0])


def circulation() -> float:
    """境界の円 (cos t, sin t, 0)（0 <= t <= 2π）に沿った F の線積分を求める."""
    def integrand(t: float) -> float:
        point = np.array([np.cos(t), np.sin(t), 0.0])
        velocity = np.array([-np.sin(t), np.cos(t), 0.0])
        return float(field(point) @ velocity)

    return float(integrate.quad(integrand, 0, 2 * np.pi)[0])


def rot_flux(surface: Surface, u_range: tuple[float, float], v_range: tuple[float, float]) -> float:
    """曲面 r(u, v) を通る ∇×F の流束 ∬(∇×F)·(r_u × r_v) du dv を求める.

    r_u と r_v は中心差分で近似する。r_u × r_v の向き（どちらが表か）は、
    パラメーターの取り方で決まるので、境界の向きと右ねじの関係になるように選んでおく。
    """
    h = 1e-6

    def integrand(v: float, u: float) -> float:
        r_u = (surface(u + h, v) - surface(u - h, v)) / (2 * h)
        r_v = (surface(u, v + h) - surface(u, v - h)) / (2 * h)
        return float(rot_field(surface(u, v)) @ np.cross(r_u, r_v))

    return float(integrate.dblquad(integrand, u_range[0], u_range[1], v_range[0], v_range[1])[0])


def disk(rho: float, phi: float) -> NDArray[np.float64]:
    """xy 平面上の単位円板（法線は +z 向き）."""
    return np.array([rho * np.cos(phi), rho * np.sin(phi), 0.0])


def hemisphere(theta: float, phi: float) -> NDArray[np.float64]:
    """上半分の単位球面（法線は外向き＝上向き）."""
    return np.array([np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)])


def paraboloid(rho: float, phi: float) -> NDArray[np.float64]:
    """回転放物面 z = 1 - x^2 - y^2 の z >= 0 の部分（法線は上向き）."""
    return np.array([rho * np.cos(phi), rho * np.sin(phi), 1 - rho**2])


def report() -> None:
    """境界の線積分と、3 つの曲面を通る回転の流束を表示する."""
    print("F = (-y, x, xz)、境界 C = xy 平面上の単位円（反時計回り）")
    print(f"  境界 C の線積分          : {circulation():.6f}")
    print(f"  円板を通る回転の流束     : {rot_flux(disk, (0, 1), (0, 2 * np.pi)):.6f}")
    print(f"  半球面を通る回転の流束   : {rot_flux(hemisphere, (0, np.pi / 2), (0, 2 * np.pi)):.6f}")
    print(f"  放物面を通る回転の流束   : {rot_flux(paraboloid, (0, 1), (0, 2 * np.pi)):.6f}")
    print(f"  厳密値 2π                : {2 * np.pi:.6f}")


def main() -> None:
    vc_plot.setup_font()
    report()


if __name__ == "__main__":
    main()
