"""第 17 章「生成の設計と評価」: 表現範囲の分析と、生成して検査する方式の図を作る。

この章専用の小さなダンジョン生成器（部屋をランダムに置き、通路でつなぐ）を使う。

* samples.png: 2 つのパラメーター設定で生成したダンジョンの例
* knob.png: 1 つの「つまみ」complexity から内部のパラメーターを決めた例
* expressive_range.png: 1000 個ずつ生成し、2 つの指標の分布をヒートマップにしたもの
* rejection.png: 経路長の分布と、受け入れる範囲（生成して検査する方式）

棄却サンプリングの受け入れ率は、標準出力に表として出力する。
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from typing import Any

import numpy as np
from numpy.typing import NDArray

from common import FloatArray, IntArray, output_dir, save_figure, setup_matplotlib

BoolArray = NDArray[np.bool_]

SIZE = 40  # ダンジョンは SIZE × SIZE の格子。True が床、False が壁
SAMPLES = 1000  # 表現範囲の分析で生成する個数


@dataclass(frozen=True)
class Params:
    """生成器のパラメーター。"""

    attempts: int  # 部屋を置こうとする回数（重なったら置かない）
    min_size: int  # 部屋の一辺の最小値
    max_size: int  # 部屋の一辺の最大値
    chain: float  # 新しい部屋を「直前の部屋」につなぐ確率。残りは「最も近い部屋」につなぐ


@dataclass
class Level:
    """生成したダンジョンと、評価に使う情報。"""

    floor: BoolArray  # (SIZE, SIZE) の bool。True が床
    rooms: list[tuple[int, int, int, int]]  # 部屋の (x, y, 幅, 高さ)
    start: tuple[int, int]  # 入口（最初の部屋の中心）
    goal: tuple[int, int]  # 出口（入口から最も遠い部屋の中心）
    path: list[tuple[int, int]]  # 入口から出口までの最短経路


SETTING_A = Params(attempts=8, min_size=5, max_size=11, chain=0.2)
SETTING_B = Params(attempts=30, min_size=3, max_size=6, chain=0.2)


def center(room: tuple[int, int, int, int]) -> tuple[int, int]:
    """部屋の中心のマスの座標。"""
    x, y, w, h = room
    return x + w // 2, y + h // 2


def carve_corridor(floor: BoolArray, a: tuple[int, int], b: tuple[int, int], horizontal_first: bool) -> None:
    """a から b まで、L 字形の通路を掘る。"""
    (x0, y0), (x1, y1) = a, b
    corner = (x1, y0) if horizontal_first else (x0, y1)
    for (xa, ya), (xb, yb) in ((a, corner), (corner, b)):
        floor[min(ya, yb):max(ya, yb) + 1, min(xa, xb):max(xa, xb) + 1] = True


def place_rooms(params: Params, rng: np.random.Generator) -> list[tuple[int, int, int, int]]:
    """重ならないように部屋を置く。周囲に 1 マスの壁を残す。"""
    rooms: list[tuple[int, int, int, int]] = []
    for _ in range(params.attempts):
        w, h = rng.integers(params.min_size, params.max_size + 1, size=2)
        x = int(rng.integers(1, SIZE - w))
        y = int(rng.integers(1, SIZE - h))
        # 1 マスの隙間を空けて重なりを調べる
        if all(x + w + 1 <= rx or rx + rw + 1 <= x or y + h + 1 <= ry or ry + rh + 1 <= y
               for rx, ry, rw, rh in rooms):
            rooms.append((x, y, int(w), int(h)))
    return rooms


def bfs(floor: BoolArray, start: tuple[int, int]) -> IntArray:
    """start から床の上を上下左右に歩いたときの最短距離。届かないマスは -1。"""
    distance = np.full(floor.shape, -1, dtype=np.int64)
    distance[start[1], start[0]] = 0
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < SIZE and 0 <= ny < SIZE and floor[ny, nx] and distance[ny, nx] < 0:
                distance[ny, nx] = distance[y, x] + 1
                queue.append((nx, ny))
    return distance


def trace_path(distance: IntArray, goal: tuple[int, int]) -> list[tuple[int, int]]:
    """BFS の距離を、出口から距離が 1 ずつ減る方向にたどって最短経路を得る。"""
    path = [goal]
    x, y = goal
    while distance[y, x] > 0:
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < SIZE and 0 <= ny < SIZE and distance[ny, nx] == distance[y, x] - 1:
                x, y = nx, ny
                break
        path.append((x, y))
    return path[::-1]


def generate(params: Params, seed: int) -> Level:
    """部屋を置き、通路でつなぎ、入口と出口を決める。"""
    rng = np.random.default_rng(seed)
    rooms = place_rooms(params, rng)
    floor = np.zeros((SIZE, SIZE), dtype=bool)
    for x, y, w, h in rooms:
        floor[y:y + h, x:x + w] = True
    # 2 番目以降の部屋を、それより前に置いた部屋のどれかとつなぐ（どの部屋も最初の部屋から必ず到達できる）
    for index in range(1, len(rooms)):
        here = center(rooms[index])
        if rng.random() < params.chain:
            target = index - 1
        else:
            target = min(range(index), key=lambda k: abs(center(rooms[k])[0] - here[0])
                         + abs(center(rooms[k])[1] - here[1]))
        carve_corridor(floor, here, center(rooms[target]), bool(rng.random() < 0.5))
    start = center(rooms[0])
    distance = bfs(floor, start)
    goal = max((center(room) for room in rooms), key=lambda c: int(distance[c[1], c[0]]))
    return Level(floor, rooms, start, goal, trace_path(distance, goal))


def knob_params(complexity: float) -> Params:
    """0〜1 の「つまみ」complexity 1 つから、内部のパラメーターをまとめて決める。

    complexity を上げると、部屋は小さく多くなり、つなぎ方は枝分かれが増える。
    """
    t = float(np.clip(complexity, 0.0, 1.0))
    return Params(attempts=round(6 + 34 * t), min_size=round(6 - 3 * t), max_size=round(12 - 6 * t),
                  chain=0.8 - 0.7 * t)


def metrics(level: Level) -> dict[str, float]:
    """評価の指標を計算する。"""
    path_cells = set(level.path)
    on_path = sum(1 for x, y, w, h in level.rooms
                  if any((cx, cy) in path_cells for cx in range(x, x + w) for cy in range(y, y + h)))
    return {
        "rooms": float(len(level.rooms)),
        "floor_ratio": float(level.floor.mean()),  # 床の割合
        "path_length": float(len(level.path) - 1),  # 入口から出口までの最短経路長（マス）
        "linearity": on_path / len(level.rooms),  # 最短経路が通る部屋の割合（1 なら一本道）
    }


def evaluate(params: Params, count: int, seed: int) -> dict[str, FloatArray]:
    """count 個を生成して、各指標の値を配列にまとめる。"""
    rows = [metrics(generate(params, seed + index)) for index in range(count)]
    return {key: np.array([row[key] for row in rows]) for key in rows[0]}


def draw_level(ax: Any, level: Level) -> None:
    """ダンジョンを 1 枚描く（床は明るく、最短経路は線、入口は緑、出口は赤）。"""
    ax.imshow(np.where(level.floor, 0.92, 0.25), cmap="gray", vmin=0.0, vmax=1.0, interpolation="nearest")
    xs, ys = zip(*level.path)
    ax.plot(xs, ys, color="#dd8452", linewidth=1.2)
    ax.plot(*level.start, marker="o", color="#55a868", markersize=6)
    ax.plot(*level.goal, marker="s", color="#c44e52", markersize=6)
    ax.set_xticks([])
    ax.set_yticks([])


def draw_samples(file_name: str) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(2, 5, figsize=(12, 5.2))
    for row, (label, params) in enumerate((("設定 A", SETTING_A), ("設定 B", SETTING_B))):
        for column in range(5):
            level = generate(params, seed=column)
            draw_level(axes[row, column], level)
            m = metrics(level)
            axes[row, column].set_title(f"部屋 {m['rooms']:.0f}、経路 {m['path_length']:.0f}", fontsize=10)
        axes[row, 0].set_ylabel(label, fontsize=11)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_knob(file_name: str) -> None:
    import matplotlib.pyplot as plt

    values = [0.0, 0.25, 0.5, 0.75, 1.0]
    figure, axes = plt.subplots(1, len(values), figsize=(12, 2.9))
    for ax, value in zip(axes, values):
        draw_level(ax, generate(knob_params(value), seed=7))
        ax.set_title(f"complexity = {value:g}", fontsize=10)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_expressive_range(file_name: str, results: list[tuple[str, dict[str, FloatArray]]]) -> None:
    import matplotlib.pyplot as plt

    x_edges = np.linspace(0.0, 0.45, 31)
    y_edges = np.linspace(0.0, 1.0, 21)
    figure, axes = plt.subplots(1, len(results), figsize=(11, 4.4))
    for ax, (label, values) in zip(axes, results):
        counts, _, _ = np.histogram2d(values["floor_ratio"], values["linearity"], bins=(x_edges, y_edges))
        image = ax.imshow(counts.T, origin="lower", aspect="auto", cmap="viridis",
                          extent=(x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]))
        ax.set_title(label, fontsize=11)
        ax.set_xlabel("床の割合")
        ax.set_ylabel("直線性（最短経路が通る部屋の割合）")
        figure.colorbar(image, ax=ax, label="個数")
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_rejection(file_name: str, values: dict[str, FloatArray], low: float, high: float) -> None:
    import matplotlib.pyplot as plt

    lengths = values["path_length"]
    bins = np.arange(2, lengths.max() + 6, 4).tolist()  # 受け入れ範囲の端が区間の境目に来るようにする
    accepted = (lengths >= low) & (lengths < high)
    figure, ax = plt.subplots(figsize=(8, 3.4))
    ax.hist(lengths[~accepted], bins=bins, color="#bbbbbb", label="棄却")
    ax.hist(lengths[accepted], bins=bins, color="#4c72b0", label="受け入れ")
    ax.axvspan(low, high, color="#4c72b0", alpha=0.08)
    ax.set_xlabel("入口から出口までの最短経路長（マス）")
    ax.set_ylabel("個数")
    ax.set_title(f"設定 B の経路長の分布（{low:g} 以上 {high:g} 未満を受け入れる。受け入れ率 {accepted.mean():.0%}）",
                 fontsize=11)
    ax.legend()
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def generate_with_rejection(params: Params, low: float, high: float, seed: int,
                            max_tries: int = 1000) -> tuple[Level | None, int]:
    """経路長が low 以上 high 未満になるまで生成し直す。(結果, 試した回数) を返す。"""
    for tries in range(1, max_tries + 1):
        level = generate(params, seed * max_tries + tries)
        if low <= len(level.path) - 1 < high:
            return level, tries
    return None, max_tries


def print_rejection_table(params: Params, ranges: list[tuple[float, float]], count: int = 100) -> None:
    """経路長の範囲ごとに、count 個を受け入れるまでに試した回数を数えて表にする。"""
    print("経路長の範囲 | 受け入れ率 | 1 個あたりの平均試行回数 | 最大試行回数 | 受け入れた結果の直線性の平均")
    for low, high in ranges:
        results = [generate_with_rejection(params, low, high, seed) for seed in range(count)]
        tries = [t for _, t in results]
        linearity = [metrics(level)["linearity"] for level, _ in results if level is not None]
        print(f"{low:g} 以上 {high:g} 未満 | {count / sum(tries):.1%} | {np.mean(tries):.1f} | {max(tries)} | "
              f"{np.mean(linearity):.2f}")


def main() -> None:
    setup_matplotlib()
    draw_samples("samples.png")
    draw_knob("knob.png")
    results = [("設定 A（大きな部屋・少数）", evaluate(SETTING_A, SAMPLES, seed=10000)),
               ("設定 B（小さな部屋・多数）", evaluate(SETTING_B, SAMPLES, seed=20000))]
    for label, values in results:
        summary = "、".join(f"{key} 平均 {values[key].mean():.3f}（標準偏差 {values[key].std():.3f}）"
                           for key in values)
        print(f"{label}: {summary}")
    draw_expressive_range("expressive_range.png", results)
    draw_rejection("rejection.png", results[1][1], low=50.0, high=70.0)
    print_rejection_table(SETTING_B, [(30.0, 50.0), (50.0, 70.0), (70.0, 90.0), (90.0, 110.0)])


if __name__ == "__main__":
    main()
