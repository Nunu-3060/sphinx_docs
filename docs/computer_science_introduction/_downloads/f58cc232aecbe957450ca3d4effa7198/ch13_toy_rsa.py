"""小さな素数を使った教科書的 RSA による暗号化・復号・署名のサンプル。

警告: これは仕組みを理解するための学習用コードであり、実運用には
絶対に使ってはならない。鍵が小さすぎて瞬時に素因数分解できるうえ、
パディング（OAEP や PSS）を行わない教科書的 RSA は、同じ平文が
常に同じ暗号文になるなど多くの攻撃に弱い。実際のシステムでは、
検証済みの暗号ライブラリを使うこと。

実行方法: python ch13_toy_rsa.py
関連する章: 第 13 章「情報セキュリティと暗号」
"""

from math import gcd
from typing import NamedTuple


class KeyPair(NamedTuple):
    """RSA の鍵の組。公開鍵は (n, e)、秘密鍵は (n, d)。"""

    n: int
    e: int
    d: int


def generate_keys(p: int, q: int, e: int) -> KeyPair:
    """素数 p, q と公開指数 e から鍵の組を作る。"""
    n = p * q
    phi = (p - 1) * (q - 1)  # オイラーの関数 φ(n)
    if gcd(e, phi) != 1:
        raise ValueError("e と φ(n) が互いに素ではない")
    d = pow(e, -1, phi)  # e·d ≡ 1 (mod φ(n)) を満たす d
    return KeyPair(n, e, d)


def encrypt(m: int, key: KeyPair) -> int:
    """公開鍵で平文 m（0 <= m < n）を暗号化する。"""
    return pow(m, key.e, key.n)


def decrypt(c: int, key: KeyPair) -> int:
    """秘密鍵で暗号文 c を復号する。"""
    return pow(c, key.d, key.n)


def sign(m: int, key: KeyPair) -> int:
    """秘密鍵で m に署名する（実際には m のハッシュ値に署名する）。"""
    return pow(m, key.d, key.n)


def verify(m: int, s: int, key: KeyPair) -> bool:
    """公開鍵で署名 s が m に対するものかを検証する。"""
    return pow(s, key.e, key.n) == m


def main() -> None:
    """鍵生成、暗号化・復号、署名・検証の結果を表示する。"""
    p, q = 61, 53
    key = generate_keys(p, q, e=17)
    print(f"p = {p}, q = {q}, n = {key.n}, phi = {(p - 1) * (q - 1)}")
    print(f"公開鍵 (n, e) = ({key.n}, {key.e})")
    print(f"秘密鍵 d = {key.d}")
    print(f"e * d mod phi = {key.e * key.d % ((p - 1) * (q - 1))}")

    m = 65
    c = encrypt(m, key)
    print(f"平文 {m} -> 暗号文 {c} -> 復号 {decrypt(c, key)}")
    print(f"同じ平文を再度暗号化: {encrypt(m, key)}")

    s = sign(m, key)
    print(f"署名 s = {s}, 検証: {verify(m, s, key)}")
    print(f"改ざんした m = {m + 1} の検証: {verify(m + 1, s, key)}")


if __name__ == "__main__":
    main()
