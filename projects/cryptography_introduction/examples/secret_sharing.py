"""シャミアの秘密分散法（(k, n) しきい値法）。

秘密を n 個のシェアに分け、そのうち k 個以上あれば秘密を復元でき、k - 1 個以下では
秘密について何も分からないようにする。

実行方法::

    python secret_sharing.py
"""

import secrets

PRIME = 2**127 - 1  # 有限体 F_p の位数（メルセンヌ素数）


def split(secret: int, k: int, n: int) -> list[tuple[int, int]]:
    """f(0) = secret となる k - 1 次の乱数多項式 f を作り、(i, f(i)) を n 個返す。"""
    if not 0 <= secret < PRIME:
        raise ValueError("秘密は 0 以上 PRIME 未満でなければならない")
    coefficients = [secret] + [secrets.randbelow(PRIME) for _ in range(k - 1)]
    shares = []
    for x in range(1, n + 1):
        y = 0
        for c in reversed(coefficients):  # ホーナー法
            y = (y * x + c) % PRIME
        shares.append((x, y))
    return shares


def combine(shares: list[tuple[int, int]]) -> int:
    """ラグランジュ補間で f(0) を求める。"""
    secret = 0
    for i, (xi, yi) in enumerate(shares):
        numerator = 1
        denominator = 1
        for j, (xj, _) in enumerate(shares):
            if i != j:
                numerator = numerator * (-xj) % PRIME
                denominator = denominator * (xi - xj) % PRIME
        secret = (secret + yi * numerator * pow(denominator, -1, PRIME)) % PRIME
    return secret


def main() -> None:
    secret = int.from_bytes(b"open sesame", "big")
    shares = split(secret, k=3, n=5)
    for x, y in shares:
        print(f"シェア {x}: {y}")

    recovered = combine(shares[:3])
    print(f"シェア 1, 2, 3 から復元: {recovered.to_bytes(11, 'big')!r}")
    recovered = combine([shares[1], shares[3], shares[4]])
    print(f"シェア 2, 4, 5 から復元: {recovered.to_bytes(11, 'big')!r}")
    print(f"シェア 2 個から計算した値は秘密と一致するか: {combine(shares[:2]) == secret}")


if __name__ == "__main__":
    main()
