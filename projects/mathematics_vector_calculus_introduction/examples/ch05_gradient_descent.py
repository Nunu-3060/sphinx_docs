"""勾配降下法で関数の最小点を探し、ステップ幅による進み方の違いを描く.

使い方: python ch05_gradient_descent.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import vc_plot


def f(x: NDArray[np.float64], y: NDArray[np.float64]) -> NDArray[np.float64]:
    """目的関数 f(x, y) = x^2 / 2 + 5 y^2. 最小点は原点."""
    return 0.5 * x**2 + 5.0 * y**2


def grad_f(p: NDArray[np.float64]) -> NDArray[np.float64]:
    """f の勾配 (x, 10 y)."""
    return np.array([p[0], 10.0 * p[1]])


def gradient_descent(start: NDArray[np.float64], step: float, n_iter: int) -> NDArray[np.float64]:
    """p_{k+1} = p_k - step * grad f(p_k) を n_iter 回繰り返し、通った点を (n_iter + 1) 行 2 列で返す."""
    points = [start]
    p = start
    for _ in range(n_iter):
        p = p - step * grad_f(p)
        points.append(p)
    return np.array(points)


def create_figure() -> Figure:
    """ステップ幅 0.05 と 0.18 の 2 通りで、探索の経路を等高線に重ねて描く."""
    xx, yy = vc_plot.mesh((-4.5, 1.0), (-1.6, 1.6), 200)
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    ax.contour(xx, yy, f(xx, yy), levels=[0.1, 0.5, 1, 2, 4, 6, 8, 10, 13], colors="0.6", linewidths=0.7)

    start = np.array([-4.0, 1.2])
    for step, color in ((0.05, "C0"), (0.18, "C3")):
        path = gradient_descent(start, step, 20)
        ax.plot(path[:, 0], path[:, 1], "o-", color=color, markersize=3, linewidth=1.2,
                label=f"ステップ幅 {step}")
    ax.plot(0.0, 0.0, "k*", markersize=10)
    ax.set_xlim(-4.5, 1.0)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title(r"勾配降下法（$f = x^2/2 + 5y^2$、20 回の反復）")
    ax.legend(loc="lower right")
    fig.tight_layout()
    return fig


def main() -> None:
    vc_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
