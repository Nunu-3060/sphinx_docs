"""第 13 章「群れと粒子」: ボイド（Reynolds、1987 年）と近傍探索。

各個体（ボイド）は、近くの仲間だけを見て次の 3 つの規則で向きを変える。

* 分離: 近すぎる仲間から離れる
* 整列: 仲間の平均の速度に合わせる
* 結合: 仲間の平均の位置に向かう

近くの仲間を探す処理（近傍探索）は、全組の距離を調べると個体数 n の 2 乗に比例して遅くなる。
ここでは scipy の k-d 木（cKDTree）を使って速くする。空間は上下・左右がつながったトーラスとする。

* boids_params.png: 規則の重みを変えたときの群れの形
* neighbor_timing.png: 総当たりと k-d 木の近傍探索の時間
* boids.mp4: 群れの動き
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass

import numpy as np
from scipy.spatial import cKDTree

from color import oklch_to_srgb
from common import FloatArray, IntArray, output_dir, save_figure, setup_matplotlib
from draw2d import Canvas, rgb
from video import VideoWriter, find_ffmpeg

WIDTH, HEIGHT, FPS, DURATION = 640, 360, 30, 10.0


@dataclass
class Rules:
    """ボイドの規則のパラメーター。"""

    radius: float = 0.12             # 仲間として見る距離
    separation_radius: float = 0.04  # これより近い仲間から離れる
    separation: float = 0.004        # 分離の強さ
    alignment: float = 1.0           # 整列の強さ
    cohesion: float = 1.0            # 結合の強さ
    min_speed: float = 0.25
    max_speed: float = 0.5


def wrap_offset(offset: FloatArray, box: FloatArray) -> FloatArray:
    """トーラス上で最も近い向きの差分にする（端をまたぐ近道を選ぶ）。"""
    result: FloatArray = offset - box * np.round(offset / box)
    return result


def pairs_kdtree(position: FloatArray, box: FloatArray, radius: float) -> IntArray:
    """距離 radius 以内の組 (i, j)（i < j）を k-d 木で探す。"""
    tree = cKDTree(position, boxsize=box)
    pairs: IntArray = tree.query_pairs(radius, output_type="ndarray").astype(np.int64)
    return pairs


def pairs_brute_force(position: FloatArray, box: FloatArray, radius: float, block: int = 512) -> IntArray:
    """距離 radius 以内の組 (i, j)（i < j）を、すべての組の距離を計算して探す。"""
    found = []
    for start in range(0, len(position), block):
        offset = wrap_offset(position[None, :, :] - position[start:start + block, None, :], box)
        distance2 = np.einsum("ijk,ijk->ij", offset, offset)
        i, j = np.nonzero(distance2 < radius * radius)
        i += start
        keep = i < j
        found.append(np.stack([i[keep], j[keep]], axis=1))
    return np.concatenate(found).astype(np.int64)


def steer(position: FloatArray, velocity: FloatArray, box: FloatArray, rules: Rules) -> FloatArray:
    """3 つの規則による加速度 (n, 2) を求める。"""
    n = len(position)
    pairs = pairs_kdtree(position, box, rules.radius)
    i, j = pairs[:, 0], pairs[:, 1]
    offset = wrap_offset(position[j] - position[i], box)  # i から j への向き
    distance2 = np.maximum(np.einsum("ij,ij->i", offset, offset), 1e-9)

    def accumulate(index: IntArray, values: FloatArray) -> FloatArray:
        return np.stack([np.bincount(index, values[:, k], n) for k in range(2)], axis=1)

    both = np.concatenate([i, j])
    count = np.bincount(both, minlength=n)[:, None].astype(np.float64)
    has_neighbor = count > 0
    count = np.maximum(count, 1.0)
    # 結合: 仲間の平均の位置（自分から見た相対位置の平均）へ向かう。
    center = accumulate(both, np.concatenate([offset, -offset])) / count
    # 整列: 仲間の平均の速度と自分の速度の差。
    mean_velocity = accumulate(both, np.concatenate([velocity[j], velocity[i]])) / count
    alignment = np.where(has_neighbor, mean_velocity - velocity, 0.0)
    # 分離: 近すぎる仲間から、距離の 2 乗に反比例する強さで離れる。
    close = distance2 < rules.separation_radius ** 2
    push = offset[close] / distance2[close][:, None]
    separation = accumulate(np.concatenate([i[close], j[close]]), np.concatenate([-push, push]))
    result: FloatArray = rules.separation * separation + rules.alignment * alignment + rules.cohesion * center
    return result


def step(position: FloatArray, velocity: FloatArray, box: FloatArray, rules: Rules,
         dt: float) -> tuple[FloatArray, FloatArray]:
    """1 ステップ進める。速さは min_speed〜max_speed に収める。"""
    velocity = velocity + steer(position, velocity, box, rules) * dt
    speed = np.linalg.norm(velocity, axis=1, keepdims=True)
    velocity = velocity / np.maximum(speed, 1e-9) * np.clip(speed, rules.min_speed, rules.max_speed)
    position = np.mod(position + velocity * dt, box)
    return position, velocity


def initial_state(count: int, box: FloatArray, seed: int) -> tuple[FloatArray, FloatArray]:
    rng = np.random.default_rng(seed)
    position = rng.uniform(0.0, 1.0, (count, 2)) * box
    angle = rng.uniform(0.0, 2.0 * math.pi, count)
    velocity = np.stack([np.cos(angle), np.sin(angle)], axis=1) * 0.35
    return position, velocity


def draw_params(file_name: str) -> None:
    import matplotlib.pyplot as plt

    box = np.array([3.2, 1.8])
    cases = [
        ("整列なし（alignment = 0）", Rules(alignment=0.0)),
        ("標準", Rules()),
        ("結合なし（cohesion = 0）", Rules(cohesion=0.0)),
    ]
    figure, axes = plt.subplots(1, 3, figsize=(14, 3.0))
    dt = 1.0 / 30.0
    for ax, (title, rules) in zip(axes, cases):
        position, velocity = initial_state(400, box, seed=1)
        for _ in range(int(15.0 / dt)):
            position, velocity = step(position, velocity, box, rules, dt)
        direction = velocity / np.linalg.norm(velocity, axis=1, keepdims=True)
        ax.quiver(position[:, 0], position[:, 1], direction[:, 0], direction[:, 1], angles="xy",
                  scale=40, width=0.004, color="#4c72b0")
        ax.set_xlim(0.0, box[0])
        ax.set_ylim(0.0, box[1])
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title, fontsize=11)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def measure(function: object, *args: object, repeat: int = 3) -> float:
    """関数を repeat 回呼んだときの最短の時間 [s]。"""
    best = math.inf
    for _ in range(repeat):
        start = time.perf_counter()
        function(*args)  # type: ignore[operator]
        best = min(best, time.perf_counter() - start)
    return best


def draw_timing(file_name: str) -> None:
    import matplotlib.pyplot as plt

    density = 400 / (3.2 * 1.8)  # 個体の密度を一定にして、仲間の数がほぼ変わらないようにする
    sizes = [250, 500, 1000, 2000, 4000, 8000, 16000, 32000]
    brute_times = []
    tree_times = []
    for n in sizes:
        side = math.sqrt(n / density / (16 / 9))
        box = np.array([side * 16 / 9, side])
        position, _ = initial_state(n, box, seed=2)
        tree_times.append(measure(pairs_kdtree, position, box, 0.12))
        if n <= 4000:
            brute_times.append(measure(pairs_brute_force, position, box, 0.12, repeat=1 if n > 2000 else 3))
            if n == 1000:  # 2 つの方法が同じ組を見つけることを確かめる
                a = {tuple(p) for p in pairs_kdtree(position, box, 0.12).tolist()}
                b = {tuple(p) for p in pairs_brute_force(position, box, 0.12).tolist()}
                assert a == b
    figure, ax = plt.subplots(figsize=(6, 3.8))
    ax.loglog(sizes[:len(brute_times)], np.array(brute_times) * 1000, "-o", label="総当たり（NumPy）")
    ax.loglog(sizes, np.array(tree_times) * 1000, "-o", label="k-d 木（cKDTree）")
    ax.set_xlabel("個体数 n")
    ax.set_ylabel("近傍探索 1 回の時間 [ms]")
    ax.grid(alpha=0.3, which="both")
    ax.legend()
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)
    for n, brute, tree in zip(sizes, brute_times + [math.nan] * len(sizes), tree_times):
        print(f"n = {n}: 総当たり {brute * 1000:.2f} ms、k-d 木 {tree * 1000:.2f} ms")


def render_video(file_name: str) -> None:
    box = np.array([3.2, 1.8])
    position, velocity = initial_state(400, box, seed=5)
    rules = Rules()
    dt = 1.0 / FPS
    for _ in range(int(4.0 / dt)):  # 群れがまとまるまで 4 秒ぶん進めておく
        position, velocity = step(position, velocity, box, rules, dt)
    shape = np.array([[0.045, 0.0], [-0.025, 0.018], [-0.015, 0.0], [-0.025, -0.018]])  # 進む向きが +x の矢じり
    with VideoWriter(output_dir(__file__) / file_name, WIDTH, HEIGHT, fps=FPS) as writer:
        for _ in range(int(DURATION * FPS)):
            for _ in range(2):
                position, velocity = step(position, velocity, box, rules, dt / 2)
            canvas = Canvas(WIDTH, HEIGHT, background=(0.08, 0.09, 0.13), center=(1.6, 0.9), scale=200.0)
            angle = np.arctan2(velocity[:, 1], velocity[:, 0])
            colors = oklch_to_srgb(np.full(len(angle), 0.75), np.full(len(angle), 0.12), angle)
            for p, a, color in zip(position, angle, colors):
                c, s = math.cos(a), math.sin(a)
                canvas.polygon(p + shape @ np.array([[c, s], [-s, c]]), fill=rgb(color))
            writer.write(canvas.to_array())


def main() -> None:
    setup_matplotlib()
    draw_params("boids_params.png")
    draw_timing("neighbor_timing.png")
    if find_ffmpeg() is None:
        print("ffmpeg が見つからないので動画を作らない")
        return
    render_video("boids.mp4")


if __name__ == "__main__":
    main()
