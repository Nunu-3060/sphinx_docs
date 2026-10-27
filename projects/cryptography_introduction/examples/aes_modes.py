"""AES の暗号利用モード（ECB / CBC / CTR）の比較。

cryptography ライブラリを使う。ECB モードは同じ平文ブロックが同じ暗号文ブロックになることを示すために
使っているだけであり、実際のシステムで使ってはならない。

実行方法::

    pip install cryptography
    python aes_modes.py
"""

import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

BLOCK_SIZE = 16  # AES のブロック長 [バイト]


def blocks_hex(data: bytes) -> list[str]:
    """バイト列を 16 バイトごとに区切り、16 進文字列のリストにする。"""
    return [data[i:i + BLOCK_SIZE].hex() for i in range(0, len(data), BLOCK_SIZE)]


def pkcs7_pad(data: bytes) -> bytes:
    """PKCS #7 パディングを付ける。"""
    padder = padding.PKCS7(BLOCK_SIZE * 8).padder()
    return padder.update(data) + padder.finalize()


def pkcs7_unpad(data: bytes) -> bytes:
    """PKCS #7 パディングを取り除く。"""
    unpadder = padding.PKCS7(BLOCK_SIZE * 8).unpadder()
    return unpadder.update(data) + unpadder.finalize()


def encrypt_ecb(key: bytes, plaintext: bytes) -> bytes:
    """ECB モードで暗号化する（学習用）。"""
    encryptor = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
    return encryptor.update(pkcs7_pad(plaintext)) + encryptor.finalize()


def encrypt_cbc(key: bytes, plaintext: bytes) -> bytes:
    """CBC モードで暗号化し、先頭に IV を付けて返す。"""
    iv = os.urandom(BLOCK_SIZE)
    encryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
    return iv + encryptor.update(pkcs7_pad(plaintext)) + encryptor.finalize()


def decrypt_cbc(key: bytes, data: bytes) -> bytes:
    """先頭 16 バイトを IV として CBC モードで復号する。"""
    iv, ciphertext = data[:BLOCK_SIZE], data[BLOCK_SIZE:]
    decryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    return pkcs7_unpad(decryptor.update(ciphertext) + decryptor.finalize())


def encrypt_ctr(key: bytes, plaintext: bytes) -> bytes:
    """CTR モードで暗号化し、先頭に初期カウンタ値（ナンス）を付けて返す。パディングは不要である。"""
    nonce = os.urandom(BLOCK_SIZE)
    encryptor = Cipher(algorithms.AES(key), modes.CTR(nonce)).encryptor()
    return nonce + encryptor.update(plaintext) + encryptor.finalize()


def decrypt_ctr(key: bytes, data: bytes) -> bytes:
    """先頭 16 バイトを初期カウンタ値として CTR モードで復号する。"""
    nonce, ciphertext = data[:BLOCK_SIZE], data[BLOCK_SIZE:]
    decryptor = Cipher(algorithms.AES(key), modes.CTR(nonce)).decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


def main() -> None:
    key = os.urandom(16)  # AES-128 の鍵
    plaintext = b"YELLOW SUBMARINE" * 2 + b"END"  # 同じ 16 バイトのブロックが 2 回続く

    print("ECB:", blocks_hex(encrypt_ecb(key, plaintext)))
    print("  -> 1 番目と 2 番目のブロックが同じになる")

    cbc = encrypt_cbc(key, plaintext)
    print("CBC:", blocks_hex(cbc[BLOCK_SIZE:]))
    print("  -> 同じ平文ブロックでも暗号文ブロックは異なる")
    print("  復号:", decrypt_cbc(key, cbc))

    ctr = encrypt_ctr(key, plaintext)
    print(f"CTR: 平文 {len(plaintext)} バイト -> 暗号文 {len(ctr) - BLOCK_SIZE} バイト（パディングなし）")
    print("  復号:", decrypt_ctr(key, ctr))


if __name__ == "__main__":
    main()
