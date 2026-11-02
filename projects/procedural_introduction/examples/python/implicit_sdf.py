"""第 9 章「陰関数と体積表現」: 3 次元の距離関数と、その組み合わせの図を作る。

* sdf_slice.png: 球・直方体・トーラスの距離関数を、y = 0 の断面で色と等高線にしたもの
* sdf_primitives.png: 同じ 3 つの形をメッシュ化して表示したもの
* sdf_boolean.png: 直方体と球の和・共通部分・差・スムーズな和
* smooth_min.png: min とスムーズな min のグラフ、k を変えたときの断面
"""

from __future__ import annotations

from typing import Any

import numpy as np

from common import FloatArray, output_dir, save_figure, setup_matplotlib
from marching_tetrahedra import marching_tetrahedra
from mesh import Mesh, draw_mesh, fit_view
from sdf3d import (Sdf, grid3, op_intersection, op_subtraction, op_union, sd_box, sd_sphere, sd_torus,
                   smooth_min)

PRIMITIVES: list[tuple[str, Sdf]] = [
    ("球 sd_sphere", lambda p: sd_sphere(p, 0.8)),
    ("直方体 sd_box", lambda p: sd_box(p, (0.7, 0.5, 0.5))),
    ("トーラス sd_torus", lambda p: sd_torus(p, 0.65, 0.25)),
]


def box_and_sphere(p: FloatArray) -> tuple[FloatArray, FloatArray]:
    """ブーリアン演算の例に使う、直方体と、右上にずらした球の距離。"""
    box = sd_box(p, (0.55, 0.55, 0.55))
    sphere = sd_sphere(p - np.array([0.45, -0.45, 0.45]), 0.55)
    return box, sphere


BOOLEANS: list[tuple[str, Sdf]] = [
    ("和 min(a, b)", lambda p: op_union(*box_and_sphere(p))),
    ("共通部分 max(a, b)", lambda p: op_intersection(*box_and_sphere(p))),
    ("差 max(a, −b)", lambda p: op_subtraction(*box_and_sphere(p))),
    ("スムーズな和（k = 0.3）", lambda p: smooth_min(*box_and_sphere(p), 0.3)),
]


def distance_colors(d: FloatArray) -> FloatArray:
    """距離を色にする（内側は青、外側は橙。等間隔の縞で距離の大きさを表す）。"""
    inside = np.array([0.30, 0.48, 0.78])
    outside = np.array([0.90, 0.60, 0.35])
    base = np.where(d[..., None] < 0.0, inside, outside)
    fade = 1.0 - np.exp(-3.0 * np.abs(d))[..., None]  # 表面から離れるほど濃くする
    stripes = 0.85 + 0.15 * np.cos(2.0 * np.pi * d / 0.1)[..., None]
    color = (1.0 - 0.7 * fade) * 1.0 + 0.7 * fade * base
    result: FloatArray = np.clip(color * stripes, 0.0, 1.0)
    return result


def slice_xz(sdf: Sdf, size: int = 240, extent: float = 1.2) -> FloatArray:
    """y = 0 の断面（横軸 x、縦軸 z）で距離関数の値を計算する。"""
    xs = np.linspace(-extent, extent, size)
    x, z = np.meshgrid(xs, xs[::-1])
    p = np.stack([x, np.zeros_like(x), z], axis=-1)
    return sdf(p)


def mesh_of(sdf: Sdf, resolution: int = 48, extent: float = 1.2) -> Mesh:
    """距離関数を格子点で評価し、値が 0 の面をメッシュにする。"""
    points = grid3((-extent, -extent, -extent), (extent, extent, extent), (resolution,) * 3)
    return marching_tetrahedra(sdf(points), points)


def draw_slices(file_name: str) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 3, figsize=(10.5, 3.6))
    for ax, (title, sdf) in zip(axes, PRIMITIVES):
        d = slice_xz(sdf)
        ax.imshow(distance_colors(d), extent=(-1.2, 1.2, -1.2, 1.2))
        ax.contour(np.linspace(-1.2, 1.2, d.shape[1]), np.linspace(1.2, -1.2, d.shape[0]), d, levels=[0.0],
                   colors="black", linewidths=1.5)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("x")
        ax.set_ylabel("z")
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_meshes(
    file_name: str, shapes: list[tuple[str, Sdf]], color: tuple[float, float, float], resolution: int = 48
) -> None:
    import matplotlib.pyplot as plt

    figure = plt.figure(figsize=(3.4 * len(shapes), 3.6))
    for index, (title, sdf) in enumerate(shapes):
        ax: Any = figure.add_subplot(1, len(shapes), index + 1, projection="3d")
        mesh = mesh_of(sdf, resolution)
        draw_mesh(ax, mesh, color=color)
        fit_view(ax, [mesh], elev=22.0, azim=-55.0)
        ax.set_title(title, fontsize=10)
    figure.subplots_adjust(left=0.0, right=1.0, top=0.92, bottom=0.0, wspace=0.0)
    save_figure(figure, output_dir(__file__) / file_name)


def draw_smooth_min(file_name: str) -> None:
    import matplotlib.pyplot as plt

    figure = plt.figure(figsize=(12, 3.4))
    grid = figure.add_gridspec(1, 4, width_ratios=[1.3, 1, 1, 1])

    # 左: a = x、b = 1 − x のときの min と smooth min
    ax = figure.add_subplot(grid[0])
    x = np.linspace(-0.5, 1.5, 400)
    a = x
    b = 1.0 - x
    ax.plot(x, a, color="#999999", linewidth=0.8, linestyle="--")
    ax.plot(x, b, color="#999999", linewidth=0.8, linestyle="--")
    ax.plot(x, np.minimum(a, b), color="black", label="min")
    for k, color in [(0.3, "#4c72b0"), (0.8, "#dd8452")]:
        ax.plot(x, smooth_min(a, b, k), color=color, label=f"smooth min（k = {k}）")
    ax.set_ylim(-0.4, 1.0)
    ax.set_xlabel("x")
    ax.legend(fontsize=8, loc="lower center")
    ax.set_title("a = x, b = 1 − x の最小値", fontsize=10)

    # 右: 2 つの球を k を変えてつないだ断面
    for index, k in enumerate([0.0, 0.2, 0.5]):
        ax = figure.add_subplot(grid[index + 1])

        def two_spheres(p: FloatArray, k: float = k) -> FloatArray:
            left = sd_sphere(p - np.array([-0.45, 0.0, 0.1]), 0.45)
            right = sd_sphere(p - np.array([0.5, 0.0, -0.1]), 0.35)
            return smooth_min(left, right, k)

        d = slice_xz(two_spheres)
        ax.imshow(distance_colors(d), extent=(-1.2, 1.2, -1.2, 1.2))
        ax.contour(np.linspace(-1.2, 1.2, d.shape[1]), np.linspace(1.2, -1.2, d.shape[0]), d, levels=[0.0],
                   colors="black", linewidths=1.5)
        ax.set_title(f"2 つの球のスムーズな和（k = {k}）", fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_slices("sdf_slice.png")
    draw_meshes("sdf_primitives.png", PRIMITIVES, (0.62, 0.72, 0.88))
    draw_meshes("sdf_boolean.png", BOOLEANS, (0.85, 0.70, 0.55), resolution=72)
    draw_smooth_min("smooth_min.png")


if __name__ == "__main__":
    main()
