"""第 6 章「メッシュの基礎と生成」: 回転体とスイープの図、OBJ ファイルを作る。

* lathe.png: 断面の曲線と、それを回転させた壺（パラメーター違い）
* frames.png: フレネ標構と回転最小化標構で作ったパイプのねじれの比較
* pipe.png: 結び目に沿ったパイプと、太さを変えながら伸びる触手
* road.png: スプラインに沿って道路の断面をスイープした道（上から見た図と立体）
* quad.obj: OBJ 形式で書き出した四角形のメッシュ
"""

from __future__ import annotations

from typing import Any

import numpy as np

from common import FloatArray, output_dir, save_figure, setup_matplotlib
from mesh import Mesh, draw_mesh, fit_view, write_obj
from meshgen import (catmull_rom, circle_section, draw_faces, frenet_frames, lathe, plane, rotation_minimizing_frames,
                     shaded_colors, sweep)

BLUE = (0.62, 0.72, 0.88)
CLAY = (0.80, 0.52, 0.36)


def vase_profile(base: float, belly: float, belly_height: float, neck: float, lip: float, height: float,
                 thickness: float = 0.05, samples: int = 12) -> tuple[FloatArray, FloatArray]:
    """壺の断面（半径と高さの列）。底の中心から外側を上り、口で折り返して内側を下りる。

    外側の輪郭は、底・胴・首・口の 4 つの制御点を通る Catmull-Rom スプラインで作る。
    """
    control = np.array([[base, 0.0], [belly, belly_height * height], [neck, 0.8 * height], [lip, height]])
    outer = catmull_rom(control, samples)
    inner = outer[::-1].copy()
    inner[:, 0] = np.maximum(inner[:, 0] - thickness, 0.0)
    inner = inner[inner[:, 1] >= thickness]
    profile = np.concatenate([[[0.0, 0.0]], outer, inner, [[0.0, thickness]]])
    return profile[:, 0], profile[:, 1]


# 壺のパラメーター（底の半径、胴の半径、胴の高さの割合、首の半径、口の半径、高さ）
VASES = [
    ("胴が低く口が広い", (0.35, 0.75, 0.35, 0.30, 0.45, 1.4)),
    ("胴が高い", (0.30, 0.55, 0.60, 0.20, 0.30, 1.8)),
    ("首が太い", (0.45, 0.65, 0.45, 0.50, 0.55, 1.3)),
]


def draw_lathe(file_name: str) -> None:
    import matplotlib.pyplot as plt

    figure = plt.figure(figsize=(12, 3.6))
    ax = figure.add_subplot(1, 4, 1)
    radius, height = vase_profile(*VASES[0][1])
    ax.plot(radius, height, color="#4c72b0", marker="o", markersize=2)
    base, belly, belly_height, neck, lip, total = VASES[0][1]
    control = np.array([[base, 0.0], [belly, belly_height * total], [neck, 0.8 * total], [lip, total]])
    ax.scatter(control[:, 0], control[:, 1], color="#c44e52", zorder=3, label="制御点")
    ax.axvline(0.0, color="#888888", linestyle="--", linewidth=1)
    ax.text(0.02, 0.6, "回転軸", color="#666666", fontsize=9)
    ax.set_aspect("equal")
    ax.set_xlim(-0.1, 1.0)
    ax.set_xlabel("半径 r")
    ax.set_ylabel("高さ z")
    ax.legend(loc="lower right", fontsize=8)
    ax.set_title("断面の曲線", fontsize=10)
    for k, (title, parameters) in enumerate(VASES):
        radius, height = vase_profile(*parameters)
        mesh = lathe(radius, height, 48)
        ax3 = figure.add_subplot(1, 4, k + 2, projection="3d")
        draw_mesh(ax3, mesh, color=CLAY, linewidth=0.0)
        fit_view(ax3, [mesh], elev=25.0)
        ax3.set_title(title, fontsize=10)
    figure.subplots_adjust(wspace=0.05, left=0.04, right=1.0)
    save_figure(figure, output_dir(__file__) / file_name)


def s_curve(count: int = 160) -> FloatArray:
    """途中で曲がる向きが反転する（変曲点を持つ）、上りながらうねる曲線。"""
    t = np.linspace(0.0, 2.0 * np.pi, count)
    return np.stack([0.9 * t, 1.6 * np.sin(t), 0.25 * t], axis=-1)


def stripe_colors(mesh: Mesh, columns: int) -> FloatArray:
    """断面の 1 周を 8 等分し、1 区画だけ赤く塗った縞模様（パイプのねじれを見るため）。"""
    column = mesh.faces[:, 0] % columns
    red = (column * 8 // (columns - 1)) == 0
    return np.where(red[:, None], np.array([0.85, 0.30, 0.30]), np.array(BLUE))


def draw_frames(file_name: str) -> None:
    import matplotlib.pyplot as plt

    points = s_curve()
    section = circle_section(0.35, 32)
    figure = plt.figure(figsize=(12, 4.0))
    cases = [("フレネ標構", frenet_frames(points)), ("回転最小化標構", rotation_minimizing_frames(points))]
    for k, (title, (_, normals, binormals)) in enumerate(cases):
        mesh = sweep(points, normals, binormals, section)
        ax = figure.add_subplot(1, 2, k + 1, projection="3d")
        draw_faces(ax, mesh, shaded_colors(mesh.face_normals(), stripe_colors(mesh, len(section))))
        for index in range(0, len(points), 16):
            p = points[index]
            q = p + 0.9 * normals[index]
            ax.plot([p[0], q[0]], [p[1], q[1]], [p[2], q[2]], color="#2a7a2a", linewidth=1.5)
        fit_view(ax, [mesh], elev=30.0, azim=-70.0)
        ax.set_box_aspect((1.0, 1.0, 1.0), zoom=1.6)
        ax.set_title(f"{title}（緑の線は法線 N）", fontsize=10)
    figure.subplots_adjust(wspace=0.0, left=0.0, right=1.0)
    save_figure(figure, output_dir(__file__) / file_name)


def trefoil(count: int) -> FloatArray:
    """三葉結び目の曲線（始点と終点が一致する閉曲線）。"""
    t = np.linspace(0.0, 2.0 * np.pi, count)
    return np.stack([np.sin(t) + 2.0 * np.sin(2.0 * t), np.cos(t) - 2.0 * np.cos(2.0 * t), -np.sin(3.0 * t)],
                    axis=-1)


def closed_frames(points: FloatArray) -> tuple[FloatArray, FloatArray, FloatArray]:
    """閉曲線用の回転最小化標構。1 周して戻ったときの法線のずれを、曲線全体に少しずつ割り振る。"""
    t, n, b = rotation_minimizing_frames(points)
    # 終点の法線が始点の法線から、接線の周りにどれだけ回っているか
    mismatch = float(np.arctan2(np.dot(n[-1], b[0]), np.dot(n[-1], n[0])))
    angle = -mismatch * np.linspace(0.0, 1.0, len(points))[:, None]
    n2 = np.cos(angle) * n + np.sin(angle) * b
    b2 = np.cross(t, n2)
    return t, n2, b2


def tentacle(seed: int, count: int = 120) -> tuple[FloatArray, FloatArray]:
    """乱数で曲がりながら上へ伸びる経路と、根元から先へ細くなる太さ。"""
    rng = np.random.default_rng(seed)
    direction = np.array([0.0, 0.0, 1.0])
    points = [np.zeros(3)]
    turn = np.zeros(3)
    for _ in range(count - 1):
        turn = 0.85 * turn + 0.15 * rng.normal(size=3)
        direction = direction + 0.12 * turn
        direction /= np.linalg.norm(direction)
        points.append(points[-1] + 0.05 * direction)
    scale = 1.0 - np.linspace(0.0, 0.95, count) ** 1.5
    return np.array(points), scale


def draw_pipe(file_name: str) -> None:
    import matplotlib.pyplot as plt

    figure = plt.figure(figsize=(12, 4.6))
    points = trefoil(240)
    section = circle_section(0.35, 24)
    _, normals, binormals = closed_frames(points)
    knot = sweep(points, normals, binormals, section)
    ax = figure.add_subplot(1, 2, 1, projection="3d")
    draw_faces(ax, knot, shaded_colors(knot.face_normals(), stripe_colors(knot, len(section))))
    fit_view(ax, [knot], elev=50.0)
    ax.set_box_aspect((1.0, 1.0, 1.0), zoom=1.2)
    ax.set_title("三葉結び目に沿ったパイプ", fontsize=10)

    ax = figure.add_subplot(1, 2, 2, projection="3d")
    meshes = []
    for k in range(5):
        path, scale = tentacle(seed=k)
        angle = 2.0 * np.pi * k / 5
        path = path + np.array([0.6 * np.cos(angle), 0.6 * np.sin(angle), 0.0])
        _, normals, binormals = rotation_minimizing_frames(path)
        meshes.append(sweep(path, normals, binormals, circle_section(0.18, 16), scale))
    for mesh in meshes:
        draw_mesh(ax, mesh, color=(0.80, 0.55, 0.75), linewidth=0.0)
    fit_view(ax, meshes, elev=15.0)
    ax.set_box_aspect((1.0, 1.0, 1.0), zoom=1.3)
    ax.set_title("太さを変えながらスイープした触手（シード 0〜4）", fontsize=10)
    figure.subplots_adjust(wspace=0.0, left=0.0, right=1.0)
    save_figure(figure, output_dir(__file__) / file_name)


# 道路の断面（道の中心からの左右の位置 x と高さ y）。左の端から右の端へ並べる。
ROAD_SECTION = np.array([
    [-6.0, -0.6], [-4.4, 0.0], [-4.0, 0.15], [-3.6, 0.15], [-0.2, 0.15], [0.2, 0.15],
    [3.6, 0.15], [4.0, 0.15], [4.4, 0.0], [6.0, -0.6],
])
# 断面の各区間（隣り合う 2 点の間）の種類: 0 法面、1 縁石、2 路面、3 中央線
ROAD_KINDS = np.array([0, 1, 1, 2, 3, 2, 1, 1, 0])
ROAD_COLORS = np.array([[0.45, 0.65, 0.35], [0.75, 0.75, 0.72], [0.30, 0.30, 0.33], [0.95, 0.95, 0.90]])
ROAD_CONTROL = np.array([[0, 0, 0], [30, 10, 2], [55, -5, 4], [80, 15, 3], [100, 40, 0], [90, 70, -1]],
                        dtype=np.float64)


def road_frames(points: FloatArray) -> tuple[FloatArray, FloatArray]:
    """道路用の座標系。左右の向きを常に水平に保ち（道が横に傾かない）、上の向きを残りで決める。"""
    t = np.gradient(points, axis=0)
    t /= np.linalg.norm(t, axis=1, keepdims=True)
    up = np.array([0.0, 0.0, 1.0])
    left = np.cross(up, t)
    left /= np.linalg.norm(left, axis=1, keepdims=True)
    normal_up = np.cross(t, left)
    return -left, normal_up  # 断面の x の正の向き（右）と y の正の向き（上）


def road_mesh() -> tuple[Mesh, FloatArray]:
    """道路のメッシュと、三角形ごとの色を返す。中央線は道のりに応じて破線にする。"""
    points = catmull_rom(ROAD_CONTROL, 24)
    right, up = road_frames(points)
    mesh = sweep(points, right, up, ROAD_SECTION)
    columns = len(ROAD_SECTION)
    column = mesh.faces[:, 0] % columns
    row = mesh.faces[:, 0] // columns
    distance = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(points, axis=0), axis=1))])
    kinds = ROAD_KINDS[column]
    dashed = (kinds == 3) & ((distance[row] // 4.0) % 2 == 1)  # 4 m ごとに線を途切れさせる
    kinds = np.where(dashed, 2, kinds)
    return mesh, ROAD_COLORS[kinds]


def draw_road(file_name: str) -> None:
    import matplotlib.pyplot as plt

    mesh, colors = road_mesh()
    figure = plt.figure(figsize=(12, 4.4))
    grid = figure.add_gridspec(1, 3, width_ratios=[0.9, 1.0, 1.4])
    ax = figure.add_subplot(grid[0, 0])
    section = ROAD_SECTION
    for k, kind in enumerate(ROAD_KINDS):
        ax.plot(section[k:k + 2, 0], section[k:k + 2, 1], color=ROAD_COLORS[kind] * 0.9, linewidth=4)
    ax.scatter(section[:, 0], section[:, 1], color="#333333", s=10, zorder=3)
    ax.set_aspect("equal")
    ax.set_ylim(-1.5, 1.0)
    ax.set_xlabel("中心からの距離 [m]")
    ax.set_title("断面（法面・縁石・路面・中央線）", fontsize=10)

    ax = figure.add_subplot(grid[0, 1])
    for face, color in zip(mesh.faces, colors):
        triangle = mesh.vertices[face, :2]
        ax.fill(triangle[:, 0], triangle[:, 1], facecolor=color, edgecolor=color, linewidth=0.3)
    curve = catmull_rom(ROAD_CONTROL, 24)
    ax.plot(curve[:, 0], curve[:, 1], color="#c44e52", linewidth=0.6, linestyle="--")
    ax.scatter(ROAD_CONTROL[:, 0], ROAD_CONTROL[:, 1], color="#c44e52", s=14, zorder=3)
    ax.set_aspect("equal")
    ax.set_title("上から見た図（赤は制御点とスプライン）", fontsize=10)
    ax.set_axis_off()

    ax3: Any = figure.add_subplot(grid[0, 2], projection="3d")
    draw_faces(ax3, mesh, shaded_colors(mesh.face_normals(), colors), linewidth=0.4)
    fit_view(ax3, [mesh], elev=30.0, azim=-120.0)
    ax3.set_zlim(-20, 20)
    ax3.set_box_aspect((1.0, 1.0, 0.35), zoom=1.3)
    ax3.set_title("立体（高さの変化も制御点で与える）", fontsize=10)
    figure.subplots_adjust(wspace=0.1, left=0.02, right=1.0)
    save_figure(figure, output_dir(__file__) / file_name)


def to_y_up(mesh: Mesh) -> Mesh:
    """z 軸が上の座標を、y 軸が上の座標（Godot や多くのツールの規約）に回転する。"""
    rotation = np.array([[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, -1.0, 0.0]])
    return mesh.transformed(rotation)


def export_obj() -> None:
    """説明用の四角形 1 枚（三角形 2 枚）を OBJ 形式で保存する。"""
    write_obj(to_y_up(plane(1.0, 1.0, 2, 2)), output_dir(__file__) / "quad.obj")


def main() -> None:
    setup_matplotlib()
    draw_lathe("lathe.png")
    draw_frames("frames.png")
    draw_pipe("pipe.png")
    draw_road("road.png")
    export_obj()


if __name__ == "__main__":
    main()
