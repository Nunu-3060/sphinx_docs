"""正方形の板の定常温度分布（ラプラス方程式）をヤコビ法で解く.

上の辺を温度 1、ほかの 3 辺を温度 0 に保つ。
使い方: python ch18_jacobi_laplace.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import vc_plot

N = 41  # 1 辺の格子点の数（境界を含む）
TOLERANCE = 1e-9  # 1 回の反復での変化の最大値がこれより小さくなったら止める


def solve() -> tuple[NDArray[np.float64], int]:
    """ヤコビ法で温度を求め、温度の配列（軸 0 が y、軸 1 が x）と反復回数を返す."""
    t = np.zeros((N, N))
    t[-1, 1:-1] = 1.0  # 上の辺（y = 1）
    for count in range(1, 100_000):
        new = t.copy()
        # 内部の各点を、上下左右の 4 点の平均で置き換える
        new[1:-1, 1:-1] = 0.25 * (t[1:-1, 2:] + t[1:-1, :-2] + t[2:, 1:-1] + t[:-2, 1:-1])
        change = np.max(np.abs(new - t))
        t = new
        if change < TOLERANCE:
            return t, count
    raise RuntimeError("収束しなかった")


def create_figure() -> Figure:
    """温度の等高線と、熱流束 q = -grad T の向きを描く."""
    t, _ = solve()
    x = np.linspace(0.0, 1.0, N)
    xx, yy = np.meshgrid(x, x)
    h = x[1] - x[0]
    dt_dx = np.gradient(t, h, axis=1)
    dt_dy = np.gradient(t, h, axis=0)

    fig, ax = plt.subplots(figsize=(5.6, 4.6))
    filled = ax.contourf(xx, yy, t, levels=np.linspace(0.0, 1.0, 21), cmap="inferno")
    ax.contour(xx, yy, t, levels=np.linspace(0.1, 0.9, 9), colors="white", linewidths=0.5)
    step = 4
    ax.quiver(xx[::step, ::step], yy[::step, ::step], -dt_dx[::step, ::step], -dt_dy[::step, ::step],
              color="C0", width=0.004)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title("定常温度分布と熱流束 $-\\nabla T$")
    fig.colorbar(filled, ax=ax, label="温度 $T$")
    fig.tight_layout()
    return fig


def report() -> None:
    """反復回数と、板の中心の温度を表示する（中心の正しい値は 0.25）."""
    t, count = solve()
    center = N // 2
    print(f"反復回数: {count}")
    print(f"中心の温度: {t[center, center]:.6f}")


def main() -> None:
    vc_plot.setup_font()
    report()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
