"""ストレンジアトラクタのフラクタル次元を、相関次元（グラスバーガー＝プロカッチャ法）で推定する.

アトラクタ上の N 個の点から、距離が r 未満の点の組の割合 C(r)（相関積分）を求める。
C(r) ∝ r^ν となるとき、指数 ν が相関次元である。

使い方: python ch10_correlation_dimension.py [--save DIR]
"""

from functools import cache

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import plot_util
from ch06_henon import henon_points
from ch06_lorenz import trajectory
from ch07_box_counting import estimate_dimension

Array = NDArray[np.float64]


def correlation_integral(points: Array, radii: Array, chunk: int = 500) -> Array:
    """各半径 r について、距離が r 未満の点の組の割合 C(r) を返す.

    すべての組の距離を一度に計算するとメモリーを多く使うので、chunk 個ずつに分けて計算する。
    """
    n = len(points)
    counts = np.zeros(len(radii))
    for start in range(0, n, chunk):
        block = points[start:start + chunk]
        d = np.sqrt(((block[:, None, :] - points[None, :, :]) ** 2).sum(axis=-1))
        # 自分自身との組（距離 0）と、同じ組を 2 回数えるのを避けるため、番号が大きい相手だけを数える
        idx = np.arange(start, start + len(block))
        mask = idx[:, None] < np.arange(n)[None, :]
        dist = np.sort(d[mask])
        counts += np.searchsorted(dist, radii)
    result: Array = counts / (n * (n - 1) / 2)
    return result


def fit_slope(radii: Array, c: Array, r_min: float, r_max: float) -> float:
    """r_min <= r <= r_max の範囲で、log C(r) を log r に対して直線で近似した傾きを返す."""
    use = (radii >= r_min) & (radii <= r_max) & (c > 0)
    slope, _ = np.polyfit(np.log(radii[use]), np.log(c[use]), 1)
    return float(slope)


def henon_sample(n: int = 4000) -> Array:
    """エノン・アトラクタ上の点を n 個返す（1 本の長い軌道から間引いて取る）."""
    points = henon_points(n_orbits=1, n_steps=n * 5, transient=1000)
    return points[::5]


def lorenz_sample(n: int = 4000) -> Array:
    """ローレンツ・アトラクタ上の点を n 個返す（時間間隔 0.1 ごとに取る）."""
    xs = trajectory((1.0, 1.0, 1.0), 0.01, n * 10, transient=1000)
    return xs[::10][:n]


CASES = [
    ("エノン写像", henon_sample, np.logspace(-3.0, 0.5, 30), (2e-3, 1e-1), 1.21),
    ("ローレンツ方程式", lorenz_sample, np.logspace(-1.0, 1.7, 30), (3e-1, 5.0), 2.05),
]


@cache
def results() -> list[tuple[Array, float]]:
    """CASES の順に、相関積分 C(r) の配列と、直線を当てはめた傾きを返す（2 回目以降は計算済みの値を返す）."""
    out = []
    for _, sample, radii, (r0, r1), _ in CASES:
        c = correlation_integral(sample(), radii)
        out.append((c, fit_slope(radii, c, r0, r1)))
    return out


def create_figures() -> dict[str, Figure]:
    """相関積分の両対数グラフ（correlation）を描く."""
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))
    for ax, (name, _, radii, (r0, r1), known), (c, slope) in zip(axes, CASES, results()):
        ax.loglog(radii, c, "o", markersize=4)
        use = (radii >= r0) & (radii <= r1)
        k = np.argmax(use)
        ax.loglog(radii[use], c[k] * (radii[use] / radii[k]) ** slope, color="C3",
                  label=f"当てはめた直線（傾き {slope:.2f}）")
        ax.set_xlabel("$r$")
        ax.set_ylabel("$C(r)$")
        ax.set_title(f"{name}（文献値 約 {known}）")
        ax.grid(True, which="both", color="0.9")
        ax.legend(loc="lower right")
    fig.tight_layout()
    return {"correlation": fig}


def report() -> None:
    """相関次元と、エノン・アトラクタのボックスカウント次元を表示する."""
    for (name, _, _, _, known), (_, slope) in zip(CASES, results()):
        print(f"{name}: 相関次元の推定値 {slope:.3f}（文献値 約 {known}）")
    points = henon_points()
    normalized = (points - points.min(axis=0)) / (points.max(axis=0) - points.min(axis=0)).max()
    sizes = np.asarray(2.0 ** -np.arange(3, 10), dtype=np.float64)
    dim, _ = estimate_dimension(normalized, sizes)
    print(f"エノン写像: ボックスカウント次元の推定値 {dim:.3f}（文献値 約 1.26）")


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures, report)


if __name__ == "__main__":
    main()
