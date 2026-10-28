"""エノン写像のストレンジアトラクタと、その層状の構造.

x_{n+1} = 1 - a x_n^2 + y_n,  y_{n+1} = b x_n
（a = 1.4, b = 0.3）

使い方: python ch06_henon.py [--save DIR]
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from numpy.typing import NDArray

import plot_util

A, B = 1.4, 0.3

# 図に描く範囲（x の最小・最大、y の最小・最大）。順に拡大していく
VIEWS = [
    (-1.5, 1.5, -0.45, 0.45),
    (0.55, 0.80, 0.14, 0.22),
    (0.695, 0.715, 0.1725, 0.1805),
]


def henon_points(n_orbits: int = 4000, n_steps: int = 1000, transient: int = 100,
                 seed: int = 0) -> NDArray[np.float64]:
    """エノン・アトラクタ上の点を返す（形は (n_orbits * n_steps, 2)）.

    原点の近くに n_orbits 個の初期値を置き、まとめて（ベクトル化して）反復する。
    """
    rng = np.random.default_rng(seed)
    x = rng.uniform(-0.1, 0.1, n_orbits)
    y = rng.uniform(-0.1, 0.1, n_orbits)
    for _ in range(transient):
        x, y = 1.0 - A * x**2 + y, B * x
    points = np.empty((n_steps, n_orbits, 2))
    for i in range(n_steps):
        x, y = 1.0 - A * x**2 + y, B * x
        points[i, :, 0] = x
        points[i, :, 1] = y
    return points.reshape(-1, 2)


def create_figures() -> dict[str, Figure]:
    """アトラクタの全体と、2 段階の拡大図を並べる（attractor）."""
    points = henon_points()
    fig, axes = plt.subplots(1, 3, figsize=(14.0, 4.4))
    for i, (ax, (x0, x1, y0, y1)) in enumerate(zip(axes, VIEWS)):
        inside = (points[:, 0] > x0) & (points[:, 0] < x1) & (points[:, 1] > y0) & (points[:, 1] < y1)
        ax.plot(points[inside, 0], points[inside, 1], ",", color="k", alpha=0.4 if i == 0 else 0.8)
        ax.set_xlim(x0, x1)
        ax.set_ylim(y0, y1)
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
        if i + 1 < len(VIEWS):
            nx0, nx1, ny0, ny1 = VIEWS[i + 1]
            ax.add_patch(Rectangle((nx0, ny0), nx1 - nx0, ny1 - ny0, fill=False, edgecolor="C3", linewidth=1.2))
    axes[0].set_title("全体")
    axes[1].set_title("赤枠の拡大")
    axes[2].set_title("さらに赤枠の拡大")
    fig.tight_layout()
    return {"attractor": fig}


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures)


if __name__ == "__main__":
    main()
