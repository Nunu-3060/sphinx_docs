"""第 16 章の図: Houdini が書き出した OBJ ファイルを matplotlib で描く。

hython ではなく通常の Python で実行する。先に hython で build_terrain.py・build_lsystem.py・
export_variations.py を実行し、examples/houdini/out/ に OBJ ファイルを作っておく。
examples/python の共通ライブラリ（common.py・mesh.py）を使う。

    py render_previews.py [出力先のフォルダー]

出力先を省略すると examples/houdini/out/previews/ に保存する。本文の図は
source/_static/houdini/ に保存したものである（本文のビルドでは実行しない）。
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import numpy as np

HOUDINI_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(HOUDINI_DIR.parent / "python"))

from color import gradient_map  # noqa: E402
from common import FloatArray, save_figure, setup_matplotlib  # noqa: E402
from mesh import shade  # noqa: E402

OUT_DIR = HOUDINI_DIR / "out"

# 高さに応じた地形の色（海岸の砂から、草地・岩・雪へ）
TERRAIN_STOPS = [(0.0, (0.80, 0.75, 0.55)), (0.15, (0.45, 0.62, 0.32)),
                 (0.6, (0.42, 0.40, 0.36)), (1.0, (0.95, 0.95, 0.95))]


class ObjData:
    """OBJ ファイルの中身。座標は Houdini の Y 上向きから、matplotlib の Z 上向きに直す。"""

    def __init__(self, path: Path) -> None:
        points: list[list[float]] = []
        colors: list[list[float]] = []
        self.polygons: list[list[int]] = []
        self.lines: list[list[int]] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            fields = line.split()
            if not fields:
                continue
            if fields[0] == "v":
                x, y, z = (float(value) for value in fields[1:4])
                points.append([x, -z, y])
                # Houdini は色（Cd 属性）があれば v x y z r g b の形で書く
                colors.append([float(value) for value in fields[4:7]] if len(fields) >= 7 else [0.5, 0.5, 0.5])
            elif fields[0] in ("f", "l"):
                indices = [int(value.split("/")[0]) - 1 for value in fields[1:]]
                (self.polygons if fields[0] == "f" else self.lines).append(indices)
        self.points: FloatArray = np.array(points)
        self.colors: FloatArray = np.array(colors)


def polygon_normals(points: FloatArray, polygons: list[list[int]]) -> FloatArray:
    """多角形の法線をニューウェル法で求める（四角形がわずかにねじれていても安定する）。"""
    normals = np.zeros((len(polygons), 3))
    for index, polygon in enumerate(polygons):
        p = points[polygon]
        q = np.roll(p, -1, axis=0)
        normals[index] = [np.sum((p[:, 1] - q[:, 1]) * (p[:, 2] + q[:, 2])),
                          np.sum((p[:, 2] - q[:, 2]) * (p[:, 0] + q[:, 0])),
                          np.sum((p[:, 0] - q[:, 0]) * (p[:, 1] + q[:, 1]))]
    lengths = np.linalg.norm(normals, axis=1, keepdims=True)
    result: FloatArray = normals / np.maximum(lengths, 1e-12)
    # 表裏の向きがそろっていない面もあるので、陰影は上向きにそろえて計算する
    result[result[:, 2] < 0] *= -1.0
    return result


def draw_polygons(ax: Any, objects: list[tuple[ObjData, FloatArray | None]]) -> None:
    """複数の OBJ の多角形を 1 つのコレクションにまとめて描く（奥行きの並べ替えを共通にするため）。

    各要素の 2 番目に (面の数, 3) の色を渡すとその色で、None なら OBJ の頂点色の平均で塗る。
    """
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    faces: list[FloatArray] = []
    face_colors: list[FloatArray] = []
    for data, colors in objects:
        faces += [data.points[polygon] for polygon in data.polygons]
        if colors is None:
            colors = np.array([data.colors[polygon].mean(axis=0) for polygon in data.polygons])
        lit = shade(polygon_normals(data.points, data.polygons), (1.0, 1.0, 1.0), light=(-0.5, -0.4, 0.8))
        face_colors.append(lit * colors)
    shaded = np.concatenate(face_colors)
    ax.add_collection3d(Poly3DCollection(faces, facecolors=shaded, edgecolors=shaded, linewidths=0.1))


def height_colors(data: ObjData) -> FloatArray:
    """多角形の平均の高さから、地形の色を決める。"""
    heights = np.array([data.points[polygon, 2].mean() for polygon in data.polygons])
    low, high = float(heights.min()), float(heights.max())
    colors = gradient_map((heights - low) / (high - low), TERRAIN_STOPS)
    colors[heights <= low + 1e-6] = (0.30, 0.48, 0.70)  # いちばん低い所（海面）は水の色
    return colors


def set_view(ax: Any, points: FloatArray, elev: float = 35.0, azim: float = -60.0, zoom: float = 1.0) -> None:
    """軸の範囲を points に合わせ、縦横比を実際の大きさどおりにして軸を消す。"""
    low = points.min(axis=0)
    high = points.max(axis=0)
    center = (low + high) / 2.0
    half = (high - low).max() / 2.0 / zoom
    ax.set_xlim(center[0] - half, center[0] + half)
    ax.set_ylim(center[1] - half, center[1] + half)
    ax.set_zlim(center[2] - half, center[2] + half)
    ax.set_box_aspect((1.0, 1.0, 1.0))
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()


def draw_terrain(target: Path) -> None:
    """ポリゴンの島と、ハイトフィールドの地形を並べた図。"""
    import matplotlib.pyplot as plt

    figure = plt.figure(figsize=(10, 4.0))
    for column, (name, title) in enumerate((("terrain_island.obj", "Grid → Mountain → 島の形"),
                                            ("terrain_heightfield.obj", "HeightField → Noise → Erode"))):
        data = ObjData(OUT_DIR / name)
        ax = figure.add_subplot(1, 2, column + 1, projection="3d")
        draw_polygons(ax, [(data, height_colors(data))])
        set_view(ax, data.points, zoom=1.8)
        ax.set_title(title, fontsize=11)
    figure.subplots_adjust(left=0, right=1, bottom=0, top=0.95, wspace=0)
    save_figure(figure, target)


def draw_scatter(target: Path) -> None:
    """密度で色分けした地形と、木を散布した結果を並べた図（シード 0）。"""
    import matplotlib.pyplot as plt

    terrain = ObjData(OUT_DIR / "variations" / "terrain_000.obj")
    trees = ObjData(OUT_DIR / "variations" / "trees_000.obj")
    figure = plt.figure(figsize=(10, 4.0))
    ax = figure.add_subplot(1, 2, 1, projection="3d")
    draw_polygons(ax, [(terrain, None)])
    set_view(ax, terrain.points, zoom=1.8)
    ax.set_title("density（緑: 生える、灰: 生えない）", fontsize=11)
    ax = figure.add_subplot(1, 2, 2, projection="3d")
    draw_polygons(ax, [(terrain, height_colors(terrain)), (trees, None)])
    set_view(ax, terrain.points, zoom=1.8)
    ax.set_title("Copy to Points で木を複製", fontsize=11)
    figure.subplots_adjust(left=0, right=1, bottom=0, top=0.95, wspace=0)
    save_figure(figure, target)


def draw_variations(target: Path, count: int = 4) -> None:
    """export_variations.py が書き出したシード違いの結果を並べた図。"""
    import matplotlib.pyplot as plt

    figure = plt.figure(figsize=(12, 3.4))
    for seed in range(count):
        terrain = ObjData(OUT_DIR / "variations" / f"terrain_{seed:03d}.obj")
        trees = ObjData(OUT_DIR / "variations" / f"trees_{seed:03d}.obj")
        ax = figure.add_subplot(1, count, seed + 1, projection="3d")
        draw_polygons(ax, [(terrain, height_colors(terrain)), (trees, None)])
        set_view(ax, terrain.points, elev=45.0, zoom=1.8)
        ax.set_title(f"seed = {seed}", fontsize=11)
    figure.subplots_adjust(left=0, right=1, bottom=0, top=0.92, wspace=0)
    save_figure(figure, target)


def draw_lsystem(target: Path) -> None:
    """L-System SOP の折れ線を、正面（XY 平面）から見た図。"""
    import matplotlib.pyplot as plt

    data = ObjData(OUT_DIR / "lsystem.obj")
    figure, ax = plt.subplots(figsize=(10, 4.2))
    for line in data.lines:
        ax.plot(data.points[line, 0], data.points[line, 2], color="#4c6b2f", linewidth=0.8)
    labels = [(0.0, "plant"), (1.5, "bush（seed 1）"), (2.7, "seed 2"), (3.9, "seed 3"), (6.0, "tree")]
    for x, label in labels:
        ax.text(x, -0.35, label, ha="center", va="top", fontsize=10)
    ax.set_aspect("equal")
    ax.set_ylim(-0.8, None)
    ax.set_axis_off()
    save_figure(figure, target)


def main() -> None:
    setup_matplotlib()
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else OUT_DIR / "previews"
    target.mkdir(parents=True, exist_ok=True)
    draw_terrain(target / "terrain.png")
    draw_scatter(target / "scatter.png")
    draw_variations(target / "variations.png")
    draw_lsystem(target / "lsystem.png")
    print(f"保存した: {target}")


if __name__ == "__main__":
    main()
