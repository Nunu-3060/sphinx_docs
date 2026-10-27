"""第 10 章 確率の不等式と極限定理のサンプルコード。

マルコフ・チェビシェフ・チェルノフの各不等式による上界と実際の確率を比較し、
大数の法則と中心極限定理をシミュレーションで確かめる。
"""

import math

import numpy as np
from scipy import stats


def compare_tail_bounds(n: int, p: float, a: int) -> None:
    """X ~ Bin(n, p) について P(X >= a) の真の値と各不等式の上界を比較する。"""
    mu = n * p
    var = n * p * (1 - p)
    exact = float(stats.binom.sf(a - 1, n, p))  # sf(a-1) = P(X > a-1) = P(X >= a)
    markov = mu / a
    # チェビシェフ: P(X >= a) <= P(|X - μ| >= a - μ) <= V / (a - μ)^2
    chebyshev = var / (a - mu) ** 2
    # チェルノフ: P(X >= (1 + δ)μ) <= exp(-δ^2 μ / 3)  (0 < δ <= 1)
    delta = a / mu - 1
    chernoff = math.exp(-delta ** 2 * mu / 3)
    print(f"P(X >= {a}) の真の値 = {exact:.3e}")
    print(f"  マルコフの不等式     <= {markov:.3e}")
    print(f"  チェビシェフの不等式 <= {chebyshev:.3e}")
    print(f"  チェルノフ限界       <= {chernoff:.3e}")


def law_of_large_numbers(rng: np.random.Generator) -> None:
    """サイコロの目の標本平均が期待値 3.5 に近づく様子を調べる。"""
    for n in [10, 100, 1000, 10000, 100000]:
        # 長さ n の系列を 200 本作り、それぞれの標本平均を求める
        means = rng.integers(1, 7, size=(200, n), dtype=np.int8).mean(axis=1)
        within = np.mean(np.abs(means - 3.5) < 0.1)
        print(f"n={n:>6}: 標本平均の例 {means[0]:.4f}, |標本平均 - 3.5| < 0.1 となる割合 {within:.3f}")


def central_limit_theorem(rng: np.random.Generator) -> None:
    """サイコロ n 個の和を標準化した値が標準正規分布に近づく様子を調べる。"""
    mu, sigma = 3.5, math.sqrt(35 / 12)
    for n in [1, 2, 5, 30]:
        sums = rng.integers(1, 7, size=(100000, n)).sum(axis=1)
        z = (sums - n * mu) / (sigma * math.sqrt(n))
        print(f"n={n:>2}: P(Z <= 1) の推定値 {np.mean(z <= 1):.4f}, "
              f"P(|Z| <= 2) の推定値 {np.mean(np.abs(z) <= 2):.4f}")
    print(f"標準正規分布: P(Z <= 1) = {stats.norm.cdf(1):.4f}, P(|Z| <= 2) = {stats.norm.cdf(2) - stats.norm.cdf(-2):.4f}")


def main() -> None:
    rng = np.random.default_rng(2026)
    print("--- 裾確率の上界 (X ~ Bin(100, 0.5)) ---")
    compare_tail_bounds(100, 0.5, 60)
    compare_tail_bounds(100, 0.5, 75)
    print("--- 大数の法則 ---")
    law_of_large_numbers(rng)
    print("--- 中心極限定理 ---")
    central_limit_theorem(rng)


if __name__ == "__main__":
    main()
