"""ボックスカウント法でフラクタル次元を推定する.

平面を一辺 ε の正方形（ボックス）で区切り、図形と重なるボックスの数 N(ε) を数える。
N(ε) ∝ ε^(-D) となるとき、D がボックスカウント次元である。両対数グラフで
log N(ε) を log(1/ε) に対してプロットし、直線の傾きから D を推定する。

使い方: python ch07_box_counting.py [--save DIR]
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from numpy.typing import NDArray

import plot_util
from ch07_classic_fractals import cantor_intervals, koch_curve

Points = NDArray[np.float64]


def box_count(points: Points, eps: float) -> int:
    """点の集まり points（形は (n, 2)、座標は [0, 1] の範囲）と重なる、一辺 eps のボックスの数を返す."""
    boxes = np.floor(points / eps).astype(np.int64)
    # ボックスの番号の組 (i, j) を 1 つの整数にまとめてから、重複を除いて数える
    keys = boxes[:, 0] * (2 * round(1.0 / eps) + 1) + boxes[:, 1]
    return len(np.unique(keys))


def estimate_dimension(points: Points, sizes: NDArray[np.float64]) -> tuple[float, NDArray[np.float64]]:
    """ボックスの大きさ sizes ごとに数を数え、最小二乗法で直線を当てはめた傾きと、数の配列を返す."""
    counts = np.array([box_count(points, float(eps)) for eps in sizes], dtype=np.float64)
    slope, _ = np.polyfit(np.log(1.0 / sizes), np.log(counts), 1)
    return float(slope), counts


def koch_points(level: int = 8) -> Points:
    """コッホ曲線上の点を返す。折れ線の各線分の上に点を 4 個ずつ置く."""
    p = koch_curve(level)
    t = np.linspace(0.0, 1.0, 4, endpoint=False)
    pts = (p[:-1, None] + (p[1:] - p[:-1])[:, None] * t).ravel()
    return np.column_stack([pts.real, pts.imag + 0.3])


def sierpinski_points(k: int = 10) -> Points:
    """シェルピンスキーのギャスケット（直角三角形の形）上の点を返す.

    2^k × 2^k の格子点 (i, j) のうち、i と j の 2 進数で 1 の桁が重ならない
    （i & j == 0 となる）ものを残すと、ギャスケットの形になる。これはパスカルの
    三角形の各数を 2 で割った余りが 1 の位置と同じである。
    """
    n = 2**k
    i, j = np.meshgrid(np.arange(n), np.arange(n))
    mask = (i & j) == 0
    points: Points = np.column_stack([i[mask], j[mask]]).astype(np.float64) / n
    return points


def cantor_points(level: int = 13) -> Points:
    """カントール集合（を x 軸上に置いたもの）の近似として、level 段階目の区間の端点を返す."""
    ends = np.array(cantor_intervals(level)).ravel()
    points: Points = np.column_stack([ends, np.full(ends.shape, 0.5)])
    return points


SHAPES: list[tuple[str, float]] = [
    ("コッホ曲線", np.log(4.0) / np.log(3.0)),
    ("シェルピンスキーのギャスケット", np.log(3.0) / np.log(2.0)),
    ("カントール集合", np.log(2.0) / np.log(3.0)),
]


def shape_points() -> list[Points]:
    """SHAPES の順に、各図形の点の集まりを返す."""
    return [koch_points(), sierpinski_points(), cantor_points()]


SIZES: NDArray[np.float64] = np.asarray(2.0 ** -np.arange(2, 10), dtype=np.float64)


def create_figures() -> dict[str, Figure]:
    """コッホ曲線に重なるボックス（boxes）と、両対数グラフ（loglog）を作る."""
    points = koch_points(6)
    fig1, axes = plt.subplots(1, 2, figsize=(11.0, 3.6))
    for ax, eps in zip(axes, (1.0 / 8.0, 1.0 / 32.0)):
        boxes = np.unique(np.floor(points / eps).astype(np.int64), axis=0)
        for bx, by in boxes:
            ax.add_patch(Rectangle((bx * eps, by * eps), eps, eps, facecolor="#f6c9a8", edgecolor="C1", linewidth=0.5))
        ax.plot(points[:, 0], points[:, 1], ",", color="k")
        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(0.2, 0.65)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"$\\varepsilon = 1/{round(1.0 / eps)}$, $N(\\varepsilon) = {len(boxes)}$")
    fig1.tight_layout()

    fig2, ax2 = plt.subplots(figsize=(6.4, 4.8))
    for (name, theory), pts, marker in zip(SHAPES, shape_points(), "os^"):
        slope, counts = estimate_dimension(pts, SIZES)
        ax2.loglog(1.0 / SIZES, counts, marker=marker, linestyle="-",
                   label=f"{name}（推定 {slope:.3f}、理論値 {theory:.3f}）")
    ax2.set_xlabel("$1/\\varepsilon$")
    ax2.set_ylabel("$N(\\varepsilon)$")
    ax2.grid(True, which="both", color="0.9")
    ax2.legend(fontsize=9)
    fig2.tight_layout()
    return {"boxes": fig1, "loglog": fig2}


def report() -> None:
    """各図形の次元の推定値と理論値を表示する."""
    for (name, theory), pts in zip(SHAPES, shape_points()):
        slope, _ = estimate_dimension(pts, SIZES)
        print(f"{name}: 推定値 {slope:.4f}, 理論値 {theory:.4f}")


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures, report)


if __name__ == "__main__":
    main()
