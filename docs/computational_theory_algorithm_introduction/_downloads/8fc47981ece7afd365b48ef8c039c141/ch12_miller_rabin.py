"""第 12 章: ミラー-ラビン素数判定法 (乱択アルゴリズム)。

n が素数なら必ず「素数らしい」と答える。n が合成数のとき、1 回の試行で
誤って「素数らしい」と答える確率は 1/4 以下なので、k 回独立に試せば
誤り確率は 4^(-k) 以下になる。

実行例::

    python ch12_miller_rabin.py
"""

from __future__ import annotations

import random


def is_probable_prime(n: int, rounds: int = 20) -> bool:
    """n が素数らしければ True、合成数と確定すれば False を返す。"""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:  # n - 1 = d * 2^s (d は奇数) と分解する
        d //= 2
        s += 1
    for _ in range(rounds):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False  # a は n が合成数であることの証拠
    return True


def is_prime_trial_division(n: int) -> bool:
    """試し割りによる確定的な判定 (比較用)。O(√n) 回の割り算を行う。"""
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def main() -> None:
    random.seed(0)
    mismatches = [n for n in range(2, 10_000)
                  if is_probable_prime(n) != is_prime_trial_division(n)]
    print("1 万未満で試し割りと結果が異なる数:", mismatches)
    print("561 (カーマイケル数):", is_probable_prime(561))
    mersenne = 2 ** 127 - 1
    print("2^127 - 1:", is_probable_prime(mersenne))
    print("2^127 + 1:", is_probable_prime(mersenne + 2))


if __name__ == "__main__":
    main()
