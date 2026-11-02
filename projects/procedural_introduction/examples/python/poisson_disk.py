"""ポアソンディスク・サンプリング（Bridson の方法、2007 年）。

どの 2 点の間隔も半径 r 以上で、しかも r の 2 倍程度より大きな空きの無い点の集まりを、
点の数にほぼ比例する時間で作る。bridson は半径が一定の場合、bridson_variable は
場所によって半径を変える場合である。
"""

from __future__ import annotations

import math
from collections.abc import Callable

import numpy as np

from common import FloatArray


def bridson(width: float, height: float, radius: float, rng: np.random.Generator, attempts: int = 30) -> FloatArray:
    """幅 width、高さ height の長方形に、間隔 radius 以上の点を敷き詰めて (N, 2) の配列で返す。

    1. 一辺 radius / √2 の格子を用意する。この大きさのセルには点が 1 個しか入らない。
    2. 最初の点を無作為に置き、「活性リスト」に入れる。
    3. 活性リストから点を 1 個選び、その周りの半径 r〜2r の円環に候補を attempts 個作る。
       近くの点と r 以上離れた候補があれば採用し、活性リストに加える。
       どの候補も採用できなければ、その点の周りは埋まったとみなして活性リストから除く。
    4. 活性リストが空になるまで 3 を繰り返す。
    """
    cell = radius / math.sqrt(2.0)
    columns = int(math.ceil(width / cell))
    rows = int(math.ceil(height / cell))
    grid = np.full((rows, columns), -1, dtype=np.int64)  # セルに入っている点の番号（無ければ -1）
    points: list[tuple[float, float]] = []
    active: list[int] = []  # 周りにまだ点を置ける可能性のある点の番号

    def add(x: float, y: float) -> None:
        grid[int(y / cell), int(x / cell)] = len(points)
        points.append((x, y))
        active.append(len(points) - 1)

    def is_far(x: float, y: float) -> bool:
        """候補 (x, y) が、既存のどの点からも radius 以上離れているか。近くの 5 × 5 セルだけを調べる。"""
        gx, gy = int(x / cell), int(y / cell)
        for j in range(max(gy - 2, 0), min(gy + 3, rows)):
            for i in range(max(gx - 2, 0), min(gx + 3, columns)):
                k = grid[j, i]
                if k >= 0 and (points[k][0] - x) ** 2 + (points[k][1] - y) ** 2 < radius * radius:
                    return False
        return True

    add(rng.uniform(0.0, width), rng.uniform(0.0, height))
    while active:
        index = int(rng.integers(len(active)))
        px, py = points[active[index]]
        for _ in range(attempts):
            # 円環 r〜2r の中で面積あたり均等になるように、半径は √ をとって選ぶ。
            distance = radius * math.sqrt(rng.uniform(1.0, 4.0))
            angle = rng.uniform(0.0, 2.0 * math.pi)
            x = px + distance * math.cos(angle)
            y = py + distance * math.sin(angle)
            if 0.0 <= x < width and 0.0 <= y < height and is_far(x, y):
                add(x, y)
                break
        else:
            active[index] = active[-1]  # 候補が見つからなかった点を活性リストから除く（末尾と入れ替えて削除）
            active.pop()
    return np.array(points)


def bridson_variable(
    width: float,
    height: float,
    radius_at: Callable[[float, float], float],
    min_radius: float,
    max_radius: float,
    rng: np.random.Generator,
    attempts: int = 30,
) -> FloatArray:
    """場所 (x, y) ごとに半径 radius_at(x, y) を変えるポアソンディスク・サンプリング。

    radius_at の値は min_radius〜max_radius の範囲にあるものとする。2 点の間隔は、
    両方の点の半径の大きい方以上にする。格子は最小の半径に合わせて作り（セルに入る点は
    やはり 1 個まで）、最大の半径が届く範囲のセルを調べる。
    """
    cell = min_radius / math.sqrt(2.0)
    columns = int(math.ceil(width / cell))
    rows = int(math.ceil(height / cell))
    reach = int(math.ceil(max_radius / cell))
    grid = np.full((rows, columns), -1, dtype=np.int64)
    # 点はセルに 1 個までなので、点の数はセルの数を超えない。その大きさの配列を用意しておく。
    points = np.zeros((rows * columns, 3))  # 各点の (x, y, 半径)
    count = 0
    active: list[int] = []

    def add(x: float, y: float, r: float) -> None:
        nonlocal count
        grid[int(y / cell), int(x / cell)] = count
        points[count] = (x, y, r)
        active.append(count)
        count += 1

    def is_far(x: float, y: float, r: float) -> bool:
        """近くのセルに入っている点をまとめて取り出し、NumPy で距離を調べる。"""
        gx, gy = int(x / cell), int(y / cell)
        nearby = grid[max(gy - reach, 0):gy + reach + 1, max(gx - reach, 0):gx + reach + 1]
        others = points[nearby[nearby >= 0]]
        distance = np.hypot(others[:, 0] - x, others[:, 1] - y)
        return bool(np.all(distance >= np.maximum(r, others[:, 2])))

    x0, y0 = rng.uniform(0.0, width), rng.uniform(0.0, height)
    add(x0, y0, radius_at(x0, y0))
    while active:
        index = int(rng.integers(len(active)))
        px, py, r = points[active[index]]
        for _ in range(attempts):
            distance = r * math.sqrt(rng.uniform(1.0, 4.0))
            angle = rng.uniform(0.0, 2.0 * math.pi)
            x = px + distance * math.cos(angle)
            y = py + distance * math.sin(angle)
            if 0.0 <= x < width and 0.0 <= y < height:
                rc = radius_at(x, y)
                if is_far(x, y, rc):
                    add(x, y, rc)
                    break
        else:
            active[index] = active[-1]
            active.pop()
    return points[:count, :2].copy()
