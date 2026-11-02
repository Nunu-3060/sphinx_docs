"""第 4 章「パターンとマテリアル」: 繰り返し可能（シームレス）なテクスチャの図を作る。

* seamless.png: 周期を持たないノイズと、周期 period のノイズを 2 × 2 に並べた比較
"""

from __future__ import annotations

import numpy as np

from common import FloatArray, grid, output_dir, save_figure, setup_matplotlib
from noise import fbm, perlin2, worley2

TILE = 160  # 1 枚のテクスチャの画素数
PERIOD = 4  # テクスチャ 1 枚に入る格子の数


def tile_texture(periodic: bool, kind: str) -> FloatArray:
    """1 枚分のテクスチャ。periodic なら、右端と左端、上端と下端がつながる。"""
    x, y = grid(TILE, TILE, scale=float(PERIOD))  # 座標は 0〜PERIOD
    period = PERIOD if periodic else None
    if kind == "fbm":
        return np.clip(fbm(perlin2, x, y, octaves=5, seed=3, period=period) * 1.1 + 0.5, 0.0, 1.0)
    f1, f2, _ = worley2(x, y, seed=3, period=period)
    return np.clip((f2 - f1) * 2.0, 0.0, 1.0)


def draw_seamless(file_name: str) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 4, figsize=(13, 3.6))
    cases = [("fbm", False, "fBm（周期なし）"), ("fbm", True, f"fBm（period = {PERIOD}）"),
             ("worley", False, "セルラー（周期なし）"), ("worley", True, f"セルラー（period = {PERIOD}）")]
    for ax, (kind, periodic, title) in zip(axes, cases):
        texture = tile_texture(periodic, kind)
        ax.imshow(np.tile(texture, (2, 2)), cmap="gray", vmin=0, vmax=1)  # 同じ画像を 2 × 2 に並べる
        # 継ぎ目の位置を、画像の外側に置いた三角の印で示す（画像の上には線を引かない）。
        ax.plot([TILE - 0.5], [-8], marker="v", color="#dd8452", markersize=8, clip_on=False)
        ax.plot([-8], [TILE - 0.5], marker=">", color="#dd8452", markersize=8, clip_on=False)
        ax.set_title(title, fontsize=10)
        ax.set_axis_off()
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_seamless("seamless.png")


if __name__ == "__main__":
    main()
