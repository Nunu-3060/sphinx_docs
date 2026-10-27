"""第 11 章: 一様グリッドによるブロードフェーズ。

広い空間にばらまいた円について、重なっている組を 2 つの方法で探し、調べた組の数と時間を比べる。

* 総当たり: すべての組を調べる。
* 一様グリッド: 空間をマス目に分け、同じマスにいる物どうしだけを調べる。

実行方法:
    py spatial_grid.py
"""

import itertools
import math
import random
import time
from collections import defaultdict

WORLD_SIZE = 4000.0
CIRCLE_COUNT = 2000
MAX_RADIUS = 20.0
CELL_SIZE = 2 * MAX_RADIUS  # マスの大きさは、最大の物の直径くらいにする

Circle = tuple[float, float, float]  # (x, y, 半径)


def overlaps(a: Circle, b: Circle) -> bool:
    dx, dy = a[0] - b[0], a[1] - b[1]
    return dx * dx + dy * dy < (a[2] + b[2]) ** 2


class UniformGrid:
    """物の外接長方形が重なるマスすべてに、その物の番号を登録する。"""

    def __init__(self, cell_size: float) -> None:
        self.cell_size = cell_size
        self.cells: defaultdict[tuple[int, int], list[int]] = defaultdict(list)

    def insert(self, index: int, circle: Circle) -> None:
        x, y, r = circle
        for cx in range(math.floor((x - r) / self.cell_size), math.floor((x + r) / self.cell_size) + 1):
            for cy in range(math.floor((y - r) / self.cell_size), math.floor((y + r) / self.cell_size) + 1):
                self.cells[cx, cy].append(index)

    def candidate_pairs(self) -> set[tuple[int, int]]:
        """同じマスに登録された物の組。複数のマスにまたがる組は 1 回だけ数える。"""
        pairs = set()
        for members in self.cells.values():
            for i, j in itertools.combinations(members, 2):
                pairs.add((min(i, j), max(i, j)))
        return pairs


def brute_force(circles: list[Circle]) -> tuple[set[tuple[int, int]], int]:
    """総当たりで重なっている組を探す。(重なっている組, 調べた組の数) を返す。"""
    hits = set()
    checks = 0
    for i, j in itertools.combinations(range(len(circles)), 2):
        checks += 1
        if overlaps(circles[i], circles[j]):
            hits.add((i, j))
    return hits, checks


def with_grid(circles: list[Circle]) -> tuple[set[tuple[int, int]], int]:
    """グリッドで候補を絞ってから調べる。"""
    grid = UniformGrid(CELL_SIZE)
    for i, c in enumerate(circles):
        grid.insert(i, c)
    candidates = grid.candidate_pairs()
    hits = {(i, j) for i, j in candidates if overlaps(circles[i], circles[j])}
    return hits, len(candidates)


def main() -> None:
    rng = random.Random(0)
    circles = [(rng.uniform(0, WORLD_SIZE), rng.uniform(0, WORLD_SIZE), rng.uniform(5, MAX_RADIUS))
               for _ in range(CIRCLE_COUNT)]
    for name, method in (('総当たり', brute_force), ('一様グリッド', with_grid)):
        start = time.perf_counter()
        hits, checks = method(circles)
        elapsed = time.perf_counter() - start
        print(f'{name:<8} 調べた組: {checks:>9,}  重なっていた組: {len(hits):>4}  時間: {elapsed * 1000:7.1f} ms')


if __name__ == '__main__':
    main()
