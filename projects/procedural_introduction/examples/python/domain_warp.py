"""第 3 章「ノイズ」: ドメインワーピング（座標をノイズで歪める手法）の図を作る。

* warp_grid.png: 座標の歪みを、変形した格子線で示した図
* warp_strength.png: 歪みの強さを変えた 1 段のドメインワーピング
* domain_warp.png: ワープなし・1 段・2 段の比較と、色を付けた 2 段の結果
"""

from __future__ import annotations

import numpy as np

from color import gradient_map, hex_to_rgb
from common import FloatArray, grid, output_dir, save_figure, setup_matplotlib
from noise import fbm, perlin2
from texture import mix, show_panels

SIZE = 256


def offset(x: FloatArray, y: FloatArray, seed: int) -> tuple[FloatArray, FloatArray]:
    """座標ごとのずれのベクトル (qx, qy)。シードの異なる 2 つの fBm で x, y 成分を作る。"""
    qx = fbm(perlin2, x, y, octaves=4, seed=seed)
    qy = fbm(perlin2, x, y, octaves=4, seed=seed + 100)
    return qx, qy


def warped_fbm(x: FloatArray, y: FloatArray, strength: float, levels: int, seed: int = 0) -> FloatArray:
    """levels 段のドメインワーピングを施した fBm。levels = 0 なら普通の fBm になる。

    1 段目は元の座標でずれを求め、2 段目以降は前の段で歪めた座標でずれを求める。
    どの段でも、ずれは元の座標 (x, y) に加える。
    """
    wx, wy = x, y
    for level in range(levels):
        qx, qy = offset(wx, wy, seed + 10 * (level + 1))
        wx, wy = x + strength * qx, y + strength * qy
    return fbm(perlin2, wx, wy, octaves=5, seed=seed)


def to_unit(values: FloatArray) -> FloatArray:
    return np.clip(values * 0.5 + 0.5, 0.0, 1.0)


def draw_warp_grid(file_name: str) -> None:
    """規則的な格子線を warp で写し、空間がどう歪むかを見せる。"""
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 2, figsize=(8, 4.2))
    t = np.linspace(0.0, 3.0, 400)
    for ax, strength in zip(axes, (0.0, 0.4)):
        for k in np.linspace(0.0, 3.0, 16):
            constant = np.full_like(t, k)
            for xs, ys in ((t, constant), (constant, t)):
                qx, qy = offset(xs, ys, seed=11)
                ax.plot(xs + strength * qx, ys + strength * qy, color="#4c72b0", linewidth=0.8)
        ax.set_xlim(0.2, 2.8)
        ax.set_ylim(2.8, 0.2)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title("元の格子" if strength == 0.0 else f"ずらした格子（強さ {strength:g}）", fontsize=10)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_strength(file_name: str) -> None:
    x, y = grid(SIZE, SIZE, scale=3.0)
    strengths = (0.0, 0.5, 1.0, 2.0)
    images = [to_unit(warped_fbm(x, y, strength, levels=1) * 1.4) for strength in strengths]
    titles = [f"強さ {strength:g}" for strength in strengths]
    show_panels(images, titles, output_dir(__file__) / file_name)


def draw_domain_warp(file_name: str) -> None:
    x, y = grid(SIZE, SIZE, scale=3.0)
    plain = warped_fbm(x, y, 1.0, levels=0)
    one = warped_fbm(x, y, 1.0, levels=1)
    two = warped_fbm(x, y, 1.0, levels=2)
    # 色付け: 値をグラデーションマップで色にし、1 段目のずれの大きさで別の色を混ぜる。
    qx, qy = offset(x, y, seed=10)
    shift = np.clip(np.hypot(qx, qy) * 1.6, 0.0, 1.0)
    base = gradient_map(to_unit(two * 1.4), [
        (0.0, hex_to_rgb("#102a43")), (0.45, hex_to_rgb("#3e7cb1")), (0.7, hex_to_rgb("#e9d8a6")),
        (1.0, hex_to_rgb("#fffbea")),
    ])
    colored = mix(base, mix(base, np.array(hex_to_rgb("#ae2012")), np.full(shift.shape, 0.6)), shift ** 2)
    images = [to_unit(plain * 1.4), to_unit(one * 1.4), to_unit(two * 1.4), colored]
    titles = ["ワープなし（fBm）", "1 段のワープ", "2 段のワープ", "2 段のワープに色を付けた例"]
    show_panels(images, titles, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_warp_grid("warp_grid.png")
    draw_strength("warp_strength.png")
    draw_domain_warp("domain_warp.png")


if __name__ == "__main__":
    main()
