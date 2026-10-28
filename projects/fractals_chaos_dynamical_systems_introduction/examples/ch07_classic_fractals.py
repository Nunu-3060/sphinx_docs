"""古典的なフラクタル: カントール集合、コッホ曲線、シェルピンスキーのギャスケット.

どれも「図形の一部を、縮小した自分自身の複製で置き換える」操作を繰り返して作る。

使い方: python ch07_classic_fractals.py [--save DIR]
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Polygon
from numpy.typing import NDArray

import plot_util

Points = NDArray[np.complex128]


def cantor_intervals(level: int) -> list[tuple[float, float]]:
    """カントール集合を作る途中の、level 段階目の区間の一覧を返す."""
    intervals = [(0.0, 1.0)]
    for _ in range(level):
        next_intervals = []
        for a, b in intervals:
            third = (b - a) / 3.0
            next_intervals += [(a, a + third), (b - third, b)]  # 真ん中の 1/3 を取り除く
        intervals = next_intervals
    return intervals


def koch_curve(level: int, start: complex = 0.0, end: complex = 1.0) -> Points:
    """コッホ曲線の level 段階目の折れ線の頂点を、複素数の配列で返す.

    線分を 3 等分し、真ん中の部分を、正三角形の 2 辺で置き換える。
    """
    points = np.array([start, end])
    rotate = np.exp(1j * np.pi / 3.0)  # 60 度の回転
    for _ in range(level):
        a, b = points[:-1], points[1:]
        d = (b - a) / 3.0
        p1 = a + d
        peak = p1 + d * rotate
        p2 = a + 2.0 * d
        new = np.stack([a, p1, peak, p2], axis=1).ravel()
        points = np.append(new, points[-1])
    return points


def koch_snowflake(level: int) -> Points:
    """正三角形の 3 辺をコッホ曲線で置き換えたコッホ雪片の頂点を返す."""
    corners = [np.exp(1j * (np.pi / 2.0 - 2.0 * np.pi * k / 3.0)) for k in range(4)]
    parts = [koch_curve(level, corners[k], corners[k + 1])[:-1] for k in range(3)]
    return np.concatenate(parts + [parts[0][:1]])


def sierpinski_triangles(level: int) -> list[Points]:
    """シェルピンスキーのギャスケットの level 段階目に残る三角形（頂点 3 つ）の一覧を返す."""
    triangles = [np.array([0.0, 1.0, 0.5 + 1j * np.sqrt(3.0) / 2.0])]
    for _ in range(level):
        next_triangles = []
        for t in triangles:
            a, b, c = t
            ab, bc, ca = (a + b) / 2.0, (b + c) / 2.0, (c + a) / 2.0
            next_triangles += [np.array([a, ab, ca]), np.array([ab, b, bc]), np.array([ca, bc, c])]
        triangles = next_triangles
    return triangles


def create_figures() -> dict[str, Figure]:
    """カントール集合（cantor）、コッホ曲線と雪片（koch）、ギャスケット（sierpinski）の図を作る."""
    fig1, ax1 = plt.subplots(figsize=(9.0, 3.2))
    for level in range(7):
        for a, b in cantor_intervals(level):
            ax1.plot([a, b], [-level, -level], color="k", linewidth=5, solid_capstyle="butt")
    ax1.set_yticks(-np.arange(7), [f"{k} 段階" for k in range(7)])
    ax1.set_xlim(-0.02, 1.02)
    ax1.set_ylim(-6.6, 0.6)
    for side in ("top", "right", "left"):
        ax1.spines[side].set_visible(False)
    fig1.tight_layout()

    fig2, axes2 = plt.subplots(1, 4, figsize=(14.0, 3.4))
    for ax, level in zip(axes2[:3], (0, 1, 4)):
        p = koch_curve(level)
        ax.plot(p.real, p.imag, color="k", linewidth=0.8)
        ax.set_title(f"{level} 段階")
        ax.set_xlim(-0.02, 1.02)
        ax.set_ylim(-0.1, 0.4)
    snow = koch_snowflake(5)
    axes2[3].fill(snow.real, snow.imag, facecolor="#cfe3f5", edgecolor="k", linewidth=0.5)
    axes2[3].set_title("コッホ雪片（5 段階）")
    for ax in axes2:
        ax.set_aspect("equal")
        ax.axis("off")
    fig2.tight_layout()

    fig3, axes3 = plt.subplots(1, 4, figsize=(14.0, 3.6))
    for ax, level in zip(axes3, (0, 1, 2, 6)):
        for t in sierpinski_triangles(level):
            ax.add_patch(Polygon(np.column_stack([t.real, t.imag]), closed=True, facecolor="k", edgecolor="none"))
        ax.set_xlim(-0.02, 1.02)
        ax.set_ylim(-0.02, 0.9)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(f"{level} 段階")
    fig3.tight_layout()
    return {"cantor": fig1, "koch": fig2, "sierpinski": fig3}


def report() -> None:
    """コッホ雪片の周の長さと面積を、段階ごとに表示する（最初の正三角形の 1 辺を 1 とする）."""
    print("段階  周の長さ    面積（最初の正三角形との比）")
    for level in (0, 1, 2, 3, 5, 10, 20):
        perimeter = 3.0 * (4.0 / 3.0) ** level
        # 段階 k で追加される小三角形は 3 * 4^(k-1) 個で、それぞれの面積は元の 1/9^k
        area = 1.0 + sum(3.0 * 4.0 ** (k - 1) / 9.0**k for k in range(1, level + 1))
        print(f"{level:4d}  {perimeter:10.3f}  {area:.6f}")
    print("面積の極限: 8/5 = 1.6")


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures, report)


if __name__ == "__main__":
    main()
