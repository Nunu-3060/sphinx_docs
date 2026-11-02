"""第 7 章「地形」: ハイトマップの生成（fBm とダイアモンドスクエア法）の図を作る。

* fbm_terrain.png: fBm のハイトマップと、色・陰影・高さの再配分・島のマスクによる整形
* diamond_square_rule.png: ダイアモンドスクエア法の 2 つの段階で値を決める点
* diamond_square_steps.png: 格子を細かくしていく途中経過
* diamond_square_roughness.png: 粗さのパラメーターによる違いと、fBm との比較
"""

from __future__ import annotations

import numpy as np

from common import FloatArray, normalize, output_dir, save_figure, setup_matplotlib
from heightmap import diamond_square, fbm_heightmap, island_mask, shaded_relief

SIZE = 256


def draw_fbm(file_name: str) -> None:
    import matplotlib.pyplot as plt

    h = fbm_heightmap(SIZE, seed=5, scale=3.0, octaves=6)
    redistributed = h ** 2.0
    island = normalize(h * 0.75 + 0.55 * island_mask(SIZE, 2.5))
    panels = [
        ("ハイトマップ（明るいほど高い）", np.repeat(h[..., None], 3, axis=2)),
        ("標高の色 + 陰影", shaded_relief(h)),
        ("高さを 2 乗（低地が広がる）", shaded_relief(normalize(redistributed))),
        ("島のマスクを足す", shaded_relief(island)),
    ]
    figure, axes = plt.subplots(1, 4, figsize=(12, 3.4))
    for ax, (title, image) in zip(axes, panels):
        ax.imshow(image)
        ax.set_title(title, fontsize=10)
        ax.set_axis_off()
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_rule(file_name: str) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 3, figsize=(10, 3.6))
    coords = np.arange(5)
    gx, gy = np.meshgrid(coords, coords)
    stages = [
        ("① 4 隅に乱数を置く", [(0, 0), (0, 4), (4, 0), (4, 4)], [], []),
        ("② ダイアモンド段階: 中心", [(0, 0), (0, 4), (4, 0), (4, 4)], [(2, 2)], [(0, 0), (0, 4), (4, 0), (4, 4)]),
        ("③ スクエア段階: 辺の中点", [(0, 0), (0, 4), (4, 0), (4, 4), (2, 2)], [(0, 2), (2, 0), (2, 4), (4, 2)],
         [(0, 0), (4, 0), (2, 2)]),
    ]
    for ax, (title, known, new, sources) in zip(axes, stages):
        ax.scatter(gx, gy, s=12, color="#cccccc")
        for p in known:
            ax.scatter([p[0]], [p[1]], s=90, color="#4c72b0", zorder=3)
        for p in new:
            ax.scatter([p[0]], [p[1]], s=110, color="#dd8452", marker="D", zorder=3)
        # 新しい点のうち 1 つについて、平均に使う点を線で結ぶ。
        if new:
            target = new[0] if len(new) == 1 else (2, 0)
            for p in sources:
                ax.plot([target[0], p[0]], [target[1], p[1]], color="#dd8452", linestyle="--", linewidth=1)
        ax.set_xlim(-0.5, 4.5)
        ax.set_ylim(-0.5, 4.5)
        ax.set_aspect("equal")
        ax.set_axis_off()
        ax.set_title(title, fontsize=10)
    axes[2].text(2, -0.45, "（地図の端では 3 点の平均）", ha="center", fontsize=9)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_steps(file_name: str) -> None:
    import matplotlib.pyplot as plt

    levels = 8
    h = diamond_square(levels, roughness=0.55, seed=2)
    figure, axes = plt.subplots(1, 5, figsize=(12, 2.8))
    for ax, level in zip(axes, [1, 2, 3, 5, 8]):
        # ダイアモンドスクエア法は一度決めた点を変えないので、完成した地図を間引くと途中の段階になる。
        step = 2 ** (levels - level)
        coarse: FloatArray = h[::step, ::step]
        ax.imshow(coarse, cmap="gray", vmin=0, vmax=1, interpolation="nearest")
        ax.set_title(f"{level} 段目（{coarse.shape[0]} × {coarse.shape[1]}）", fontsize=10)
        ax.set_axis_off()
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_roughness(file_name: str) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 4, figsize=(12, 3.4))
    for ax, roughness in zip(axes[:3], [0.45, 0.6, 0.75]):
        h = diamond_square(8, roughness=roughness, seed=2)[:SIZE, :SIZE]
        ax.imshow(shaded_relief(h))
        ax.set_title(f"ダイアモンドスクエア法（粗さ {roughness}）", fontsize=10)
        ax.set_axis_off()
    axes[3].imshow(shaded_relief(fbm_heightmap(SIZE, seed=2, scale=3.0, octaves=8, gain=0.6)))
    axes[3].set_title("比較: fBm（gain 0.6）", fontsize=10)
    axes[3].set_axis_off()
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_fbm("fbm_terrain.png")
    draw_rule("diamond_square_rule.png")
    draw_steps("diamond_square_steps.png")
    draw_roughness("diamond_square_roughness.png")


if __name__ == "__main__":
    main()
