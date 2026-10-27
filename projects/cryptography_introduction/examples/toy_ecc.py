"""有限体上の楕円曲線の点演算と ECDH のおもちゃ実装（学習専用）。

曲線は y^2 = x^3 + x + 4 (mod 97) とする。この曲線の点の個数（群の位数）は素数 89 である。無限遠点 O は None で表す。

実行方法::

    python toy_ecc.py
"""

import secrets

P = 97
A = 1
B = 4

Point = tuple[int, int] | None


def is_on_curve(point: Point) -> bool:
    """点が曲線上にあるかを調べる。"""
    if point is None:
        return True
    x, y = point
    return (y * y - (x ** 3 + A * x + B)) % P == 0


def add(p1: Point, p2: Point) -> Point:
    """楕円曲線上の点の加算 p1 + p2 を求める。"""
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2 and (y1 + y2) % P == 0:
        return None  # P + (-P) = O
    if p1 == p2:
        slope = (3 * x1 * x1 + A) * pow(2 * y1, -1, P) % P  # 接線の傾き
    else:
        slope = (y2 - y1) * pow(x2 - x1, -1, P) % P  # 2 点を通る直線の傾き
    x3 = (slope * slope - x1 - x2) % P
    y3 = (slope * (x1 - x3) - y1) % P
    return (x3, y3)


def scalar_mult(k: int, point: Point) -> Point:
    """二倍加算法で k * point を求める。"""
    result: Point = None
    addend = point
    while k:
        if k & 1:
            result = add(result, addend)
        addend = add(addend, addend)
        k >>= 1
    return result


def order(point: Point) -> int:
    """n * point = O となる最小の正整数 n（点の位数）を求める。"""
    n = 1
    current = point
    while current is not None:
        current = add(current, point)
        n += 1
    return n


def main() -> None:
    g: Point = (0, 2)
    assert is_on_curve(g)
    n = order(g)
    print(f"ベースポイント G = {g}, 位数 n = {n}")
    print("G の倍数:", [scalar_mult(k, g) for k in range(1, 6)], "...")

    # ECDH: 秘密鍵は 1 <= d < n の整数、公開鍵は d * G
    d_alice = secrets.randbelow(n - 1) + 1
    d_bob = secrets.randbelow(n - 1) + 1
    q_alice = scalar_mult(d_alice, g)
    q_bob = scalar_mult(d_bob, g)
    shared_alice = scalar_mult(d_alice, q_bob)
    shared_bob = scalar_mult(d_bob, q_alice)
    print(f"Alice: 秘密鍵 {d_alice}, 公開鍵 {q_alice}")
    print(f"Bob  : 秘密鍵 {d_bob}, 公開鍵 {q_bob}")
    print(f"共有した点: Alice {shared_alice}, Bob {shared_bob}")


if __name__ == "__main__":
    main()
