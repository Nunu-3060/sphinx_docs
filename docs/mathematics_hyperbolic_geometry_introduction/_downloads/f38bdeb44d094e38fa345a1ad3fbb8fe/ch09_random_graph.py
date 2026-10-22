"""双曲平面上のランダムグラフ（Krioukov らのモデル）を作り、次数の分布を調べる.

半径 R の双曲円板の中に N 個の点をばらまき、双曲的な距離が R 未満の 2 点を辺で結ぶ。
点の偏角は一様に、原点からの距離 r は密度 alpha sinh(alpha r) / (cosh(alpha R) - 1) に従って選ぶ。

使い方: python ch09_random_graph.py
"""

import functools

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import hg_plot

N = 1000  # 点の数
R = 12.0  # 円板の半径
ALPHA = 0.75  # 点の密度の偏り. 次数の分布はべき指数 2 alpha + 1 のべき分布に近づく

FloatArray = NDArray[np.float64]
BoolArray = NDArray[np.bool_]


@functools.cache
def random_graph(seed: int = 0) -> tuple[FloatArray, FloatArray, BoolArray]:
    """点の極座標 (r, theta) と、隣接行列を返す."""
    rng = np.random.default_rng(seed)
    theta = rng.uniform(0.0, 2.0 * np.pi, N)
    u = rng.uniform(0.0, 1.0, N)
    r = np.arccosh(1.0 + u * (np.cosh(ALPHA * R) - 1.0)) / ALPHA  # 分布関数の逆関数で r を選ぶ
    # 極座標で表した 2 点の距離: cosh d = cosh r1 cosh r2 - sinh r1 sinh r2 cos(theta1 - theta2)
    cosh_d = (np.cosh(r)[:, None] * np.cosh(r)[None, :]
              - np.sinh(r)[:, None] * np.sinh(r)[None, :] * np.cos(theta[:, None] - theta[None, :]))
    adjacency = np.arccosh(np.maximum(cosh_d, 1.0)) < R
    np.fill_diagonal(adjacency, False)
    return r, theta, adjacency


def create_figure() -> Figure:
    """左にグラフ（半径を原点からの双曲的な距離とする極座標表示）、右に次数の分布を描く."""
    r, theta, adjacency = random_graph()
    degree = adjacency.sum(axis=1)
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.8))

    ax = axes[0]
    x, y = r * np.cos(theta), r * np.sin(theta)
    i, j = np.nonzero(np.triu(adjacency))
    for a, b in zip(i, j):
        ax.plot([x[a], x[b]], [y[a], y[b]], color="C0", linewidth=0.2, alpha=0.3)
    ax.scatter(x, y, s=2.0 + degree / 3.0, color="C3", zorder=3)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"双曲ランダムグラフ（$N = {N}$）")

    ax = axes[1]
    values, counts = np.unique(degree[degree > 0], return_counts=True)
    ccdf = np.array([np.sum(degree >= v) for v in values]) / N  # 次数が v 以上の点の割合
    ax.loglog(values, ccdf, "o", color="C0", markersize=3, label="シミュレーション")
    k = np.array([5.0, 200.0])
    gamma = 2.0 * ALPHA + 1.0
    ax.loglog(k, 0.6 * (k / 5.0) ** (1.0 - gamma), "--", color="C3",
              label=f"傾き $1 - \\gamma = {1.0 - gamma:.1f}$")
    ax.set_xlabel("次数 $k$")
    ax.set_ylabel("次数が $k$ 以上の点の割合")
    ax.grid(True, color="0.9", which="both")
    ax.legend()
    fig.tight_layout()
    return fig


def report() -> None:
    """平均次数、最大次数、次数の大きい点の位置を表示する."""
    r, _, adjacency = random_graph()
    degree = adjacency.sum(axis=1)
    print(f"点の数 {N}、辺の数 {int(adjacency.sum()) // 2}")
    print(f"平均次数 {degree.mean():.2f}、最大次数 {degree.max()}、次数 0 の点 {int(np.sum(degree == 0))} 個")
    order = np.argsort(-degree)[:5]
    print("次数の大きい 5 点")
    for idx in order:
        print(f"  次数 {degree[idx]:4d}、原点からの距離 r = {r[idx]:.2f}")
    print(f"全点の r の平均 {r.mean():.2f}")


def main() -> None:
    hg_plot.setup_font()
    report()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
