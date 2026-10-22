"""2 つのベクトル場 F1 = (y, x) と F2 = (-y, x) を、3 つの経路に沿って線積分して比べる.

使い方: python ch11_two_paths.py
"""

from collections.abc import Callable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray
from scipy import integrate

import vc_plot

Vec = NDArray[np.float64]
Field = Callable[[Vec], Vec]
# 経路は、パラメーター t から位置 r(t) と速度 r'(t) を返す関数の組で表す
Path = tuple[Callable[[float], Vec], Callable[[float], Vec]]


def field_1(p: Vec) -> Vec:
    """F1 = (y, x)：ポテンシャル xy の勾配."""
    return np.array([p[1], p[0]])


def field_2(p: Vec) -> Vec:
    """F2 = (-y, x)：原点のまわりを反時計回りに回る場."""
    return np.array([-p[1], p[0]])


def line_integral(field: Field, path: Path, t0: float, t1: float) -> float:
    """∫_C F·dr = ∫_{t0}^{t1} F(r(t))·r'(t) dt を数値計算する."""
    r, dr = path
    value, _ = integrate.quad(lambda t: float(field(r(t)) @ dr(t)), t0, t1)
    # 丸め誤差で -0.000000 と表示されないように、ごく小さい値は 0 にする
    return 0.0 if abs(value) < 1e-12 else float(value)


# 経路 C1：原点から (1, 1) への線分 r(t) = (t, t)
C1: Path = (lambda t: np.array([t, t]), lambda t: np.array([1.0, 1.0]))
# 経路 C2：原点から (1, 0) を経由して (1, 1) へ。t ∈ [0, 2] で表す
C2: Path = (lambda t: np.array([min(t, 1.0), max(t - 1.0, 0.0)]),
            lambda t: np.array([1.0, 0.0]) if t < 1.0 else np.array([0.0, 1.0]))
# 経路 C3：放物線 r(t) = (t, t^2)
C3: Path = (lambda t: np.array([t, t**2]), lambda t: np.array([1.0, 2.0 * t]))
# 閉曲線：単位円を反時計回りに 1 周する r(t) = (cos t, sin t)
CIRCLE: Path = (lambda t: np.array([np.cos(t), np.sin(t)]), lambda t: np.array([-np.sin(t), np.cos(t)]))


def create_figure() -> Figure:
    """2 つのベクトル場と 3 つの経路を並べて描く."""
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.8))
    xx, yy = vc_plot.mesh((-0.2, 1.2), (-0.2, 1.2), 11)
    t = np.linspace(0.0, 1.0, 50)
    for ax, (u, v), title in [(axes[0], (yy, xx), r"$\mathbf{F}_1 = (y, x)$"),
                              (axes[1], (-yy, xx), r"$\mathbf{F}_2 = (-y, x)$")]:
        vc_plot.setup_plane(ax, (-0.2, 1.25), (-0.2, 1.25))
        ax.quiver(xx, yy, u, v, color="0.6", angles="xy", scale_units="xy", scale=8.0, width=0.004)
        ax.plot(t, t, color="C0", linewidth=2, label="$C_1$：線分")
        ax.plot([0.0, 1.0, 1.0], [0.0, 0.0, 1.0], color="C1", linewidth=2, label="$C_2$：折れ線")
        ax.plot(t, t**2, color="C2", linewidth=2, label="$C_3$：放物線")
        ax.plot([0.0, 1.0], [0.0, 1.0], "ko", markersize=5)
        ax.text(-0.15, 0.05, "A", fontsize=12)
        ax.text(1.04, 1.04, "B", fontsize=12)
        ax.set_title(title)
    axes[0].legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    return fig


def report() -> None:
    """各経路に沿った線積分と、単位円に沿った循環を表示する."""
    paths = [("C1（線分）", C1, 1.0), ("C2（折れ線）", C2, 2.0), ("C3（放物線）", C3, 1.0)]
    print("A = (0, 0) から B = (1, 1) までの線積分")
    for name, path, t_end in paths:
        w1 = line_integral(field_1, path, 0.0, t_end)
        w2 = line_integral(field_2, path, 0.0, t_end)
        print(f"  {name:10s}  F1: {w1:.6f}   F2: {w2:.6f}")
    print("単位円を反時計回りに 1 周する循環")
    print(f"  F1: {line_integral(field_1, CIRCLE, 0.0, 2.0 * np.pi):.6f}"
          f"   F2: {line_integral(field_2, CIRCLE, 0.0, 2.0 * np.pi):.6f}  (2 pi = {2.0 * np.pi:.6f})")


def main() -> None:
    vc_plot.setup_font()
    report()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
