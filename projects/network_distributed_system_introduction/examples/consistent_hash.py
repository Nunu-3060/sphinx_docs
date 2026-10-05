"""剰余による割り当てとコンシステントハッシュを比較するサンプル。

10,000 個のキーを 4 台のノードに割り当て、ノードを 1 台追加して 5 台に
したときに、割り当て先が変わる（移動する）キーの割合を比べます。

* 剰余方式：hash(key) mod N で割り当て先を決めます。
* コンシステントハッシュ：ハッシュ値の空間をリング状に並べ、キーを
  時計回りに進んで最初に出会うノードに割り当てます。

また、コンシステントハッシュで 1 台のノードをリング上の何か所に置くか
（仮想ノードの数）を変えて、各ノードが受け持つキーの数の偏りを比べます。

ハッシュ関数には hashlib の MD5 を使うので、結果は毎回同じになります
（Python 組み込みの hash() は、文字列に対しては実行のたびに値が変わる
ため使いません）。ここでの MD5 は暗号用途ではなく、値を散らすためだけ
に使っています。

実行方法:
    python consistent_hash.py
"""

import bisect
import hashlib
import statistics
from collections import Counter

NUM_KEYS = 10_000
NODES_BEFORE = [f"node-{i}" for i in range(4)]
NODES_AFTER = NODES_BEFORE + ["node-4"]
KEYS = [f"key-{i}" for i in range(NUM_KEYS)]


def hash64(text: str) -> int:
    """文字列を 64 ビットの整数に変換する（決定的なハッシュ）。"""
    digest = hashlib.md5(text.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


def assign_modulo(keys: list[str], nodes: list[str]) -> dict[str, str]:
    """剰余方式：hash(key) mod N 番目のノードに割り当てる。"""
    return {key: nodes[hash64(key) % len(nodes)] for key in keys}


class HashRing:
    """仮想ノードを持つコンシステントハッシュのリング。"""

    def __init__(self, nodes: list[str], vnodes: int) -> None:
        # (リング上の位置, ノード名) を位置の順に並べて持つ
        points: list[tuple[int, str]] = []
        for node in nodes:
            for v in range(vnodes):
                points.append((hash64(f"{node}#{v}"), node))
        points.sort()
        self._positions = [pos for pos, _ in points]
        self._nodes = [node for _, node in points]

    def lookup(self, key: str) -> str:
        """キーから時計回りに進んで、最初に出会うノードを返す。"""
        index = bisect.bisect_right(self._positions, hash64(key))
        # リングの終端を越えたら先頭に戻る
        return self._nodes[index % len(self._nodes)]


def assign_ring(keys: list[str], nodes: list[str],
                vnodes: int) -> dict[str, str]:
    """コンシステントハッシュでキーを割り当てる。"""
    ring = HashRing(nodes, vnodes)
    return {key: ring.lookup(key) for key in keys}


def moved_ratio(before: dict[str, str], after: dict[str, str]) -> float:
    """割り当て先が変わったキーの割合を返す。"""
    moved = sum(1 for key in before if before[key] != after[key])
    return moved / len(before)


def load_stats(assignment: dict[str, str],
               nodes: list[str]) -> tuple[int, int, float]:
    """各ノードのキー数の最小値、最大値、標準偏差を返す。"""
    counts = Counter(assignment.values())
    loads = [counts[node] for node in nodes]
    return min(loads), max(loads), statistics.pstdev(loads)


def main() -> None:
    print(f"キー {NUM_KEYS} 個、ノード {len(NODES_BEFORE)} 台 → "
          f"{len(NODES_AFTER)} 台に追加")
    print()

    # 1. ノード追加で移動するキーの割合
    print("[ノードを 1 台追加したときに移動するキーの割合]")
    before = assign_modulo(KEYS, NODES_BEFORE)
    after = assign_modulo(KEYS, NODES_AFTER)
    print(f"  剰余方式 (hash mod N)        : "
          f"{moved_ratio(before, after):6.1%}")
    for vnodes in (1, 10, 100, 1000):
        before = assign_ring(KEYS, NODES_BEFORE, vnodes)
        after = assign_ring(KEYS, NODES_AFTER, vnodes)
        print(f"  コンシステントハッシュ (v={vnodes:4d}): "
              f"{moved_ratio(before, after):6.1%}")
    ideal = 1 / len(NODES_AFTER)
    print(f"  (理想的な値は 1/{len(NODES_AFTER)} = {ideal:.1%})")
    print()

    # 2. 仮想ノードの数とキー数の偏り（ノード 4 台）
    mean = NUM_KEYS / len(NODES_BEFORE)
    print(f"[仮想ノードの数と各ノードのキー数の偏り "
          f"(4 台、平均 {mean:.0f} 個)]")
    print("  方式                 最小   最大   標準偏差")
    lo, hi, sd = load_stats(assign_modulo(KEYS, NODES_BEFORE),
                            NODES_BEFORE)
    print(f"  剰余方式           {lo:6d} {hi:6d} {sd:9.1f}")
    for vnodes in (1, 10, 100, 1000):
        assignment = assign_ring(KEYS, NODES_BEFORE, vnodes)
        lo, hi, sd = load_stats(assignment, NODES_BEFORE)
        print(f"  仮想ノード {vnodes:4d} 個 {lo:6d} {hi:6d} {sd:9.1f}")


if __name__ == "__main__":
    main()
