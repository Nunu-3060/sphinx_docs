"""靴ひも公式と線積分で多角形の面積を求め、境界の向きを図に描く.

使い方: python ch13_shoelace.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray
from scipy import integrate

import vc_plot

# 反時計回りに並べた多角形の頂点
VERTICES = np.array([[1.0, 0.0], [4.0, 0.5], [5.0, 2.5], [2.5, 4.0], [0.0, 2.0]])


def shoelace_area(vertices: NDArray[np.float64]) -> float:
    """靴ひも公式 A = (1/2) Σ (x_i y_{i+1} - x_{i+1} y_i) で多角形の面積を求める.

    頂点が反時計回りなら正、時計回りなら負の値になる。
    """
    x = vertices[:, 0]
    y = vertices[:, 1]
    x_next = np.roll(x, -1)  # x_{i+1}（最後の頂点の次は最初の頂点）
    y_next = np.roll(y, -1)
    return float(0.5 * np.sum(x * y_next - x_next * y))


def line_integral_area(vertices: NDArray[np.float64]) -> float:
    """面積を線積分 (1/2)∮(x dy - y dx) で、辺ごとに数値積分して求める."""
    total = 0.0
    for start, end in zip(vertices, np.roll(vertices, -1, axis=0)):
        dx, dy = end - start

        def integrand(t: float, start: NDArray[np.float64] = start, dx: float = dx, dy: float = dy) -> float:
            x, y = start + t * np.array([dx, dy])
            return float(0.5 * (x * dy - y * dx))

        total += float(integrate.quad(integrand, 0.0, 1.0)[0])
    return total


def create_figure() -> Figure:
    """多角形と、正の向き（反時計回り）に回る境界を描く."""
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    vc_plot.setup_plane(ax, (-0.8, 5.8), (-0.8, 4.8))
    ax.fill(VERTICES[:, 0], VERTICES[:, 1], color="C0", alpha=0.15)
    for k, (start, end) in enumerate(zip(VERTICES, np.roll(VERTICES, -1, axis=0))):
        vc_plot.draw_vector(ax, end - start, origin=start, color="C0")
        ax.plot(*start, "o", color="C3")
        ax.text(start[0] + 0.1, start[1] - 0.35, f"$P_{k + 1}$", fontsize=12)
    ax.text(2.0, 1.8, "領域 $D$", fontsize=12)
    ax.set_title("多角形の境界を反時計回りにたどる")
    fig.tight_layout()
    return fig


def report() -> None:
    """2 つの方法で求めた面積を表示する."""
    print(f"靴ひも公式                 = {shoelace_area(VERTICES):.6f}")
    print(f"線積分 (1/2)∮(x dy - y dx) = {line_integral_area(VERTICES):.6f}")
    print(f"時計回りの頂点で靴ひも公式 = {shoelace_area(VERTICES[::-1]):.6f}")


def main() -> None:
    vc_plot.setup_font()
    report()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
