"""円柱を過ぎるポテンシャル流（一様流と二重湧き出しの重ね合わせ）を流線で描く.

使い方: python ch17_potential_flow.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Circle
from numpy.typing import NDArray

import vc_plot

V_INF = 1.0  # 遠方での一様流の速さ（本文の v_∞）
A = 1.0  # 円柱の半径


def velocity(x: NDArray[np.float64],
             y: NDArray[np.float64]) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """速度ポテンシャル phi = v_inf x (1 + A^2 / r^2) の勾配として、流れの速度 (v_x, v_y) を返す."""
    r2 = x**2 + y**2
    vx = V_INF * (1.0 - A**2 * (x**2 - y**2) / r2**2)
    vy = -2.0 * V_INF * A**2 * x * y / r2**2
    return vx, vy


def create_figure() -> Figure:
    """流線と速さの分布を描く. 円柱の内部は流れの外なので塗りつぶす."""
    xx, yy = vc_plot.mesh((-3.0, 3.0), (-2.0, 2.0), 200)
    inside = xx**2 + yy**2 < A**2
    vx, vy = velocity(xx, yy)
    vx[inside] = np.nan
    vy[inside] = np.nan
    speed = np.hypot(vx, vy)

    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    stream = ax.streamplot(xx, yy, vx, vy, color=speed, cmap="viridis", density=1.4, linewidth=1.0)
    ax.add_patch(Circle((0.0, 0.0), A, color="0.6"))
    ax.set_xlim(-3.0, 3.0)
    ax.set_ylim(-2.0, 2.0)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title("円柱を過ぎるポテンシャル流（色は速さ）")
    fig.colorbar(stream.lines, ax=ax, label="速さ $|\\mathbf{v}|$", shrink=0.8)
    fig.tight_layout()
    return fig


def main() -> None:
    vc_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
