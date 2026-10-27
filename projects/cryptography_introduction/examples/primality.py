"""ミラー・ラビン素数判定法と、指定したビット長の素数の生成。

実行方法::

    python primality.py
"""

import secrets

SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]


def is_probable_prime(n: int, rounds: int = 40) -> bool:
    """n が素数なら必ず True を返す。合成数を誤って True とする確率は 4^(-rounds) 以下である。"""
    if n < 2:
        return False
    for p in SMALL_PRIMES:
        if n % p == 0:
            return n == p

    # n - 1 = 2^s * d（d は奇数）と分解する
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2  # 2 <= a <= n - 2
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # a は n が合成数であることの証拠
    return True


def generate_prime(bits: int) -> int:
    """最上位ビットと最下位ビットを 1 にした乱数を、素数が見つかるまで生成する。"""
    while True:
        candidate = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(candidate):
            return candidate


def main() -> None:
    # 561 = 3 * 11 * 17 はカーマイケル数（フェルマーテストを欺く合成数）
    for n in [97, 561, 7919, 2**61 - 1, 2**61 + 1]:
        print(f"{n} は素数か: {is_probable_prime(n)}")
    p = generate_prime(512)
    print(f"512 ビットの素数: {p}")


if __name__ == "__main__":
    main()
