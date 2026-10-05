"""線形探索と二分探索のサンプル。

要素数を 10 倍ずつ増やしながら、最悪の場合（探す値が存在しない場合）の
比較回数を数える。線形探索は要素数に比例して増え、二分探索は要素数が
10 倍になっても 3〜4 回しか増えないことを確かめる。後半では標準
ライブラリの bisect を使う。

実行方法: python ch05_search.py
関連する章: 第 5 章「アルゴリズムと計算量」
"""

import bisect


def linear_search(items: list[int], target: int) -> tuple[int, int]:
    """先頭から順に調べる。(見つかった添字または -1, 比較回数) を返す。"""
    comparisons = 0
    for i, x in enumerate(items):
        comparisons += 1
        if x == target:
            return i, comparisons
    return -1, comparisons


def binary_search(items: list[int], target: int) -> tuple[int, int]:
    """整列済みの items を二分探索する。戻り値は linear_search と同じ形。"""
    lo, hi = 0, len(items) - 1
    comparisons = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        comparisons += 1  # target と items[mid] の大小比較を 1 回と数える
        if items[mid] == target:
            return mid, comparisons
        if items[mid] < target:
            lo = mid + 1  # 探す範囲を右半分に絞る
        else:
            hi = mid - 1  # 探す範囲を左半分に絞る
    return -1, comparisons


def main() -> None:
    """比較回数の比較と bisect の使用例を表示する。"""
    print("存在しない値を探したときの比較回数")
    for n in [10, 100, 1_000, 10_000, 100_000, 1_000_000]:
        items = list(range(0, 2 * n, 2))  # 偶数だけが並ぶ整列済みリスト
        target = 2 * n  # 存在しない値（最悪の場合）
        _, lin = linear_search(items, target)
        _, bin_ = binary_search(items, target)
        print(f"n = {n:>9,}: 線形探索 {lin:>9,} 回, 二分探索 {bin_:>2} 回")

    scores = [35, 48, 60, 60, 72, 85, 91]
    print("scores:", scores)
    # bisect_left は、値を挿入しても整列が保たれる最も左の位置を返す
    print("60 以上の最初の位置:", bisect.bisect_left(scores, 60))
    print("60 より大きい最初の位置:", bisect.bisect_right(scores, 60))
    count = bisect.bisect_right(scores, 80) - bisect.bisect_left(scores, 50)
    print("50 以上 80 以下の個数:", count)
    bisect.insort(scores, 66)
    print("66 を挿入:", scores)


if __name__ == "__main__":
    main()
