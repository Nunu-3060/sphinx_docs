"""ECDSA のおもちゃ実装と、ナンス k の再利用による秘密鍵の復元（学習専用）。

曲線には secp256k1 を使う。署名に使うナンス k を 2 つのメッセージで使い回すと、
2 つの署名から秘密鍵 d が計算できてしまうことを示す。

実行方法::

    python ecdsa_nonce_reuse.py
"""

import hashlib
import secrets

# secp256k1 のパラメータ（y^2 = x^3 + 7 over F_p）
P = 2**256 - 2**32 - 977
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141  # ベースポイントの位数
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

Point = tuple[int, int] | None
G: Point = (GX, GY)


def add(p1: Point, p2: Point) -> Point:
    """楕円曲線上の点の加算（a = 0 の曲線用）。"""
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2 and (y1 + y2) % P == 0:
        return None
    if p1 == p2:
        slope = 3 * x1 * x1 * pow(2 * y1, -1, P) % P
    else:
        slope = (y2 - y1) * pow(x2 - x1, -1, P) % P
    x3 = (slope * slope - x1 - x2) % P
    return (x3, (slope * (x1 - x3) - y1) % P)


def scalar_mult(k: int, point: Point) -> Point:
    """二倍加算法で k * point を求める。"""
    result: Point = None
    while k:
        if k & 1:
            result = add(result, point)
        point = add(point, point)
        k >>= 1
    return result


def hash_to_int(message: bytes) -> int:
    """メッセージの SHA-256 ハッシュ値を整数 z に変換する。"""
    return int.from_bytes(hashlib.sha256(message).digest(), "big")


def sign(d: int, message: bytes, k: int) -> tuple[int, int]:
    """ナンス k を使って署名 (r, s) を作る。本来 k は署名ごとに秘密の乱数でなければならない。"""
    z = hash_to_int(message)
    point = scalar_mult(k, G)
    assert point is not None
    r = point[0] % N
    s = pow(k, -1, N) * (z + r * d) % N
    return r, s


def verify(q: Point, message: bytes, signature: tuple[int, int]) -> bool:
    """公開鍵 q で署名 (r, s) を検証する。"""
    r, s = signature
    if not (1 <= r < N and 1 <= s < N):
        return False
    z = hash_to_int(message)
    w = pow(s, -1, N)
    point = add(scalar_mult(z * w % N, G), scalar_mult(r * w % N, q))
    return point is not None and point[0] % N == r


def recover_private_key(m1: bytes, sig1: tuple[int, int], m2: bytes, sig2: tuple[int, int]) -> int:
    """同じ k で作られた 2 つの署名から秘密鍵 d を求める。"""
    r, s1 = sig1
    _, s2 = sig2
    z1, z2 = hash_to_int(m1), hash_to_int(m2)
    k = (z1 - z2) * pow(s1 - s2, -1, N) % N
    return (s1 * k - z1) * pow(r, -1, N) % N


def main() -> None:
    d = secrets.randbelow(N - 1) + 1  # 秘密鍵
    q = scalar_mult(d, G)  # 公開鍵
    print(f"秘密鍵 d      : {d:064x}")

    k = secrets.randbelow(N - 1) + 1
    m1, m2 = b"message one", b"message two"
    sig1 = sign(d, m1, k)
    sig2 = sign(d, m2, k)  # 同じ k を再利用してしまった
    print(f"署名 1 の検証 : {verify(q, m1, sig1)}")
    print(f"署名 2 の検証 : {verify(q, m2, sig2)}")
    print(f"r が一致する  : {sig1[0] == sig2[0]}（k の再利用は署名から分かる）")

    recovered = recover_private_key(m1, sig1, m2, sig2)
    print(f"復元した d    : {recovered:064x}")
    print(f"一致するか    : {recovered == d}")


if __name__ == "__main__":
    main()
