"""中点変位法で、フラクタルな地形（山の稜線と地形図）を作る.

線分の中点を、ランダムな量だけ上下にずらす操作を、区間を半分にしながら繰り返す。
ずらす量の大きさを、区間が半分になるたびに 2^(-H) 倍にする。H（ハースト指数、0 < H < 1）が
小さいほど、ギザギザの激しい（フラクタル次元の大きい）形になる。

使い方: python ch11_terrain.py [--save DIR]
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LightSource
from matplotlib.figure import Figure
from numpy.typing import NDArray

import plot_util

Array = NDArray[np.float64]


def midpoint_displacement_1d(levels: int, hurst: float, rng: np.random.Generator) -> Array:
    """長さ 2^levels + 1 の稜線（高さの列）を作る."""
    n = 2**levels
    h = np.zeros(n + 1)
    scale = 1.0
    step = n
    while step > 1:
        half = step // 2
        mid = (h[:-1:step] + h[step::step]) / 2.0  # 各区間の両端の平均
        h[half::step] = mid + scale * rng.normal(size=mid.shape)
        scale *= 2.0 ** (-hurst)
        step = half
    return h


def diamond_square(levels: int, hurst: float, rng: np.random.Generator) -> Array:
    """ダイヤモンド・スクエア法（中点変位法の 2 次元版）で、(2^levels + 1) 四方の高さの地図を作る.

    1. ダイヤモンド段階: 正方形の中心に、4 隅の平均にランダムな量を加えた高さを置く
    2. スクエア段階: 辺の中点に、周りの 4 点（端では 3 点）の平均にランダムな量を加えた高さを置く
    """
    n = 2**levels
    h = np.zeros((n + 1, n + 1))
    scale = 1.0
    step = n
    while step > 1:
        half = step // 2
        corners = (h[:-1:step, :-1:step] + h[:-1:step, step::step]
                   + h[step::step, :-1:step] + h[step::step, step::step])
        h[half::step, half::step] = corners / 4.0 + scale * rng.normal(size=corners.shape)
        for row_start, col_start in ((0, half), (half, 0)):
            rows = np.arange(row_start, n + 1, step)
            cols = np.arange(col_start, n + 1, step)
            r, c = np.meshgrid(rows, cols, indexing="ij")
            total = np.zeros(r.shape)
            count = np.zeros(r.shape)
            for dr, dc in ((-half, 0), (half, 0), (0, -half), (0, half)):
                rr, cc = r + dr, c + dc
                ok = (rr >= 0) & (rr <= n) & (cc >= 0) & (cc <= n)
                total[ok] += h[rr[ok], cc[ok]]
                count[ok] += 1
            h[r, c] = total / count + scale * rng.normal(size=r.shape)
        scale *= 2.0 ** (-hurst)
        step = half
    return h


def create_figures() -> dict[str, Figure]:
    """ハースト指数の違う稜線（profiles）と、地形図（terrain）を作る."""
    fig1, ax1 = plt.subplots(figsize=(10.0, 4.0))
    x = np.linspace(0.0, 1.0, 2**10 + 1)
    for i, hurst in enumerate((0.2, 0.5, 0.8)):
        h = midpoint_displacement_1d(10, hurst, np.random.default_rng(7))
        ax1.plot(x, h - h.mean() + 3.0 * (2 - i), linewidth=0.8,
                 label=f"$H = {hurst}$（次元 {2.0 - hurst:.1f}）")
    ax1.set_yticks([])
    ax1.set_xlabel("位置")
    ax1.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0))
    fig1.tight_layout()

    fig2, axes = plt.subplots(1, 2, figsize=(11.0, 5.2))
    for ax, hurst in zip(axes, (0.4, 0.8)):
        h = diamond_square(8, hurst, np.random.default_rng(11))
        h = (h - h.min()) / (h.max() - h.min())
        # 海面より下は平らにし、陰影を付けて立体的に見せる
        land = np.maximum(h, 0.4)
        shade = LightSource(azdeg=315, altdeg=45).shade(land, cmap=plt.get_cmap("terrain"), vert_exag=40.0,
                                                        blend_mode="soft", vmin=0.25, vmax=1.0)
        ax.imshow(shade)
        ax.set_title(f"$H = {hurst}$")
        ax.axis("off")
    fig2.tight_layout()
    return {"profiles": fig1, "terrain": fig2}


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures)


if __name__ == "__main__":
    main()
