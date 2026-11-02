"""第 5 章「規則から生まれる模様」: セル・オートマトンの図と動画を作る。

* rule_table.png: ルール 30 の規則表（近傍の 8 通りの並びと、次の状態）
* elementary.png: 1 次元セル・オートマトン（ルール 30・90・110・184）の時間発展
* cyclic.png: 2 次元の巡回セル・オートマトンが渦巻きを作る様子
* majority.png: 多数決の規則でノイズが塊にまとまる様子
* cyclic.mp4: 巡回セル・オートマトンの動画（6 秒）
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from color import cosine_palette
from common import FloatArray, output_dir, save_figure, setup_matplotlib
from texture import show_panels
from video import VideoWriter, find_ffmpeg

IntGrid = NDArray[np.int64]


def elementary(rule: int, width: int, steps: int, random_start: bool = False, seed: int = 0) -> IntGrid:
    """1 次元セル・オートマトン（基本セル・オートマトン）を steps 世代計算し、(steps, width) で返す。

    各セルの次の状態は、自分と左右の 3 セルの状態（8 通り）で決まる。3 セルを 2 進数の
    (左, 中, 右) と読んだ番号 0〜7 について、ルール番号 rule の該当する bit が次の状態になる。
    端は反対側とつながる。
    """
    table = np.array([(rule >> index) & 1 for index in range(8)], dtype=np.int64)
    rows = np.zeros((steps, width), dtype=np.int64)
    if random_start:
        rows[0] = np.random.default_rng(seed).integers(0, 2, width)
    else:
        rows[0, width // 2] = 1  # 中央の 1 セルだけ 1 にする
    for t in range(1, steps):
        left = np.roll(rows[t - 1], 1)
        right = np.roll(rows[t - 1], -1)
        rows[t] = table[4 * left + 2 * rows[t - 1] + right]
    return rows


def cyclic_step(state: IntGrid, states: int, threshold: int) -> IntGrid:
    """巡回セル・オートマトンを 1 歩進める。

    状態 s のセルは、周囲 8 セルのうち「次の状態 (s + 1) mod states」のセルが threshold 個以上あれば、
    その状態に進む。食物連鎖のように、次の状態が今の状態を侵食していく。
    """
    successor = (state + 1) % states
    count = np.zeros_like(state)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx or dy:
                count += np.roll(state, (dy, dx), axis=(0, 1)) == successor
    return np.where(count >= threshold, successor, state)


def majority_step(state: IntGrid) -> IntGrid:
    """多数決の規則。自分を含む 3 × 3 の 9 セルのうち 5 個以上が 1 なら 1、そうでなければ 0 にする。"""
    total = np.zeros_like(state)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            total += np.roll(state, (dy, dx), axis=(0, 1))
    return (total >= 5).astype(np.int64)


def draw_rule_table(file_name: str, rule: int = 30) -> None:
    """近傍の 8 通りの並びと、そのときの次の状態を図にする。"""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    figure, ax = plt.subplots(figsize=(10, 2.0))
    for slot, index in enumerate(range(7, -1, -1)):
        x0 = slot * 4.5
        for position in range(3):
            bit = (index >> (2 - position)) & 1
            ax.add_patch(Rectangle((x0 + position, 1.2), 1, 1, facecolor="#222222" if bit else "white",
                                   edgecolor="#555555"))
        bit = (rule >> index) & 1
        ax.add_patch(Rectangle((x0 + 1, 0), 1, 1, facecolor="#dd8452" if bit else "white", edgecolor="#555555"))
        ax.text(x0 + 1.5, -0.45, str(bit), ha="center", va="center", fontsize=11)
    ax.set_xlim(-0.5, 8 * 4.5)
    ax.set_ylim(-0.9, 2.4)
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.set_title(f"ルール {rule}（2 進数 {rule:08b}）: 上段が (左, 中, 右) の並び、下段が次の状態", fontsize=10)
    save_figure(figure, output_dir(__file__) / file_name)


def draw_elementary(file_name: str) -> None:
    width, steps = 161, 80
    cases = [(30, False), (90, False), (110, True), (184, True)]
    images = [1.0 - elementary(rule, width, steps, random_start, seed=rule).astype(np.float64)
              for rule, random_start in cases]
    titles = [f"ルール {rule}（{'ランダムな初期状態' if random_start else '中央の 1 セルから'}）"
              for rule, random_start in cases]
    show_panels(images, titles, output_dir(__file__) / file_name, columns=2, size=4.4,
                interpolation="nearest")


def cyclic_colors(state: IntGrid, states: int) -> FloatArray:
    return cosine_palette(state / states, d=(0.0, 0.15, 0.3))


def draw_cyclic(file_name: str, size: int = 160, states: int = 14) -> None:
    rng = np.random.default_rng(4)
    state = rng.integers(0, states, (size, size)).astype(np.int64)
    checkpoints = (0, 30, 100, 400)
    images = []
    done = 0
    for checkpoint in checkpoints:
        for _ in range(checkpoint - done):
            state = cyclic_step(state, states, threshold=1)
        done = checkpoint
        images.append(cyclic_colors(state, states))
    show_panels(images, [f"{n} 世代" for n in checkpoints], output_dir(__file__) / file_name, interpolation="nearest")


def draw_majority(file_name: str, size: int = 160) -> None:
    rng = np.random.default_rng(5)
    state = (rng.random((size, size)) < 0.5).astype(np.int64)
    checkpoints = (0, 1, 3, 10)
    images = []
    done = 0
    for checkpoint in checkpoints:
        for _ in range(checkpoint - done):
            state = majority_step(state)
        done = checkpoint
        images.append(state.astype(np.float64))
    show_panels(images, [f"{n} 回" for n in checkpoints], output_dir(__file__) / file_name, interpolation="nearest")


def write_cyclic_video(file_name: str, seconds: int = 6, fps: int = 30, states: int = 14) -> None:
    """160 × 90 のセルで計算し、1 セルを 4 × 4 画素に拡大して 640 × 360 の動画にする。"""
    rng = np.random.default_rng(6)
    state = rng.integers(0, states, (90, 160)).astype(np.int64)
    with VideoWriter(output_dir(__file__) / file_name, 640, 360, fps=fps) as writer:
        for _ in range(seconds * fps):
            frame = cyclic_colors(state, states)
            writer.write(np.repeat(np.repeat(frame, 4, axis=0), 4, axis=1))
            state = cyclic_step(state, states, threshold=1)


def main() -> None:
    setup_matplotlib()
    draw_rule_table("rule_table.png")
    draw_elementary("elementary.png")
    draw_cyclic("cyclic.png")
    draw_majority("majority.png")
    if find_ffmpeg() is None:
        print("ffmpeg が見つからないので動画を作らない")
        return
    write_cyclic_video("cyclic.mp4")


if __name__ == "__main__":
    main()
