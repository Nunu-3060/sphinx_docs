"""前進差分と中心差分の誤差が、刻み幅 h とともにどう小さくなるかを比べる.

使い方: python ch18_finite_difference.py
"""

from collections.abc import Callable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import vc_plot

X0 = 1.0  # 微分係数を求める点


def forward_diff(f: Callable[[float], float], x: float, h: float) -> float:
    """前進差分 (f(x + h) - f(x)) / h."""
    return (f(x + h) - f(x)) / h


def central_diff(f: Callable[[float], float], x: float, h: float) -> float:
    """中心差分 (f(x + h) - f(x - h)) / (2h)."""
    return (f(x + h) - f(x - h)) / (2.0 * h)


def errors(hs: NDArray[np.float64]) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """f(x) = sin x の x = X0 での微分係数を差分で求め、真の値 cos X0 との誤差を返す."""
    exact = np.cos(X0)
    fwd = np.array([abs(forward_diff(np.sin, X0, h) - exact) for h in hs])
    cen = np.array([abs(central_diff(np.sin, X0, h) - exact) for h in hs])
    return fwd, cen


def create_figure() -> Figure:
    """誤差と刻み幅の関係を両対数グラフで描く."""
    hs = np.logspace(-12, -1, 45)
    fwd, cen = errors(hs)
    fig, ax = plt.subplots(figsize=(6.0, 4.4))
    ax.loglog(hs, fwd, "o-", color="C0", markersize=4, label="前進差分")
    ax.loglog(hs, cen, "s-", color="C1", markersize=4, label="中心差分")
    ax.loglog(hs, 0.5 * hs, ":", color="C0", label="傾き 1（$h$ に比例）")
    ax.loglog(hs, 0.2 * hs**2, ":", color="C1", label="傾き 2（$h^2$ に比例）")
    ax.set_xlabel("刻み幅 $h$")
    ax.set_ylabel("誤差の絶対値")
    ax.set_ylim(1e-14, 1e2)
    ax.set_title(r"$\sin x$ の $x = 1$ での微分係数の誤差")
    ax.grid(True, which="major", color="0.9")
    ax.legend(fontsize=9)
    fig.tight_layout()
    return fig


def report() -> None:
    """刻み幅を 1/10 ずつ小さくしたときの誤差を表にする."""
    hs = np.array([1e-1, 1e-2, 1e-3, 1e-4])
    fwd, cen = errors(hs)
    print("      h    前進差分の誤差  中心差分の誤差")
    for h, e1, e2 in zip(hs, fwd, cen):
        print(f"{h:7.0e}  {e1:14.3e}  {e2:14.3e}")


def main() -> None:
    vc_plot.setup_font()
    report()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
