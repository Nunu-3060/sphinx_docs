"""挿入ソート・マージソート・クイックソートの比較回数を数えるサンプル。

実行時間は環境によって変わるため、ここでは要素同士の比較回数を数えて
アルゴリズムの効率を比べる。最後に sorted() が安定なソートであることを
確かめる。

実行方法: python ch05_sort.py
関連する章: 第 5 章「アルゴリズムと計算量」
"""

import math
import random


class Counter:
    """比較回数を数えるためのカウンタ。"""

    def __init__(self) -> None:
        """回数を 0 で初期化する。"""
        self.count = 0

    def less_equal(self, a: int, b: int) -> bool:
        """a <= b を判定し、比較回数を 1 増やす。"""
        self.count += 1
        return a <= b


def insertion_sort(a: list[int], c: Counter) -> None:
    """a をその場で昇順に並べ替える。"""
    for i in range(1, len(a)):
        x = a[i]
        j = i - 1
        # x より大きい要素を 1 つずつ右へずらす
        while j >= 0 and not c.less_equal(a[j], x):
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = x


def merge_sort(a: list[int], c: Counter) -> list[int]:
    """a を昇順に並べた新しいリストを返す。"""
    if len(a) <= 1:
        return a[:]
    mid = len(a) // 2
    left = merge_sort(a[:mid], c)  # 分割して再帰的に整列する
    right = merge_sort(a[mid:], c)
    merged: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        # 等しいときは左を先に出すことで安定性を保つ
        if c.less_equal(left[i], right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def quick_sort(a: list[int], lo: int, hi: int, c: Counter) -> None:
    """a[lo..hi] をその場で並べ替える。末尾の要素をピボットに使う。"""
    if lo >= hi:
        return
    pivot = a[hi]
    i = lo
    for j in range(lo, hi):
        if c.less_equal(a[j], pivot):
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]  # ピボットを確定した位置に置く
    quick_sort(a, lo, i - 1, c)
    quick_sort(a, i + 1, hi, c)


def count_all(data: list[int]) -> list[int]:
    """3 つのソートの比較回数を返す。結果が正しいことも確かめる。"""
    counts: list[int] = []
    c = Counter()
    a = data[:]
    insertion_sort(a, c)
    assert a == sorted(data)
    counts.append(c.count)
    c = Counter()
    assert merge_sort(data, c) == sorted(data)
    counts.append(c.count)
    c = Counter()
    a = data[:]
    quick_sort(a, 0, len(a) - 1, c)
    assert a == sorted(data)
    counts.append(c.count)
    return counts


def main() -> None:
    """入力の種類ごとに比較回数を表示し、安定性を確かめる。"""
    n = 500
    random.seed(0)
    inputs = {"ランダム": random.sample(range(n), n),
              "整列済み": list(range(n)),
              "逆順": list(range(n, 0, -1))}
    print(f"n = {n}, n log2 n = {n * math.log2(n):.0f}, "
          f"下限 log2(n!) = {math.lgamma(n + 1) / math.log(2):.0f}")
    for label, data in inputs.items():
        ins, mer, qui = count_all(data)
        print(f"{label}: 挿入 {ins:>7,}, マージ {mer:>5,}, クイック {qui:>7,}")

    # 安定なソート: 点数が同じ人は元の並び（受付順）が保たれる
    entries = [("佐藤", 80), ("鈴木", 90), ("高橋", 80), ("田中", 90)]
    print(sorted(entries, key=lambda e: e[1], reverse=True))


if __name__ == "__main__":
    main()
