"""SciPy の dblquad と tplquad で重積分を数値計算し、手計算の値と比べる.

使い方: python ch10_scipy_integrals.py
"""

import math

import numpy as np
from scipy import integrate


def region_xy() -> float:
    """領域 x^2 <= y <= x (0 <= x <= 1) での xy の 2 重積分.

    dblquad(f, a, b, g, h) は ∫_a^b ∫_{g(x)}^{h(x)} f(y, x) dy dx を計算する。
    被積分関数の引数は (y, x) の順で、内側の積分変数が先に来ることに注意する。
    """
    value, _ = integrate.dblquad(lambda y, x: x * y, 0.0, 1.0, lambda x: x**2, lambda x: x)
    return float(value)


def exchanged_order() -> float:
    """∫_0^1 ∫_x^1 exp(y^2) dy dx を、積分の順序を交換した ∫_0^1 ∫_0^y exp(y^2) dx dy で計算する."""
    value, _ = integrate.dblquad(lambda x, y: math.exp(y**2), 0.0, 1.0, lambda y: 0.0, lambda y: y)
    return float(value)


def gaussian_polar() -> float:
    """平面全体での exp(-(x^2 + y^2)) の積分を、極座標 (dx dy = r dr dθ) で計算する."""
    value, _ = integrate.dblquad(lambda r, t: math.exp(-r**2) * r, 0.0, 2.0 * math.pi,
                                 lambda t: 0.0, lambda t: math.inf)
    return float(value)


def ball_volume() -> float:
    """単位球の体積を、直交座標の 3 重積分で計算する.

    tplquad(f, a, b, g, h, q, r) は ∫_a^b ∫_{g(x)}^{h(x)} ∫_{q(x,y)}^{r(x,y)} f(z, y, x) dz dy dx を計算する。
    """
    def z_max(x: float, y: float) -> float:
        return math.sqrt(max(1.0 - x**2 - y**2, 0.0))

    value, _ = integrate.tplquad(lambda z, y, x: 1.0, -1.0, 1.0,
                                 lambda x: -math.sqrt(1.0 - x**2), lambda x: math.sqrt(1.0 - x**2),
                                 lambda x, y: -z_max(x, y), z_max)
    return float(value)


def half_disk_centroid() -> float:
    """半径 1 の半円板（y >= 0）の重心の y 座標を、極座標で計算する（密度は一様）."""
    area, _ = integrate.dblquad(lambda r, t: r, 0.0, math.pi, lambda t: 0.0, lambda t: 1.0)
    moment, _ = integrate.dblquad(lambda r, t: r * math.sin(t) * r, 0.0, math.pi,
                                  lambda t: 0.0, lambda t: 1.0)
    return float(moment / area)


def sphere_inertia_ratio() -> float:
    """一様な球（半径 1、質量 1）の z 軸まわりの慣性モーメントを、球座標で計算する.

    体積素は r^2 sinθ dr dθ dφ、z 軸からの距離の 2 乗は (r sinθ)^2 である。
    """
    density = 1.0 / (4.0 / 3.0 * math.pi)
    value, _ = integrate.tplquad(lambda r, t, p: density * (r * math.sin(t))**2 * r**2 * math.sin(t),
                                 0.0, 2.0 * math.pi, lambda p: 0.0, lambda p: math.pi,
                                 lambda p, t: 0.0, lambda p, t: 1.0)
    return float(value)


def report() -> None:
    """数値計算の結果と、手計算で求めた厳密な値を並べて表示する."""
    rows = [
        ("x^2 <= y <= x での xy の積分", region_xy(), 1.0 / 24.0, "1/24"),
        ("順序を交換した exp(y^2) の積分", exchanged_order(), (math.e - 1.0) / 2.0, "(e - 1)/2"),
        ("平面全体での exp(-(x^2+y^2))", gaussian_polar(), math.pi, "pi"),
        ("単位球の体積", ball_volume(), 4.0 / 3.0 * math.pi, "4 pi/3"),
        ("半円板の重心の y 座標", half_disk_centroid(), 4.0 / (3.0 * math.pi), "4/(3 pi)"),
        ("球の慣性モーメント / (M R^2)", sphere_inertia_ratio(), 0.4, "2/5"),
    ]
    for name, numeric, exact, formula in rows:
        print(f"{name}")
        # 差は計算環境によって細かい値が変わるため、1e-9 未満かどうかだけを表示する
        diff = abs(numeric - exact)
        diff_text = "1e-9 未満" if diff < 1e-9 else f"{diff:.1e}"
        print(f"  数値: {numeric:.10f}  厳密: {exact:.10f} = {formula}  差: {diff_text}")
    print(f"参考: exp(-x^2) の実数全体での積分 = sqrt(pi) = {np.sqrt(np.pi):.10f}")


def main() -> None:
    report()


if __name__ == "__main__":
    main()
