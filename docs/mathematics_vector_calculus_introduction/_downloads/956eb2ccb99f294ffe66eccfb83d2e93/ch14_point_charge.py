"""点電荷の場 r/r^3 が閉曲面を通る流束を求め、原点を囲むかどうかで値が変わることを確かめる.

使い方: python ch14_point_charge.py
"""

from collections.abc import Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray
from scipy import integrate

import vc_plot


def field(point: NDArray[np.float64]) -> NDArray[np.float64]:
    """原点に置いた点電荷の場 F = r / r^3（係数 q/(4πε0) を 1 とした電場）."""
    r = float(np.linalg.norm(point))
    return point / r**3


def sphere_flux(center: Sequence[float], radius: float) -> float:
    """中心 center、半径 radius の球面を外向きに通る F の流束を求める."""
    c = np.asarray(center, dtype=float)

    def integrand(theta: float, phi: float) -> float:
        n = np.array([np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)])
        point = c + radius * n
        return float(field(point) @ n * radius**2 * np.sin(theta))

    return float(integrate.dblquad(integrand, 0, 2 * np.pi, 0, np.pi)[0])


def box_flux(lower: Sequence[float], upper: Sequence[float]) -> float:
    """直方体 [lower, upper] の表面を外向きに通る F の流束を、6 つの面の和で求める."""
    lo = np.asarray(lower, dtype=float)
    hi = np.asarray(upper, dtype=float)
    total = 0.0
    for axis in range(3):
        a, b = [k for k in range(3) if k != axis]
        for side, sign in ((hi[axis], 1.0), (lo[axis], -1.0)):
            def integrand(v: float, u: float, axis: int = axis, a: int = a, b: int = b,
                          side: float = side, sign: float = sign) -> float:
                point = np.empty(3)
                point[axis], point[a], point[b] = side, u, v
                return float(sign * field(point)[axis])

            total += float(integrate.dblquad(integrand, lo[a], hi[a], lo[b], hi[b])[0])
    return total


def create_figure() -> Figure:
    """xy 平面上の場の向きと、原点を囲む球面 S1、囲まない球面 S2 の断面を描く."""
    fig, ax = plt.subplots(figsize=(5.8, 5.0))
    vc_plot.setup_plane(ax, (-3.0, 4.0), (-3.0, 3.0))
    xx, yy = vc_plot.mesh((-3.0, 4.0), (-3.0, 3.0), 14)  # 格子点が原点に重ならない個数
    r = np.hypot(xx, yy)
    # 向きだけを見るため、矢印の長さをそろえる
    ax.quiver(xx, yy, xx / r, yy / r, color="0.55", scale=28, width=0.004)
    ax.plot(0, 0, "o", color="C3", markersize=8)
    t = np.linspace(0, 2 * np.pi, 200)
    ax.plot(1.5 * np.cos(t), 1.5 * np.sin(t), color="C0", linewidth=2)
    ax.plot(2.6 + 0.8 * np.cos(t), 1.6 + 0.8 * np.sin(t), color="C2", linewidth=2)
    ax.text(-1.2, -2.0, r"$S_1$：流束 $4\pi$", color="C0", fontsize=12,
            bbox={"facecolor": "white", "edgecolor": "none"})
    ax.text(1.9, 2.55, r"$S_2$：流束 $0$", color="C2", fontsize=12,
            bbox={"facecolor": "white", "edgecolor": "none"})
    ax.set_title("点電荷の場と 2 つの閉曲面（xy 平面での断面）")
    fig.tight_layout()
    return fig


def show(label: str, value: float) -> None:
    """値を小数点以下 6 桁で表示する（-0.000000 とならないように 0 を足す）."""
    print(f"  {label}: {round(value, 6) + 0.0:.6f}")


def report() -> None:
    """いろいろな閉曲面を通る流束を表示する."""
    print("原点を囲む閉曲面")
    for radius in (0.5, 1.0, 2.0):
        show(f"中心 (0, 0, 0)、半径 {radius} の球面", sphere_flux((0, 0, 0), radius))
    show("中心 (0.3, 0.2, 0)、半径 1 の球面", sphere_flux((0.3, 0.2, 0), 1.0))
    show("立方体 [-1, 1]^3 の表面", box_flux((-1, -1, -1), (1, 1, 1)))
    print("原点を囲まない閉曲面")
    show("中心 (3, 0, 0)、半径 1 の球面", sphere_flux((3, 0, 0), 1.0))
    show("直方体 [1, 3] × [-1, 1] × [-1, 1] の表面", box_flux((1, -1, -1), (3, 1, 1)))
    print(f"参考：4π = {4 * np.pi:.6f}")


def main() -> None:
    vc_plot.setup_font()
    report()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
