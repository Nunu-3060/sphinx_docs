"""ガウスの発散定理の両辺を数値積分で別々に計算し、一致を確かめる.

使い方: python ch14_gauss_check.py
"""

import numpy as np
from scipy import integrate

import vc_plot


def sphere_flux() -> float:
    """F = (x^3, y^3, z^3) の、単位球面を外向きに通る流束を求める.

    球面上の点は (sinθ cosφ, sinθ sinφ, cosθ)、外向きの単位法線ベクトルは
    その点の位置ベクトルに等しく、面素は dS = sinθ dθ dφ である。
    """
    def integrand(theta: float, phi: float) -> float:
        n = np.array([np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)])
        f = n**3  # 球面上では (x, y, z) = n
        return float(f @ n * np.sin(theta))

    # dblquad(f(θ, φ), φ の範囲, θ の範囲)：内側の変数が第 1 引数になる
    return float(integrate.dblquad(integrand, 0, 2 * np.pi, 0, np.pi)[0])


def sphere_divergence_integral() -> float:
    """∇·F = 3(x^2 + y^2 + z^2) = 3r^2 を、単位球の内部で体積積分する.

    球座標の体積素 dV = r^2 sinθ dr dθ dφ を使う。
    """
    def integrand(r: float, theta: float, phi: float) -> float:
        return float(3 * r**2 * r**2 * np.sin(theta))

    # tplquad(f(r, θ, φ), φ の範囲, θ の範囲, r の範囲)
    return float(integrate.tplquad(integrand, 0, 2 * np.pi, 0, np.pi, 0, 1)[0])


def cube_flux() -> float:
    """G = (xy, yz, zx) の、立方体 [0, 1]^3 の表面を外向きに通る流束を、6 つの面の和で求める."""
    total = 0.0
    for axis in range(3):
        for side, sign in ((1.0, 1.0), (0.0, -1.0)):  # x = 1 の面は外向き法線 +e_x、x = 0 は -e_x
            def integrand(v: float, u: float, axis: int = axis, side: float = side, sign: float = sign) -> float:
                point = np.empty(3)
                point[axis] = side
                others = [k for k in range(3) if k != axis]
                point[others[0]], point[others[1]] = u, v
                x, y, z = point
                g = np.array([x * y, y * z, z * x])
                return float(sign * g[axis])

            total += float(integrate.dblquad(integrand, 0, 1, 0, 1)[0])
    return total


def cube_divergence_integral() -> float:
    """∇·G = y + z + x を、立方体 [0, 1]^3 で体積積分する."""
    return float(integrate.tplquad(lambda z, y, x: x + y + z, 0, 1, 0, 1, 0, 1)[0])


def report() -> None:
    """2 つの例で、閉曲面の流束と発散の体積積分を比べる."""
    print("F = (x^3, y^3, z^3)、V = 単位球")
    print(f"  閉曲面の流束   = {sphere_flux():.6f}")
    print(f"  発散の体積積分 = {sphere_divergence_integral():.6f}")
    print(f"  厳密値 12π/5   = {12 * np.pi / 5:.6f}")
    print("G = (xy, yz, zx)、V = 立方体 [0, 1]^3")
    print(f"  閉曲面の流束   = {cube_flux():.6f}")
    print(f"  発散の体積積分 = {cube_divergence_integral():.6f}")
    print("  厳密値 3/2     = 1.500000")


def main() -> None:
    vc_plot.setup_font()
    report()


if __name__ == "__main__":
    main()
