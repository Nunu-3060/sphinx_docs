"""ローレンツ方程式のストレンジアトラクタ、初期値鋭敏性、ローレンツ写像.

x' = σ (y - x),  y' = x (ρ - z) - y,  z' = x y - β z
（σ = 10, ρ = 28, β = 8/3）

使い方: python ch06_lorenz.py [--save DIR]
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import ode
import plot_util
from ode import Vector

SIGMA = 10.0
RHO = 28.0
BETA = 8.0 / 3.0


def lorenz(state: Vector) -> Vector:
    """ローレンツ方程式の右辺."""
    x, y, z = state[..., 0], state[..., 1], state[..., 2]
    return np.stack([SIGMA * (y - x), x * (RHO - z) - y, x * y - BETA * z], axis=-1)


def trajectory(x0: tuple[float, float, float], dt: float, n: int, transient: int = 0) -> Vector:
    """初期値 x0 から n ステップの軌道を返す。最初の transient ステップは捨てる."""
    xs = ode.integrate(lorenz, np.array(x0), dt, n + transient)
    return xs[transient:]


def local_maxima(values: NDArray[np.float64]) -> NDArray[np.float64]:
    """時系列の極大値（両隣より大きい値）を順に返す."""
    inner = values[1:-1]
    result: NDArray[np.float64] = inner[(inner > values[:-2]) & (inner > values[2:])]
    return result


def create_figures() -> dict[str, Figure]:
    """アトラクタ（attractor）、2 本の軌道の時系列（divergence）、ローレンツ写像（lorenz_map）の図を作る."""
    dt = 0.01
    xs = trajectory((1.0, 1.0, 1.0), dt, 8000, transient=500)
    fig1 = plt.figure(figsize=(7.0, 6.0))
    ax1 = fig1.add_subplot(projection="3d")
    ax1.plot(xs[:, 0], xs[:, 1], xs[:, 2], linewidth=0.4)
    ax1.set_xlabel("$x$")
    ax1.set_ylabel("$y$")
    ax1.set_zlabel("$z$")
    ax1.view_init(elev=20.0, azim=-60.0)
    fig1.tight_layout()

    a = trajectory((1.0, 1.0, 1.0), dt, 4000)
    b = trajectory((1.0 + 1e-8, 1.0, 1.0), dt, 4000)
    t = np.arange(len(a)) * dt
    fig2, ax2 = plt.subplots(figsize=(10.0, 3.4))
    ax2.plot(t, a[:, 0], linewidth=0.9, label="$x(0) = 1$")
    ax2.plot(t, b[:, 0], linewidth=0.9, linestyle="--", label="$x(0) = 1 + 10^{-8}$")
    ax2.set_xlabel("時刻 $t$")
    ax2.set_ylabel("$x$")
    ax2.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0))
    ax2.grid(True, color="0.9")
    fig2.tight_layout()

    long = trajectory((1.0, 1.0, 1.0), dt, 60000, transient=500)
    peaks = local_maxima(long[:, 2])
    fig3, ax3 = plt.subplots(figsize=(5.0, 5.0))
    ax3.plot(peaks[:-1], peaks[1:], ".", markersize=2)
    ax3.plot([28.0, 48.0], [28.0, 48.0], color="0.5", linewidth=0.8)
    ax3.set_xlim(28.0, 48.0)
    ax3.set_ylim(28.0, 48.0)
    ax3.set_aspect("equal")
    ax3.set_xlabel("$z$ の $k$ 番目の極大値 $M_k$")
    ax3.set_ylabel("$M_{k+1}$")
    fig3.tight_layout()
    return {"attractor": fig1, "divergence": fig2, "lorenz_map": fig3}


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures)


if __name__ == "__main__":
    main()
