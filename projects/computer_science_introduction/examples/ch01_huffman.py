"""ハフマン符号を構築し、圧縮の効果をエントロピーや zlib と比較するサンプル。

文字の出現頻度からハフマン木を作り、各文字の符号語を求める。
符号化後のビット数を、固定長（1 文字 8 ビット）の場合、
エントロピーから求まる下限、zlib（LZ77 とハフマン符号の組み合わせ）と比べる。

実行方法: python ch01_huffman.py
関連する章: 第 1 章「情報の表現」（データ圧縮）
"""

import heapq
import math
import zlib
from collections import Counter

# 葉は文字（str）、内部節点は (左, 右) の組で表す
Tree = str | tuple["Tree", "Tree"]


def build_tree(freq: Counter[str]) -> Tree:
    """出現頻度からハフマン木を作る。"""
    # (頻度, 通し番号, 木) を優先度付きキューに入れる。
    # 通し番号は頻度が同じときの順序を決め、結果を再現可能にする。
    heap: list[tuple[int, int, Tree]] = [
        (n, i, ch) for i, (ch, n) in enumerate(sorted(freq.items()))
    ]
    heapq.heapify(heap)
    count = len(heap)
    while len(heap) > 1:
        n1, _, t1 = heapq.heappop(heap)  # 最も頻度の小さい 2 つを
        n2, _, t2 = heapq.heappop(heap)
        heapq.heappush(heap, (n1 + n2, count, (t1, t2)))  # 1 つにまとめる
        count += 1
    return heap[0][2]


def make_codes(tree: Tree, prefix: str = "") -> dict[str, str]:
    """木をたどって各文字の符号語（左は 0、右は 1）を求める。"""
    if isinstance(tree, str):
        return {tree: prefix or "0"}
    left, right = tree
    codes = make_codes(left, prefix + "0")
    codes.update(make_codes(right, prefix + "1"))
    return codes


def entropy(freq: Counter[str]) -> float:
    """1 文字あたりのエントロピー（ビット）を計算する。"""
    total = sum(freq.values())
    return -sum(n / total * math.log2(n / total) for n in freq.values())


def report(label: str, text: str, show_table: bool) -> None:
    """text をハフマン符号化したときのビット数などを表示する。"""
    freq = Counter(text)
    codes = make_codes(build_tree(freq))
    huffman_bits = sum(len(codes[ch]) for ch in text)
    raw = text.encode("ascii")
    print(f"== {label}: {len(text)} 文字、{len(freq)} 種類 ==")
    if show_table:
        for ch, n in freq.most_common():
            print(f"  {ch!r}: {n} 回 符号語 {codes[ch]}")
    h = entropy(freq)
    print(f"  エントロピー  : {h:.3f} ビット/文字"
          f"（下限 {h * len(text):.1f} ビット）")
    print(f"  平均符号長    : {huffman_bits / len(text):.3f} ビット/文字")
    print(f"  固定長 8 ビット: {len(raw) * 8} ビット")
    print(f"  ハフマン符号  : {huffman_bits} ビット（符号表を除く）")
    packed = zlib.compress(raw, 9)
    print(f"  zlib          : {len(packed) * 8} ビット")


def main() -> None:
    """短い文字列と長い文章で圧縮の効果を比べる。"""
    report("abracadabra", "abracadabra", True)
    sentence = ("the quick brown fox jumps over the lazy dog. "
                "a computer represents every piece of data as bits. ")
    report("英文", sentence, False)
    report("英文を 20 回繰り返す", sentence * 20, False)


if __name__ == "__main__":
    main()
