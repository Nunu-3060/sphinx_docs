"""第 9 章「陰関数と体積表現」: 等値面のメッシュ化の図を作る。

* marching_squares.png: 2 次元の格子での等高線の取り出し（マーチング・スクエア法）と 16 通りの場合分け
* tetrahedra.png: 立方体を 6 個の四面体に分ける方法と、四面体の中で作る面
* metaballs.png: メタボールを格子の細かさを変えてメッシュ化したもの
* noise_cave.png: 3 次元ノイズの密度場から作った、張り出しと洞窟のある地形のブロック
"""

from __future__ import annotations

from typing import Any

import numpy as np

from common import FloatArray, output_dir, save_figure, setup_matplotlib
from marching_tetrahedra import CORNERS, TETRAHEDRA, marching_tetrahedra
from mesh import draw_mesh, fit_view
from noise import fbm3
from sdf3d import grid3, op_intersection, op_subtraction, sd_box


def blob_field_2d(x: FloatArray, y: FloatArray) -> FloatArray:
    """マーチング・スクエア法の説明に使う 2 次元の場（2 つの円をなめらかにつないだ形。負が内側）。"""
    a = np.hypot(x - 3.2, y - 3.0) - 2.0
    b = np.hypot(x - 6.2, y - 4.0) - 1.4
    h = np.clip(0.5 + 0.5 * (b - a) / 1.5, 0.0, 1.0)
    result: FloatArray = b + (a - b) * h - 1.5 * h * (1.0 - h)
    return result


def draw_marching_squares(file_name: str) -> None:
    import matplotlib.pyplot as plt

    figure = plt.figure(figsize=(12, 4.6))
    grid = figure.add_gridspec(1, 2, width_ratios=[1.15, 1])

    # 左: 粗い格子で場を調べ、各辺上の 0 の位置を直線でつなぐ
    ax = figure.add_subplot(grid[0])
    xs = np.arange(0, 10)
    ys = np.arange(0, 8)
    gx, gy = np.meshgrid(xs.astype(np.float64), ys.astype(np.float64))
    values = blob_field_2d(gx, gy)
    fine_x, fine_y = np.meshgrid(np.linspace(0, 9, 300), np.linspace(0, 7, 240))
    ax.contour(fine_x, fine_y, blob_field_2d(fine_x, fine_y), levels=[0.0], colors="#999999", linestyles="--")
    # matplotlib の contour は、格子の各セルの辺上で線形補間した点を結ぶ（マーチング・スクエア法と同じ）。
    ax.contour(gx, gy, values, levels=[0.0], colors="#c44e52", linewidths=2.0)
    for x in xs:
        ax.axvline(float(x), color="#dddddd", linewidth=0.8, zorder=0)
    for y in ys:
        ax.axhline(float(y), color="#dddddd", linewidth=0.8, zorder=0)
    inside = values < 0.0
    ax.scatter(gx[inside], gy[inside], s=30, color="#4c72b0", zorder=3, label="内側（値 < 0）")
    ax.scatter(gx[~inside], gy[~inside], s=30, facecolor="white", edgecolor="#4c72b0", zorder=3,
               label="外側（値 ≥ 0）")
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(loc="upper right", fontsize=8, framealpha=1.0)
    ax.set_title("格子点の内外と、取り出した線（赤）。破線は本当の境界", fontsize=10)

    # 右: 4 つの角の内外の 16 通りの組み合わせと、引く線分
    ax = figure.add_subplot(grid[1])
    corners = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])
    for code in range(16):
        ox, oy = (code % 4) * 1.6, (3 - code // 4) * 1.6
        square = corners + [ox, oy]
        ax.plot(*np.vstack([square, square[:1]]).T, color="#888888", linewidth=0.8)
        crossings = []
        for edge in range(4):
            a, b = edge, (edge + 1) % 4
            if (code >> a & 1) != (code >> b & 1):
                crossings.append((square[a] + square[b]) / 2.0)
        if len(crossings) == 2:
            ax.plot(*np.array(crossings).T, color="#c44e52", linewidth=2.0)
        elif len(crossings) == 4:  # 対角の 2 角だけが内側: 線の引き方が 2 通りある
            ax.plot(*np.array(crossings[:2]).T, color="#c44e52", linewidth=2.0)
            ax.plot(*np.array(crossings[2:]).T, color="#c44e52", linewidth=2.0)
            ax.text(ox + 0.5, oy - 0.12, "曖昧", ha="center", va="top", fontsize=8, color="#c44e52")
        for corner in range(4):
            filled = code >> corner & 1
            ax.scatter(square[corner][0], square[corner][1], s=28, zorder=3, color="#4c72b0" if filled else "white",
                       edgecolor="#4c72b0")
        ax.text(ox - 0.12, oy + 1.12, str(code), fontsize=8, color="#555555")
    ax.set_xlim(-0.3, 6.2)
    ax.set_ylim(-0.4, 6.2)
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.set_title("4 つの角の内外の 16 通りと、セルに引く線分", fontsize=10)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_tetrahedra(file_name: str) -> None:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    figure = plt.figure(figsize=(12, 4.0))
    cube_edges = [(a, b) for a in range(8) for b in range(a + 1, 8) if bin(a ^ b).count("1") == 1]

    def draw_cube(ax: Any) -> None:
        for a, b in cube_edges:
            ax.plot(*CORNERS[[a, b]].T, color="#555555", linewidth=1.0)
        ax.set_box_aspect((1.0, 1.0, 1.0))
        ax.view_init(elev=20.0, azim=-62.0)
        ax.set_axis_off()

    def faces_of(tetra: Any) -> list[Any]:
        points = CORNERS[tetra].astype(np.float64)
        return [points[[i, j, k]] for i, j, k in [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]]

    # 左: 立方体の角の番号と、四面体の辺になる対角線。四面体 (0, 1, 3, 7) に色を付ける
    ax: Any = figure.add_subplot(1, 3, 1, projection="3d")
    draw_cube(ax)
    diagonals = {(min(a, b), max(a, b)) for tetra in TETRAHEDRA for a in tetra for b in tetra if a != b}
    for a, b in sorted(diagonals - set(cube_edges)):
        main = (a, b) == (0, 7)
        ax.plot(*CORNERS[[a, b]].T, color="#c44e52" if main else "#999999", linewidth=2.0 if main else 0.8,
                linestyle="-" if main else "--")
    ax.add_collection3d(Poly3DCollection(faces_of(TETRAHEDRA[0]), facecolors="#4c72b0", alpha=0.35,
                                         edgecolors="#4c72b0"))
    for corner in range(8):
        ax.text(*(CORNERS[corner] * 1.12 - 0.06), str(corner), fontsize=11, color="#333333")
    ax.set_title("角の番号と四面体の辺（赤: 対角線 0–7）\n色付きは 6 個のうちの 1 個 (0, 1, 3, 7)", fontsize=10)

    # 中・右: 四面体 1 個の中で作る面（内側の頂点が 1 個の場合と 2 個の場合）
    tetra = TETRAHEDRA[0]
    points = CORNERS[tetra].astype(np.float64)
    for column, inside, title in [(2, [0], "内側の頂点が 1 個: 三角形 1 枚"), (3, [0, 1], "内側の頂点が 2 個: 四角形（三角形 2 枚）")]:
        ax = figure.add_subplot(1, 3, column, projection="3d")
        draw_cube(ax)
        for i in range(4):
            for j in range(i + 1, 4):
                ax.plot(*points[[i, j]].T, color="#4c72b0", linewidth=1.5)
        outside = [i for i in range(4) if i not in inside]
        crossing = [(points[i] + points[o]) / 2.0 for i in inside for o in outside]
        if len(crossing) == 4:
            crossing = [crossing[0], crossing[1], crossing[3], crossing[2]]  # 四角形の周を順にたどる
        ax.add_collection3d(Poly3DCollection([np.array(crossing)], facecolors="#c44e52", alpha=0.6,
                                             edgecolors="#c44e52"))
        for i in range(4):
            filled = i in inside
            ax.scatter(*points[i], s=40, color="#4c72b0" if filled else "white", edgecolor="#4c72b0",
                       depthshade=False)
        ax.set_title(title, fontsize=10)
    figure.subplots_adjust(left=0.0, right=1.0, top=0.88, bottom=0.0, wspace=0.0)
    save_figure(figure, output_dir(__file__) / file_name)


def metaball_field(points: FloatArray) -> FloatArray:
    """メタボールの場。各球の中心から半径 R までの範囲に、中心で 1、境界で 0 になる山を置いて足し合わせる。"""
    centers = np.array([[-0.45, -0.1, 0.0], [0.35, 0.25, 0.15], [0.15, -0.45, -0.25], [0.0, 0.3, -0.45]])
    radii = np.array([0.85, 0.75, 0.6, 0.55])
    total = np.zeros(points.shape[:-1])
    for center, radius in zip(centers, radii):
        r2 = np.sum((points - center) ** 2, axis=-1) / radius ** 2
        total += np.where(r2 < 1.0, (1.0 - r2) ** 3, 0.0)
    return total


def draw_metaballs(file_name: str) -> None:
    import matplotlib.pyplot as plt

    threshold = 0.3  # 場の値がこれ以上の所を内側とする
    figure = plt.figure(figsize=(12, 4.0))
    for index, resolution in enumerate([10, 20, 56]):
        points = grid3((-1.2, -1.2, -1.2), (1.2, 1.2, 1.2), (resolution,) * 3)
        # marching_tetrahedra は値が iso より小さい側を内側とするので、符号を反転して渡す。
        mesh = marching_tetrahedra(threshold - metaball_field(points), points)
        ax: Any = figure.add_subplot(1, 3, index + 1, projection="3d")
        draw_mesh(ax, mesh, color=(0.55, 0.75, 0.62), edgecolor="#2f4f3a" if resolution < 30 else None,
                  linewidth=0.3)
        fit_view(ax, [mesh], elev=20.0, azim=-60.0)
        ax.set_title(f"格子 {resolution}³（三角形 {len(mesh.faces)} 枚）", fontsize=10)
    figure.subplots_adjust(left=0.0, right=1.0, top=0.92, bottom=0.0, wspace=0.0)
    save_figure(figure, output_dir(__file__) / file_name)


def cave_density(points: FloatArray) -> FloatArray:
    """洞窟のある地形の場（負が岩）。

    高さとともに増える項に 3 次元ノイズを足して、張り出しのある地面を作る。さらに、
    2 つのノイズ n1, n2 がどちらも 0 に近い所（2 枚の曲面が交わる線の周り）を
    管状にくり抜いて洞窟にし、最後に横長のブロックで切り取る。
    """
    x, y, z = points[..., 0], points[..., 1], points[..., 2]
    ground = (z - 0.62) * 2.0  # 高さ 0.62 より下ほど岩になりやすい
    rock = ground + 0.7 * fbm3(x * 1.8, y * 1.8, z * 1.8, octaves=4, seed=7)
    n1 = fbm3(x * 1.5, y * 1.5, z * 1.5, octaves=2, seed=11)
    n2 = fbm3(x * 1.5, y * 1.5, z * 1.5, octaves=2, seed=12)
    tunnel = np.maximum(np.abs(n1), np.abs(n2)) - 0.09  # 負なら洞窟の中
    block = sd_box(points - np.array([1.0, 0.6, 0.5]), (0.98, 0.58, 0.48))
    return op_intersection(op_subtraction(rock, tunnel), block)


def draw_noise_cave(file_name: str) -> None:
    import matplotlib.pyplot as plt

    points = grid3((0.0, 0.0, 0.0), (2.0, 1.2, 1.0), (90, 54, 45))
    density = cave_density(points)
    mesh = marching_tetrahedra(density, points)

    # 上を向いた面は草、それ以外は岩の色にする。
    normals = mesh.face_normals()
    grass = np.array([0.45, 0.68, 0.35])
    rock = np.array([0.62, 0.55, 0.48])
    upward = np.clip((normals[:, 2] - 0.55) / 0.25, 0.0, 1.0)[:, None]
    colors = rock + (grass - rock) * upward

    figure = plt.figure(figsize=(12, 4.4))
    grid = figure.add_gridspec(1, 2, width_ratios=[1.6, 1])
    ax: Any = figure.add_subplot(grid[0], projection="3d")
    draw_mesh(ax, mesh, color=colors)
    ax.set_xlim(0.0, 2.0)
    ax.set_ylim(0.0, 1.2)
    ax.set_zlim(0.0, 1.0)
    ax.set_box_aspect((2.0, 1.2, 1.0), zoom=1.0)
    ax.view_init(elev=22.0, azim=-62.0)
    ax.set_axis_off()
    ax.set_title(f"メッシュ化した地形（三角形 {len(mesh.faces)} 枚）", fontsize=10)

    ax2 = figure.add_subplot(grid[1])
    section = density[:, 27, :].T  # y = 0.6 の断面（横軸 x、縦軸 z）
    ax2.imshow(section, origin="lower", extent=(0.0, 2.0, 0.0, 1.0), cmap="RdBu", vmin=-1.0, vmax=1.0)
    ax2.contour(np.linspace(0.0, 2.0, 90), np.linspace(0.0, 1.0, 45), section, levels=[0.0], colors="black",
                linewidths=1.2)
    ax2.set_xlabel("x")
    ax2.set_ylabel("z（高さ）")
    ax2.set_title("y = 0.6 の断面の密度（赤: 岩、青: 空気）", fontsize=10)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_marching_squares("marching_squares.png")
    draw_tetrahedra("tetrahedra.png")
    draw_metaballs("metaballs.png")
    draw_noise_cave("noise_cave.png")


if __name__ == "__main__":
    main()
