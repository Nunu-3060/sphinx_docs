"""3D グラフィックスの座標変換: モデル変換、ビュー変換、透視投影.

立方体の頂点を同次座標 (x, y, z, 1) で表し、4 行 4 列の行列を
掛けて画面の座標に変換する。ここでは簡単のため、カメラは原点にあり、
z 軸の正の向きを見ているとする。透視投影の後、第 4 成分 w で割ると
遠くのものほど小さく描かれる。

使い方: python ch14_projection_3d.py
"""

from itertools import combinations, product

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from numpy.typing import NDArray

import la_plot

Matrix = NDArray[np.float64]


def rotation_x(degrees: float) -> Matrix:
    """x 軸のまわりの回転（同次座標）."""
    c, s = np.cos(np.radians(degrees)), np.sin(np.radians(degrees))
    return np.array([[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]], dtype=float)


def rotation_y(degrees: float) -> Matrix:
    """y 軸のまわりの回転（同次座標）."""
    c, s = np.cos(np.radians(degrees)), np.sin(np.radians(degrees))
    return np.array([[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]], dtype=float)


def translation(tx: float, ty: float, tz: float) -> Matrix:
    """平行移動（同次座標）."""
    m = np.eye(4)
    m[:3, 3] = [tx, ty, tz]
    return m


def perspective(focal: float) -> Matrix:
    """透視投影. 変換後の w 成分が元の z になり、w で割ると (f x / z, f y / z) になる."""
    return np.array([[focal, 0, 0, 0], [0, focal, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0]], dtype=float)


def cube() -> tuple[Matrix, list[tuple[int, int]]]:
    """1 辺の長さ 2 の立方体の頂点（4 行 8 列の同次座標）と辺のリストを返す."""
    corners = np.array(list(product((-1.0, 1.0), repeat=3))).T
    vertices = np.vstack([corners, np.ones(8)])
    # 座標が 1 つだけ異なる頂点の組が辺になる
    edges = [(i, j) for i, j in combinations(range(8), 2)
             if np.sum(corners[:, i] != corners[:, j]) == 1]
    return vertices, edges


MODEL = rotation_x(20) @ rotation_y(30)  # y 軸のまわりに回した後、x 軸のまわりに回す


def project(distance: float, focal: float = 2.0) -> Matrix:
    """立方体を、カメラから distance だけ離して透視投影した 2 次元の座標を返す."""
    vertices, _ = cube()
    clip = perspective(focal) @ translation(0, 0, distance) @ MODEL @ vertices
    screen: Matrix = clip[:2] / clip[3]  # w で割る（透視除算）
    return screen


def report() -> None:
    """合成した変換行列と、頂点 (1, 1, 1) の変換結果を表示する."""
    m = perspective(2.0) @ translation(0, 0, 5.0) @ MODEL
    p = np.array([1.0, 1.0, 1.0, 1.0])
    with np.printoptions(precision=4, suppress=True):
        print("P V M =")
        print(m)
        clip = m @ p
        print("(1, 1, 1, 1) の変換結果 =", clip)
        print("w で割った画面の座標 =", clip[:2] / clip[3])


def create_figure() -> Figure:
    """平行投影と、2 つの距離からの透視投影で立方体を描く."""
    vertices, edges = cube()
    orthographic = (MODEL @ vertices)[:2]  # z を捨てるだけの平行投影
    views = [
        ("平行投影", orthographic),
        ("透視投影（距離 5）", project(5.0)),
        ("透視投影（距離 2.5）", project(2.5)),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.8))
    for ax, (title, points) in zip(axes, views):
        for i, j in edges:
            ax.plot(points[0, [i, j]], points[1, [i, j]], color="C0")
        ax.plot(points[0], points[1], "o", color="C0", markersize=3)
        # 投影の方法で図の大きさが変わるので、図ごとに範囲を決める
        limit = 1.2 * np.abs(points).max()
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title)
    fig.tight_layout()
    return fig


def main() -> None:
    report()
    la_plot.setup_font()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
