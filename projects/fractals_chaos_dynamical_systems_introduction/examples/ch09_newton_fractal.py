"""ニュートン法フラクタル: 複素平面の各点から出発したニュートン法が、どの解に収束するかで色分けする.

方程式 p(z) = 0 に対するニュートン法の写像 N(z) = z - p(z) / p'(z) を反復する。

使い方: python ch09_newton_fractal.py [--save DIR]
"""

from collections.abc import Callable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import hsv_to_rgb
from matplotlib.figure import Figure
from numpy.typing import NDArray

import plot_util
from ch09_mandelbrot_julia import complex_grid

Complex = NDArray[np.complex128]
Poly = Callable[[Complex], Complex]


def newton_basins(p: Poly, dp: Poly, roots: list[complex], z0: Complex, max_iter: int = 60,
                  tol: float = 1e-6) -> tuple[NDArray[np.int64], NDArray[np.int64]]:
    """各点が収束した解の番号（収束しなければ -1）と、収束までの反復回数を返す."""
    z = z0.copy()
    which = np.full(z.shape, -1, dtype=np.int64)
    steps = np.full(z.shape, max_iter, dtype=np.int64)
    for n in range(max_iter):
        with np.errstate(divide="ignore", invalid="ignore"):
            z = z - p(z) / dp(z)
        for k, r in enumerate(roots):
            hit = (np.abs(z - r) < tol) & (which < 0)
            which[hit] = k
            steps[hit] = n
    return which, steps


def basin_image(which: NDArray[np.int64], steps: NDArray[np.int64], n_roots: int, max_iter: int) -> NDArray[np.float64]:
    """解ごとに色相を変え、収束が遅い点ほど暗くした RGB 画像を作る（収束しない点は黒）."""
    hue = np.where(which >= 0, which / n_roots, 0.0)
    value = np.where(which >= 0, 1.0 - 0.8 * np.sqrt(steps / max_iter), 0.0)
    hsv = np.stack([hue, np.full(hue.shape, 0.65), value], axis=-1)
    image: NDArray[np.float64] = hsv_to_rgb(hsv)
    return image


def create_figures() -> dict[str, Figure]:
    """z^3 - 1 = 0 と z^3 - 2z + 2 = 0 のニュートン法フラクタルを描く（basins）."""
    cases: list[tuple[str, Poly, Poly]] = [
        ("$z^3 - 1 = 0$", lambda z: z**3 - 1.0, lambda z: 3.0 * z**2),
        ("$z^3 - 2z + 2 = 0$", lambda z: z**3 - 2.0 * z + 2.0, lambda z: 3.0 * z**2 - 2.0),
    ]
    roots_list = [list(np.roots([1.0, 0.0, 0.0, -1.0])), list(np.roots([1.0, 0.0, -2.0, 2.0]))]
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 5.4))
    max_iter = 60
    width = 4.0
    for ax, (title, p, dp), roots in zip(axes, cases, roots_list):
        z0 = complex_grid(0.0, width, 600, 600)
        which, steps = newton_basins(p, dp, [complex(r) for r in roots], z0, max_iter)
        ax.imshow(basin_image(which, steps, len(roots), max_iter), extent=(-2.0, 2.0, -2.0, 2.0))
        ax.plot([complex(r).real for r in roots], [complex(r).imag for r in roots], "o", color="w",
                markeredgecolor="k", markersize=6)
        ax.set_title(title)
        ax.set_xlabel("実部")
        ax.set_ylabel("虚部")
    fig.tight_layout()
    return {"basins": fig}


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures)


if __name__ == "__main__":
    main()
