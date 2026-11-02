"""第 5 章「規則から生まれる模様」: 例示からのテクスチャ合成（Wave Function Collapse の重複モデル）。

小さな見本の画像から N × N の小片（パターン）をすべて切り出し、隣り合う小片が重なり部分で
一致するように、出力の各セルの小片を 1 つずつ決めていく。

* wfc_results.png: 2 種類の見本と、それぞれから合成した結果
* wfc_progress.png: 合成の途中経過（未確定のセルは、候補の色の平均で表示する）
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from color import hex_to_rgb
from common import FloatArray, output_dir, save_figure, setup_matplotlib

BoolArray = NDArray[np.bool_]
IntArray = NDArray[np.int64]

# 見本 1: 入れ子の四角形（線の模様）
SAMPLE_LINES = [
    "..........",
    ".########.",
    ".#......#.",
    ".#.####.#.",
    ".#.#..#.#.",
    ".#.#..#.#.",
    ".#.####.#.",
    ".#......#.",
    ".########.",
    "..........",
]
# 見本 2: 海（w）に浮かぶ島。砂浜（s）が草地（g）を囲む
SAMPLE_ISLAND = [
    "wwwwwwwwwwww",
    "wwwwssswwwww",
    "wwwsgggsswww",
    "wwsggggggsww",
    "wwsgggggswww",
    "wwwssgggswww",
    "wwwwwssswwww",
    "wwwwwwwwwwww",
    "wwwwwwwwwwww",
    "wwwwwwwwssww",
    "wwwwwwwsggsw",
    "wwwwwwwwssww",
]
PALETTE = {
    ".": hex_to_rgb("#f4efe6"), "#": hex_to_rgb("#2b2d42"),
    "w": hex_to_rgb("#3d7ab8"), "s": hex_to_rgb("#e9d8a6"), "g": hex_to_rgb("#6a994e"),
}
# 隣のセルの向き (dy, dx): 下・上・右・左
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


@dataclass
class Patterns:
    """見本から切り出した小片の一覧。"""

    tiles: IntArray  # (P, N, N): 各小片の色の番号
    weights: FloatArray  # (P,): 見本の中での出現回数
    compatible: BoolArray  # (4, P, P): compatible[d, a, b] は、a の d 側の隣に b を置けるか


def to_indices(rows: list[str]) -> tuple[IntArray, list[str]]:
    """文字で書いた見本を、色の番号の 2 次元配列にする。"""
    symbols = sorted({c for row in rows for c in row})
    image = np.array([[symbols.index(c) for c in row] for row in rows], dtype=np.int64)
    return image, symbols


def extract_patterns(sample: IntArray, n: int, symmetry: bool) -> Patterns:
    """見本から N × N の小片をすべて切り出し、重複をまとめて数える。見本の端は反対側とつながるとみなす。"""
    height, width = sample.shape
    counts: dict[bytes, int] = {}
    tiles: dict[bytes, IntArray] = {}
    variants = [sample]
    if symmetry:  # 回転と鏡映を加えると、少ない見本からでも多様な結果が出る
        variants = [np.rot90(sample, r) for r in range(4)]
        variants += [np.fliplr(v) for v in variants]
    for image in variants:
        height, width = image.shape
        for y in range(height):
            for x in range(width):
                tile = np.take(np.take(image, range(y, y + n), axis=0, mode="wrap"), range(x, x + n), axis=1,
                               mode="wrap")
                key = tile.tobytes()
                counts[key] = counts.get(key, 0) + 1
                tiles[key] = tile
    keys = list(tiles)
    stack = np.array([tiles[k] for k in keys])
    weights = np.array([counts[k] for k in keys], dtype=np.float64)
    # 2 つの小片を 1 セルずらして重ねたとき、重なる部分が一致すれば隣に置ける。
    compatible = np.zeros((4, len(keys), len(keys)), dtype=bool)
    for d, (dy, dx) in enumerate(DIRECTIONS):
        a = stack[:, max(dy, 0):n + min(dy, 0), max(dx, 0):n + min(dx, 0)]
        b = stack[:, max(-dy, 0):n + min(-dy, 0), max(-dx, 0):n + min(-dx, 0)]
        compatible[d] = (a[:, None] == b[None, :]).all(axis=(2, 3))
    return Patterns(stack, weights, compatible)


class Contradiction(Exception):
    """候補が 1 つも残らないセルが生じた。"""


def propagate(wave: BoolArray, patterns: Patterns, start: tuple[int, int]) -> None:
    """start のセルの候補が減ったことを、周りのセルへ伝える（出力の端は反対側とつながる）。"""
    height, width, _ = wave.shape
    stack = [start]
    while stack:
        y, x = stack.pop()
        for d, (dy, dx) in enumerate(DIRECTIONS):
            ny, nx = (y + dy) % height, (x + dx) % width
            # このセルに残る候補のどれかと両立する小片だけを、隣のセルに残す。
            allowed = patterns.compatible[d][wave[y, x]].any(axis=0)
            reduced = wave[ny, nx] & allowed
            if not reduced.any():
                raise Contradiction
            if (reduced != wave[ny, nx]).any():
                wave[ny, nx] = reduced
                stack.append((ny, nx))


def observe(wave: BoolArray, patterns: Patterns, rng: np.random.Generator) -> tuple[int, int] | None:
    """候補が最も少ない（エントロピーが最小の）未確定セルを選び、重みに従って小片を 1 つに決める。"""
    weighted = wave * patterns.weights
    totals = weighted.sum(axis=2)
    # シャノンのエントロピー H = log W - Σ w log w / W（W は候補の重みの合計）
    with np.errstate(divide="ignore", invalid="ignore"):
        entropy = np.log(totals) - (weighted * np.log(np.where(wave, patterns.weights, 1.0))).sum(axis=2) / totals
    entropy = np.where(wave.sum(axis=2) > 1, entropy, np.inf)
    if np.isinf(entropy).all():
        return None  # すべてのセルが確定した
    entropy = entropy + 1e-6 * rng.random(entropy.shape)  # 同点のセルからランダムに選ぶ
    y, x = np.unravel_index(int(np.argmin(entropy)), entropy.shape)
    probabilities = weighted[y, x] / totals[y, x]
    choice = rng.choice(len(probabilities), p=probabilities)
    wave[y, x] = False
    wave[y, x, choice] = True
    return int(y), int(x)


def synthesize(patterns: Patterns, height: int, width: int, seed: int, snapshots: tuple[int, ...] = (),
               max_attempts: int = 20) -> tuple[BoolArray, list[BoolArray]]:
    """出力の wave（各セルに残る候補の真偽）を返す。矛盾したらシードを変えてやり直す。

    snapshots に観測（セルを 1 つ選んで決める操作）の回数を与えると、その時点の wave の写しも返す（途中経過の図に使う）。
    """
    for attempt in range(max_attempts):
        rng = np.random.default_rng(seed + 1000 * attempt)
        wave = np.ones((height, width, len(patterns.weights)), dtype=bool)
        saved: list[BoolArray] = []
        try:
            for count in range(height * width + 1):
                if count in snapshots:
                    saved.append(wave.copy())
                cell = observe(wave, patterns, rng)
                if cell is None:
                    return wave, saved
                propagate(wave, patterns, cell)
        except Contradiction:
            print(f"矛盾が生じたのでやり直す（シード {seed}、{attempt + 1} 回目）")
    raise RuntimeError("やり直しの上限に達した")


def render(wave: BoolArray, patterns: Patterns, colors: FloatArray) -> FloatArray:
    """各セルの色を、残っている候補の小片の左上の色の平均（重み付き）にする。確定したセルはその色になる。"""
    corner = colors[patterns.tiles[:, 0, 0]]  # (P, 3)
    weighted = wave * patterns.weights
    result: FloatArray = (weighted @ corner) / weighted.sum(axis=2, keepdims=True)
    return result


def palette_for(symbols: list[str]) -> FloatArray:
    return np.array([PALETTE[s] for s in symbols])


def draw_results(file_name: str) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(2, 3, figsize=(10, 7), gridspec_kw={"width_ratios": [1, 2, 2]})
    for row, (rows, symmetry, title) in enumerate([(SAMPLE_LINES, True, "線"), (SAMPLE_ISLAND, True, "島")]):
        sample, symbols = to_indices(rows)
        colors = palette_for(symbols)
        patterns = extract_patterns(sample, 3, symmetry)
        axes[row, 0].imshow(colors[sample], interpolation="nearest")
        axes[row, 0].set_title(f"見本「{title}」（{sample.shape[1]} × {sample.shape[0]}）\n小片 {len(patterns.weights)} 種類",
                               fontsize=10)
        for column, seed in enumerate((1, 2), start=1):
            wave, _ = synthesize(patterns, 40, 40, seed=seed + 10 * row)
            axes[row, column].imshow(render(wave, patterns, colors), interpolation="nearest")
            axes[row, column].set_title(f"合成結果（40 × 40、シード {seed}）", fontsize=10)
    for ax in axes.flat:
        ax.set_xticks([])
        ax.set_yticks([])
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_progress(file_name: str) -> None:
    import matplotlib.pyplot as plt

    sample, symbols = to_indices(SAMPLE_ISLAND)
    colors = palette_for(symbols)
    patterns = extract_patterns(sample, 3, symmetry=True)
    snapshots = (0, 15, 60, 150)
    wave, saved = synthesize(patterns, 40, 40, seed=5, snapshots=snapshots)
    states = saved + [wave]
    figure, axes = plt.subplots(1, len(states), figsize=(13, 3))
    for index, (ax, state) in enumerate(zip(axes, states)):
        decided = int((state.sum(axis=2) == 1).sum())
        label = f"観測 {snapshots[index]} 回" if index < len(snapshots) else "完成"
        ax.imshow(render(state, patterns, colors), interpolation="nearest")
        ax.set_title(f"{label}（確定 {decided} セル）", fontsize=10)
        ax.set_axis_off()
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_results("wfc_results.png")
    draw_progress("wfc_progress.png")


if __name__ == "__main__":
    main()
