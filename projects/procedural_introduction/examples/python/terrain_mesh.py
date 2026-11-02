"""第 7 章「地形」: ハイトマップから地形のメッシュを作り、チャンクと LOD を説明する図を作る。

* terrain_mesh.png: 侵食した地形のメッシュ（バイオームの色）と、格子の構造の拡大
* chunks.png: 関数型のノイズで作った 4 × 4 個のチャンクと、境界を共有する様子
* lod.png: 距離に応じて分割数を変えたチャンクと、分割数の違う境界にできる隙間
"""

from __future__ import annotations

import numpy as np

from color import gradient_map
from common import FloatArray, output_dir, save_figure, setup_matplotlib
from heightmap import SEA_LEVEL, TERRAIN_STOPS, surface_normals
from mesh import Mesh
from meshgen import draw_faces, heightfield, shaded_colors
from noise import fbm, perlin2
from terrain_biomes import biome_colors, terrain_layers

HEIGHT_SCALE = 48.0  # ハイトマップの高さ 1 を、格子の何個分の高さにするか


def terrain_mesh(heights: FloatArray, step: int = 1) -> tuple[Mesh, FloatArray]:
    """ハイトマップから格子のメッシュを作る。step ごとに間引き、海面より下は海面の高さにそろえる。

    戻り値は、メッシュと、ハイトマップの勾配から求めた頂点の法線。
    """
    sampled = np.maximum(heights[::step, ::step], SEA_LEVEL)
    mesh = heightfield(sampled * HEIGHT_SCALE, spacing=float(step))
    normals = surface_normals(sampled, HEIGHT_SCALE / step).reshape(-1, 3)
    return mesh, normals


def face_values(mesh: Mesh, values: FloatArray) -> FloatArray:
    """頂点ごとの値（色や法線）を、三角形ごとに 3 頂点で平均する。"""
    result: FloatArray = values[mesh.faces].mean(axis=1)
    return result


def draw_terrain_mesh(file_name: str) -> None:
    import matplotlib.pyplot as plt

    heights, _, biomes, _, _ = terrain_layers()
    figure = plt.figure(figsize=(12, 5.0))
    grid_spec = figure.add_gridspec(1, 2, width_ratios=[1.6, 1.0])

    step = 2
    mesh, normals = terrain_mesh(heights, step)
    colors = biome_colors(biomes[::step, ::step]).reshape(-1, 3)
    face_normals = face_values(mesh, normals)
    face_normals /= np.linalg.norm(face_normals, axis=1, keepdims=True)
    ax = figure.add_subplot(grid_spec[0, 0], projection="3d")
    draw_faces(ax, mesh, shaded_colors(face_normals, face_values(mesh, colors)), linewidth=0.3)
    ax.set_xlim(0, 256)
    ax.set_ylim(0, 256)
    ax.set_zlim(0, 256)
    ax.set_box_aspect((1.0, 1.0, 0.35), zoom=1.45)
    ax.view_init(elev=40.0, azim=-60.0)
    ax.invert_yaxis()  # 画像（行が下向き）と同じ向きで見る
    ax.set_axis_off()
    ax.set_title(f"地形のメッシュ（{mesh.vertices.shape[0]} 頂点、三角形 {len(mesh.faces)} 枚）", fontsize=10)

    # 右: 最も高い点の周りの 24 × 24 頂点を、ワイヤーフレームで拡大する。
    top_y, top_x = np.unravel_index(int(np.argmax(heights)), heights.shape)
    crop = heights[top_y - 12:top_y + 12, top_x - 12:top_x + 12]
    small, small_normals = terrain_mesh(crop)
    ax = figure.add_subplot(grid_spec[0, 1], projection="3d")
    base = gradient_map(crop.reshape(-1), TERRAIN_STOPS)
    draw_faces(ax, small, shaded_colors(face_values(small, small_normals), face_values(small, base)),
               edgecolor="#333333", linewidth=0.3)
    ax.set_box_aspect((1.0, 1.0, 0.7))
    ax.view_init(elev=35.0, azim=-60.0)
    ax.set_axis_off()
    ax.set_title("一部を拡大（格子の 2 枚の三角形が見える）", fontsize=10)
    figure.subplots_adjust(wspace=0.0, left=0.0, right=1.0)
    save_figure(figure, output_dir(__file__) / file_name)


def chunk_heights(cx: int, cy: int, resolution: int, seed: int = 7) -> FloatArray:
    """チャンク (cx, cy) の高さ。世界座標でノイズを評価するので、隣のチャンクと境界の値が一致する。

    チャンクの幅を 1 とし、1 辺を resolution 等分した (resolution + 1) 個の頂点を置く。
    """
    coords = np.linspace(0.0, 1.0, resolution + 1)
    x, y = np.meshgrid(cx + coords, cy + coords)
    result: FloatArray = 0.55 + 0.8 * fbm(perlin2, x * 1.2, y * 1.2, octaves=5, seed=seed)
    return result


def chunk_mesh(cx: int, cy: int, resolution: int, scale: float = 32.0) -> Mesh:
    """チャンク (cx, cy) のメッシュ（世界座標に置く）。"""
    h = chunk_heights(cx, cy, resolution)
    spacing = scale / resolution
    return heightfield(h * scale * 0.6, spacing, origin=(cx * scale, cy * scale))


def draw_chunks(file_name: str) -> None:
    import matplotlib.pyplot as plt

    count = 4
    resolution = 32
    figure = plt.figure(figsize=(12, 5.0))
    ax = figure.add_subplot(1, 2, 1)
    rows = []
    for cy in range(count):
        rows.append(np.concatenate([chunk_heights(cx, cy, resolution)[:, :-1] for cx in range(count)], axis=1))
    world = np.concatenate([row[:-1] for row in rows], axis=0)
    ax.imshow(gradient_map(world, TERRAIN_STOPS), origin="lower", extent=(0, count, 0, count))
    for k in range(count + 1):
        ax.axhline(k, color="white", linewidth=1.5)
        ax.axvline(k, color="white", linewidth=1.5)
    for cy in range(count):
        for cx in range(count):
            ax.text(cx + 0.5, cy + 0.5, f"({cx}, {cy})", ha="center", va="center", fontsize=9, color="#222222")
    ax.set_title("4 × 4 個のチャンク（各チャンクを別々に生成）", fontsize=10)
    ax.set_axis_off()

    ax3 = figure.add_subplot(1, 2, 2, projection="3d")
    gap = 6.0
    meshes = []
    for cy in range(2):
        for cx in range(2):
            mesh = chunk_mesh(cx, cy, 16).transformed(offset=(cx * gap, cy * gap, 0.0))
            meshes.append(mesh)
            colors = gradient_map(mesh.vertices[:, 2] / (32.0 * 0.6), TERRAIN_STOPS)
            normals = mesh.vertex_normals()
            draw_faces(ax3, mesh, shaded_colors(face_values(mesh, normals), face_values(mesh, colors)),
                       edgecolor="#555555", linewidth=0.2)
    points = np.concatenate([m.vertices for m in meshes])
    ax3.set_xlim(points[:, 0].min(), points[:, 0].max())
    ax3.set_ylim(points[:, 1].min(), points[:, 1].max())
    ax3.set_zlim(0, 40)
    ax3.set_box_aspect((1.0, 1.0, 0.45), zoom=1.2)
    ax3.view_init(elev=35.0, azim=-60.0)
    ax3.set_axis_off()
    ax3.set_title("2 × 2 個のチャンクを離して表示（境界の形が一致する）", fontsize=10)
    figure.subplots_adjust(wspace=0.05, left=0.02, right=1.0)
    save_figure(figure, output_dir(__file__) / file_name)


def draw_lod(file_name: str) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    count = 6
    camera = np.array([0.5, 0.5])
    figure, axes = plt.subplots(1, 2, figsize=(12, 5.0), gridspec_kw={"width_ratios": [1.0, 1.25]})
    ax = axes[0]
    colors = {16: "#c44e52", 8: "#dd8452", 4: "#55a868", 2: "#4c72b0"}
    for cy in range(count):
        for cx in range(count):
            distance = float(np.hypot(cx + 0.5 - camera[0], cy + 0.5 - camera[1]))
            resolution = 16 if distance < 1.5 else 8 if distance < 3.0 else 4 if distance < 4.5 else 2
            lines = np.linspace(0.0, 1.0, resolution + 1)
            for t in lines:
                ax.plot([cx, cx + 1], [cy + t, cy + t], color=colors[resolution], linewidth=0.4)
                ax.plot([cx + t, cx + t], [cy, cy + 1], color=colors[resolution], linewidth=0.4)
    ax.scatter([camera[0]], [camera[1]], marker="*", s=220, color="black", zorder=3)
    ax.text(camera[0] + 0.15, camera[1] + 0.15, "カメラ", fontsize=10, zorder=3,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.8})
    for k in range(count + 1):
        ax.axhline(k, color="black", linewidth=1.0)
        ax.axvline(k, color="black", linewidth=1.0)
    ax.set_xlim(0, count)
    ax.set_ylim(0, count)
    ax.set_aspect("equal")
    ax.set_axis_off()
    handles = [Line2D([], [], color=color, label=f"1 辺 {resolution} 分割") for resolution, color in colors.items()]
    ax.legend(handles=handles, loc="upper right", fontsize=8, framealpha=0.9)
    ax.set_title("カメラからの距離で分割数を変える（LOD）", fontsize=10)

    # 右: 分割数 16 と 4 のチャンクが接する境界の断面。粗い側は間の頂点を持たないので隙間ができる。
    ax = axes[1]
    fine = chunk_heights(0, 0, 16)[:, -1]
    coarse = chunk_heights(1, 0, 4)[:, 0]
    t_fine = np.linspace(0.0, 1.0, 17)
    t_coarse = np.linspace(0.0, 1.0, 5)
    coarse_at_fine = np.interp(t_fine, t_coarse, coarse)
    ax.fill_between(t_fine, fine, coarse_at_fine, color="#f2b8a0", label="隙間（向こう側が見える）")
    ax.plot(t_fine, fine, color="#c44e52", marker="o", markersize=4, label="細かいチャンクの境界（16 分割）")
    ax.plot(t_coarse, coarse, color="#4c72b0", marker="s", markersize=6, label="粗いチャンクの境界（4 分割）")
    ax.set_xlabel("境界に沿った位置")
    ax.set_ylabel("高さ")
    ax.legend(fontsize=8, loc="best")
    ax.set_title("分割数の違うチャンクの境界（断面）", fontsize=10)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_terrain_mesh("terrain_mesh.png")
    draw_chunks("chunks.png")
    draw_lod("lod.png")


if __name__ == "__main__":
    main()
