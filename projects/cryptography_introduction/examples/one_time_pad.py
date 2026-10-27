"""ワンタイムパッド（バーナム暗号）と、鍵を再利用した場合の危険性。

実行方法::

    python one_time_pad.py
"""

import secrets


def xor_bytes(a: bytes, b: bytes) -> bytes:
    """同じ長さのバイト列どうしの排他的論理和を求める。"""
    if len(a) != len(b):
        raise ValueError("長さが異なる")
    return bytes(x ^ y for x, y in zip(a, b))


def encrypt(plaintext: bytes, key: bytes) -> bytes:
    """平文と鍵の排他的論理和を暗号文とする。"""
    return xor_bytes(plaintext, key)


def decrypt(ciphertext: bytes, key: bytes) -> bytes:
    """排他的論理和は自身が逆演算なので、暗号化と同じ処理で復号できる。"""
    return xor_bytes(ciphertext, key)


def main() -> None:
    message1 = b"MEET AT NOON"
    message2 = b"RUN TO WOODS"
    key = secrets.token_bytes(len(message1))  # 平文と同じ長さの真の乱数列

    c1 = encrypt(message1, key)
    print(f"鍵    : {key.hex()}")
    print(f"暗号文: {c1.hex()}")
    print(f"復号  : {decrypt(c1, key).decode()}")

    # 同じ鍵を 2 回使うと、暗号文どうしの XOR から鍵が消える。
    c2 = encrypt(message2, key)
    leaked = xor_bytes(c1, c2)
    print()
    print(f"c1 XOR c2           : {leaked.hex()}")
    print(f"m1 XOR m2           : {xor_bytes(message1, message2).hex()}")
    # 一方の平文が推測できれば、もう一方の平文がそのまま得られる。
    print(f"m1 を推測した場合の m2: {xor_bytes(leaked, message1).decode()}")


if __name__ == "__main__":
    main()
