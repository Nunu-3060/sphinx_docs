"""ブルームフィルタのサンプル。

m ビットのビット配列と k 個のハッシュ関数を使うブルームフィルタを実装し、
n 個の要素を追加した後、追加していない要素で偽陽性率を実測して
理論値の近似 (1 - e^(-kn/m))^k と比較する。

結果を再現できるよう、ハッシュ値は hashlib.sha256 から計算する
（組み込みの hash() は文字列に対して実行のたびに値が変わるため使わない）。

実行方法: python ch04_bloom_filter.py
関連する章: 第 4 章「データ構造」
"""

import hashlib
import math


class BloomFilter:
    """文字列の集合を表すブルームフィルタ。"""

    def __init__(self, m: int, k: int) -> None:
        """m ビットのビット配列と k 個のハッシュ関数を持つフィルタを作る。"""
        self.m = m
        self.k = k
        self.bits = bytearray((m + 7) // 8)  # 全ビット 0 で始める

    def _positions(self, item: str) -> list[int]:
        """item に対する k 個のビット位置を返す。

        SHA-256 の値から 2 つの 64 ビット整数 h1, h2 を取り出し、
        h1 + i * h2 (i = 0, 1, ..., k-1) で k 個のハッシュ値を作る。
        """
        digest = hashlib.sha256(item.encode("utf-8")).digest()
        h1 = int.from_bytes(digest[:8], "big")
        h2 = int.from_bytes(digest[8:16], "big") | 1
        return [(h1 + i * h2) % self.m for i in range(self.k)]

    def add(self, item: str) -> None:
        """item の k 個の位置のビットを 1 にする。"""
        for p in self._positions(item):
            self.bits[p // 8] |= 1 << (p % 8)

    def might_contain(self, item: str) -> bool:
        """k 個の位置がすべて 1 なら True（含むかもしれない）を返す。"""
        return all(
            self.bits[p // 8] & (1 << (p % 8)) for p in self._positions(item)
        )


def theoretical_rate(m: int, n: int, k: int) -> float:
    """偽陽性率の近似値 (1 - e^(-kn/m))^k を返す。"""
    return (1 - math.exp(-k * n / m)) ** k


def main() -> None:
    """いくつかの k について偽陽性率を実測し、理論値と比べる。"""
    m, n, trials = 10_000, 1_000, 100_000
    members = [f"user{i}" for i in range(n)]
    others = [f"guest{i}" for i in range(trials)]  # 追加しない要素
    print(f"m = {m} ビット, n = {n} 個, 確認する非要素 {trials} 個")
    for k in [1, 3, 7, 10]:
        bf = BloomFilter(m, k)
        for item in members:
            bf.add(item)
        missed = sum(not bf.might_contain(x) for x in members)
        false_pos = sum(bf.might_contain(x) for x in others)
        measured = false_pos / trials
        expected = theoretical_rate(m, n, k)
        print(
            f"k = {k:2d}: 偽陰性 {missed} 個, 偽陽性率 実測 {measured:.4f}"
            f" 理論 {expected:.4f}"
        )
    best_k = m / n * math.log(2)
    print(f"偽陽性率を最小にする k は約 {best_k:.1f}")
    print(f"ビット配列の大きさ: {len(BloomFilter(m, 1).bits)} バイト")


if __name__ == "__main__":
    main()
