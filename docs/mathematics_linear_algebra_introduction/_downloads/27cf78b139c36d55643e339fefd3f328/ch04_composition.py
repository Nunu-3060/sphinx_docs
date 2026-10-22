"""線形変換の合成: 回転とせん断を行う順序で結果が変わることを確かめる.

R は 90 度の回転、S はせん断である。「R の後に S」は行列 SR、
「S の後に R」は行列 RS に対応する。

使い方: python ch04_composition.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import la_plot

R = np.array([[0.0, -1.0], [1.0, 0.0]])  # 90 度の回転
S = np.array([[1.0, 1.0], [0.0, 1.0]])  # せん断


def report() -> None:
    """合成した変換の行列を表示する."""
    print("S @ R =")
    print(S @ R)
    print("R @ S =")
    print(R @ S)


def create_figure() -> Figure:
    """変換前、R の後に S、S の後に R の 3 つの図を描く."""
    cases = [
        ("変換前", np.eye(2)),
        (r"$R$ の後に $S$（行列 $SR$）", S @ R),
        (r"$S$ の後に $R$（行列 $RS$）", R @ S),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.8))
    shape = la_plot.letter_f()
    for ax, (title, a) in zip(axes, cases):
        la_plot.setup_plane(ax, (-2.5, 2.5), (-2.5, 2.5))
        la_plot.draw_grid(ax, a, color="0.4")
        moved = a @ shape
        ax.fill(moved[0], moved[1], color="C2", alpha=0.5)
        ax.plot(moved[0], moved[1], color="C2")
        la_plot.draw_vector(ax, a[:, 0], color="C3")
        la_plot.draw_vector(ax, a[:, 1], color="C0")
        ax.set_title(title)
    fig.tight_layout()
    return fig


def main() -> None:
    report()
    la_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
