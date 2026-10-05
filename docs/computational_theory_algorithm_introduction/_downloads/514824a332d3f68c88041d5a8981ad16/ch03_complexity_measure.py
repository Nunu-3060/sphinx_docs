"""第 3 章: 計算量の違いを実行時間で確かめる。

「リストに重複する要素があるか」を判定する 3 つの関数を用意し、
入力サイズ n を 2 倍にしたときに実行時間がどう増えるかを計測する。

* has_duplicate_quadratic: 全ての組を比べる。O(n^2)
* has_duplicate_sort: 整列してから隣同士を比べる。O(n log n)
* has_duplicate_set: 集合を使う。平均 O(n)

実行例::

    python ch03_complexity_measure.py
"""

from __future__ import annotations

import random
import time
from collections.abc import Callable


def has_duplicate_quadratic(values: list[int]) -> bool:
    """全ての組 (i, j) を調べて重複の有無を判定する。"""
    n = len(values)
    for i in range(n):
        for j in range(i + 1, n):
            if values[i] == values[j]:
                return True
    return False


def has_duplicate_sort(values: list[int]) -> bool:
    """整列すると等しい要素は隣り合うことを利用する。"""
    ordered = sorted(values)
    return any(a == b for a, b in zip(ordered, ordered[1:]))


def has_duplicate_set(values: list[int]) -> bool:
    """集合 (ハッシュテーブル) に要素を入れながら重複を探す。"""
    seen: set[int] = set()
    for value in values:
        if value in seen:
            return True
        seen.add(value)
    return False


def measure(func: Callable[[list[int]], bool], values: list[int]) -> float:
    """func(values) の実行にかかった秒数を返す。"""
    start = time.perf_counter()
    func(values)
    return time.perf_counter() - start


def main() -> None:
    random.seed(0)
    funcs: list[Callable[[list[int]], bool]] = [
        has_duplicate_quadratic,
        has_duplicate_sort,
        has_duplicate_set,
    ]
    print(f"{'n':>6} {'O(n^2)':>10} {'O(n log n)':>12} {'O(n)':>10}")
    for n in (1000, 2000, 4000):
        # 重複がない入力は、どの関数にとっても最後まで調べる最悪の入力になる。
        values = random.sample(range(10 * n), n)
        times = [measure(func, values) for func in funcs]
        print(f"{n:>6} {times[0]:>10.4f} {times[1]:>12.4f} {times[2]:>10.4f}")


if __name__ == "__main__":
    main()
