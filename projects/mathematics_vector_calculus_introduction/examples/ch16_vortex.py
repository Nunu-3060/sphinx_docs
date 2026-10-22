"""自由渦 F = (-y, x)/(x^2 + y^2) の循環が、閉曲線が原点を囲むかどうかで変わることを確かめる.

使い方: python ch16_vortex.py
"""

from collections.abc import Callable

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from matplotlib.figure import Figure
from scipy import integrate

import vc_plot

Curve = Callable[[float], tuple[float, float]]


def field(x: float, y: float) -> tuple[float, float]:
    """自由渦の場 F = (-y, x) / (x^2 + y^2)."""
    r2 = x**2 + y**2
    return -y / r2, x / r2


def circulation(curve: Curve, velocity: Curve) -> float:
    """閉曲線 curve(t)（0 <= t <= 2π、反時計回り）に沿った F の線積分を求める."""
    def integrand(t: float) -> float:
        fx, fy = field(*curve(t))
        dx, dy = velocity(t)
        return fx * dx + fy * dy

    return float(integrate.quad(integrand, 0, 2 * np.pi, limit=200)[0])


def circle(cx: float, cy: float, radius: float) -> tuple[Curve, Curve]:
    """中心 (cx, cy)、半径 radius の円と、その t による微分を返す."""
    return ((lambda t: (cx + radius * np.cos(t), cy + radius * np.sin(t))),
            (lambda t: (-radius * np.sin(t), radius * np.cos(t))))


def ellipse(a: float, b: float) -> tuple[Curve, Curve]:
    """原点を中心とする、半径 a（x 方向）と b（y 方向）の楕円と、その t による微分を返す."""
    return ((lambda t: (a * np.cos(t), b * np.sin(t))),
            (lambda t: (-a * np.sin(t), b * np.cos(t))))


def show(label: str, value: float) -> None:
    """値を小数点以下 6 桁で表示する（-0.000000 とならないように 0 を足す）."""
    print(f"  {label}: {round(value, 6) + 0.0:.6f}")


def report() -> None:
    """回転が 0 であることを SymPy で確かめ、いろいろな閉曲線で循環を求める."""
    x, y = sp.symbols("x y", real=True)
    fx = -y / (x**2 + y**2)
    fy = x / (x**2 + y**2)
    print(f"回転の z 成分 ∂Fy/∂x - ∂Fx/∂y = {sp.simplify(sp.diff(fy, x) - sp.diff(fx, y))}（原点以外）")
    print("原点を囲む閉曲線")
    show("中心 (0, 0)、半径 1 の円", circulation(*circle(0, 0, 1)))
    show("中心 (0, 0)、半径 0.1 の円", circulation(*circle(0, 0, 0.1)))
    show("中心 (0.5, 0.3)、半径 1 の円", circulation(*circle(0.5, 0.3, 1)))
    show("半径 3 と 0.5 の楕円", circulation(*ellipse(3, 0.5)))
    print("原点を囲まない閉曲線")
    show("中心 (2, 0)、半径 1 の円", circulation(*circle(2, 0, 1)))
    show("中心 (0, -1.5)、半径 0.5 の円", circulation(*circle(0, -1.5, 0.5)))
    print(f"参考：2π = {2 * np.pi:.6f}")


def create_figure() -> Figure:
    """自由渦の流線と、原点を囲む円 C1、囲まない円 C2 を描く."""
    fig, ax = plt.subplots(figsize=(5.4, 5.0))
    vc_plot.setup_plane(ax, (-3.0, 3.0), (-3.0, 3.0))
    xx, yy = vc_plot.mesh((-3.0, 3.0), (-3.0, 3.0), 60)
    r2 = xx**2 + yy**2
    ax.streamplot(xx, yy, -yy / r2, xx / r2, color="0.6", density=0.9, linewidth=0.8)
    ax.plot(0, 0, "o", color="k", markersize=6)
    t = np.linspace(0, 2 * np.pi, 200)
    ax.plot(1.2 * np.cos(t), 1.2 * np.sin(t), color="C0", linewidth=2)
    ax.plot(2.0 + 0.7 * np.cos(t), 1.6 + 0.7 * np.sin(t), color="C2", linewidth=2)
    box = {"facecolor": "white", "edgecolor": "none"}
    ax.text(-0.9, -1.75, r"$C_1$：循環 $2\pi$", color="C0", fontsize=12, bbox=box)
    ax.text(1.3, 2.45, r"$C_2$：循環 $0$", color="C2", fontsize=12, bbox=box)
    ax.set_title("自由渦の流線（原点で定義されない）")
    fig.tight_layout()
    return fig


def main() -> None:
    vc_plot.setup_font()
    report()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
