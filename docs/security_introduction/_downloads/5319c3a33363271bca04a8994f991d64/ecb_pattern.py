"""ECB モードの問題点を確認するサンプル.

ECB モードでは同じ平文ブロックが同じ暗号文ブロックになるため、
暗号文から平文の繰り返しパターンが分かってしまいます。

実行方法:
    python ecb_pattern.py

必要なライブラリ:
    cryptography（python -m pip install cryptography）
"""

import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

BLOCK_SIZE = 16  # AES のブロック長（バイト）


def encrypt_ecb(key: bytes, plaintext: bytes) -> bytes:
    """ECB モードで暗号化する（悪い例。実際には使わないこと）."""
    encryptor = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
    return encryptor.update(plaintext) + encryptor.finalize()


def encrypt_ctr(key: bytes, plaintext: bytes) -> bytes:
    """CTR モードで暗号化する（比較用）."""
    nonce = os.urandom(BLOCK_SIZE)
    encryptor = Cipher(algorithms.AES(key), modes.CTR(nonce)).encryptor()
    return encryptor.update(plaintext) + encryptor.finalize()


def show_blocks(label: str, data: bytes) -> None:
    """データをブロックごとに 16 進数で表示する."""
    print(label)
    for i in range(0, len(data), BLOCK_SIZE):
        print(f"  {data[i:i + BLOCK_SIZE].hex()}")


def main() -> None:
    key = os.urandom(32)
    # 16 バイトの同じブロックを 3 回繰り返した平文
    plaintext = b"ATTACK AT DAWN!!" * 3

    show_blocks("[ECB モード] 同じブロックが並ぶ", encrypt_ecb(key, plaintext))
    show_blocks("[CTR モード] パターンが現れない", encrypt_ctr(key, plaintext))


if __name__ == "__main__":
    main()
