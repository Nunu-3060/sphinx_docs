"""ファン・デル・ポール振動子のリミットサイクル.

x'' - μ (1 - x^2) x' + x = 0 は、振幅が小さいと振動が増幅され、大きいと減衰する。
その結果、どの初期値から出発しても、同じ 1 つの閉軌道（リミットサイクル）に近づく。

使い方: python ch03_van_der_pol.py [--save DIR]
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import ode
import plot_util
from ode import Vector

MU = 1.0


def van_der_pol(state: Vector) -> Vector:
    """ファン・デル・ポール方程式を 1 階の連立方程式 x' = v, v' = μ (1 - x^2) v - x として表した右辺."""
    x, v = state[..., 0], state[..., 1]
    return np.stack([v, MU * (1.0 - x**2) * v - x], axis=-1)


def create_figures() -> dict[str, Figure]:
    """相平面（左）と時系列（右）に、内側と外側から出発した 2 本の軌道を描く（limit_cycle）."""
    dt = 0.01
    n = 3000
    starts = [(np.array([0.1, 0.0]), "内側から出発", "C0"), (np.array([3.5, 3.0]), "外側から出発", "C3")]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.4))
    t = np.arange(n + 1) * dt
    for x0, label, color in starts:
        xs = ode.integrate(van_der_pol, x0, dt, n)
        ax1.plot(xs[:, 0], xs[:, 1], color=color, linewidth=1.0, label=label)
        ax1.plot(x0[0], x0[1], "o", color=color)
        ax2.plot(t, xs[:, 0], color=color, linewidth=1.0, label=label)
    ax1.set_xlabel("$x$")
    ax1.set_ylabel("速度 $v$")
    ax1.set_title("相平面")
    ax1.legend(loc="upper left", fontsize=9)
    ax1.grid(True, color="0.9")
    ax2.set_xlabel("時刻 $t$")
    ax2.set_ylabel("$x$")
    ax2.set_title("時系列")
    ax2.grid(True, color="0.9")
    fig.tight_layout()
    return {"limit_cycle": fig}


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures)


if __name__ == "__main__":
    main()
