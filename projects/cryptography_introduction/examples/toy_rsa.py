"""教科書的 RSA のおもちゃ実装（学習専用）。

パディングを使わない RSA（教科書的 RSA）は安全ではない。実際のシステムでは rsa_oaep.py のように
ライブラリと OAEP / PSS を使うこと。

実行方法::

    python toy_rsa.py
"""

import hashlib
import math
import secrets
from dataclasses import dataclass


@dataclass(frozen=True)
class PublicKey:
    n: int
    e: int


@dataclass(frozen=True)
class PrivateKey:
    n: int
    d: int


def is_probable_prime(n: int, rounds: int = 40) -> bool:
    """ミラー・ラビン素数判定法（primality.py と同じ）。"""
    if n < 4:
        return n in (2, 3)
    if n % 2 == 0:
        return False
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(rounds):
        x = pow(secrets.randbelow(n - 3) + 2, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits: int) -> int:
    """bits ビットの素数を生成する。"""
    while True:
        candidate = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(candidate):
            return candidate


def generate_keypair(bits: int = 1024, e: int = 65537) -> tuple[PublicKey, PrivateKey]:
    """法 n が約 bits ビットになる RSA 鍵ペアを生成する。"""
    while True:
        p = generate_prime(bits // 2)
        q = generate_prime(bits // 2)
        if p == q:
            continue
        lam = math.lcm(p - 1, q - 1)  # カーマイケル関数 λ(n)
        if math.gcd(e, lam) == 1:
            break
    d = pow(e, -1, lam)  # e の法 λ(n) における逆元
    n = p * q
    return PublicKey(n, e), PrivateKey(n, d)


def encrypt(pub: PublicKey, m: int) -> int:
    """c = m^e mod n"""
    if not 0 <= m < pub.n:
        raise ValueError("平文は 0 以上 n 未満の整数でなければならない")
    return pow(m, pub.e, pub.n)


def decrypt(priv: PrivateKey, c: int) -> int:
    """m = c^d mod n"""
    return pow(c, priv.d, priv.n)


def sign(priv: PrivateKey, message: bytes) -> int:
    """メッセージの SHA-256 ハッシュ値 h に対して s = h^d mod n を署名とする（学習用）。"""
    h = int.from_bytes(hashlib.sha256(message).digest(), "big") % priv.n
    return pow(h, priv.d, priv.n)


def verify(pub: PublicKey, message: bytes, signature: int) -> bool:
    """s^e mod n がメッセージのハッシュ値と一致するかを調べる。"""
    h = int.from_bytes(hashlib.sha256(message).digest(), "big") % pub.n
    return pow(signature, pub.e, pub.n) == h


def main() -> None:
    # 小さな数での手計算の例: p = 61, q = 53
    small_pub, small_priv = PublicKey(3233, 17), PrivateKey(3233, 413)
    c = encrypt(small_pub, 65)
    print(f"小さな例: 平文 65 -> 暗号文 {c} -> 復号 {decrypt(small_priv, c)}")

    pub, priv = generate_keypair(1024)
    print(f"n のビット長: {pub.n.bit_length()}")
    m = int.from_bytes(b"hello RSA", "big")
    c = encrypt(pub, m)
    recovered = decrypt(priv, c)
    print(f"復号結果: {recovered.to_bytes((recovered.bit_length() + 7) // 8, 'big')!r}")

    # 教科書的 RSA の問題点 1: 決定的（同じ平文は常に同じ暗号文になる）
    print(f"同じ平文を 2 回暗号化して一致するか: {encrypt(pub, m) == encrypt(pub, m)}")

    # 教科書的 RSA の問題点 2: 可鍛性（暗号文どうしの積は平文どうしの積の暗号文になる）
    m1, m2 = 6, 7
    product = encrypt(pub, m1) * encrypt(pub, m2) % pub.n
    print(f"E(6) * E(7) を復号した値: {decrypt(priv, product)}")

    s = sign(priv, b"I agree")
    print(f"署名の検証（正しいメッセージ）    : {verify(pub, b'I agree', s)}")
    print(f"署名の検証（改ざんされたメッセージ）: {verify(pub, b'I disagree', s)}")


if __name__ == "__main__":
    main()
