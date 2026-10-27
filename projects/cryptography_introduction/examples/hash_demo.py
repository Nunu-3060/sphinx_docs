"""hashlib によるハッシュ値の計算と、雪崩効果の観察。

実行方法::

    python hash_demo.py
"""

import hashlib


def bit_difference(a: bytes, b: bytes) -> int:
    """2 つのバイト列で値が異なるビットの数を数える。"""
    return sum(bin(x ^ y).count("1") for x, y in zip(a, b))


def main() -> None:
    for name in ["sha256", "sha3_256", "blake2b"]:
        digest = hashlib.new(name, b"hello").hexdigest()
        print(f"{name:9s}('hello') = {digest}")

    # 入力の 1 ビットだけを変えると、出力のおよそ半分のビットが変わる（雪崩効果）。
    m1 = b"cryptography"
    m2 = bytes([m1[0] ^ 0x01]) + m1[1:]  # 先頭バイトの最下位ビットを反転
    h1 = hashlib.sha256(m1).digest()
    h2 = hashlib.sha256(m2).digest()
    print()
    print(f"{m1!r} -> {h1.hex()}")
    print(f"{m2!r} -> {h2.hex()}")
    print(f"異なるビット数: {bit_difference(h1, h2)} / {len(h1) * 8}")


if __name__ == "__main__":
    main()
