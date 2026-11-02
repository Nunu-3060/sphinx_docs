"""第 10 章「配置と散布」: 点の配置方法の比較と、ポアソンディスク・サンプリングの図を作る。

* point_sets.png: 一様乱数・ジッター付き格子・ポアソンディスクの点と、そのパワースペクトル
* spectrum_profile.png: パワースペクトルの動径方向の平均と、最近接点までの距離の分布
* bridson_step.png: Bridson の方法の 1 歩（活性な点の周りの円環に候補を作り、近すぎる候補を捨てる）
"""

from __future__ import annotations

import math

import numpy as np

from common import FloatArray, output_dir, save_figure, setup_matplotlib
from poisson_disk import bridson

COUNT_SIDE = 20  # ジッター付き格子の 1 辺の点の数（点は 400 個）
RADIUS = 0.04  # ポアソンディスクの半径（1 × 1 の正方形におよそ 400 個入る）
MAX_FREQUENCY = 40


def uniform_points(rng: np.random.Generator, count: int) -> FloatArray:
    """一様乱数で count 個の点を置く。"""
    return rng.random((count, 2))


def jittered_grid(rng: np.random.Generator, side: int, jitter: float = 1.0) -> FloatArray:
    """side × side の格子の各セルに 1 個ずつ、セルの中で無作為にずらした点を置く。

    jitter はずらす量（セルの幅に対する割合）で、0 なら規則正しい格子、1 ならセル全体に散らばる。
    """
    i, j = np.meshgrid(np.arange(side), np.arange(side))
    offsets = 0.5 + jitter * (rng.random((side, side, 2)) - 0.5)
    points = (np.stack([i, j], axis=-1) + offsets) / side
    return points.reshape(-1, 2)


def periodogram(points: FloatArray, max_frequency: int = MAX_FREQUENCY) -> FloatArray:
    """点の集まりのパワースペクトル |Σ exp(−2πi f·x)|² / N を、整数の周波数 f の格子で求める。

    点の並びにどの周波数（どの間隔・向き）の規則性があるかを表す。中心（周波数 0）は点の数で決まる
    定数なので 0 にする。
    """
    f = np.arange(-max_frequency, max_frequency + 1)
    fx, fy = np.meshgrid(f, f)
    phase = -2.0 * math.pi * (fx.reshape(-1, 1) * points[:, 0] + fy.reshape(-1, 1) * points[:, 1])
    total = np.exp(1j * phase).sum(axis=1)
    power = (np.abs(total) ** 2 / len(points)).reshape(fx.shape)
    power[max_frequency, max_frequency] = 0.0
    return power


def generators() -> list[tuple[str, str]]:
    return [("一様乱数", "#c44e52"), ("ジッター付き格子", "#dd8452"), ("ポアソンディスク", "#4c72b0")]


def make_points(name: str, seed: int) -> FloatArray:
    rng = np.random.default_rng(seed)
    if name == "一様乱数":
        return uniform_points(rng, COUNT_SIDE * COUNT_SIDE)
    if name == "ジッター付き格子":
        return jittered_grid(rng, COUNT_SIDE)
    return bridson(1.0, 1.0, RADIUS, rng)


def average_periodogram(name: str, trials: int = 10) -> FloatArray:
    """乱数のシードを変えて何回か作った点のスペクトルを平均する（1 回分だけでは値のばらつきが大きい）。"""
    result: FloatArray = np.mean([periodogram(make_points(name, seed)) for seed in range(trials)], axis=0)
    return result


def draw_point_sets(file_name: str, spectra: dict[str, FloatArray]) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(2, 3, figsize=(11, 7.4))
    for column, (name, color) in enumerate(generators()):
        points = make_points(name, seed=100)
        ax = axes[0, column]
        ax.scatter(points[:, 0], points[:, 1], s=6, color=color)
        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(0.0, 1.0)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"{name}（{len(points)} 点）", fontsize=10)

        ax = axes[1, column]
        extent = (-MAX_FREQUENCY - 0.5, MAX_FREQUENCY + 0.5, -MAX_FREQUENCY - 0.5, MAX_FREQUENCY + 0.5)
        ax.imshow(np.clip(spectra[name], 0.0, 2.5), cmap="gray", extent=extent, origin="lower")
        ax.set_title("パワースペクトル（中心が低い周波数）", fontsize=10)
        ax.set_xticks([-40, 0, 40])
        ax.set_yticks([-40, 0, 40])
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_profile(file_name: str, spectra: dict[str, FloatArray]) -> None:
    import matplotlib.pyplot as plt
    from scipy.spatial import cKDTree

    figure, axes = plt.subplots(1, 2, figsize=(11, 3.8))
    f = np.arange(-MAX_FREQUENCY, MAX_FREQUENCY + 1)
    fx, fy = np.meshgrid(f, f)
    radius = np.hypot(fx, fy)
    bins = np.arange(1, MAX_FREQUENCY + 1)
    for name, color in generators():
        spectrum = spectra[name]
        profile = [spectrum[(radius >= b - 0.5) & (radius < b + 0.5)].mean() for b in bins]
        axes[0].plot(bins, profile, color=color, label=name)

        distances = []
        for seed in range(10):
            points = make_points(name, seed)
            d, _ = cKDTree(points).query(points, k=2)
            distances.append(d[:, 1])
        axes[1].hist(np.concatenate(distances), bins=np.linspace(0.0, 0.08, 41), histtype="step", color=color,
                     label=name, linewidth=1.5, density=True)
    axes[0].axhline(1.0, color="#999999", linewidth=0.8, linestyle="--")
    axes[0].set_xlabel("周波数の大きさ |f|（1 辺あたりの波の数）")
    axes[0].set_ylabel("パワー（動径方向の平均）")
    axes[0].set_title("パワースペクトルの動径方向の平均", fontsize=10)
    axes[0].legend(fontsize=9)
    axes[1].axvline(RADIUS, color="#4c72b0", linewidth=0.8, linestyle="--")
    axes[1].set_xlabel("最も近い点までの距離")
    axes[1].set_yticks([])
    axes[1].set_title("最も近い点までの距離の分布（破線はポアソンディスクの半径）", fontsize=10)
    axes[1].legend(fontsize=9)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_bridson_step(file_name: str) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle

    radius = 0.1
    rng = np.random.default_rng(4)  # 24 番目の点が中央付近に来るシード
    points = bridson(1.0, 1.0, radius, rng)[:24]  # 生成の途中（最初の 24 点）の状態として見せる
    center = points[-1]

    figure, ax = plt.subplots(figsize=(6.4, 6.4))
    cell = radius / math.sqrt(2.0)
    for k in np.arange(0.0, 1.0 + 1e-9, cell):
        ax.axvline(k, color="#e4e4e4", linewidth=0.7, zorder=0)
        ax.axhline(k, color="#e4e4e4", linewidth=0.7, zorder=0)
    ax.add_patch(Circle(tuple(center), 2.0 * radius, color="#4c72b0", alpha=0.12))
    ax.add_patch(Circle(tuple(center), radius, color="white"))
    for point in points[:-1]:
        ax.add_patch(Circle(tuple(point), radius / 2.0, fill=False, edgecolor="#bbbbbb", linewidth=0.6))
    ax.scatter(points[:-1, 0], points[:-1, 1], s=16, color="#333333", label="置いた点", zorder=3)
    ax.scatter(center[0], center[1], s=40, color="#4c72b0", label="選んだ活性な点", zorder=4)

    # 円環の中に候補を作り、既存の点と近すぎるかで色分けする
    candidate_rng = np.random.default_rng(8)
    accepted_drawn = False
    rejected_drawn = False
    for _ in range(14):
        distance = radius * math.sqrt(candidate_rng.uniform(1.0, 4.0))
        angle = candidate_rng.uniform(0.0, 2.0 * math.pi)
        candidate = center + distance * np.array([math.cos(angle), math.sin(angle)])
        far = np.min(np.hypot(*(points - candidate).T)) >= radius - 1e-12
        inside = bool(np.all((candidate >= 0.0) & (candidate < 1.0)))
        if far and inside:
            ax.scatter(candidate[0], candidate[1], s=40, marker="o", facecolor="white", edgecolor="#55a868",
                       linewidth=1.8, zorder=4, label=None if accepted_drawn else "採用できる候補")
            accepted_drawn = True
        else:
            ax.scatter(candidate[0], candidate[1], s=40, marker="x", color="#c44e52", zorder=4,
                       label=None if rejected_drawn else "近すぎる（または範囲外の）候補")
            rejected_drawn = True
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=2, fontsize=8, frameon=False)
    ax.set_title("Bridson の方法の 1 歩。青い円環（r〜2r）に候補を作る\n灰色の円（半径 r/2）が重ならないことが条件", fontsize=10)
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    spectra = {name: average_periodogram(name) for name, _ in generators()}
    draw_point_sets("point_sets.png", spectra)
    draw_profile("spectrum_profile.png", spectra)
    draw_bridson_step("bridson_step.png")


if __name__ == "__main__":
    main()
