"""第 5 章: 二分探索と各種の整列アルゴリズム。

どの関数も新しいリストを返し、引数のリストは変更しない。
main() ではランダムな入力に対して組み込みの sorted() と結果を比べる。

実行例::

    python ch05_sorting.py
"""

from __future__ import annotations

import random


def binary_search(values: list[int], target: int) -> int:
    """整列済みの values から target の位置を探す。無ければ -1 を返す。"""
    lo, hi = 0, len(values)  # 探す範囲は values[lo:hi]
    while lo < hi:
        mid = (lo + hi) // 2
        if values[mid] == target:
            return mid
        if values[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return -1


def insertion_sort(values: list[int]) -> list[int]:
    """挿入ソート。最悪 O(n^2)、ほぼ整列済みの入力には速い。"""
    a = list(values)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(values: list[int]) -> list[int]:
    """マージソート。常に O(n log n)、安定。"""
    if len(values) <= 1:
        return list(values)
    mid = len(values) // 2
    left = merge_sort(values[:mid])
    right = merge_sort(values[mid:])
    merged: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # <= にすることで安定になる
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def quick_sort(values: list[int]) -> list[int]:
    """乱択クイックソート。期待 O(n log n)、最悪 O(n^2)。"""
    a = list(values)

    def sort(lo: int, hi: int) -> None:  # a[lo:hi + 1] を整列する
        if lo >= hi:
            return
        p = random.randint(lo, hi)  # ピボットを無作為に選ぶ
        a[p], a[hi] = a[hi], a[p]
        pivot = a[hi]
        i = lo
        for j in range(lo, hi):  # pivot 未満の要素を左側に集める
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[hi] = a[hi], a[i]
        sort(lo, i - 1)
        sort(i + 1, hi)

    sort(0, len(a) - 1)
    return a


def heap_sort(values: list[int]) -> list[int]:
    """ヒープソート。常に O(n log n)、追加の領域は O(1)。"""
    a = list(values)
    n = len(a)

    def sift_down(root: int, end: int) -> None:  # a[:end] の範囲で調整
        while 2 * root + 1 < end:
            child = 2 * root + 1
            if child + 1 < end and a[child + 1] > a[child]:
                child += 1
            if a[root] >= a[child]:
                return
            a[root], a[child] = a[child], a[root]
            root = child

    for i in range(n // 2 - 1, -1, -1):  # 最大ヒープを作る
        sift_down(i, n)
    for end in range(n - 1, 0, -1):  # 最大値を末尾へ移していく
        a[0], a[end] = a[end], a[0]
        sift_down(0, end)
    return a


def counting_sort(values: list[int], max_value: int) -> list[int]:
    """計数ソート。0 以上 max_value 以下の整数を O(n + max_value) で整列。"""
    counts = [0] * (max_value + 1)
    for v in values:
        counts[v] += 1
    result: list[int] = []
    for v, c in enumerate(counts):
        result.extend([v] * c)
    return result


def radix_sort(values: list[int], base: int = 10) -> list[int]:
    """基数ソート (LSD)。0 以上の整数を下の桁から安定に振り分ける。"""
    a = list(values)
    if not a:
        return a
    place = 1
    while place <= max(a):
        buckets: list[list[int]] = [[] for _ in range(base)]
        for v in a:
            buckets[(v // place) % base].append(v)
        a = [v for bucket in buckets for v in bucket]
        place *= base
    return a


def main() -> None:
    random.seed(1)
    data = [random.randint(0, 999) for _ in range(500)]
    expected = sorted(data)
    print("insertion_sort:", insertion_sort(data) == expected)
    print("merge_sort    :", merge_sort(data) == expected)
    print("quick_sort    :", quick_sort(data) == expected)
    print("heap_sort     :", heap_sort(data) == expected)
    print("counting_sort :", counting_sort(data, 999) == expected)
    print("radix_sort    :", radix_sort(data) == expected)
    target = expected[123]
    index = binary_search(expected, target)
    print(f"binary_search: {target} は位置 {index} にある")
    print("binary_search(1000):", binary_search(expected, 1000))


if __name__ == "__main__":
    main()
