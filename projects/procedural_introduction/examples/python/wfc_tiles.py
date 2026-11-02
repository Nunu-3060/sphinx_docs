"""第 11 章「レベルとダンジョン」: Wave Function Collapse（タイルモデル）で地図を作る。

* wfc_tiles.png: タイルの一覧（辺の種類: 草・道・川）
* wfc_progress.png: 確定したセルが増えていく途中の様子と完成図
* wfc.mp4: 確定していく過程の動画
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from common import FloatArray, output_dir, save_figure, setup_matplotlib
from video import VideoWriter, find_ffmpeg

BoolArray = np.ndarray[Any, np.dtype[np.bool_]]

GRASS, ROAD, RIVER = 0, 1, 2
# 方向の番号: 0 = 上、1 = 右、2 = 下、3 = 左。OPPOSITE[d] は反対の方向、OFFSETS[d] は (dy, dx)
OPPOSITE = [2, 3, 0, 1]
OFFSETS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


@dataclass
class Tile:
    """タイル。sockets は上・右・下・左の辺の種類、weight は選ばれやすさ。"""

    name: str
    sockets: tuple[int, int, int, int]
    weight: float


def rotations(name: str, sockets: tuple[int, int, int, int], weight: float, count: int) -> list[Tile]:
    """タイルを 90 度ずつ count 通りに回したものを作る（右に 90 度回すと、上の辺が右へ移る）。"""
    tiles = []
    for k in range(count):
        rotated = tuple(sockets[(i - k) % 4] for i in range(4))
        tiles.append(Tile(f"{name}{k}", rotated, weight / count))  # type: ignore[arg-type]
    return tiles


def make_tiles() -> list[Tile]:
    """タイルの一覧。回転で同じになるものは、異なる向きの数だけ作る。"""
    tiles = [Tile("草", (GRASS, GRASS, GRASS, GRASS), 14.0)]
    tiles += rotations("道・直線", (ROAD, GRASS, ROAD, GRASS), 1.6, 2)
    tiles += rotations("道・曲がり角", (ROAD, ROAD, GRASS, GRASS), 1.0, 4)
    tiles += rotations("道・T 字路", (ROAD, ROAD, ROAD, GRASS), 0.3, 4)
    tiles += [Tile("道・十字路", (ROAD, ROAD, ROAD, ROAD), 0.1)]
    tiles += rotations("川・直線", (RIVER, GRASS, RIVER, GRASS), 1.4, 2)
    tiles += rotations("川・曲がり角", (RIVER, RIVER, GRASS, GRASS), 0.6, 4)
    tiles += rotations("橋", (ROAD, RIVER, ROAD, RIVER), 0.4, 2)
    return tiles


def compatibility(tiles: list[Tile]) -> BoolArray:
    """隣接の規則。allowed[d, a, b] は、タイル a の方向 d の隣にタイル b を置けるかどうか。

    向かい合う 2 つの辺の種類が同じなら置ける（a の右の辺と b の左の辺、など）。
    """
    n = len(tiles)
    allowed = np.zeros((4, n, n), dtype=bool)
    for d in range(4):
        for a in range(n):
            for b in range(n):
                allowed[d, a, b] = tiles[a].sockets[d] == tiles[b].sockets[OPPOSITE[d]]
    return allowed


class Contradiction(Exception):
    """候補が 1 つも残らないセルができた（矛盾）。"""


def propagate(wave: BoolArray, allowed: BoolArray, start: tuple[int, int]) -> None:
    """セル start の候補が減ったことを、隣へ、さらにその隣へと伝える（制約の伝播）。

    隣のセルの候補のうち、このセルに残っているどの候補とも隣り合えないものを消す。
    候補が減ったセルはスタックに積み、変化が無くなるまで繰り返す。
    """
    height, width, _ = wave.shape
    stack = [start]
    while stack:
        y, x = stack.pop()
        for d, (dy, dx) in enumerate(OFFSETS):
            ny, nx = y + dy, x + dx
            if not (0 <= ny < height and 0 <= nx < width):
                continue
            # このセルの候補のどれかと隣り合えるタイル（allowed の行の論理和）
            possible = allowed[d][wave[y, x]].any(axis=0)
            reduced = wave[ny, nx] & possible
            if not reduced.any():
                raise Contradiction
            if (reduced != wave[ny, nx]).any():
                wave[ny, nx] = reduced
                stack.append((ny, nx))


def lowest_entropy_cell(wave: BoolArray, weights: FloatArray, rng: np.random.Generator) -> tuple[int, int] | None:
    """まだ確定していないセルのうち、エントロピー（候補の不確かさ）が最小のセルを返す。全部確定なら None。

    候補の重みを w として H = log Σw − Σ(w log w) / Σw を計算する。同じ値のセルが多いので、
    ごく小さな乱数を足して選ぶセルをばらつかせる。
    """
    counts = wave.sum(axis=2)
    if (counts == 1).all():
        return None
    total = wave @ weights
    entropy = np.log(total) - (wave @ (weights * np.log(weights))) / total
    entropy = entropy + rng.random(entropy.shape) * 1e-6
    entropy[counts == 1] = np.inf
    y, x = np.unravel_index(int(np.argmin(entropy)), entropy.shape)
    return int(y), int(x)


def collapse(wave: BoolArray, weights: FloatArray, cell: tuple[int, int], rng: np.random.Generator) -> None:
    """セルの候補から、重みに比例する確率で 1 つを選んで確定させる（観測）。"""
    y, x = cell
    candidates = np.flatnonzero(wave[y, x])
    p = weights[candidates] / weights[candidates].sum()
    chosen = rng.choice(candidates, p=p)
    wave[y, x] = False
    wave[y, x, chosen] = True


def wave_function_collapse(tiles: list[Tile], width: int, height: int, seed: int,
                           snapshots: list[BoolArray] | None = None, max_restarts: int = 20) -> BoolArray:
    """WFC で width × height の地図を作り、確定した wave (height, width, タイル数) を返す。

    矛盾が起きたら、シードを変えて最初からやり直す（再始動）。snapshots を渡すと、
    セルを 1 個確定させるたびに wave の写しを追加する。
    """
    allowed = compatibility(tiles)
    weights = np.array([tile.weight for tile in tiles])
    for attempt in range(max_restarts):
        rng = np.random.default_rng(seed + attempt * 1000)
        wave = np.ones((height, width, len(tiles)), dtype=bool)  # 最初はどのセルも全タイルが候補
        if snapshots is not None:
            snapshots.clear()
        try:
            while (cell := lowest_entropy_cell(wave, weights, rng)) is not None:
                collapse(wave, weights, cell, rng)
                propagate(wave, allowed, cell)
                if snapshots is not None:
                    snapshots.append(wave.copy())
            return wave
        except Contradiction:
            continue
    raise RuntimeError("再始動しても矛盾が解消しなかった")


TILE_PIXELS = 12
COLORS = {GRASS: (0.56, 0.74, 0.42), ROAD: (0.62, 0.58, 0.52), RIVER: (0.30, 0.55, 0.85)}


def tile_image(tile: Tile) -> FloatArray:
    """タイルの画像（TILE_PIXELS 四方）。中心から、道・川の辺へ向かう帯を描く。"""
    size = TILE_PIXELS
    image = np.empty((size, size, 3))
    image[:] = COLORS[GRASS]
    middle = size // 2
    for kind, half in [(RIVER, 3), (ROAD, 2)]:  # 川を先に描き、橋の道を上に重ねる
        directions = [d for d in range(4) if tile.sockets[d] == kind]
        if not directions:
            continue
        lo, hi = middle - half, middle + half
        image[lo:hi, lo:hi] = COLORS[kind]
        for d in directions:
            if d == 0:
                image[:middle, lo:hi] = COLORS[kind]
            elif d == 1:
                image[lo:hi, middle:] = COLORS[kind]
            elif d == 2:
                image[middle:, lo:hi] = COLORS[kind]
            else:
                image[lo:hi, :middle] = COLORS[kind]
    return image


def render(wave: BoolArray, tiles: list[Tile]) -> FloatArray:
    """wave を画像にする。未確定のセルは、残っている候補のタイル画像の平均（重ね合わせ）で表す。"""
    images = np.array([tile_image(tile) for tile in tiles])  # (タイル数, p, p, 3)
    height, width, _ = wave.shape
    counts = wave.sum(axis=2, keepdims=True)
    mean = np.einsum("hwt,tpqc->hwpqc", wave / counts, images)
    undecided = (counts[..., 0] > 1)[..., None, None, None]
    mean = np.where(undecided, mean * 0.6 + 0.4, mean)  # 未確定のセルは白っぽくする
    result: FloatArray = mean.transpose(0, 2, 1, 3, 4).reshape(height * TILE_PIXELS, width * TILE_PIXELS, 3)
    return result


def draw_tiles(file_name: str, tiles: list[Tile]) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(2, 12, figsize=(13, 2.9))
    names = {GRASS: "草", ROAD: "道", RIVER: "川"}
    for ax, tile in zip(axes.ravel(), tiles):
        ax.imshow(tile_image(tile), interpolation="nearest")
        ax.set_title(tile.name, fontsize=8)
        ax.set_xlabel("".join(names[s] for s in tile.sockets), fontsize=8)
        ax.set_xticks([])
        ax.set_yticks([])
    for ax in axes.ravel()[len(tiles):]:
        ax.set_axis_off()
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_progress(file_name: str, snapshots: list[BoolArray], tiles: list[Tile]) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(2, 2, figsize=(11, 7.0))
    total = len(snapshots)
    for ax, fraction in zip(axes.ravel(), [0.0, 0.1, 0.5, 1.0]):
        index = max(int(fraction * total) - 1, 0)
        ax.imshow(render(snapshots[index], tiles), interpolation="nearest")
        ax.set_title(f"{index + 1} 回確定させた後" if fraction < 1.0 else "完成", fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def write_video(file_name: str, snapshots: list[BoolArray], tiles: list[Tile]) -> None:
    if find_ffmpeg() is None:
        print("ffmpeg が見つからないので動画を作らない")
        return
    first = render(snapshots[0], tiles)
    height, width = first.shape[:2]
    frames = list(range(0, len(snapshots), 4)) + [len(snapshots) - 1] * 45  # 最後に完成図を 1.5 秒止める
    with VideoWriter(output_dir(__file__) / file_name, width, height, fps=30) as writer:
        for index in frames:
            writer.write(render(snapshots[index], tiles))


def main() -> None:
    setup_matplotlib()
    tiles = make_tiles()
    snapshots: list[BoolArray] = []
    wave_function_collapse(tiles, 40, 24, seed=3, snapshots=snapshots)
    draw_tiles("wfc_tiles.png", tiles)
    draw_progress("wfc_progress.png", snapshots, tiles)
    write_video("wfc.mp4", snapshots, tiles)


if __name__ == "__main__":
    main()
