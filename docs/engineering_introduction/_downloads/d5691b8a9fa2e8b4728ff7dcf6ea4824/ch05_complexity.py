"""第 5 章: 計算量の違いが処理時間に与える影響を確かめる。

「リストに重複する値があるか」を調べる 3 つの方法を比べます。

* 総当たり: すべての組を比べる。計算量は O(n^2)
* 並べ替え: 並べ替えてから隣どうしを比べる。計算量は O(n log n)
* 集合: 集合 (ハッシュ表) に入れながら調べる。計算量は O(n)

データの数 n を 2 倍にしたときに、処理時間が何倍になるかを測定します。

実行例::

    python ch05_complexity.py
"""

from __future__ import annotations

import random
import time
from collections.abc import Callable


def has_duplicate_bruteforce(values: list[int]) -> bool:
    """すべての組を比べる (O(n^2))。"""
    n = len(values)
    for i in range(n):
        for j in range(i + 1, n):
            if values[i] == values[j]:
                return True
    return False


def has_duplicate_sort(values: list[int]) -> bool:
    """並べ替えてから隣どうしを比べる (O(n log n))。"""
    ordered = sorted(values)
    return any(a == b for a, b in zip(ordered, ordered[1:]))


def has_duplicate_set(values: list[int]) -> bool:
    """集合に入れながら調べる (O(n))。"""
    seen: set[int] = set()
    for value in values:
        if value in seen:
            return True
        seen.add(value)
    return False


def measure(func: Callable[[list[int]], bool], values: list[int]) -> float:
    """func の処理時間 [ms] を 3 回測定し、最小値を返す。"""
    best = float("inf")
    for _ in range(3):
        start = time.perf_counter()
        func(values)
        best = min(best, time.perf_counter() - start)
    return best * 1000


def main() -> None:
    methods = {
        "総当たり": has_duplicate_bruteforce,
        "並べ替え": has_duplicate_sort,
        "集合": has_duplicate_set,
    }
    sizes = [500, 1000, 2000, 4000]
    rng = random.Random(0)
    print("データ数  " + "  ".join(f"{name:>12}" for name in methods)
          + "   (単位: ms、括弧内は n が半分のときに対する倍率)")
    previous: dict[str, float] = {}
    for n in sizes:
        # 重複のないデータ (最後まで調べる最悪の場合)
        values = rng.sample(range(10 * n), n)
        cells = []
        for name, func in methods.items():
            elapsed = measure(func, values)
            ratio = f"(×{elapsed / previous[name]:4.1f})" \
                if name in previous else "        "
            cells.append(f"{elapsed:7.2f}{ratio}")
            previous[name] = elapsed
        print(f"{n:8d}  " + "  ".join(cells))


if __name__ == "__main__":
    main()
