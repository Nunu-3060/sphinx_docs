"""第 6 章「メッシュの基礎と生成」: メッシュの表現と基本形状の図を作る。

* mesh_buffers.png: 頂点配列とインデックス配列、頂点の並び順（ワインディング）と表裏
* normals_2d.png: 面の法線と頂点の法線（断面で見た図）
* shading.png: フラットシェーディングとスムーズシェーディング、ハードエッジのための頂点の分割
* uv_mapping.png: UV 座標の展開図と、チェッカー模様を貼った球と円柱
* primitives.png: 手続きで作った格子・円柱・球（ワイヤーフレームと陰影付き）
* sphere_resolution.png: 分割数を変えた球
"""

from __future__ import annotations

from typing import Any

import numpy as np

from common import FloatArray, output_dir, save_figure, setup_matplotlib
from mesh import Mesh, draw_mesh, fit_view
from meshgen import (cylinder, draw_faces, grid_faces, plane, shaded_colors, subdivide_smooth, uv_sphere)

BLUE = (0.62, 0.72, 0.88)
ORANGE = (0.95, 0.70, 0.50)

# 図 mesh_buffers の小さなメッシュ: 2 × 1 マスの格子を 4 枚の三角形に分けたもの
SMALL_VERTICES = np.array([[0, 0, 0], [1, 0, 0], [2, 0, 0], [0, 1, 0], [1, 1, 0], [2, 1, 0]], dtype=np.float64)
SMALL_FACES = np.array([[0, 1, 4], [0, 4, 3], [1, 2, 5], [1, 5, 4]], dtype=np.int64)


def draw_turn_arrow(ax: Any, center: FloatArray, radius: float, clockwise: bool, color: str) -> None:
    """三角形の中に、頂点の並び順の向きを表す円弧の矢印を描く。"""
    from matplotlib.patches import FancyArrowPatch

    start, end = (np.deg2rad(200.0), np.deg2rad(-80.0)) if clockwise else (np.deg2rad(-20.0), np.deg2rad(260.0))
    angles = np.linspace(start, end, 30)
    xs = center[0] + radius * np.cos(angles)
    ys = center[1] + radius * np.sin(angles)
    ax.plot(xs[:-1], ys[:-1], color=color, linewidth=1.2)
    ax.add_patch(FancyArrowPatch((xs[-2], ys[-2]), (xs[-1], ys[-1]), arrowstyle="-|>", mutation_scale=10,
                                 color=color))


def draw_buffers(file_name: str) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 3, figsize=(12, 3.6), gridspec_kw={"width_ratios": [1.5, 1.1, 1.3]})

    # 左: メッシュの図。頂点番号を丸で、三角形の番号と並び順を矢印で示す。
    ax = axes[0]
    for k, face in enumerate(SMALL_FACES):
        triangle = SMALL_VERTICES[face, :2]
        ax.fill(triangle[:, 0], triangle[:, 1], color=BLUE, alpha=0.35 + 0.1 * (k % 2), edgecolor="#4c72b0")
        center = triangle.mean(axis=0)
        draw_turn_arrow(ax, center, 0.11, clockwise=False, color="#c44e52")
        ax.text(center[0], center[1], f"面{k}", ha="center", va="center", fontsize=8)
    for k, (x, y, _) in enumerate(SMALL_VERTICES):
        ax.scatter([x], [y], s=260, color="white", edgecolor="#333333", zorder=3)
        ax.text(x, y, str(k), ha="center", va="center", fontsize=10, zorder=4)
    ax.set_xlim(-0.3, 2.3)
    ax.set_ylim(-0.3, 1.3)
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.set_title("メッシュ（○ は頂点番号、矢印は並び順）", fontsize=10)

    # 中央と右: 頂点配列とインデックス配列を表として示す。
    tables = [
        ("頂点配列 vertices", ["番号", "x", "y", "z"],
         [[str(k)] + [f"{value:g}" for value in vertex] for k, vertex in enumerate(SMALL_VERTICES)]),
        ("インデックス配列 faces", ["面", "頂点番号"],
         [[f"面{k}", ", ".join(str(i) for i in face)] for k, face in enumerate(SMALL_FACES)]),
    ]
    for ax, (title, header, rows) in zip(axes[1:], tables):
        ax.set_axis_off()
        table = ax.table(cellText=rows, colLabels=header, loc="center", cellLoc="center")
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.0, 1.4)
        for (row, _), cell in table.get_celld().items():
            if row == 0:
                cell.set_facecolor("#eef3fb")
        ax.set_title(title, fontsize=10)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_winding(file_name: str) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 2, figsize=(7.5, 3.2))
    triangle = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, 0.85]])
    cases = [("(0, 1, 2): 反時計回り → 表", [0, 1, 2], False, "法線は手前向き ⊙"),
             ("(0, 2, 1): 時計回り → 裏", [0, 2, 1], True, "法線は奥向き ⊗")]
    for ax, (title, order, clockwise, note) in zip(axes, cases):
        color = BLUE if not clockwise else (0.85, 0.85, 0.85)
        ax.fill(triangle[:, 0], triangle[:, 1], color=color, edgecolor="#4c72b0")
        for rank, k in enumerate(order):
            x, y = triangle[k]
            ax.scatter([x], [y], s=240, color="white", edgecolor="#333333", zorder=3)
            ax.text(x, y, str(rank), ha="center", va="center", fontsize=10, zorder=4)
        draw_turn_arrow(ax, triangle.mean(axis=0), 0.13, clockwise, "#c44e52")
        ax.text(0.5, -0.22, note, ha="center", fontsize=10)
        ax.set_title(title, fontsize=10)
        ax.set_xlim(-0.2, 1.2)
        ax.set_ylim(-0.35, 1.0)
        ax.set_aspect("equal")
        ax.set_axis_off()
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_normals_2d(file_name: str) -> None:
    import matplotlib.pyplot as plt

    count = 8
    angle = np.linspace(0.0, 2.0 * np.pi, count, endpoint=False) + np.pi / count
    points = np.stack([np.cos(angle), np.sin(angle)], axis=-1)
    following = np.roll(points, -1, axis=0)
    edges = following - points
    face_normals = np.stack([edges[:, 1], -edges[:, 0]], axis=-1)
    face_normals /= np.linalg.norm(face_normals, axis=1, keepdims=True)
    vertex_normals = face_normals + np.roll(face_normals, 1, axis=0)
    vertex_normals /= np.linalg.norm(vertex_normals, axis=1, keepdims=True)

    figure, axes = plt.subplots(1, 2, figsize=(9, 4.2))
    for ax in axes:
        closed = np.concatenate([points, points[:1]])
        ax.fill(closed[:, 0], closed[:, 1], color=BLUE, alpha=0.3)
        ax.plot(closed[:, 0], closed[:, 1], color="#4c72b0", linewidth=1.5)
        ax.scatter(points[:, 0], points[:, 1], color="#333333", s=12, zorder=3)
        ax.set_xlim(-1.7, 1.7)
        ax.set_ylim(-1.7, 1.7)
        ax.set_aspect("equal")
        ax.set_axis_off()
    middle = (points + following) / 2.0
    for p, n in zip(middle, face_normals):
        axes[0].annotate("", p + 0.5 * n, p, arrowprops={"arrowstyle": "-|>", "color": "#c44e52"})
    axes[0].set_title("面の法線（面ごとに 1 本）", fontsize=10)
    for p, n in zip(points, vertex_normals):
        axes[1].annotate("", p + 0.5 * n, p, arrowprops={"arrowstyle": "-|>", "color": "#c44e52"})
    # 辺の途中では、両端の頂点の法線を補間した向きになる（細い矢印）。
    for k in range(count):
        for t in (0.25, 0.5, 0.75):
            p = points[k] * (1 - t) + following[k] * t
            n = vertex_normals[k] * (1 - t) + vertex_normals[(k + 1) % count] * t
            n /= np.linalg.norm(n)
            style = {"arrowstyle": "-|>", "color": "#dd8452", "linewidth": 0.6}
            axes[1].annotate("", p + 0.3 * n, p, arrowprops=style)
    axes[1].set_title("頂点の法線（赤）と、面の内部で補間した法線（橙）", fontsize=10)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def shared_rim_cylinder(radius: float, height: float, segments: int) -> Mesh:
    """側面とふたが縁の頂点を共有する円柱（スムーズシェーディングの失敗例に使う）。"""
    angle = np.linspace(0.0, 2.0 * np.pi, segments, endpoint=False)
    ring = np.stack([radius * np.cos(angle), radius * np.sin(angle)], axis=-1)
    bottom = np.concatenate([ring, np.zeros((segments, 1))], axis=1)
    top = np.concatenate([ring, np.full((segments, 1), height)], axis=1)
    vertices = np.concatenate([bottom, top, [[0.0, 0.0, 0.0], [0.0, 0.0, height]]])
    side = grid_faces(2, segments, wrap=True)
    i = np.arange(segments)
    j = (i + 1) % segments
    bottom_cap = np.stack([np.full(segments, 2 * segments), j, i], axis=-1)
    top_cap = np.stack([np.full(segments, 2 * segments + 1), segments + i, segments + j], axis=-1)
    return Mesh(vertices, np.concatenate([side, bottom_cap, top_cap]).astype(np.int64))


def draw_smooth(ax: Any, mesh: Mesh, color: tuple[float, float, float], level: int = 5) -> None:
    """頂点の法線を補間して陰影を付ける（スムーズシェーディングの近似）。"""
    fine, normals = subdivide_smooth(mesh, mesh.vertex_normals(), level)
    draw_faces(ax, fine, shaded_colors(normals, color), linewidth=0.4)


def draw_shading(file_name: str) -> None:
    import matplotlib.pyplot as plt

    sphere = uv_sphere(1.0, 12, 8, wrap=True)
    shared = shared_rim_cylinder(0.8, 1.2, 12)
    split = cylinder(0.8, 1.2, 12)
    figure = plt.figure(figsize=(12, 3.4))
    panels = [
        ("球: フラットシェーディング", sphere, False, BLUE),
        ("球: スムーズシェーディング", sphere, True, BLUE),
        ("円柱: 縁の頂点を共有", shared, True, ORANGE),
        ("円柱: 縁の頂点を分割", split, True, ORANGE),
    ]
    for k, (title, mesh, smooth, color) in enumerate(panels):
        ax = figure.add_subplot(1, 4, k + 1, projection="3d")
        if smooth:
            draw_smooth(ax, mesh, color)
        else:
            draw_mesh(ax, mesh, color=color, linewidth=0.0)
        fit_view(ax, [mesh], elev=30.0)
        ax.set_title(title, fontsize=10)
    figure.subplots_adjust(wspace=0.0, left=0.0, right=1.0)
    save_figure(figure, output_dir(__file__) / file_name)


def checker(uvs: FloatArray, count_u: int, count_v: int) -> FloatArray:
    """UV 座標から、count_u × count_v 個のマスのチェッカー模様の色を決める。"""
    cell = (np.floor(uvs[:, 0] * count_u) + np.floor(uvs[:, 1] * count_v)).astype(np.int64) % 2
    light = np.array([0.95, 0.80, 0.55])
    dark = np.array([0.35, 0.45, 0.70])
    return np.where(cell[:, None] == 0, light, dark)


def face_uvs(mesh: Mesh) -> FloatArray:
    """三角形ごとの UV（3 頂点の UV の平均）。"""
    assert mesh.uvs is not None
    result: FloatArray = mesh.uvs[mesh.faces].mean(axis=1)
    return result


def draw_uv_mapping(file_name: str) -> None:
    import matplotlib.pyplot as plt

    sphere = uv_sphere(1.0, 32, 16)
    tube = cylinder(0.7, 2.0, 32, rings=9)
    figure = plt.figure(figsize=(12, 3.8))

    # 左: UV 空間（テクスチャ画像の座標）に、球の三角形を展開して描く。
    ax = figure.add_subplot(1, 3, 1)
    assert sphere.uvs is not None
    u, v = np.meshgrid(np.linspace(0, 1, 256), np.linspace(0, 1, 256))
    image = checker(np.stack([u.ravel(), v.ravel()], axis=-1), 8, 4).reshape(256, 256, 3)
    ax.imshow(image, origin="lower", extent=(0, 1, 0, 1))
    for face in sphere.faces:
        triangle = sphere.uvs[np.append(face, face[0])]
        ax.plot(triangle[:, 0], triangle[:, 1], color="white", linewidth=0.3)
    ax.set_xlabel("u（経度）")
    ax.set_ylabel("v（緯度）")
    ax.set_title("UV 空間に展開した球の三角形", fontsize=10)

    for k, (title, mesh, count_u, count_v) in enumerate([("球", sphere, 8, 4), ("円柱", tube, 8, 2)]):
        ax = figure.add_subplot(1, 3, k + 2, projection="3d")
        colors = checker(face_uvs(mesh), count_u, count_v)
        draw_faces(ax, mesh, shaded_colors(mesh.face_normals(), colors))
        fit_view(ax, [mesh], elev=20.0)
        ax.set_title(f"UV でチェッカー模様を貼った{title}", fontsize=10)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def wavy_grid() -> Mesh:
    """高さを sin で変えた格子（格子の頂点の z を後から書き換えるだけで地形のようになる）。"""
    grid = plane(2.0, 2.0, 17, 17)
    x, y = grid.vertices[:, 0], grid.vertices[:, 1]
    grid.vertices[:, 2] = 0.15 * np.sin(3.0 * x) * np.cos(2.0 * y)
    return grid


def draw_primitives(file_name: str) -> None:
    import matplotlib.pyplot as plt

    shapes = [
        ("格子（17 × 17 頂点）", wavy_grid()),
        ("円柱（16 分割、ふた付き）", cylinder(0.6, 1.5, 16, rings=4)),
        ("UV 球（経度 16、緯度 10 分割）", uv_sphere(1.0, 16, 10)),
    ]
    figure = plt.figure(figsize=(12, 7))
    for k, (title, mesh) in enumerate(shapes):
        top = figure.add_subplot(2, 3, k + 1, projection="3d")
        draw_mesh(top, mesh, color=(1.0, 1.0, 1.0), edgecolor="#4c72b0", linewidth=0.5)
        fit_view(top, [mesh])
        top.set_title(title, fontsize=10)
        bottom = figure.add_subplot(2, 3, k + 4, projection="3d")
        draw_mesh(bottom, mesh, color=BLUE, linewidth=0.0)
        fit_view(bottom, [mesh])
    figure.subplots_adjust(wspace=0.0, hspace=0.05, left=0.0, right=1.0)
    save_figure(figure, output_dir(__file__) / file_name)


def draw_sphere_resolution(file_name: str) -> None:
    import matplotlib.pyplot as plt

    figure = plt.figure(figsize=(12, 3.2))
    for k, (segments, rings) in enumerate([(6, 4), (12, 6), (24, 12), (48, 24)]):
        mesh = uv_sphere(1.0, segments, rings)
        ax = figure.add_subplot(1, 4, k + 1, projection="3d")
        draw_mesh(ax, mesh, color=BLUE, edgecolor="#2f4f7f", linewidth=0.3)
        fit_view(ax, [mesh], elev=20.0)
        ax.set_title(f"{segments} × {rings}（三角形 {len(mesh.faces)} 枚）", fontsize=10)
    figure.subplots_adjust(wspace=0.0, left=0.0, right=1.0)
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_buffers("mesh_buffers.png")
    draw_winding("winding.png")
    draw_normals_2d("normals_2d.png")
    draw_shading("shading.png")
    draw_uv_mapping("uv_mapping.png")
    draw_primitives("primitives.png")
    draw_sphere_resolution("sphere_resolution.png")


if __name__ == "__main__":
    main()
