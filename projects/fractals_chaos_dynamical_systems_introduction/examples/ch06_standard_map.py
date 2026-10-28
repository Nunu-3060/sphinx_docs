"""標準写像（チリコフ写像）: 保存系で、規則的な運動とカオス的な運動が混在する様子.

p_{n+1} = p_n + K sin θ_n,  θ_{n+1} = θ_n + p_{n+1}  （θ と p はともに 2π を法とする）

使い方: python ch06_standard_map.py [--save DIR]
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import plot_util

TWO_PI = 2.0 * np.pi


def create_figures() -> dict[str, Figure]:
    """3 つの K の値について、多数の初期値からの軌道を重ねて描く（phase）."""
    ks = (0.5, 0.97, 2.0)
    fig, axes = plt.subplots(1, 3, figsize=(14.0, 4.8))
    rng = np.random.default_rng(3)
    n_orbits = 150
    for ax, k in zip(axes, ks):
        theta = rng.uniform(0.0, TWO_PI, n_orbits)
        p = rng.uniform(0.0, TWO_PI, n_orbits)
        colors = plt.get_cmap("hsv")(np.linspace(0.0, 1.0, n_orbits, endpoint=False))
        ths = np.empty((800, n_orbits))
        ps = np.empty((800, n_orbits))
        for i in range(800):
            p = (p + k * np.sin(theta)) % TWO_PI
            theta = (theta + p) % TWO_PI
            ths[i] = theta
            ps[i] = p
        for j in range(n_orbits):
            ax.plot(ths[:, j], ps[:, j], ",", color=colors[j])
        ax.set_xlim(0.0, TWO_PI)
        ax.set_ylim(0.0, TWO_PI)
        ax.set_aspect("equal")
        ax.set_xlabel("$\\theta$")
        ax.set_ylabel("$p$")
        ax.set_title(f"$K = {k}$")
    fig.tight_layout()
    return {"phase": fig}


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures)


if __name__ == "__main__":
    main()
