"""クリフォード・アトラクタとピーター・デ・ヨング・アトラクタ.

どちらも三角関数だけでできた 2 次元の写像で、パラメータ a, b, c, d によって
さまざまな形のアトラクタが現れる。ジェネラティブアートの題材として人気がある。

* クリフォード:    x' = sin(a y) + c cos(a x),  y' = sin(b x) + d cos(b y)
* デ・ヨング:      x' = sin(a y) - cos(b x),    y' = sin(c x) - cos(d y)

使い方: python ch06_clifford.py [--save DIR]
"""

from collections.abc import Callable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import plot_util

Array = NDArray[np.float64]
Params = tuple[float, float, float, float]
Map2D = Callable[[Array, Array, Params], tuple[Array, Array]]


def clifford(x: Array, y: Array, params: Params) -> tuple[Array, Array]:
    """クリフォード・アトラクタの写像."""
    a, b, c, d = params
    return np.sin(a * y) + c * np.cos(a * x), np.sin(b * x) + d * np.cos(b * y)


def de_jong(x: Array, y: Array, params: Params) -> tuple[Array, Array]:
    """ピーター・デ・ヨング・アトラクタの写像."""
    a, b, c, d = params
    return np.sin(a * y) - np.cos(b * x), np.sin(c * x) - np.cos(d * y)


def attractor_points(f: Map2D, params: Params, n_orbits: int = 2000, n_steps: int = 200,
                     transient: int = 50, seed: int = 0) -> tuple[Array, Array]:
    """写像 f のアトラクタ上の点を、n_orbits 本の軌道をまとめて計算して返す."""
    rng = np.random.default_rng(seed)
    x = rng.uniform(-1.0, 1.0, n_orbits)
    y = rng.uniform(-1.0, 1.0, n_orbits)
    for _ in range(transient):
        x, y = f(x, y, params)
    xs = np.empty((n_steps, n_orbits))
    ys = np.empty((n_steps, n_orbits))
    for i in range(n_steps):
        x, y = f(x, y, params)
        xs[i] = x
        ys[i] = y
    return xs.ravel(), ys.ravel()


EXAMPLES: list[tuple[str, Map2D, Params]] = [
    ("クリフォード", clifford, (-1.4, 1.6, 1.0, 0.7)),
    ("ピーター・デ・ヨング", de_jong, (1.4, -2.3, 2.4, -2.1)),
]


def create_figures() -> dict[str, Figure]:
    """2 種類のアトラクタを点で描く（scatter）."""
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 5.4))
    for ax, (name, f, params) in zip(axes, EXAMPLES):
        x, y = attractor_points(f, params)
        ax.plot(x, y, ",", color="k", alpha=0.2)
        ax.set_aspect("equal")
        ax.set_title(f"{name}\n$(a, b, c, d) = {params}$", fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    return {"scatter": fig}


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures)


if __name__ == "__main__":
    main()
