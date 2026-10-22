"""連立一次方程式の解の構造: 一般解 = 特殊解 + 同次方程式の解.

方程式 x + 2y = 4 の解は、特殊解 xp = (4, 0) に、同次方程式
x + 2y = 0 の解 t (-2, 1) を加えたもの全体である。解の集合は、
零空間（原点を通る直線）を xp だけ平行移動した直線になる。

使い方: python ch08_solution_structure.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import la_plot


def create_figure() -> Figure:
    """零空間、解の集合、特殊解、最小ノルム解を描く."""
    a = np.array([[1.0, 2.0]])
    b = np.array([4.0])
    xp = np.array([4.0, 0.0])  # 特殊解の 1 つ
    n = np.array([-2.0, 1.0])  # 零空間の基底ベクトル
    x_min = np.linalg.pinv(a) @ b  # ノルムが最小の解（第 12 章で扱う）

    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    la_plot.setup_plane(ax, (-3.5, 5.5), (-1.5, 3.5))
    t = np.linspace(-3, 3, 2)
    ax.plot(t * n[0], t * n[1], color="C0", label=r"零空間 $x + 2y = 0$")
    ax.plot(xp[0] + t * n[0], xp[1] + t * n[1], color="C3", label=r"解の集合 $x + 2y = 4$")
    la_plot.draw_vector(ax, n, color="C0", label=r"$\mathbf{n}$", offset=(-0.3, 0.15))
    la_plot.draw_vector(ax, xp, color="C1", label=r"$\mathbf{x}_p$", offset=(-0.2, -0.45))
    la_plot.draw_vector(ax, 2 * n, origin=xp, color="C0", linestyle="--")  # xp に 2n を加える
    la_plot.draw_vector(ax, xp + 2 * n, color="C2", label=r"$\mathbf{x}_p + 2\mathbf{n}$",
                        offset=(-1.7, 0.2))
    ax.plot(x_min[0], x_min[1], "o", color="C4", label="ノルム最小の解 (0.8, 1.6)")
    ax.legend(loc="upper right", fontsize=9)
    ax.set_title("一般解 = 特殊解 + 同次方程式の解")
    fig.tight_layout()
    return fig


def main() -> None:
    la_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
