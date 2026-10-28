"""レスラー方程式のアトラクタと、ポアンカレ断面による解析.

x' = -y - z,  y' = x + a y,  z' = b + z (x - c)
（a = 0.2, b = 0.2, c = 5.7）

軌道が半平面 {y = 0, x < 0} を正の側から負の側へ横切るたびに x を記録すると、
連続時間の力学系を、離散時間の写像（ポアンカレ写像）として調べられる。

使い方: python ch06_rossler.py [--save DIR]
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import ode
import plot_util
from ode import Vector

A, B, C = 0.2, 0.2, 5.7


def rossler(state: Vector) -> Vector:
    """レスラー方程式の右辺."""
    x, y, z = state[..., 0], state[..., 1], state[..., 2]
    return np.stack([-y - z, x + A * y, B + z * (x - C)], axis=-1)


def section_crossings(xs: Vector) -> NDArray[np.float64]:
    """軌道 xs が半平面 {y = 0, x < 0} を y > 0 から y < 0 へ横切る点の x 座標を返す.

    横切る前後の 2 点を直線で結び、y = 0 になる位置を線形補間で求める。
    """
    y0, y1 = xs[:-1, 1], xs[1:, 1]
    idx = np.nonzero((y0 > 0.0) & (y1 <= 0.0) & (xs[:-1, 0] < 0.0))[0]
    s = y0[idx] / (y0[idx] - y1[idx])
    result: NDArray[np.float64] = xs[idx, 0] + s * (xs[idx + 1, 0] - xs[idx, 0])
    return result


def create_figures() -> dict[str, Figure]:
    """アトラクタ（attractor）と、ポアンカレ断面の帰還写像（section）の図を作る."""
    dt = 0.02
    xs = ode.integrate(rossler, np.array([1.0, 1.0, 0.0]), dt, 60000)[2000:]
    fig1 = plt.figure(figsize=(12.0, 5.0))
    ax1 = fig1.add_subplot(1, 2, 1, projection="3d")
    part = xs[:8000]
    ax1.plot(part[:, 0], part[:, 1], part[:, 2], linewidth=0.4)
    ax1.set_xlabel("$x$")
    ax1.set_ylabel("$y$")
    ax1.set_zlabel("$z$")
    ax2 = fig1.add_subplot(1, 2, 2)
    ax2.plot(part[:, 0], part[:, 1], linewidth=0.3)
    ax2.plot([-12.0, 0.0], [0.0, 0.0], color="C3", linewidth=2.0, label="断面 $y = 0,\\ x < 0$")
    ax2.set_aspect("equal")
    ax2.set_xlabel("$x$")
    ax2.set_ylabel("$y$")
    ax2.set_title("$xy$ 平面への射影")
    ax2.legend(loc="upper right", fontsize=9)
    fig1.tight_layout()

    u = -section_crossings(xs)
    fig2, ax3 = plt.subplots(figsize=(5.0, 5.0))
    ax3.plot(u[:-1], u[1:], ".", markersize=3)
    lo, hi = float(u.min()) - 0.5, float(u.max()) + 0.5
    ax3.plot([lo, hi], [lo, hi], color="0.5", linewidth=0.8)
    ax3.set_xlim(lo, hi)
    ax3.set_ylim(lo, hi)
    ax3.set_aspect("equal")
    ax3.set_xlabel("$k$ 回目に断面を横切った位置 $u_k = -x$")
    ax3.set_ylabel("$u_{k+1}$")
    fig2.tight_layout()
    return {"attractor": fig1, "section": fig2}


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures)


if __name__ == "__main__":
    main()
