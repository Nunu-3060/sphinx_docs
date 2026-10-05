"""結合のアルゴリズムごとに、必要な比較や操作の回数を数えるサンプル。

注文表 R（4000 行）と顧客表 S（1000 行）を顧客番号で等価結合する。
入れ子ループ結合、インデックス（ソート済み配列の二分探索）を使う
入れ子ループ結合、ハッシュ結合、ソートマージ結合の 4 つを実装し、
結果が一致することと、操作回数の違いを確かめる。

実行方法: python ch11_join_algorithms.py
関連する章: 第 11 章「データベース」、第 5 章「アルゴリズムと計算量」
"""

import random
from collections import defaultdict
from functools import cmp_to_key

Row = tuple[int, int]  # (結合キー, 値)
Pair = tuple[int, int]  # 結合結果（R の値, S の値）


class Counter:
    """比較や操作の回数を数える。"""

    def __init__(self) -> None:
        self.count = 0


def nested_loop(r: list[Row], s: list[Row], c: Counter) -> list[Pair]:
    """R の各行について S の全行と比較する。"""
    result = []
    for rk, rv in r:
        for sk, sv in s:
            c.count += 1
            if rk == sk:
                result.append((rv, sv))
    return result


def index_nested_loop(r: list[Row], s: list[Row],
                      c: Counter) -> list[Pair]:
    """S のキーの索引（ソート済み配列）を二分探索で引く。

    S のキーは一意（主キー）と仮定する。索引の構築は事前に
    済んでいるものとして数えない。
    """
    index = sorted(s)
    result = []
    for rk, rv in r:
        lo, hi = 0, len(index)
        while lo < hi:  # 二分探索
            mid = (lo + hi) // 2
            c.count += 1
            if index[mid][0] < rk:
                lo = mid + 1
            else:
                hi = mid
        if lo < len(index) and index[lo][0] == rk:
            result.append((rv, index[lo][1]))
    return result


def hash_join(r: list[Row], s: list[Row], c: Counter) -> list[Pair]:
    """小さい S からハッシュ表を作り（構築）、R の各行で引く（探索）。"""
    table: defaultdict[int, list[int]] = defaultdict(list)
    for sk, sv in s:  # 構築: S の行数だけ挿入する
        c.count += 1
        table[sk].append(sv)
    result = []
    for rk, rv in r:  # 探索: R の行数だけ引く
        c.count += 1
        for sv in table.get(rk, []):
            result.append((rv, sv))
    return result


def sort_merge(r: list[Row], s: list[Row], c: Counter) -> list[Pair]:
    """両方をキーでソートし、先頭から並行にたどって突き合わせる。"""
    def cmp(x: Row, y: Row) -> int:
        c.count += 1
        return (x[0] > y[0]) - (x[0] < y[0])

    rs = sorted(r, key=cmp_to_key(cmp))
    ss = sorted(s, key=cmp_to_key(cmp))
    result = []
    i = j = 0
    while i < len(rs) and j < len(ss):
        c.count += 1
        if rs[i][0] < ss[j][0]:
            i += 1
        elif rs[i][0] > ss[j][0]:
            j += 1
        else:  # S のキーは一意なので、R 側だけを進める
            result.append((rs[i][1], ss[j][1]))
            i += 1
    return result


def main() -> None:
    """4 つの結合方式の操作回数と結果の件数を表示する。"""
    rng = random.Random(1)  # 結果を再現できるようシードを固定する
    n_r, n_s = 4000, 1000
    s = [(k, k * 10) for k in rng.sample(range(2000), n_s)]
    r = [(rng.randrange(2000), i) for i in range(n_r)]
    print(f"|R| = {n_r}, |S| = {n_s}")
    print(" 操作回数  結果の行数  一致  方式")
    expected = None
    for name, join in [("入れ子ループ結合", nested_loop),
                       ("インデックス入れ子ループ結合", index_nested_loop),
                       ("ハッシュ結合", hash_join),
                       ("ソートマージ結合", sort_merge)]:
        c = Counter()
        result = sorted(join(r, s, c))
        if expected is None:
            expected = result
        same = result == expected
        print(f"{c.count:>9,}  {len(result):>10}  {same!s:<4}  {name}")


if __name__ == "__main__":
    main()
