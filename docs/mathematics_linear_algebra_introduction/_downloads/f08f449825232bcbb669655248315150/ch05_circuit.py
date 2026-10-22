"""キルヒホッフの法則で、抵抗の回路に流れる電流を求める.

電源 E = 10 V に抵抗 R1 = 2 Ω をつなぎ、その先に抵抗 R2 = 4 Ω と
R3 = 4 Ω を並列につないだ回路である。電流 I1、I2、I3 は次の式を満たす。

    I1 - I2 - I3 = 0        （節点の電流の保存）
    R1 I1 + R2 I2 = E        （左の閉路の電圧）
    R2 I2 - R3 I3 = 0        （右の閉路の電圧）

使い方: python ch05_circuit.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

import la_plot

E = 10.0  # 電源の電圧 [V]
R1, R2, R3 = 2.0, 4.0, 4.0  # 抵抗 [Ω]


def report() -> None:
    """連立一次方程式を作って解き、電流を表示する."""
    a = np.array([[1.0, -1.0, -1.0],
                  [R1, R2, 0.0],
                  [0.0, R2, -R3]])
    b = np.array([0.0, E, 0.0])
    currents = np.linalg.solve(a, b)
    for name, value in zip(["I1", "I2", "I3"], currents):
        print(f"{name} = {value:.3f} A")


def _resistor(ax: Axes, start: tuple[float, float], end: tuple[float, float], label: str,
              label_offset: tuple[float, float]) -> None:
    """start から end までの導線の中央に、抵抗の記号（ジグザグの線）を描く."""
    p0 = np.array(start)
    p1 = np.array(end)
    direction = p1 - p0
    normal = np.array([-direction[1], direction[0]]) / np.linalg.norm(direction)
    t = np.linspace(0.3, 0.7, 13)  # 導線の 30% から 70% の区間をジグザグにする
    amplitude = 0.12 * np.array([0, 1, 0, -1] * 3 + [0])
    points = p0 + np.outer(t, direction) + np.outer(amplitude, normal)
    ax.plot([p0[0], points[0, 0]], [p0[1], points[0, 1]], color="k")
    ax.plot(points[:, 0], points[:, 1], color="k")
    ax.plot([points[-1, 0], p1[0]], [points[-1, 1], p1[1]], color="k")
    middle = (p0 + p1) / 2
    ax.text(middle[0] + label_offset[0], middle[1] + label_offset[1], label, ha="center", va="center")


def create_figure() -> Figure:
    """回路図を描く."""
    fig, ax = plt.subplots(figsize=(6, 3.6))
    # 電源（左の縦の枝）: 長い線が正極
    ax.plot([0, 0], [0, 0.9], color="k")
    ax.plot([-0.25, 0.25], [1.1, 1.1], color="k", linewidth=2)
    ax.plot([-0.12, 0.12], [0.9, 0.9], color="k", linewidth=2)
    ax.plot([0, 0], [1.1, 2], color="k")
    ax.text(-0.35, 1.0, f"E = {E:g} V", ha="right", va="center")
    # 抵抗
    _resistor(ax, (0.0, 2.0), (2.0, 2.0), f"R1 = {R1:g} Ω", (0.0, 0.35))
    _resistor(ax, (2.0, 2.0), (2.0, 0.0), f"R2 = {R2:g} Ω", (0.75, 0.0))
    _resistor(ax, (4.0, 2.0), (4.0, 0.0), f"R3 = {R3:g} Ω", (0.75, 0.0))
    # 導線
    ax.plot([2, 4], [2, 2], color="k")
    ax.plot([0, 4], [0, 0], color="k")
    # 電流の向き
    la_plot.draw_vector(ax, (0.4, 0.0), origin=(0.1, 2.25), color="C3")
    ax.text(0.15, 2.4, "I1", color="C3")
    la_plot.draw_vector(ax, (0.0, -0.4), origin=(1.65, 1.6), color="C3")
    ax.text(1.35, 1.4, "I2", color="C3")
    la_plot.draw_vector(ax, (0.0, -0.4), origin=(3.65, 1.6), color="C3")
    ax.text(3.35, 1.4, "I3", color="C3")
    ax.set_xlim(-1.8, 5.2)
    ax.set_ylim(-0.4, 2.7)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    return fig


def main() -> None:
    report()
    la_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
