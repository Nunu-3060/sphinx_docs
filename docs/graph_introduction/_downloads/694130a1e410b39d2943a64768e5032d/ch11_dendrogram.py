"""デンドログラム: 階層クラスタリングの結果を描く.

平面上の 10 個の点を、群平均法で階層的にまとめる。まとめた順序と
距離を、左に点の散布図、右にデンドログラム（樹形図）として描く。

使い方: python ch11_dendrogram.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

import jpfont

# 結合の記録: (結合したクラスター a, クラスター b, 結合したときの距離)
# 最初の点の番号は 0 から n - 1、k 回目の結合で作られたクラスターは n + k
Merge = tuple[int, int, float]

POINTS = np.array([
    [1.0, 1.0], [1.5, 1.2], [1.2, 1.8], [0.6, 1.5],   # 左下のまとまり
    [4.0, 4.0], [4.6, 4.3], [4.2, 4.8],               # 右上のまとまり
    [4.5, 1.0], [5.0, 1.4], [5.4, 0.8],               # 右下のまとまり
])
LABELS = [f"P{i}" for i in range(len(POINTS))]
CUT_HEIGHT = 2.5  # この高さで切ると 3 つのクラスターに分かれる


def average_linkage(points: np.ndarray) -> list[Merge]:
    """群平均法でクラスターを 1 つになるまで結合し、結合の記録を返す."""
    distances = np.linalg.norm(points[:, np.newaxis] - points, axis=2)
    members = {i: [i] for i in range(len(points))}
    merges: list[Merge] = []
    while len(members) > 1:
        ids = list(members)
        best: Merge | None = None
        for i, a in enumerate(ids):
            for b in ids[i + 1:]:
                # クラスター間の距離: すべての点の組の距離の平均
                d = float(distances[np.ix_(members[a], members[b])].mean())
                if best is None or d < best[2]:
                    best = (a, b, d)
        assert best is not None
        a, b, d = best
        merges.append(best)
        members[len(points) + len(merges) - 1] = (members.pop(a)
                                                  + members.pop(b))
    return merges


def draw_dendrogram(ax: Axes, merges: list[Merge], labels: list[str]) -> None:
    """結合の記録からデンドログラムを描く."""
    n = len(labels)
    children = {n + k: (a, b) for k, (a, b, _) in enumerate(merges)}

    # 線が交差しないよう、木を左からたどった順に葉（元の点）を並べる
    order: list[int] = []

    def visit(node: int) -> None:
        if node < n:
            order.append(node)
            return
        left, right = children[node]
        visit(left)
        visit(right)

    visit(n + len(merges) - 1)
    x = {leaf: float(position) for position, leaf in enumerate(order)}
    y = {leaf: 0.0 for leaf in order}
    # 結合の順に、2 つの子を「コ」の字を下に向けた線でつなぐ
    for k, (a, b, height) in enumerate(merges):
        ax.plot([x[a], x[a], x[b], x[b]], [y[a], height, height, y[b]],
                color="C0")
        x[n + k] = (x[a] + x[b]) / 2
        y[n + k] = height
    ax.set_xticks(range(n), [labels[leaf] for leaf in order])


def create_figure() -> Figure:
    """点の散布図とデンドログラムを並べて描く."""
    merges = average_linkage(POINTS)
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(10, 3.8))

    ax_left.scatter(POINTS[:, 0], POINTS[:, 1], color="C0")
    for label, (px, py) in zip(LABELS, POINTS):
        ax_left.annotate(label, (px, py), xytext=(5, 5),
                         textcoords="offset points")
    ax_left.set_aspect("equal")
    ax_left.set_xlim(0, 6)
    ax_left.set_ylim(0, 5.5)
    ax_left.set_title("10 個の点")

    draw_dendrogram(ax_right, merges, LABELS)
    ax_right.axhline(CUT_HEIGHT, color="gray", linestyle="--")
    ax_right.set_ylabel("結合したときの距離")
    ax_right.set_title("デンドログラム（群平均法）")
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    for a, b, d in average_linkage(POINTS):
        print(f"クラスター {a} と {b} を距離 {d:.2f} で結合")
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
