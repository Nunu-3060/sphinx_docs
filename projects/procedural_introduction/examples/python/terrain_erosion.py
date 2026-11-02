"""第 7 章「地形」: 熱侵食と、水滴による水力侵食。

* erosion.png: 元の地形、熱侵食、水力侵食、両方を順に適用した地形の比較（陰影起伏図）
* erosion_detail.png: 水力侵食の前後の拡大図と、削られた所・積もった所の分布
* erosion.mp4: 水滴を落としていく途中経過（ffmpeg がある場合）

eroded_terrain() は、ほかのスクリプト（川・バイオーム・地形メッシュ）からも使う。
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from common import FloatArray, IntArray, output_dir, save_figure, setup_matplotlib, to_bytes
from heightmap import SEA_LEVEL, base_terrain, shaded_relief

# 8 近傍の位置のずれ (dy, dx) と距離
NEIGHBORS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def thermal_erosion(heights: FloatArray, iterations: int = 50, talus: float = 0.6, rate: float = 0.5,
                    height_scale: float = 48.0) -> FloatArray:
    """熱侵食。隣との高さの差が安息角を超える斜面から、超えた分の一部を低い隣へ崩す。

    talus は安息角の正接（傾き）、rate は 1 回に崩す割合。高さは height_scale 倍して格子の
    間隔と同じ単位で傾きを比べる。
    """
    h = heights * height_scale
    rows, columns = h.shape
    for _ in range(iterations):
        padded = np.pad(h, 1, mode="edge")
        excess = []
        for dy, dx in NEIGHBORS:
            neighbor = padded[1 + dy:1 + dy + rows, 1 + dx:1 + dx + columns]
            distance = float(np.hypot(dy, dx))
            excess.append(np.maximum(h - neighbor - talus * distance, 0.0))
        stacked = np.stack(excess)
        total = stacked.sum(axis=0)
        # 最も急な向きの超過分の半分を上限に動かす（動かしすぎて凹凸が逆転しないように）。
        moved = rate * 0.5 * stacked.max(axis=0)
        share = np.where(total > 0, moved / np.maximum(total, 1e-12), 0.0)
        change = -moved
        received = np.zeros((rows + 2, columns + 2))
        for (dy, dx), part in zip(NEIGHBORS, stacked):
            received[1 + dy:1 + dy + rows, 1 + dx:1 + dx + columns] += part * share
        # 端の外側の隣は端と同じ高さとみなすので（mode="edge"）、地図の外へは崩れない。
        change = change + received[1:-1, 1:-1]
        h = h + change
    result: FloatArray = h / height_scale
    return result


@dataclass
class DropletParameters:
    """水滴による水力侵食のパラメーター（Lague の実装の値を参考に、本章の地形に合わせて調整した）。"""

    inertia: float = 0.05  # 前の進行方向を保つ割合（0 なら常に最も急な向きへ進む）
    capacity: float = 2.0  # 運べる土砂の量の係数
    min_capacity: float = 0.01  # 平らな所でも運べる最小の量
    erode_rate: float = 0.1  # 余裕の何割を削るか
    deposit_rate: float = 0.1  # 超過分の何割を落とすか
    evaporation: float = 0.01  # 1 歩ごとに蒸発する水の割合
    gravity: float = 4.0  # 下り坂での加速
    lifetime: int = 30  # 最大の歩数
    radius: int = 3  # 削るときの範囲（ブラシの半径）
    sea_level: float = SEA_LEVEL  # 水滴が海に入ったら、土砂をすべて落として消える


def _brush(radius: int) -> tuple[IntArray, IntArray, FloatArray]:
    """半径 radius の円の中の位置のずれと、中心ほど大きい重み（合計 1）。"""
    offsets = [(dy, dx) for dy in range(-radius, radius + 1) for dx in range(-radius, radius + 1)
               if dy * dy + dx * dx <= radius * radius]
    dy = np.array([o[0] for o in offsets])
    dx = np.array([o[1] for o in offsets])
    weight = np.maximum(radius - np.hypot(dy, dx), 0.0) + 1e-3
    return dy, dx, weight / weight.sum()


def _height_and_gradient(h: FloatArray, x: FloatArray, y: FloatArray) -> tuple[FloatArray, FloatArray, FloatArray]:
    """位置 (x, y) の高さと勾配を、周りの 4 つの格子点から双線形補間で求める。"""
    ix = x.astype(np.int64)
    iy = y.astype(np.int64)
    fx = x - ix
    fy = y - iy
    h00 = h[iy, ix]
    h10 = h[iy, ix + 1]
    h01 = h[iy + 1, ix]
    h11 = h[iy + 1, ix + 1]
    gx = (h10 - h00) * (1 - fy) + (h11 - h01) * fy
    gy = (h01 - h00) * (1 - fx) + (h11 - h10) * fx
    height = h00 * (1 - fx) * (1 - fy) + h10 * fx * (1 - fy) + h01 * (1 - fx) * fy + h11 * fx * fy
    return height, gx, gy


def hydraulic_erosion(heights: FloatArray, droplets: int, seed: int = 0, batch: int = 500,
                      parameters: DropletParameters | None = None,
                      snapshots: list[FloatArray] | None = None) -> FloatArray:
    """水滴による水力侵食。

    地図の上のランダムな位置に水滴を落とし、斜面を下らせる。水滴は速さと水の量に応じて
    運べる土砂の量（運搬容量）を持ち、容量に余裕があれば地面を削って土砂を取り込み、
    超えていれば土砂を落とす。batch 個の水滴を同時に動かして NumPy で計算を速くする
    （同時に動く水滴どうしの影響は 1 歩遅れて伝わる）。snapshots にリストを渡すと、
    batch ごとの途中経過の高さを追加する。
    """
    p = DropletParameters() if parameters is None else parameters
    rng = np.random.default_rng(seed)
    h = heights.copy()
    rows, columns = h.shape
    flat = h.reshape(-1)  # h と同じメモリーを指す 1 次元の配列
    brush_dy, brush_dx, brush_w = _brush(p.radius)
    for start in range(0, droplets, batch):
        n = min(batch, droplets - start)
        x = rng.uniform(0, columns - 1, n)
        y = rng.uniform(0, rows - 1, n)
        dir_x = np.zeros(n)
        dir_y = np.zeros(n)
        speed = np.ones(n)
        water = np.ones(n)
        sediment = np.zeros(n)
        alive = h[y.astype(np.int64), x.astype(np.int64)] >= p.sea_level  # 海の上に落ちた水滴は使わない
        for _ in range(p.lifetime):
            ix = x.astype(np.int64)
            iy = y.astype(np.int64)
            fx = x - ix
            fy = y - iy
            height, gx, gy = _height_and_gradient(h, x, y)
            # 進む向き: 前の向きと、坂を下る向き（勾配の逆）を混ぜる。
            dir_x = dir_x * p.inertia - gx * (1 - p.inertia)
            dir_y = dir_y * p.inertia - gy * (1 - p.inertia)
            length = np.hypot(dir_x, dir_y)
            alive &= length > 1e-12
            dir_x = np.where(alive, dir_x / np.maximum(length, 1e-12), 0.0)
            dir_y = np.where(alive, dir_y / np.maximum(length, 1e-12), 0.0)
            new_x = x + dir_x
            new_y = y + dir_y
            alive &= (new_x >= 0) & (new_x < columns - 1) & (new_y >= 0) & (new_y < rows - 1)
            new_x = np.where(alive, new_x, x)
            new_y = np.where(alive, new_y, y)
            new_height, _, _ = _height_and_gradient(h, new_x, new_y)
            delta = new_height - height  # 下りなら負
            capacity = np.maximum(-delta * speed * water * p.capacity, p.min_capacity)
            in_sea = alive & (new_height < p.sea_level)
            depositing = alive & ((sediment > capacity) | (delta > 0) | in_sea)
            eroding = alive & ~depositing
            # 堆積: 上り坂なら穴を埋める分だけ、海に入ったらすべて、そうでなければ超過分の一部を、
            # 今いる 4 点に配る。
            deposit = np.where(delta > 0, np.minimum(delta, sediment), (sediment - capacity) * p.deposit_rate)
            deposit = np.where(in_sea, sediment, deposit)
            deposit = np.where(depositing, deposit, 0.0)
            corner_index = [iy * columns + ix, iy * columns + ix + 1, (iy + 1) * columns + ix,
                            (iy + 1) * columns + ix + 1]
            corner_weight = [(1 - fx) * (1 - fy), fx * (1 - fy), (1 - fx) * fy, fx * fy]
            for index, weight in zip(corner_index, corner_weight):
                flat += np.bincount(index, deposit * weight, minlength=flat.size)
            # 侵食: 容量の余裕の一部を、周りの円の範囲から削る（下りの高さの差より多くは削らない）。
            erode = np.where(eroding, np.minimum((capacity - sediment) * p.erode_rate, -delta), 0.0)
            by = iy[:, None] + brush_dy[None, :]
            bx = ix[:, None] + brush_dx[None, :]
            inside = (by >= 0) & (by < rows) & (bx >= 0) & (bx < columns)
            amount = erode[:, None] * brush_w[None, :] * inside
            index = np.clip(by, 0, rows - 1) * columns + np.clip(bx, 0, columns - 1)
            flat -= np.bincount(index.ravel(), amount.ravel(), minlength=flat.size)
            sediment = sediment - deposit + amount.sum(axis=1)
            # 下るほど速くなり、水は少しずつ蒸発する。
            speed = np.sqrt(np.maximum(speed * speed - delta * p.gravity, 0.0))
            water = water * (1 - p.evaporation)
            x, y = new_x, new_y
            alive &= ~in_sea
            if not alive.any():
                break
        if snapshots is not None:
            snapshots.append(h.copy())
    return h


def eroded_terrain(size: int = 256, droplets: int = 150000) -> FloatArray:
    """base_terrain に水力侵食と軽い熱侵食をかけた地形（川・バイオーム・メッシュの章で使う）。"""
    h = hydraulic_erosion(base_terrain(size), droplets, seed=1)
    return thermal_erosion(h, iterations=10)


def draw_comparison(file_name: str, original: FloatArray, thermal: FloatArray, hydraulic: FloatArray,
                    both: FloatArray) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 4, figsize=(12, 3.4))
    titles = ["元の地形（fBm）", "熱侵食（50 回）", "水力侵食（水滴 15 万個）", "水力侵食 + 熱侵食"]
    for ax, title, h in zip(axes, titles, [original, thermal, hydraulic, both]):
        ax.imshow(shaded_relief(h))
        ax.set_title(title, fontsize=10)
        ax.set_axis_off()
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_detail(file_name: str, original: FloatArray, eroded: FloatArray) -> None:
    import matplotlib.pyplot as plt

    window = (slice(60, 188), slice(70, 198))
    figure, axes = plt.subplots(1, 3, figsize=(12, 4.0))
    axes[0].imshow(shaded_relief(original)[window])
    axes[0].set_title("侵食前（中央部を拡大）", fontsize=10)
    axes[1].imshow(shaded_relief(eroded)[window])
    axes[1].set_title("水力侵食後", fontsize=10)
    change = (eroded - original)[window]
    limit = float(np.percentile(np.abs(change), 99))
    image = axes[2].imshow(change, cmap="RdBu", vmin=-limit, vmax=limit)
    axes[2].set_title("高さの変化（赤: 削られた、青: 積もった）", fontsize=10)
    for ax in axes:
        ax.set_axis_off()
    figure.colorbar(image, ax=axes[2], fraction=0.046, pad=0.02)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def write_video(file_name: str, snapshots: list[FloatArray]) -> None:
    from video import VideoWriter, find_ffmpeg

    if find_ffmpeg() is None:
        print("ffmpeg が見つからないので動画を作らない")
        return
    from PIL import Image

    size = 360
    with VideoWriter(output_dir(__file__) / file_name, size, size, fps=30) as writer:
        frames = [snapshots[0]] * 15 + snapshots[::3] + [snapshots[-1]] * 30
        for h in frames:
            image = Image.fromarray(to_bytes(shaded_relief(h))).resize((size, size), Image.Resampling.BILINEAR)
            writer.write(np.asarray(image))


def main() -> None:
    setup_matplotlib()
    original = base_terrain()
    snapshots: list[FloatArray] = [original]
    hydraulic = hydraulic_erosion(original, 150000, seed=1, snapshots=snapshots)
    thermal = thermal_erosion(original, iterations=50)
    both = thermal_erosion(hydraulic, iterations=10)
    draw_comparison("erosion.png", original, thermal, hydraulic, both)
    draw_detail("erosion_detail.png", original, hydraulic)
    write_video("erosion.mp4", snapshots)


if __name__ == "__main__":
    main()
