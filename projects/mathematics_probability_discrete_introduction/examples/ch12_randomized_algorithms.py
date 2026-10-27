"""第 12 章 アルゴリズムと確率のサンプルコード。

ハッシュ衝突・クーポンコレクター問題・乱択クイックソート・ブルームフィルタ・
モンテカルロ法について、理論値と実験値を比較する。
"""

import hashlib
import math
import random

import numpy as np


def harmonic(n: int) -> float:
    """調和数 H_n = 1 + 1/2 + ... + 1/n を返す。"""
    return sum(1 / k for k in range(1, n + 1))


def collision_probability(n: int, m: int) -> float:
    """n 個のキーを m 個のバケットへ一様にハッシュしたとき、衝突が起きる確率の厳密値を返す。"""
    log_no_collision = sum(math.log1p(-i / m) for i in range(n))
    return 1.0 - math.exp(log_no_collision)


def collision_approximation(n: int, m: int) -> float:
    """衝突確率の近似式 1 - exp(-n(n-1) / (2m)) を返す。"""
    return 1.0 - math.exp(-n * (n - 1) / (2 * m))


def coupon_collector(n: int, rng: random.Random) -> int:
    """n 種類のクーポンがすべて揃うまでに引いた回数を返す。"""
    seen: set[int] = set()
    draws = 0
    while len(seen) < n:
        seen.add(rng.randrange(n))
        draws += 1
    return draws


def quicksort_comparisons(values: list[int], rng: random.Random) -> int:
    """ピボットを一様ランダムに選ぶクイックソートで、要素同士の比較回数を返す（要素は相異なるとする）。"""
    if len(values) <= 1:
        return 0
    pivot = rng.choice(values)
    smaller = [v for v in values if v < pivot]
    larger = [v for v in values if v > pivot]
    # ピボット以外の各要素をピボットと 1 回ずつ比較する
    return len(values) - 1 + quicksort_comparisons(smaller, rng) + quicksort_comparisons(larger, rng)


class BloomFilter:
    """m ビットの配列と k 個のハッシュ関数からなるブルームフィルタ。"""

    def __init__(self, m: int, k: int) -> None:
        self.m = m
        self.k = k
        self.bits = bytearray(m)

    def _indexes(self, item: str) -> list[int]:
        # SHA-256 の値から 2 つのハッシュ値 h1, h2 を取り出し、h1 + i * h2 (mod m) で k 個の位置を作る
        digest = hashlib.sha256(item.encode()).digest()
        h1 = int.from_bytes(digest[:8], "little")
        h2 = int.from_bytes(digest[8:16], "little") | 1
        return [(h1 + i * h2) % self.m for i in range(self.k)]

    def add(self, item: str) -> None:
        """要素を登録する。"""
        for index in self._indexes(item):
            self.bits[index] = 1

    def might_contain(self, item: str) -> bool:
        """登録済みの可能性があれば True、確実に未登録なら False を返す。"""
        return all(self.bits[index] for index in self._indexes(item))


def bloom_false_positive_rate(m: int, n: int, k: int) -> float:
    """ブルームフィルタの偽陽性率の近似式 (1 - exp(-kn/m))^k を返す。"""
    return (1 - math.exp(-k * n / m)) ** k


def estimate_pi(samples: int, rng: np.random.Generator) -> float:
    """単位正方形内の一様乱数点が四分円に入る割合から円周率を推定する。"""
    x = rng.random(samples)
    y = rng.random(samples)
    return 4.0 * float(np.mean(x * x + y * y <= 1.0))


def main() -> None:
    rng = random.Random(2026)
    np_rng = np.random.default_rng(2026)

    print("--- ハッシュ衝突 ---")
    m = 2 ** 32
    for n in [10000, 50000, 77163, 100000]:
        print(f"n={n:>6}, m=2^32: 厳密値={collision_probability(n, m):.4f}  近似={collision_approximation(n, m):.4f}")

    print("--- クーポンコレクター問題 (n=50) ---")
    trials = [coupon_collector(50, rng) for _ in range(2000)]
    print(f"理論値 n H_n = {50 * harmonic(50):.2f}, シミュレーション平均 = {sum(trials) / len(trials):.2f}")

    print("--- 乱択クイックソートの比較回数 ---")
    for n in [10, 100, 1000]:
        theory = 2 * (n + 1) * harmonic(n) - 4 * n
        results = [quicksort_comparisons(list(range(n)), rng) for _ in range(300)]
        print(f"n={n:>4}: 理論値={theory:9.2f}  シミュレーション平均={sum(results) / len(results):9.2f}")

    print("--- ブルームフィルタ (m=10000, n=1000) ---")
    for k in [1, 3, 5, 7, 10]:
        bf = BloomFilter(10000, k)
        for i in range(1000):
            bf.add(f"member-{i}")
        false_positives = sum(bf.might_contain(f"other-{i}") for i in range(100000))
        print(f"k={k:>2}: 理論値={bloom_false_positive_rate(10000, 1000, k):.4f}  実測={false_positives / 100000:.4f}")

    print("--- モンテカルロ法による円周率の推定 ---")
    for samples in [100, 10000, 1000000]:
        estimate = estimate_pi(samples, np_rng)
        print(f"N={samples:>7}: 推定値={estimate:.5f}  誤差={abs(estimate - math.pi):.5f}")


if __name__ == "__main__":
    main()
