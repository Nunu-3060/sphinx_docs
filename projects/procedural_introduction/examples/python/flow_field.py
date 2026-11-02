"""第 13 章「群れと粒子」: ノイズから作るベクトル場（流れ場）と、それに沿った粒子の運動。

2 種類の流れ場を比べる。

* 角度場: ノイズの値を角度とみなし、その向きの単位ベクトルを速度にする。
* カールノイズ: ノイズ ψ を流れ関数とみなし、v = (∂ψ/∂y, -∂ψ/∂x) を速度にする。発散が 0 になる。

どちらも周期 1 の正方形の領域で継ぎ目なくつながるようにし、領域から出た粒子は反対側から戻す。

* flow_traces.png: 粒子の軌跡（上）と、一様に置いた粒子を長く流した後の分布（下）
"""

from __future__ import annotations

import math
from collections.abc import Callable

import numpy as np
from PIL import Image, ImageDraw

from common import FloatArray, output_dir, save_figure, setup_matplotlib
from noise import fbm, perlin2

CELLS = 4  # 領域の 1 辺あたりのノイズの格子の数
Field = Callable[[FloatArray], FloatArray]


def potential(p: FloatArray) -> FloatArray:
    """位置 p (N, 2) のノイズの値。領域 [0, 1) × [0, 1) の周期でつながる。"""
    return fbm(perlin2, p[:, 0] * CELLS, p[:, 1] * CELLS, octaves=3, seed=11, period=CELLS)


def angle_field(p: FloatArray) -> FloatArray:
    """ノイズの値を角度にした単位ベクトルの場。"""
    angle = potential(p) * 2.0 * math.pi * 1.5
    return np.stack([np.cos(angle), np.sin(angle)], axis=1)


def curl_field(p: FloatArray, eps: float = 1e-4) -> FloatArray:
    """カールノイズ v = (∂ψ/∂y, -∂ψ/∂x)。偏微分は中心差分で近似する。

    速さをそろえるために正規化すると発散が 0 でなくなるので、一定の倍率を掛けるだけにする。
    """
    dx = np.array([eps, 0.0])
    dy = np.array([0.0, eps])
    dpsi_dx = (potential(p + dx) - potential(p - dx)) / (2.0 * eps)
    dpsi_dy = (potential(p + dy) - potential(p - dy)) / (2.0 * eps)
    return np.stack([dpsi_dy, -dpsi_dx], axis=1) * 0.12


def advect(p: FloatArray, field: Field, h: float) -> FloatArray:
    """中点法（2 次のルンゲ＝クッタ法）で、流れに沿って 1 歩進める。"""
    middle = p + field(p) * (h / 2.0)
    result: FloatArray = p + field(middle) * h
    return result


def draw_traces(field: Field, size: int, seed: int) -> FloatArray:
    """ランダムな位置から出発した粒子の軌跡を、半透明の線で重ね描きした画像。"""
    rng = np.random.default_rng(seed)
    p = rng.uniform(0.0, 1.0, (1500, 2))
    image = Image.new("RGB", (size, size), (250, 248, 243))
    draw = ImageDraw.Draw(image, "RGBA")
    for _ in range(100):
        q = advect(p, field, 0.005)
        # 領域の端をまたいだ線分は描かない（反対側へ戻るため）。
        jump = np.abs(np.floor(q) - np.floor(p)).sum(axis=1) > 0
        a = np.mod(p, 1.0) * size
        b = np.mod(q, 1.0) * size
        for (ax, ay), (bx, by), skip in zip(a.tolist(), b.tolist(), jump.tolist()):
            if not skip:
                draw.line([(ax, size - ay), (bx, size - by)], fill=(30, 60, 110, 50), width=1)
        p = q
    return np.asarray(image, dtype=np.float64) / 255.0


def long_run(field: Field, steps: int) -> FloatArray:
    """格子状に一様に置いた粒子を、長い時間流した後の位置。"""
    k = 70
    grid = (np.stack(np.meshgrid(np.arange(k), np.arange(k)), axis=-1).reshape(-1, 2) + 0.5) / k
    p = grid
    for _ in range(steps):
        p = np.mod(advect(p, field, 0.006), 1.0)
    return p


def draw_flow(file_name: str) -> None:
    import matplotlib.pyplot as plt

    fields = [("角度場（ノイズの値を向きにする）", angle_field), ("カールノイズ", curl_field)]
    figure, axes = plt.subplots(2, 2, figsize=(9, 9.4))
    for column, (title, field) in enumerate(fields):
        axes[0, column].imshow(draw_traces(field, 520, seed=1), extent=(0.0, 1.0, 0.0, 1.0))
        axes[0, column].set_title(title, fontsize=11)
        p = long_run(field, 250)
        axes[1, column].scatter(p[:, 0], p[:, 1], s=0.6, color="#1e3c6e")
        axes[1, column].set_title("一様に置いた粒子を流した後", fontsize=11)
        for ax in axes[:, column]:
            ax.set_xlim(0.0, 1.0)
            ax.set_ylim(0.0, 1.0)
            ax.set_aspect("equal")
            ax.set_xticks([])
            ax.set_yticks([])
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_flow("flow_traces.png")


if __name__ == "__main__":
    main()
