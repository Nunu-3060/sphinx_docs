"""第 11 章「レベルとダンジョン」: ランダムウォークとセル・オートマトンで洞窟を作る。

* drunkard_walk.png: ランダムウォーク（酔歩）で床を掘り進める様子
* cave_ca.png: 無作為に壁を置いた初期状態に、4-5 規則のセル・オートマトンを繰り返し適用した様子
* cave_regions.png: 連結成分のラベル付け、小さな領域の除去、通路による接続
"""

from __future__ import annotations

from typing import Any

import numpy as np
from scipy import ndimage
from scipy.spatial import cKDTree

from common import IntArray, output_dir, save_figure, setup_matplotlib

BoolArray = np.ndarray[Any, np.dtype[np.bool_]]

WIDTH, HEIGHT = 80, 50
STEPS = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])


def drunkard_walk(rng: np.random.Generator, floor_fraction: float, width: int = WIDTH,
                  height: int = HEIGHT) -> BoolArray:
    """中央から出発し、上下左右に無作為に 1 歩ずつ進みながら床を掘る。床の割合が floor_fraction になったら止める。

    返す配列は True が床。外周の 1 マスは必ず壁として残す。
    """
    floor = np.zeros((height, width), dtype=bool)
    x, y = width // 2, height // 2
    target = int(floor_fraction * width * height)
    dug = 0
    while dug < target:
        if not floor[y, x]:
            floor[y, x] = True
            dug += 1
        dx, dy = STEPS[rng.integers(4)]
        x = int(np.clip(x + dx, 1, width - 2))
        y = int(np.clip(y + dy, 1, height - 2))
    return floor


def random_walls(rng: np.random.Generator, wall_probability: float = 0.45) -> BoolArray:
    """各マスを確率 wall_probability で壁にした初期状態（True が壁）。"""
    walls: BoolArray = rng.random((HEIGHT, WIDTH)) < wall_probability
    return walls


def cave_step(walls: BoolArray) -> BoolArray:
    """4-5 規則のセル・オートマトンを 1 回適用する。

    壁のマスは周りの 8 マスのうち 4 マス以上が壁なら壁のまま、床のマスは 5 マス以上が壁なら壁になる。
    これは「自分を含む 3 × 3 の 9 マスのうち 5 マス以上が壁なら壁」と同じである。
    範囲の外は壁とみなす（洞窟が外周で閉じるようにする）。
    """
    padded = np.pad(walls, 1, constant_values=True).astype(np.int64)
    height, width = walls.shape
    count = np.zeros((height, width), dtype=np.int64)  # 自分を含む 3 × 3 の壁の数
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            count += padded[1 + dy:1 + dy + height, 1 + dx:1 + dx + width]
    result: BoolArray = count >= 5
    return result


def label_regions(floor: BoolArray) -> tuple[IntArray, int]:
    """床を上下左右のつながりで連結成分に分け、成分ごとの番号（1, 2, ...）の配列と成分の数を返す。"""
    labels, count = ndimage.label(floor)  # 既定の構造要素は上下左右の 4 近傍
    return labels.astype(np.int64), int(count)


def remove_small_regions(floor: BoolArray, min_size: int) -> BoolArray:
    """床の連結成分のうち、マスの数が min_size 未満のものを壁で埋める。"""
    labels, count = label_regions(floor)
    sizes = np.bincount(labels.ravel(), minlength=count + 1)
    keep = sizes >= min_size
    keep[0] = False  # 番号 0 は壁
    result: BoolArray = keep[labels]
    return result


def connect_regions(floor: BoolArray) -> BoolArray:
    """最大の連結成分に、ほかの成分を 1 本ずつ通路でつなぐ。

    各成分について、最大の成分のマスのうち最も近い 1 組を探し、その間を L 字の通路で掘る。
    つないだ成分は最大の成分に加え、次の成分は加えた後のものに対して最も近い所へつなぐ。
    """
    result = floor.copy()
    labels, count = label_regions(result)
    sizes = np.bincount(labels.ravel(), minlength=count + 1)
    sizes[0] = 0
    main = labels == int(np.argmax(sizes))
    for region in np.argsort(sizes)[::-1]:
        if region == 0 or sizes[region] == 0 or main[labels == region].all():
            continue
        main_cells = np.argwhere(main)
        region_cells = np.argwhere(labels == region)
        distances, nearest = cKDTree(main_cells).query(region_cells)
        k = int(np.argmin(distances))
        (y0, x0), (y1, x1) = region_cells[k], main_cells[nearest[k]]
        result[min(y0, y1):max(y0, y1) + 1, x0] = True  # 縦に掘ってから
        result[y1, min(x0, x1):max(x0, x1) + 1] = True  # 横に掘る
        main = main | (labels == region) | result & ~floor
    return result


WALL_COLOR = np.array([0.18, 0.18, 0.22])
FLOOR_COLOR = np.array([0.92, 0.88, 0.78])


def floor_image(floor: BoolArray) -> Any:
    return np.where(floor[..., None], FLOOR_COLOR, WALL_COLOR)


def show(ax: Any, image: Any, title: str) -> None:
    ax.imshow(image, interpolation="nearest")
    ax.set_title(title, fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])


def draw_drunkard(file_name: str) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 3, figsize=(12, 2.8))
    for ax, fraction in zip(axes, [0.1, 0.25, 0.4]):
        floor = drunkard_walk(np.random.default_rng(4), fraction)
        show(ax, floor_image(floor), f"床の割合 {fraction * 100:.0f} %")
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_ca(file_name: str) -> None:
    import matplotlib.pyplot as plt

    walls = random_walls(np.random.default_rng(11))
    figure, axes = plt.subplots(1, 4, figsize=(14, 2.6))
    step = 0
    for ax, target in zip(axes, [0, 1, 2, 5]):
        while step < target:
            walls = cave_step(walls)
            step += 1
        show(ax, floor_image(~walls), "初期状態（壁 45 %）" if target == 0 else f"{target} 回適用")
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_regions(file_name: str) -> None:
    import matplotlib.pyplot as plt

    walls = random_walls(np.random.default_rng(11), 0.5)  # 壁を多めにして、離れた小部屋ができるようにする
    for _ in range(5):
        walls = cave_step(walls)
    floor = ~walls
    labels, count = label_regions(floor)
    rng = np.random.default_rng(0)
    palette = np.vstack([WALL_COLOR, 0.35 + 0.6 * rng.random((count, 3))])
    cleaned = remove_small_regions(floor, 30)
    connected = connect_regions(cleaned)
    tunnels = connected & ~cleaned
    joined = floor_image(connected)
    joined[tunnels] = (0.85, 0.35, 0.3)

    figure, axes = plt.subplots(1, 3, figsize=(12, 2.8))
    show(axes[0], palette[labels], f"連結成分ごとに色分け（{count} 個）")
    show(axes[1], floor_image(cleaned), "30 マス未満の成分を埋めた")
    show(axes[2], joined, "残りを最大の成分へ通路（赤）でつないだ")
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_drunkard("drunkard_walk.png")
    draw_ca("cave_ca.png")
    draw_regions("cave_regions.png")


if __name__ == "__main__":
    main()
