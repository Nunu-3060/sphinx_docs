"""セットアソシアティブキャッシュのシミュレーター。

2 次元配列を行優先・列優先で走査したときのアドレス列をキャッシュに
与え、ミス率と、ミスの 3C 分類（初期参照ミス、容量ミス、競合ミス）を
表示します。置換方式は LRU です。

* 初期参照ミス: そのブロックへの最初のアクセスによるミス
* 容量ミス: 同じ容量のフルアソシアティブキャッシュでもミスになるもの
* 競合ミス: それ以外（同じセットにブロックが集中したことによるミス）

実行方法: python cache_sim.py
"""

from collections import OrderedDict


class Cache:
    """LRU で置換するセットアソシアティブキャッシュ（タグだけを持つ）。"""

    def __init__(self, size: int, block: int, ways: int) -> None:
        self.block = block
        self.ways = ways
        self.num_sets = size // (block * ways)
        # セットごとに、ブロック番号を古い順に並べた OrderedDict を持つ
        self.sets: list[OrderedDict[int, None]] = [
            OrderedDict() for _ in range(self.num_sets)]

    def access(self, addr: int) -> bool:
        """アドレス addr を読み、ヒットなら True を返す。"""
        blk = addr // self.block  # ブロック番号（タグとインデックス）
        s = self.sets[blk % self.num_sets]  # インデックスでセットを選ぶ
        if blk in s:
            s.move_to_end(blk)  # 最も新しく使ったものにする
            return True
        if len(s) >= self.ways:
            s.popitem(last=False)  # 最も長く使われていないものを追い出す
        s[blk] = None
        return False


def classify(addrs: list[int], size: int, block: int,
             ways: int) -> dict[str, int]:
    """アドレス列を実行し、アクセス数と 3C 別のミス数を数える。"""
    cache = Cache(size, block, ways)
    full = Cache(size, block, size // block)  # 同容量のフルアソシアティブ
    seen: set[int] = set()
    count = {"access": 0, "compulsory": 0, "capacity": 0, "conflict": 0}
    for a in addrs:
        count["access"] += 1
        hit = cache.access(a)
        full_hit = full.access(a)
        blk = a // block
        if not hit:
            if blk not in seen:
                count["compulsory"] += 1
            elif not full_hit:
                count["capacity"] += 1
            else:
                count["conflict"] += 1
        seen.add(blk)
    return count


def traverse(rows: int, cols: int, row_major: bool,
             elem: int = 4) -> list[int]:
    """rows 行 cols 列の 4 バイト要素の配列を走査するアドレス列を返す。

    配列はアドレス 0 から行優先（C 言語と同じ）で格納されているとする。
    """
    if row_major:
        order = [(i, j) for i in range(rows) for j in range(cols)]
    else:
        order = [(i, j) for j in range(cols) for i in range(rows)]
    return [(i * cols + j) * elem for i, j in order]


def main() -> None:
    """配列の走査順とキャッシュの構成を変えてミス率を比較する。"""
    size, block = 4096, 32  # 4 KiB のキャッシュ、32 バイトのブロック
    print(f"キャッシュ {size} バイト、ブロック {block} バイト、LRU")
    print("配列       走査順  ウェイ数    ミス率  初期参照    容量    競合")
    cases = [
        (128, 128, True, 1), (128, 128, False, 1), (128, 128, False, 4),
        (128, 136, False, 1),  # 1 行を 8 要素（32 バイト）だけ長くする
        (256, 256, False, 4),
    ]
    for rows, cols, row_major, ways in cases:
        addrs = traverse(rows, cols, row_major)
        c = classify(addrs, size, block, ways)
        misses = c["compulsory"] + c["capacity"] + c["conflict"]
        order = "行優先" if row_major else "列優先"
        shape = f"{rows}x{cols}"
        print(f"{shape:<11}{order}{ways:>10}"
              f"{misses / c['access']:>10.1%}{c['compulsory']:>10}"
              f"{c['capacity']:>8}{c['conflict']:>8}")


if __name__ == "__main__":
    main()
