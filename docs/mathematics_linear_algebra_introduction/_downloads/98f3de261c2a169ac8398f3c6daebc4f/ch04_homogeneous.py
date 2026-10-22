"""同次座標によるアフィン変換: 回転と平行移動を 3 行 3 列の行列で表す.

点 (x, y) を (x, y, 1) と表すと、平行移動も行列の積で書ける。
回転と平行移動を合成すると、順序によって結果が変わる。

使い方: python ch04_homogeneous.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import la_plot

Matrix = NDArray[np.float64]


def translation(tx: float, ty: float) -> Matrix:
    """(tx, ty) だけ平行移動する同次座標の行列を返す."""
    return np.array([[1.0, 0.0, tx],
                     [0.0, 1.0, ty],
                     [0.0, 0.0, 1.0]])


def rotation(degrees: float) -> Matrix:
    """原点を中心に degrees 度だけ回転する同次座標の行列を返す."""
    theta = np.radians(degrees)
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0.0],
                     [s, c, 0.0],
                     [0.0, 0.0, 1.0]])


def house() -> Matrix:
    """家の形をした多角形の頂点を、同次座標（3 行 N 列）で返す."""
    xy = np.array([[0.0, 1.0, 1.0, 0.5, 0.0, 0.0],
                   [0.0, 0.0, 1.0, 1.6, 1.0, 0.0]])
    return np.vstack([xy, np.ones(xy.shape[1])])


T = translation(3.0, 1.0)
R = rotation(90.0)


def report() -> None:
    """合成した行列と、点 (1, 0) の行き先を表示する."""
    with np.printoptions(precision=3, suppress=True):
        print("T @ R（回転の後に平行移動）=")
        print(T @ R)
        print("R @ T（平行移動の後に回転）=")
        print(R @ T)
        p = np.array([1.0, 0.0, 1.0])  # 点 (1, 0) の同次座標
        print("(T @ R) @ p =", (T @ R) @ p)
        print("(R @ T) @ p =", (R @ T) @ p)


def create_figure() -> Figure:
    """変換前の家と、2 通りの順序で変換した家を描く."""
    fig, ax = plt.subplots(figsize=(6, 4.5))
    la_plot.setup_plane(ax, (-3.5, 4.5), (-2, 5))
    cases = [
        ("変換前", np.eye(3), "0.5"),
        (r"回転の後に平行移動（$TR$）", T @ R, "C0"),
        (r"平行移動の後に回転（$RT$）", R @ T, "C3"),
    ]
    shape = house()
    for label, m, color in cases:
        moved = m @ shape
        ax.fill(moved[0], moved[1], color=color, alpha=0.3)
        ax.plot(moved[0], moved[1], color=color, label=label)
        # 家の右下の角 (1, 0) に印を付ける
        ax.plot(moved[0, 1], moved[1, 1], "o", color=color)
    ax.legend(loc="lower left")
    ax.set_title("同次座標による回転と平行移動")
    fig.tight_layout()
    return fig


def main() -> None:
    report()
    la_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
